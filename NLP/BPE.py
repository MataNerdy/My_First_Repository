from transformers import AutoModel, AutoTokenizer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

print(1)

model = AutoModel.from_pretrained('gpt2')
tokenizer = AutoTokenizer.from_pretrained('gpt2')

embeddings = model.wte.weight.detach().numpy()
print(embeddings.shape)