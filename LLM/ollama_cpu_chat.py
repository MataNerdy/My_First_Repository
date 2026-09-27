#!/usr/bin/env python3
"""Минимальный запрос к локальной модели Ollama.

Перед запуском:
    ollama pull qwen2.5:0.5b
    python ollama_cpu_chat.py --prompt "Объясни простыми словами, что такое эмбеддинг."
"""

from __future__ import annotations

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def chat(host: str, model: str, prompt: str, max_tokens: int) -> dict:
    """Отправить один запрос в локальный API Ollama без сторонних библиотек."""
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": max_tokens},
        }
    ).encode("utf-8")
    request = Request(
        f"{host.rstrip('/')}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=300) as response:
            return json.load(response)
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama вернул HTTP {error.code}: {details}") from error
    except URLError as error:
        raise RuntimeError(
            "Не удалось подключиться к Ollama. Установите и запустите Ollama, "
            "затем загрузите модель: ollama pull qwen2.5:0.5b"
        ) from error


def main() -> None:
    parser = argparse.ArgumentParser(description="CPU-практика: один запрос к Ollama.")
    parser.add_argument("--model", default="qwen2.5:0.5b", help="локальный тег Ollama")
    parser.add_argument(
        "--prompt",
        default="Объясни простыми словами, что такое эмбеддинг текста, в двух предложениях.",
        help="вопрос модели",
    )
    parser.add_argument("--max-tokens", type=int, default=120, help="максимум новых токенов")
    parser.add_argument("--host", default="http://127.0.0.1:11434", help="адрес Ollama")
    args = parser.parse_args()

    try:
        result = chat(args.host, args.model, args.prompt, args.max_tokens)
    except RuntimeError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        raise SystemExit(2)

    print(result["message"]["content"].strip())
    eval_count = result.get("eval_count")
    eval_duration = result.get("eval_duration")
    if eval_count and eval_duration:
        tokens_per_second = eval_count / (eval_duration / 1_000_000_000)
        print(f"\nСкорость генерации: {tokens_per_second:.1f} токенов/с")


if __name__ == "__main__":
    main()
