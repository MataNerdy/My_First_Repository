# Практика: Ollama на CPU

Ollama уже установлена на этом Mac. Для CPU лучше выбирать небольшие модели: скорость зависит от процессора, а большие модели требуют много оперативной памяти.

В терминале из этой папки:

```bash
ollama pull qwen2.5:0.5b
python ollama_cpu_chat.py
```

Свой вопрос и модель:

```bash
python ollama_cpu_chat.py --model qwen2.5:0.5b --prompt "Придумай три интента для приложения доставки еды."
```

Скрипт использует локальный HTTP API `http://127.0.0.1:11434/api/chat`, без Python-зависимостей. На машине без GPU/Metal Ollama работает на CPU. Если Ollama не запущен, откройте приложение Ollama или запустите `ollama serve`.

Подробнее об API: [документация Ollama](https://docs.ollama.com/api/chat).
