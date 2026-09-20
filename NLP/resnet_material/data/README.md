# Локальная выборка MASSIVE (ru-RU)

Он содержит ровно 60 интентов MASSIVE и фиксированную стратифицированную выборку: по 2 непересекающихся русских запроса каждого интента в `train`, `validation` и `evaluation` (120 строк в каждом файле).

## Файлы

| Файл | Поля | Назначение |
| --- | --- | --- |
| `train_labeled.csv` | `text`, `intent` | Только для самостоятельного дообучения эмбеддера. |
| `validation_labeled.csv` | `query_id`, `text`, `intent` | Подбор параметров UMAP/HDBSCAN и промежуточная оценка. |
| `evaluation_queries.csv` | `query_id`, `text` | Вход финальной системы. |
| `evaluation_labels.csv` | `query_id`, `intent` | Открытый локальный эталон для `validate_clustering.py`. |

`query_id` следует читать как строку: начальные нули значимы. Метка `intent` — исходный идентификатор MASSIVE формата `scenario_intent`.

## Происхождение и воспроизводимость

Источник: Amazon Science, **MASSIVE 1.1: A 1M-Example Multilingual Natural Language Understanding Dataset with 52 Typologically-Diverse Languages**, русская конфигурация `ru-RU` на [Hugging Face](https://huggingface.co/datasets/AmazonScience/massive). Исходный датасет содержит 60 интентов; карточка датасета и репозиторий: [alexa/massive](https://github.com/alexa/massive).

