import random
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader, Dataset

SEED = 42
DATA_DIR = Path('data')

random.seed(SEED)
torch.manual_seed(SEED)
ID_TO_LANGUAGE = {0: 'ru', 1: 'en', 2: 'es'}
UNKNOWN_TOKEN = '<UNK>'
BATCH_SIZE = 128
HIDDEN_SIZE = 64
NUM_CLASSES = len(ID_TO_LANGUAGE)
EPOCHS = 10
LEARNING_RATE = 1e-2
ARTIFACT_PATH = Path('artifacts/language_classifier.pt')

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')


def load_csv(path: str | Path) -> tuple[list[str], list[int]]:
    dataframe = pd.read_csv(path)
    texts = dataframe['text'].astype(str).tolist()
    labels = dataframe['label'].astype(int).tolist()
    return texts, labels

train_texts, train_labels = load_csv(DATA_DIR/'train.csv')
val_texts, val_labels = load_csv(DATA_DIR/'validation.csv')
test_texts, test_labels = load_csv(DATA_DIR/'test.csv')
print('Train:', len(train_texts))
print('Val:', len(val_texts))
print('Test:', len(test_texts))

'''
for names, labels in {
    'Train': train_labels,
    'Val': val_labels,
    'Test': test_labels
    }.items():
    readable_counts = {
        ID_TO_LANGUAGE[label]: count
        for label, count in sorted(Counter(labels).items())
    }
    plt.figure(figsize=(10, 5))
    plt.bar(readable_counts.keys(), readable_counts.values())
    plt.title(names)
    print(names, readable_counts)
plt.show()
'''

indices = random.sample(range(len(train_texts)), k=3)
for i in indices:
    print(train_texts[i], ID_TO_LANGUAGE[train_labels[i]])

def build_vocabulary(texts: Iterable[str]) -> list[str]:
    characters = {
        c
        for t in texts
        for c in t.lower()
    }
    return [UNKNOWN_TOKEN, *sorted(characters)]

vocabulary = build_vocabulary(train_texts)
character_to_id = {
    c: i for i, c in enumerate(vocabulary)
}

print("Размер словаря:", len(vocabulary))
print("Первые 20 символов словаря:", vocabulary[:20])

def text_to_bag_of_characters(
        text: str,
        character_to_id: Mapping[str, int]
) -> torch.Tensor:
    features = torch.zeros(len(character_to_id), dtype=torch.float32)
    normalized_text = text.lower()

    for c in normalized_text:
        c_id = character_to_id.get(c, 0)
        features[c_id] += 1

    if normalized_text:
        features /= len(normalized_text)
    return features

example_features = text_to_bag_of_characters('Hello!', character_to_id=character_to_id)
print(example_features.shape)
print(example_features)
print(example_features.sum().item())
print(torch.count_nonzero(example_features).item())

class LanguageDataset(Dataset):
    def __init__(self,
            texts: Sequence[str],
            labels: Sequence[int],
            vocabulary: Sequence[str] | None = None,
            ) -> None:
        self.texts = texts
        self.labels = labels
        self.vocabulary = (
            build_vocabulary(self.texts)
            if vocabulary is None
            else list(vocabulary)
        )
        self.character_to_id = {
            c: i for i, c in enumerate(self.vocabulary)
        }
    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, index) -> tuple[torch.Tensor, str, torch.Tensor]:
        text = self.texts[index]
        features = text_to_bag_of_characters(
            self.texts[index],
            self.character_to_id
        )
        label = self.labels[index]
        return features, text, label


print(len(train_texts), len(train_labels))
train_dataset = LanguageDataset(train_texts, train_labels)
val_dataset = LanguageDataset(val_texts, val_labels, train_dataset.vocabulary)
test_dataset = LanguageDataset(test_texts, test_labels, train_dataset.vocabulary)

print(len(train_dataset))
features, text, label = train_dataset[0]
print(features.shape, text, label)

loader_generator = torch.Generator().manual_seed(SEED)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, generator=loader_generator)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)
test_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

batch_features, batch_text, batch_labels = next(iter(train_loader))
print(batch_features.shape, batch_features.dtype)
print(batch_labels.shape, batch_labels.dtype)
print(len(train_loader))

class Classifier(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )
    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features)

class LayerNormSwishClassifier(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        super().__init__()
        wide_size = hidden_size * 2
        self.network = nn.Sequential(
            nn.Linear(input_size, wide_size),
            nn.LayerNorm(wide_size),
            nn.SiLU(),
            nn.Linear(wide_size, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.SiLU(),
            nn.Linear(hidden_size, output_size),
        )
    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features)

class SwiGLU(nn.Module):
    def __init__(self, input_size: int, output_size: int) -> None:
        super().__init__()
        self.projection = nn.Linear(input_size, output_size * 2)
    def forward(self, features: torch.Tensor) -> torch.Tensor:
        value, gate = self.projection(features).chunk(2, dim=-1)
        return value * nn.functional.silu(gate)

class SwiGLUClassifier(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.LayerNorm(input_size),
            SwiGLU(input_size, hidden_size),
            nn.LayerNorm(hidden_size),
            SwiGLU(hidden_size, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.Linear(hidden_size, output_size),
        )
    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features)

def count_trainable_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

model_classes = {
    'ReLU baseline': Classifier,
    'LayerNorm + Swish': LayerNormSwishClassifier,
    'LayerNorm + SwiGLU': SwiGLUClassifier
}

for n, m in model_classes.items():
    candidate = m(
        input_size=len(train_dataset.vocabulary),
        hidden_size=64,
        output_size=len(ID_TO_LANGUAGE)
    )
    candidate_logits = candidate(batch_features)
    print(f'{n:>20}: parameters={count_trainable_parameters(candidate):>6},')
    print(f'output={tuple(candidate_logits.shape)}')


MODEL_CLASS = SwiGLUClassifier

model = MODEL_CLASS(
    input_size=len(train_dataset.vocabulary),
    hidden_size=HIDDEN_SIZE,
    output_size=NUM_CLASSES,
).to(device)

with torch.no_grad():
    example_logits = model(batch_features.to(device))
print(model)
print('Input:', batch_features.shape)
print('Output:', example_logits.shape)

def run_epoch(
    model: nn.Module,
    data_loader: DataLoader,
    loss_function: nn.Module,
    optimizer: torch.optim.Optimizer | None = None
) -> tuple[float, float]:
    is_training = optimizer is not None
    model.train(is_training)

    total_loss = 0.0
    total_correct = 0.0
    total_examples = 0

    with torch.set_grad_enabled(is_training):
        for f, _, l in data_loader:
            f = f.to(device)
            l = l.to(device)

            if is_training:
                optimizer.zero_grad(set_to_none=True)

            logits = model(f)
            loss = loss_function(logits, l)

            if is_training:
                loss.backward()
                optimizer.step()

            batch_size = l.size(0)
            total_loss += loss.item() * batch_size
            total_correct += (logits.argmax(dim=1) == l).sum().item()
            total_examples += batch_size

    if total_examples == 0:
        raise ValueError("DataLoader must contain at least one example")
    return total_loss / total_examples, total_correct / total_examples

loss_function = nn.CrossEntropyLoss()
optimizer = Adam(model.parameters(), lr=LEARNING_RATE)

history = {
    'train_loss': [],
    'val_loss': [],
    'train_acc': [],
    'val_acc': [],
}

for epoch in range(1, EPOCHS+1):
    train_loss, train_acc = run_epoch(
        model,
        train_loader,
        loss_function,
        optimizer
    )
    val_loss, val_acc = run_epoch(
        model,
        val_loader,
        loss_function
    )

    history['train_loss'].append(train_loss)
    history['train_acc'].append(train_acc)
    history['val_loss'].append(val_loss)
    history['val_acc'].append(val_acc)

    print(f'Epoch {epoch:02d} / {EPOCHS}: ')
    print(f'{train_loss=:.4f}, {train_acc=:.4f}')
    print(f'{val_loss=:.4f}, {val_acc=:.4f}')

print('Loss by epoch')
print('epoch    train   validation')
for epoch, (train_loss, val_loss) in enumerate(
    zip(history['train_loss'], history['val_loss']),
    start=1
):
    print(f'{epoch:>5}  | {train_loss:.4f}  | {val_loss:.4f}')

test_loss, test_acc = run_epoch(
    model,
    test_loader,
    loss_function
)
print(f'{test_loss=:.4f}, {test_acc=:.4f}')

def confusion_matrix(
        model: nn.Module,
        data_loader: DataLoader,
        number_of_classes: int
) -> torch.Tensor:
    matrix = torch.zeros((number_of_classes, number_of_classes), dtype=torch.int64)
    model.eval()
    with torch.no_grad():
        for f, _, l in data_loader:
            pred = model(f.to(device)).argmax(dim=1).cpu()
            for t, p in zip(l, pred):
                matrix[t, p] += 1
    return matrix

matrix = confusion_matrix(model, test_loader, NUM_CLASSES)
language_names = [ID_TO_LANGUAGE[i] for i in range(NUM_CLASSES)]
print("     " + " ".join(f"{name:>6}" for name in language_names))
for l, r in zip(language_names, matrix):
    print(f"{l:>3}: " + " ".join(f"{v.item():>6}" for v in r))

model.eval()
errors = []
with torch.no_grad():
    for ftrs, txts, lbls in test_loader:
        logits = model(ftrs.to(device))
        probs = logits.softmax(dim=1).cpu()
        preds = logits.argmax(dim=1)

        for t, tl, pl, p in zip(
            txts, lbls, preds, probs
        ):
            if pl != tl:
                errors.append({
                    'text': t,
                    'labels': ID_TO_LANGUAGE[tl.item()],
                    'predicted': ID_TO_LANGUAGE[pl.item()],
                    'confidence': p[pl].item()
                })
for e in errors:
    print(f'Текст: {e['text']}, '
          f'Истинный класс: {e['labels']}, '
          f'Предсказанный класс: {e['predicted']}, '
          f'Уверенность: {e['confidence']}')

'''
ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)

torch.save(
    {
        'model_state_dict': model.state_dict(),
        'model_class': model.__class__.__name__,
        'vocabulary': train_dataset.vocabulary,
        'hidden_size': HIDDEN_SIZE,
        'id_to_language': ID_TO_LANGUAGE
    }, ARTIFACT_PATH,
)
print(f"Saved to {ARTIFACT_PATH}")
'''
def predict_language(
    text: str,
    model: nn.Module,
    vocabulary: Sequence[str],
    id_to_language: Mapping[int, str]
) -> tuple[str, list[float]]:
    if not text.strip():
        raise ValueError("Text must not be empty")

    character_to_id = {
        ch: idx for idx, ch in enumerate(vocabulary)
    }
    features = text_to_bag_of_characters(text, character_to_id)
    model.eval()
    with torch.no_grad():
        logits = model(features.unsqueeze(0))
        probs = logits.softmax(dim=1).squeeze(0).cpu()
    pred_ids = probs.argmax().item()
    return id_to_language[pred_ids], probs.tolist()

examples = [
    "Где находится мой заказ?",
    "Where is my order?",
    "¿Dónde está mi pedido?",
]

for t in examples:
    lang, probs = predict_language(
        t, model, train_dataset.vocabulary, ID_TO_LANGUAGE
    )
    readable_probs = {
        ID_TO_LANGUAGE[i]: round(pr, 3) for i, pr in enumerate(probs)
    }
    print(t, '->', lang, readable_probs)
