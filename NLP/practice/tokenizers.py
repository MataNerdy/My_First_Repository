import math


def count_pairs(
    splits: dict[str, list[str]],
    word_frequencies: dict[str, int],
) -> dict[tuple[str, str], int]:
  pair_counts = {}

  for w, s in splits.items():
    frequency = word_frequencies[w]
    for i in range(len(s) - 1):
      pair = (s[i], s[i+1])
      pair_counts[pair] = pair_counts.get(pair, 0) + frequency

  return pair_counts

def merge_pair(symbols: list[str], pair: tuple[str, str]) -> list[str]:
  merged_symbols = []
  i = 0
  while i < len(symbols):
    if (
        i < len(symbols) - 1
        and symbols[i] == pair[0]
        and symbols[i + 1] == pair[1]
        ):
      merged_symbols.append(symbols[i] + symbols[i + 1])
      i += 2
    else:
      merged_symbols.append(symbols[i])
      i += 1
  return merged_symbols

def merge_pairs_in_corpus(
    splits: dict[str, list[str]],
    pair: tuple[str, str]
) -> dict[str, list[str]]:
  updated_splits = {}
  for w, s in splits.items():
    updated_splits[w] = merge_pair(s, pair)
  return updated_splits

def train_bpe(word_frequencies: dict[str, int], number_of_merges: int) -> tuple[dict[str, list[str]], list[tuple[str, str]]]:
  splits = {
      word: list(word) + ['</w>'] for word in word_frequencies
  }

  merges = []
  for step in range(number_of_merges):
    pair_counts = count_pairs(splits, word_frequencies)
    if not pair_counts:
      break
    best_pair = max(pair_counts, key=pair_counts.get)
    splits = merge_pairs_in_corpus(splits, best_pair)
    merges.append(best_pair)
    print(f"{step+1}", best_pair, 'frequency:', pair_counts[best_pair])
  return splits, merges

def bpe_encode(word: str, merges: list[tuple[str, str]]) -> list[str]:
  symbols = list(word) + ['</w>']
  for pair in merges:
    symbols = merge_pair(symbols, pair)
  return symbols

def build_bpe_vocabulary(word_frequencies: dict[str, int], merges: list[tuple[str, str]]) -> list[str]:
  vocabulary = {'<UNK>', '</w>'}
  for w in word_frequencies:
    for c in w:
      vocabulary.add(c)
  for f, s in merges:
    vocabulary.add(f+s)
  other_tokens = sorted(vocabulary - {'<UNK>'})
  return ['<UNK>', *other_tokens]

def bpe_encode_to_ids(word: str, merges: list[tuple[str, str]], token_to_id: dict[str, int]) -> list[int]:
  tokens = bpe_encode(word, merges)
  unknown_id = token_to_id['<UNK>']
  token_ids = []
  for t in tokens:
    token_id = token_to_id.get(t, unknown_id)
    token_ids.append(token_id)
  return token_ids

word_frequencies = {
    "низкий": 2,
    "ниже": 1,
    "новый": 1,
    "новее": 1,
}

final_splits, merges = train_bpe(word_frequencies, 8)

vocabulary = build_bpe_vocabulary(word_frequencies, merges)

token_to_id = {token: idx for idx, token in enumerate(vocabulary)}
id_to_token = {idx: token for token, idx in token_to_id.items()}

def bpe_decode_ids(token_ids: list[int], id_to_token: dict[int, str]) -> str:
  tokens = []

  for t in token_ids:
    token = id_to_token.get(t, '<UNK>')
    tokens.append(token)
  text = ''.join(tokens)
  text = text.replace('</w>', ' ')
  return text.strip()

def find_longest_wordpiece(word: str, start: int, vocabulary: set[str]) -> tuple[str | None, int]:
  for end in range(len(word), start, -1):
    piece = word[start: end]

    if start > 0:
      piece = '##' + piece
    if piece in vocabulary:
      return piece, end
  return None, start

def wordpiece_encode(word: str, vocabulary: set[str]) -> list[str]:
  tokens = []
  start = 0
  while start < len(word):
    piece, end = find_longest_wordpiece(word, start, vocabulary)
    if piece is None:
      return ['[UNK]']
    tokens.append(piece)
    start = end
  return tokens

def wordpiece_decode(tokens: list[str]) -> str:
  result = ''
  for t in tokens:
    if t.startswith('##'):
      result += t[2:]
    else: result += t
  return result

def find_tokens_ending_at(word: str, end: int, token_probabilities: dict[str, float]) -> list[tuple[int, str]]:
  candidates = []
  for start in range(end):
    token = word[start : end]
    if token in token_probabilities:
      candidates.append((start, token))
  return candidates

def unigram_best_scores(word: str, token_probabilities: dict[str, float]) -> tuple[list[float], list[tuple[int, str] | None]]:
  best_scores = [-math.inf] * (len(word)+1)
  best_scores[0] = 0.0
  previous = [None] * (len(word)+1)
  for end in range(1, len(word) + 1):
    candidates = find_tokens_ending_at(word, end, token_probabilities)
    for start, token in candidates:
      if best_scores[start] == -math.inf:
        continue
      candidate_score = (best_scores[start] + math.log(token_probabilities[token]))
      if candidate_score > best_scores[end]:
        best_scores[end] = candidate_score
        previous[end] = (start, token)
  return best_scores, previous

def restore_tokens(word: str, previous: list[tuple[int, str] | None]) -> list[str]:
  tokens = []
  end = len(word)
  while end > 0:
    step = previous[end]
    if step is None:
      return ['[UNK]']
    start, token = step
    tokens.append(token)
    end = start
  tokens.reverse()
  return tokens

def unigram_encode(word: str, token_probabilities: dict[str, float]) -> tuple[list[str], float]:
  best_scores, previous = unigram_best_scores(word, token_probabilities)
  tokens = restore_tokens(word, previous)
  final_score = best_scores[-1]
  return tokens, final_score

def sentencepiece_prepare(text: str) -> str:
  normalized = ' '.join(text.split())
  if not normalized:
    return ''
  return '▁'+normalized.replace(' ', '▁')

def sentencepiece_decode(tokens: list[str]) -> str:
  text = ''.join(tokens)
  text = text.replace('▁', ' ')
  return text.strip()

def encode_tokens(tokens: list[str], token_to_id: dict[str, int], add_special_tokens: bool = True) -> list[int]:
  token_ids = []
  if add_special_tokens:
    token_ids.append(token_to_id['[BOS]'])
  unknown_token = token_to_id['[UNK]']
  for t in tokens:
    token_id = token_to_id.get(t, unknown_token)
    token_ids.append(token_id)
  if add_special_tokens:
    token_ids.append(token_to_id['[EOS]'])
  return token_ids

def pad_sequences(sequences: list[list[int]], pad_id: int) -> tuple[list[list[int]], list[list[int]]]:
  if not sequences:
    return [], []

  max_length = max(len(s) for s in sequences)
  padded_sequences = []
  attention_masks = []

  for s in sequences:
    padding_length = max_length - len(s)
    padded_sequence = (s + [pad_id] * padding_length)
    attention_mask = ([1] * len(s) + [0] * padding_length)
    padded_sequences.append(padded_sequence)
    attention_masks.append(attention_mask)
  return padded_sequences, attention_masks