import random
from pathlib import Path
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

SEED = 42
random.seed(SEED)
torch.manual_seed(SEED)
ARTIFACT_PATH = Path('artifacts/language_classifier.pt')
HIDDEN_SIZE = 64
ID_TO_LANGUAGE = {0: 'ru', 1: 'en', 2: 'es'}
NUM_CLASSES = len(ID_TO_LANGUAGE)

def load_csv(path: str | Path) -> tuple[list[str], list[int]]:
    dataframe = pd.read_csv(path)
    texts = dataframe['text'].astype(str).tolist()
    labels = dataframe['label'].astype(int).tolist()
    return texts, labels

DATA_DIR = Path('data')
train_texts, train_labels = load_csv(DATA_DIR/'train.csv')
val_texts, val_labels = load_csv(DATA_DIR/'validation.csv')
test_texts, test_labels = load_csv(DATA_DIR/'test.csv')
print('Train:', len(train_texts))
print('Val:', len(val_texts))
print('Test:', len(test_texts))

indices = random.sample(range(len(train_texts)), k=3)
for i in indices:
    print(train_texts[i], ID_TO_LANGUAGE[train_labels[i]])

UNKNOWN_TOKEN = '<UNK>'

def build_vocabulary(texts: Iterable[str]) -> list[str]:
    characters = {
        c
        for t in texts
        for c in t.lower()
    }
    return [UNKNOWN_TOKEN, *sorted(characters)]

vocabulary = build_vocabulary(train_texts)
print(vocabulary)
character_to_id = {
    c: i for i, c in enumerate(vocabulary)
}

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
print(example_features)

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


train_dataset = LanguageDataset(train_texts, train_labels)
val_dataset = LanguageDataset(val_texts, val_labels, train_dataset.vocabulary)
test_dataset = LanguageDataset(test_texts, test_labels, train_dataset.vocabulary)

print(len(train_dataset))
features, text, label = train_dataset[0]
print(features.shape, text)

vls, idxs = torch.topk(features, k=5)
for i, v in zip(idxs, vls):
    c = train_dataset.vocabulary[i.item()]
    print(c, '-', v.item())

text='🦆'
print(text_to_bag_of_characters(text, character_to_id))

'''
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

MODEL_REGISTRY = {
    'SwiGLUClassifier': SwiGLUClassifier
}

checkpoint = torch.load(ARTIFACT_PATH)
model_class = MODEL_REGISTRY[checkpoint['model_class']]

loaded_model = model_class(
    input_size=len(checkpoint['vocabulary']),
    hidden_size=checkpoint['hidden_size'],
    output_size=len(checkpoint['id_to_language'])
)

loaded_model.load_state_dict(checkpoint['model_state_dict'])
loaded_model.eval()

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
        t, loaded_model, train_dataset.vocabulary, ID_TO_LANGUAGE
    )
    readable_probs = {
        ID_TO_LANGUAGE[i]: round(pr, 3) for i, pr in enumerate(probs)
    }
    print(t, '->', lang, readable_probs)
'''