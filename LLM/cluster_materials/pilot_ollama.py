import csv
import json
from urllib.request import Request, urlopen
from pathlib import Path


output_path = Path("ollama_synthetic.csv")

if output_path.exists():
  with output_path.open(encoding="utf-8-sig", newline="") as file:
    done = {row["intent"] for row in csv.DictReader(file)}
else:
  done = set()

with open("train_labeled.csv", encoding="utf-8-sig", newline="") as file:
  rows = list(csv.DictReader(file))

intents = sorted({row["intent"] for row in rows})
print("Amount of intents:", len(intents))
print(intents[:5])


for intent in intents:
    if intent in done:
        continue
    print(f"Генерирую: {intent}", flush=True)
    examples = [item["text"] for item in rows if item["intent"] == intent]

    prompt = f"""Напиши один новый естественный запрос пользователя на русском языке
    для интента {intent}.

    Два обучающих примера:
    1. {examples[0]}
    2. {examples[1]}

    Сохрани интент, но используй другую формулировку.
    Ответь только одной фразой без кавычек, нумерации и пояснений."""

    payload = json.dumps({
        "model": "qwen2.5:7b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.6, "num_predict": 120},
    }).encode("utf-8")

    request = Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    with urlopen(request, timeout=600) as response:
        generated = json.load(response)["response"]

    with output_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "intent"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({"text": generated.strip(), "intent": intent})

    print(f"\n{intent}: {generated}")
