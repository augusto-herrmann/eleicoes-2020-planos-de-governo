# Dados dos Planos de Governo das Eleições Municipais de 2020

Os candidatos a prefeita(o) são obrigados a apresentar à justiça eleitoral
um plano de governo, detalhando as propostas que têm ao eleitor. A análise
dessas propostas pode enriquecer bastante as discussões democráticas no
período eleitoral, uma vez que o eleitor pode comparar entre os candidatos
qual deles apresenta propostas que se aproximam dos seus anseios, daquilo
que o eleitor quer que seja feito em seu município.

Dado que o volume de planos de governo é considerável, pois são vária(o)s
candidata(o)s em cada um dos 5.570, a análise desses documentos de forma
agregada pode trazer informações imporantes para as discussões políticas.
Qual partido tem mais candidata(o)s a prefeita(o) que têm propostas que
mencionam o saneamento básico? Qual perfil de candidato se preocupa mais
com as feiras de produtos agrícolas, com o transporte público, etc.?

O Tribunal Superior Eleitoral disponibiliza os dados sobre candidaturas em
eleições de três formas:

1. Para consulta pela web, no sistema
   [DivulgaCandContas](https://divulgacandcontas.tse.jus.br/divulga/);
2. Para download, em arquivos CSV, pelo
   [repositório de dados eleitorais](https://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais);
3. Por uma API do tipo REST
   [não documentada](https://github.com/augusto-herrmann/divulgacandcontas-doc).

Baixar os documentos das propostas um a um a partir do sistema, considerando
que são dezenas de milhares, seria uma tarefa impossível. Seria ótimo se
o repositório de dados eleitorais tivesse os planos de governo, mas não os
têm. A única alternativa que encontramos foi usar a
[API do DivulgaCandContas](https://github.com/augusto-herrmann/divulgacandcontas-doc)
para encontrar os links de cada um e fazer dos downloads. E assim foi
construído este conjunto de dados.

## Organização dos dados

Os dados sobre candidatos estão no arquivo
[dados/planos-de-governo.csv](dados/planos-de-governo.csv). Os textos com
os planos de governo estão na pasta [dados/propostas](dados/propostas),
separados por estado, município e nome de urna da(o) candidata(o).
