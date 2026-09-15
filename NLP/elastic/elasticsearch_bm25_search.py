"""Индексирование Amazon ESCI и сравнение поиска Elasticsearch BM25 с baseline.

Зависимости:
    pip install "elasticsearch>=8,<10" datasets pandas

Перед запуском задайте адрес кластера:
    export ELASTICSEARCH_URL='http://localhost:9200'
    # Для Elastic Cloud также: export ELASTIC_API_KEY='...'

Пример запуска:
    python elasticsearch_bm25_search.py --recreate-index
"""

from __future__ import annotations

import argparse
import math
import os
import re
from collections import defaultdict
from collections.abc import Callable
from itertools import islice

import pandas as pd
from datasets import load_dataset
from elasticsearch import Elasticsearch, helpers


INDEX_NAME = "products-esci-demo"
POSITIVE_LABELS = {"E"}  # Exact: товар точно соответствует запросу.


def load_esci(rows_to_read: int) -> tuple[list[dict], pd.DataFrame]:
    """Потоково читает небольшой срез открытого Amazon ESCI."""
    stream = load_dataset("shuttie/esci-us-small", split="train", streaming=True)
    rows = list(islice(stream, rows_to_read))
    examples = pd.DataFrame(rows).fillna("")

    catalog = examples[
        [
            "product_id",
            "product_title",
            "product_description",
            "product_bullet_point",
            "product_brand",
        ]
    ].drop_duplicates("product_id")

    products = []
    for row in catalog.itertuples(index=False):
        products.append(
            {
                "product_id": row.product_id,
                "title": row.product_title,
                "description": f"{row.product_description} {row.product_bullet_point}",
                "brand": row.product_brand,
            }
        )
    return products, examples


def create_client() -> Elasticsearch:
    """Подключается к локальному Elasticsearch или Elastic Cloud."""
    url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    api_key = os.getenv("ELASTIC_API_KEY")
    client = Elasticsearch(url, api_key=api_key) if api_key else Elasticsearch(url)
    client.info()  # Ранняя понятная ошибка, если кластер недоступен.
    return client


def create_index(client: Elasticsearch, recreate: bool) -> None:
    """Создаёт индекс с явной настройкой BM25.

    В Elasticsearch BM25 включён по умолчанию. Настройка ниже оставлена
    явной, чтобы параметры ранжирования были видны в учебном примере.
    """
    if client.indices.exists(index=INDEX_NAME):
        if not recreate:
            raise RuntimeError(
                f"Индекс {INDEX_NAME!r} уже существует. "
                "Для пересоздания добавьте --recreate-index."
            )
        client.indices.delete(index=INDEX_NAME)

    client.indices.create(
        index=INDEX_NAME,
        settings={
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "similarity": {"product_bm25": {"type": "BM25", "k1": 1.2, "b": 0.75}},
        },
        mappings={
            "properties": {
                "product_id": {"type": "keyword"},
                "title": {"type": "text", "similarity": "product_bm25"},
                "description": {"type": "text", "similarity": "product_bm25"},
                "brand": {"type": "keyword"},
            }
        },
    )


def index_products(client: Elasticsearch, products: list[dict]) -> None:
    """Загружает карточки пачкой: это быстрее отдельных index-запросов."""
    actions = (
        {"_index": INDEX_NAME, "_id": product["product_id"], "_source": product}
        for product in products
    )
    success, errors = helpers.bulk(client, actions, raise_on_error=False)
    if errors:
        raise RuntimeError(f"Не удалось проиндексировать документов: {errors[:3]}")
    client.indices.refresh(index=INDEX_NAME)
    print(f"Проиндексировано товаров: {success:,}")


def elasticsearch_bm25_search(client: Elasticsearch, query: str, limit: int = 10) -> list[str]:
    """Единый контракт поиска: query + limit -> product_id по убыванию релевантности."""
    response = client.search(
        index=INDEX_NAME,
        size=limit,
        source=False,
        query={
            "multi_match": {
                "query": query,
                "fields": ["title^3", "description"],
                "type": "best_fields",
            }
        },
    )
    return [hit["_id"] for hit in response["hits"]["hits"]]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def build_inverted_index(products: list[dict]) -> dict[str, set[str]]:
    """Упрощённый baseline: обратный индекс без ранжирования BM25."""
    inverted_index: dict[str, set[str]] = defaultdict(set)
    for product in products:
        for token in set(tokenize(f"{product['title']} {product['description']}")):
            inverted_index[token].add(product["product_id"])
    return inverted_index


def inverse_index_search(inverted_index: dict[str, set[str]], query: str, limit: int = 10) -> list[str]:
    """Возвращает кандидатов по OR. Сортировка ID намеренно не является ранжированием."""
    candidates: set[str] = set()
    for token in tokenize(query):
        candidates.update(inverted_index.get(token, set()))
    return sorted(candidates)[:limit]


def build_validation_set(examples: pd.DataFrame, catalog_ids: set[str], max_queries: int) -> list[dict]:
    """Готовит запросы и товары с меткой Exact из ESCI."""
    validation_set = []
    for query, group in examples.groupby("query", sort=False):
        relevant_ids = set(group.loc[group["esci_label"].isin(POSITIVE_LABELS), "product_id"]) & catalog_ids
        if relevant_ids:
            validation_set.append({"query": query, "relevant_ids": relevant_ids})
        if len(validation_set) == max_queries:
            break
    return validation_set


def normalize_result(result: list[str], catalog_ids: set[str], limit: int) -> list[str]:
    """Проверяет результат алгоритма и убирает повторы и неизвестные ID."""
    if not isinstance(result, list):
        raise TypeError("Функция поиска должна вернуть list из product_id")
    unique_ids = []
    for product_id in result:
        if product_id in catalog_ids and product_id not in unique_ids:
            unique_ids.append(product_id)
    return unique_ids[:limit]


def evaluate_search(
    search: Callable[[str, int], list[str]],
    validation_set: list[dict],
    catalog_ids: set[str],
    k: int = 10,
) -> dict[str, float]:
    """Считает средние Precision@k, Recall@k, MRR@k и nDCG@k."""
    totals = defaultdict(float)
    for item in validation_set:
        results = normalize_result(search(item["query"], k), catalog_ids, k)
        hits = [product_id in item["relevant_ids"] for product_id in results]

        totals["precision"] += sum(hits) / k
        totals["recall"] += sum(hits) / len(item["relevant_ids"])
        first_hit = next((rank for rank, hit in enumerate(hits, start=1) if hit), None)
        totals["mrr"] += 1 / first_hit if first_hit else 0.0

        dcg = sum(hit / math.log2(rank + 1) for rank, hit in enumerate(hits, start=1))
        ideal_hits = min(len(item["relevant_ids"]), k)
        ideal_dcg = sum(1 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
        totals["ndcg"] += dcg / ideal_dcg if ideal_dcg else 0.0

    number_of_queries = len(validation_set)
    return {
        f"Precision@{k}": totals["precision"] / number_of_queries,
        f"Recall@{k}": totals["recall"] / number_of_queries,
        f"MRR@{k}": totals["mrr"] / number_of_queries,
        f"nDCG@{k}": totals["ndcg"] / number_of_queries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=3_000, help="Строк ESCI для чтения")
    parser.add_argument("--queries", type=int, default=100, help="Запросов для валидации")
    parser.add_argument("--recreate-index", action="store_true", help="Удалить и создать demo-индекс заново")
    args = parser.parse_args()

    products, examples = load_esci(args.rows)
    client = create_client()
    create_index(client, recreate=args.recreate_index)
    index_products(client, products)

    catalog_ids = {product["product_id"] for product in products}
    validation_set = build_validation_set(examples, catalog_ids, args.queries)
    inverted_index = build_inverted_index(products)

    algorithms = {
        "Обратный индекс без ранжирования": lambda query, limit: inverse_index_search(inverted_index, query, limit),
        "Elasticsearch BM25": lambda query, limit: elasticsearch_bm25_search(client, query, limit),
    }
    table = pd.DataFrame(
        [{"Алгоритм": name, **evaluate_search(search, validation_set, catalog_ids)} for name, search in algorithms.items()]
    ).set_index("Алгоритм")

    print(f"Запросов в валидации: {len(validation_set)}")
    print(table.round(3))


if __name__ == "__main__":
    main()