import json

with open("config.json") as f:
    cfg = json.load(f)

print(cfg["training"]["learning_rate"])