from transformers import AutoTokenizer, BertTokenizer

tokenized_text = 'Jim Henson was a puppeteer'.split()
print(tokenized_text)

tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
inputs = tokenizer("Let's try to tokenize!")
print('Auto', inputs)

tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
inputs = tokenizer("Let's try to tokenize!")
print('Bert', inputs)

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
inputs = tokenizer("Let's try to tokenize!")
print(inputs)
print(inputs['input_ids'])
tokens = tokenizer.tokenize("Let's try to tokenize!")
inputs_ids = tokenizer.convert_tokens_to_ids(tokens)
final_input_ids = [
    tokenizer.cls_token_id,
    *inputs_ids,
    tokenizer.sep_token_id,
]
print(tokens)
print(inputs_ids)
print(final_input_ids)
print(tokenizer.decode(inputs['input_ids']))

tokenizer = AutoTokenizer.from_pretrained('albert-base-v1')
tokens = tokenizer.tokenize("Let's try to tokenize!")
print(tokens)

tokenizer = AutoTokenizer.from_pretrained('roberta-base')
inputs = tokenizer("Let's try to tokenize!")
print(tokenizer.decode(inputs['input_ids']))