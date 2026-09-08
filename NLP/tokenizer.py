from transformers import AutoTokenizer

def inspect_tokenizer(model_name: str, text: str) -> None:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors='pt')

    input_ids = inputs['input_ids'][0]

    print(f'\nMODEL: {model_name}')
    print(f'Tokenizer class: {type(tokenizer).__name__}')
    print(f"Is fast: {tokenizer.is_fast}")
    print(f"Inputs: {inputs}")
    print(f"Tokenize: {tokenizer.tokenize(text)}")
    print(f"Tokens: {tokenizer.convert_ids_to_tokens(input_ids)}")
    print(f'Input IDs: {input_ids.tolist()}')
    print(f'Attention mask: {inputs['attention_mask'][0].tolist()}')
    if 'token_type_ids' in inputs:
        print(f'Token type IDs: {inputs['token_type_ids'][0].tolist()}')
    print(f'Decoded: {tokenizer.decode(input_ids)}')
    print(f"Decoded without special tokens: {tokenizer.decode(input_ids, skip_special_tokens=True)}")
    print(f'Tensor shape: {inputs['input_ids']}')

text = "Let's try to tokenize!"

inspect_tokenizer("bert-base-cased", text)