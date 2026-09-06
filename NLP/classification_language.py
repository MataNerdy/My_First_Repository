import random
from pathlib import Path

from collections import Counter

import pandas as pd
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader, Dataset

SEED = 42
random.seed(SEED)
torch.manual_seed(SEED)

def load_csv(path: str | Path) -> tuple[list[str], list[int]]:
    dataframe = pd.read_csv(path)
    texts = dataframe['text'].astype(str).tolist()
    labels = dataframe['label'].astype(int).tolist()
    return texts, labels

DATA_DIR = Path('NLP/data')
train_text, train_label = load_csv(DATA_DIR/'train.csv')
val_text, val_label = load_csv(DATA_DIR/'validation.csv')
test_text, test_label = load_csv(DATA_DIR/'test.csv')
print('Train:', len(train_text))
print('Val:', len(val_text))
print('Test:', len(test_text))