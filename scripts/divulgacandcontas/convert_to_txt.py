"""Percorre a árvore de diretórios e converte os arquivos PDF para TXT.
"""

import os
from pathlib import Path

from tika import parser

def convert_file(source_doc: str):
    "Converte o arquivo PDF para TXT."
    output_file = (
        '.'
        .join(source_doc.split('.')[:-1])
        .replace('/pdfs/', '/txts/')
     ) + '.txt'
    output_dir, file_name = os.path.split(output_file)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(output_file):
        parsed = parser.from_file(source_doc)
        if parsed['content']:
            with open(output_file, 'w') as f:
                f.write(parsed['content'])

root_dir = '.'

for dir_name, subdirs, files in os.walk(root_dir):
    print(f'Percorrendo o diretório {dir_name}...')
    for file_name in files:
        if file_name.split('.')[-1] == 'pdf':
            print(f'Convertendo {file_name}...')
            convert_file(os.path.join(dir_name,file_name))