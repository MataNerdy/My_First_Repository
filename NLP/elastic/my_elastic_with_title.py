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

for product in products.values():
    title_text = product['title']
    description_text = (product['description'] + ' ' + product['bullet_points'])
    product['title_tokens'] = tokenize(title_text)
    product['description_tokens'] = tokenize(description_text)

print("Строк запрос-товар:", len(rows))
print("Уникальных товаров:", len(products))

first_product_id, first_product = next(iter(products.items()))

print("\nПервый ID:", first_product_id)
print("Title tokens:", first_product['title_tokens'][:30])
print("Количество токенов:", len(first_product['title_tokens']))
print("\nПервые description tokens:",  first_product['description_tokens'][:30])
print("Количество токенов:", len(first_product['description_tokens']))

def build_field_statistics(token_field):
    inverted_index = {}
    document_lengths = {}
    for product_id, product in products.items():
        tokens = product[token_field]
        document_lengths[product_id] = len(tokens)
        for t in tokens:
            if t not in inverted_index:
                inverted_index[t] = {}
            if product_id not in inverted_index[t]:
                inverted_index[t][product_id] = 0
            inverted_index[t][product_id] += 1
    non_empty_lengths = []
    for length in document_lengths.values():
        if length > 0:
            non_empty_lengths.append(length)
    number_of_documents = len(document_lengths)
    average_document_length = (sum(non_empty_lengths) / number_of_documents)
    return (inverted_index, document_lengths, number_of_documents, average_document_length)


(
    title_inverted_index,
    title_lengths,
    title_document_count,
    title_avgdl) = build_field_statistics('title_tokens')

(
    description_inverted_index,
    description_lengths,
    description_document_count,
    description_avgdl) = build_field_statistics('description_tokens')

print("\nTITLE")
print("Терминов:", len(title_inverted_index))
print("Документов:", title_document_count)
print("Средняя длина:", round(title_avgdl, 2))

print("\nDESCRIPTION")
print("Терминов:", len(description_inverted_index))
print("Документов:", description_document_count)
print("Средняя длина:", round(description_avgdl, 2))

print("\nDF токена 'cfm'")

title_cfm_df = len(title_inverted_index.get('cfm', {}))
print("В title:", title_cfm_df)

description_cfm_df = len(description_inverted_index.get('cfm', {}))
print("В description:", description_cfm_df)

def inverted_index_search(query, inverted_index, limit=10):
    query_tokens = tokenize(query)

    candidate_ids = set()
    for token in query_tokens:
        postings = inverted_index.get(token, {})
        candidate_ids.update(postings)

    sorted_ids = sorted(candidate_ids)
    return sorted_ids[:limit]


def field_bm25_score(product_id, query_tokens, inverted_index, document_lengths, number_of_documents, average_document_length, k1 = 1.2, b = 0.75):
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
    return score

def fielded_bm25_search(query, limit=10, title_boost=3, combination='best_fields'):
    query_tokens = tokenize(query)

    candidate_ids = set()

    for token in query_tokens:
        title_postings = title_inverted_index.get(token, {})
        description_postings = description_inverted_index.get(token, {})
        candidate_ids.update(title_postings)
        candidate_ids.update(description_postings)

    scores = {}

    for product_id in candidate_ids:
        title_score = field_bm25_score(product_id, query_tokens, title_inverted_index, title_lengths, title_document_count, title_avgdl)
        description_score = field_bm25_score(product_id, query_tokens, description_inverted_index, description_lengths, description_document_count, description_avgdl)
        title_score *= title_boost
        if combination == 'best_fields':
            final_score = max(title_score, description_score)
        elif combination == 'sum':
            final_score = (title_score + description_score)
        else:
            raise ValueError("Unknown combination")
        scores[product_id] = final_score

    ranked_results = sorted(scores.items(), key=lambda item: (-item[1], item[0]))

    result_ids = []

    for product_id, _ in ranked_results[:limit]:
        result_ids.append(product_id)

    return result_ids

validation_set = []


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

def evaluate_configuration(title_boost, combination, k=10):
    total_precision = 0
    total_recall = 0
    total_mrr = 0
    total_ndcg = 0

    for item in validation_set:
        query = item['query']
        relevant_ids = item['relevant_ids']

        result_ids = fielded_bm25_search(query, limit=k, title_boost=title_boost, combination=combination)
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

    return {
        'combination': combination,
        'boost': title_boost,
        'precision': total_precision / number_of_queries,
        'recall': total_recall / number_of_queries,
        'mrr': total_mrr / number_of_queries,
        'ndcg': total_ndcg / number_of_queries
    }

combination_results = []

for combination in ['sum', 'best_fields']:
    metrics = evaluate_configuration(title_boost=3, combination=combination)
    combination_results.append(metrics)

print(
    "\n"
    "strategy | Precision@10 | Recall@10 "
    "| MRR@10 | nDCG@10"
)

for metrics in combination_results:
    print(
        f"{metrics['combination']:<11} | ",
        f"{metrics['precision']:.3f}       | ",
        f"{metrics['recall']:.3f}    | ",
        f"{metrics['mrr']:.3f} | ",
        f"{metrics['ndcg']:.3f}  "
    )
