import json
import math
import re


rows = []
with open("data/esci_sample.jsonl", encoding='utf-8') as f:
    for line in f:
        row = json.loads(line)
        rows.append(row)

products = {}

for row in rows:
    product_id = row['product_id']

    if product_id not in products:
        title = row['product_title'] or ''
        description = row['product_description'] or ''
        bullet_points = row['product_bullet_point'] or ''
        products[product_id] = {
            'title': title,
            'description': description,
            'bullet_points': bullet_points
        }

def tokenize(text):
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return tokens

for product in products.values():
    text = (
        product['title'] + ' ' + product['description'] + ' ' + product['bullet_points']
    )
    product['text'] = text
    product['tokens'] = tokenize(text)

print("Строк запрос-товар:", len(rows))
print("Уникальных товаров:", len(products))

first_product_id, first_product = next(iter(products.items()))

print("\nПервый ID:", first_product_id)
print("Текст:",  first_product['text'])
print("Токены:",  first_product['tokens'][:30])
print("Количество токенов:", len(first_product['tokens']))

inverted_index = {}

for product_id, product in products.items():
    for t in product['tokens']:
        if t not in inverted_index:
            inverted_index[t] = {}
        if product_id not in inverted_index[t]:
            inverted_index[t][product_id] = 0
        inverted_index[t][product_id] += 1

document_lengths = {}

for product_id, product in products.items():
    document_length = len(product['tokens'])
    document_lengths[product_id] = document_length

total_length = sum(document_lengths.values())
number_of_documents = len(document_lengths)
average_document_length = (total_length / number_of_documents)


def inverted_index_search(query, limit=10):
    query_tokens = tokenize(query)

    candidate_ids = set()
    for token in query_tokens:
        postings = inverted_index.get(token, {})
        candidate_ids.update(postings)

    sorted_ids = sorted(candidate_ids)
    return sorted_ids[:limit]


def bm25_search(query, limit=10, k1 = 1.2, b = 0.75):
    query_tokens = tokenize(query)

    candidate_ids = set()

    for token in query_tokens:
        postings = inverted_index.get(token, {})
        candidate_ids.update(postings)

    scores = {}

    for product_id in candidate_ids:
        document_length = document_lengths[product_id]
        length_normalization = (1 - b + b * document_length / average_document_length)
        score = 0
        for token in query_tokens:
            postings = inverted_index.get(token, {})
            if product_id not in postings:
                continue
            term_frequency = postings.get(product_id, 0)
            if term_frequency == 0:
                continue

            document_frequency = len(postings)

            idf = math.log(1 + (number_of_documents - document_frequency + 0.5)/(document_frequency + 0.5))
            tf_weight = (term_frequency * (k1 + 1) / (term_frequency + k1 * length_normalization))

            score += tf_weight * idf

        scores[product_id] = score

    ranked_results = sorted(scores.items(), key=lambda item: (-item[1], item[0]))

    result_ids = []

    for product_id, score in ranked_results[:limit]:
        result_ids.append(product_id)

    return result_ids


queries_in_order = []
relevant_by_query = {}

for row in rows:
    query = row['query'].strip().lower()
    if query not in relevant_by_query:
        relevant_by_query[query] = set()
        queries_in_order.append(query)
    if row["esci_label"] == 'E':
        product_id = row['product_id']
        relevant_by_query[query].add(product_id)


validation_set = []

for query in queries_in_order:
    relevant_ids = relevant_by_query[query]
    if relevant_ids:
        validation_set.append(
            {
                "query": query,
                "relevant_ids": relevant_ids
            }
        )
    if len(validation_set) == 100:
        break

print("\nЗапросов в валидации:", len(validation_set))
print("\nПервый элемент:", validation_set[0])

k = 10

total_precision = 0
total_recall = 0
total_mrr = 0
total_ndcg = 0

for item in validation_set:
    query = item['query']
    relevant_ids = item['relevant_ids']
    result_ids = bm25_search(query, limit=k)
    hits = []
    for product_id in result_ids:
        hits.append(product_id in relevant_ids)

    number_of_hits = sum(hits)
    precision = number_of_hits / k
    recall = (number_of_hits / len(relevant_ids))

    first_relevant_rank = None

    for rank, hit in enumerate(hits, start=1):
        if hit:
            first_relevant_rank = rank
            break

    if first_relevant_rank is None:
        mrr = 0
    else:
        mrr = 1 / first_relevant_rank

    dcg = 0
    for rank, hit in enumerate(hits, start=1):
        if hit:
            dcg += 1 / math.log2(rank + 1)

    ideal_hits = min(k, len(relevant_ids))

    idcg = 0
    for rank in range(1, ideal_hits + 1):
        idcg += 1 / math.log2(rank + 1)

    ndcg = dcg / idcg
    total_precision += precision
    total_recall += recall
    total_mrr += mrr
    total_ndcg += ndcg

number_of_queries = len(validation_set)

mean_precision = total_precision / number_of_queries
mean_recall = total_recall / number_of_queries
mean_mrr = total_mrr / number_of_queries
mean_ndcg = total_ndcg / number_of_queries

print("\nМетрики ручного BM25")
print("Precision@10:", round(mean_precision, 3))
print("Recall@10:", round(mean_recall, 3))
print("MRR@10:", round(mean_mrr, 3))
print("nDCG@10:", round(mean_ndcg, 3))
