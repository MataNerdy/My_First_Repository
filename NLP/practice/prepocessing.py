from bs4 import BeautifulSoup
from collections import Counter
import hashlib


def extract_text(html: str) -> str:
  soup = BeautifulSoup(html, 'html.parser')
  for tag in soup(["script", "style", "nav", "footer"]):
    tag.extract()
  text = soup.get_text(separator='\n', strip=True)
  return text

def normalize_whitespace(text: str) -> str:
  lines = text.splitlines()
  cleaned_lines = []
  for l in lines:
    words = l.split()
    if words:
      cleaned_line = ' '.join(words)
      cleaned_lines.append(cleaned_line)
  return '\n'.join(cleaned_lines)

def check_min_length(text: str, min_character: int=50) -> bool:
  return len(text) > min_character

def repeated_line_ratio(text: str) -> float:
  lines = text.splitlines()
  if not lines:
    return 0.0
  counter = Counter(lines)
  amount_of_repeated_lines = 0
  for c in counter.values():
    if c > 1:
      amount_of_repeated_lines += c
  return amount_of_repeated_lines / len(lines)


def short_lines_ratio(text: str, min_length: int = 30) -> float:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return 0.0

    number_of_short_lines = 0

    for line in lines:
        if len(line) < min_length:
            number_of_short_lines += 1

    return number_of_short_lines / len(lines)


def get_quality_issues(text: str, min_length: int=50, max_repeated_ratio: float=0.5, max_short_lines_ratio: float=0.5) -> list[str]:
  issues = []
  if len(text) < min_length:
    issues.append("too_short")
  if repeated_line_ratio(text) >= max_repeated_ratio:
    issues.append("repeated_lines")
  if short_lines_ratio(text) >= max_short_lines_ratio:
    issues.append("short_lines")
  return issues

def get_text_hash(text: str) -> str:
  normalized_text = normalize_whitespace(text).lower()
  print(normalized_text)
  encoded = normalized_text.encode('utf-8')
  return hashlib.sha256(encoded).hexdigest()

def remove_exact_duplicates(texts: list[str]) -> list[str]:
  seen_hashes = set()
  unique_texts = []
  for t in texts:
    t_hash = get_text_hash(t)
    if t_hash not in seen_hashes:
      seen_hashes.add(t_hash)
      unique_texts.append(t)
  return unique_texts

def get_word_ngrams(text: str, n: int=3) -> set[tuple[str, ...]]:
  if n <= 0:
    raise ValueError("n должно быть больше 0")
  norm_text = normalize_whitespace(text).lower()
  words = norm_text.split()

  ngrams = set()

  for i in range(len(words) - n + 1):
    ngram = tuple(words[i:i+n])
    ngrams.add(ngram)

  return ngrams

def jaccard_similarity(first: set, second: set) -> float:
  union = first | second
  if not union:
    return 1.0
  intersection = first & second
  return len(intersection) / len(union)

def are_near_duplicates(text_a: str, text_b: str, n: int=2, threshold: float=0.9) -> bool:
  first_ngrams = get_word_ngrams(text_a, n)
  second_ngrams = get_word_ngrams(text_b, n)
  if not first_ngrams or not second_ngrams:
    first_norm = normalize_whitespace(text_a).lower()
    second_norm = normalize_whitespace(text_b).lower()
    return first_norm == second_norm

  similarity = jaccard_similarity(first_ngrams, second_ngrams)
  return similarity >= threshold


def remove_near_duplicates(texts: list[str], n: int=2, threshold: float=0.4) -> list[str]:
  unique_texts = []
  for t in texts:
    duples_found = False
    for u in unique_texts:
      if are_near_duplicates(t, u, n, threshold):
        duples_found = True
        break
    if not duples_found:
      unique_texts.append(t)
  return unique_texts