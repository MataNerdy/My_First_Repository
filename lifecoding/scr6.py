from collections import Counter
import torch
import math

texts = [
    "cat likes milk",
    "dog likes bone",
    "cat and dog"
]

vocabulary = []
text_words = [t.split() for t in texts]

for words in text_words:
    for w in words:
        if w not in vocabulary:
            vocabulary.append(w)

vocabulary = sorted(vocabulary)
print(vocabulary)

word_to_id = {w:i for i, w in enumerate(vocabulary)}
print(word_to_id)

bow_matrix = []
for w in text_words:
    c = Counter(w)
    bow_matrix.append([c[v] for v in vocabulary])

bow_matrix = torch.tensor(bow_matrix)
print(bow_matrix.shape)

def compute_tf(words, vocabulary):
    if isinstance(words, str):
        words = words.split()
    c = Counter(words)
    return [c[v]/len(words) for v in vocabulary]

def compute_df(texts, vocabulary):
    if texts and isinstance(texts[0], str):
        texts = [t.split() for t in texts]
        print(texts)
    df = []
    for v in vocabulary:
        count = 0
        for words in texts:
            if v in words:
                count += 1
        df.append(count)
    return df


def compute_idf(texts, vocabulary):
    if texts and isinstance(texts[0], str):
        texts = [t.split() for t in texts]
    N = len(texts)
    dfs = compute_df(texts, vocabulary)
    return [math.log(N / df) for df in dfs]

tfs = [compute_tf(w, vocabulary) for w in text_words]
tfs = torch.tensor(tfs)
print(tfs.shape)

idfs = compute_idf(text_words, vocabulary)
idfs = torch.tensor(idfs)
print(idfs.shape)

print(tfs * idfs)
