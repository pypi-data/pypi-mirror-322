import json
import re
import os
import tiktoken


def count_tokens(input_string: str) -> int:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(input_string)
    return len(tokens)

def validate_obj(obj):
     return bool(
          (products := obj.get('products')) \
                and any(
                    list(
                        filter(
                            lambda prod: (name := prod.get('name')) \
                                            and prod.get('price_range') \
                                                and prod.get('purchase_link') \
                                                    and (re.search(r'\d', prod.get('price_range')) \
                                                        and 'http' in prod.get('purchase_link')),
                                                        products
                                )
                        )
                    )
                )

def jsonify(filename, obj):
    base_dir = 'output'
    int_dir = 'json_contents'
    good_results_dir = os.path.join(base_dir, int_dir, 'good_results')
    bad_results_dir = os.path.join(base_dir, int_dir, 'bad_results')
    os.makedirs(good_results_dir, exist_ok=True)
    os.makedirs(bad_results_dir, exist_ok=True)
    file_name = f'{filename}.json'
    file_path = os.path.join((good_results_dir if validate_obj(obj) else bad_results_dir), file_name) 
                                    
    with open(file_path, 'w') as f:
        f.write(json.dumps(obj, indent=4))
    print(f'\n📝 Stored results at `{file_path}`.\n')

def store_web_reader_contents(filename, contents):
    base_dir = 'output'
    int_dir = 'scraped_contents'
    folder_path = os.path.join(base_dir, int_dir)
    os.makedirs(folder_path, exist_ok= True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as f:
        f.write(contents)
    print(f'\n📝 Stored Scraped Contents at `{file_path}`.\n')
