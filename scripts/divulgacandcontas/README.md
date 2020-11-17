
# mayor_proposals.py

Esse script acessa a API do TSE e exporta um CSV com os links
das propostas feitas por candidatos a prefeito.

## Pré-requisitos

Instale o `requests` e baixe o arquivo de municípios do Brasil
em https://basedosdados.org/dataset/br-basedosdados-diretorios-brasil#

Coloque o arquivo baixado na mesma pasta que esse script.
Execute `python mayor_proposals.py` para exportar um CSV com os
links para as propostas.

## Como usar

Caso queira fazer download dos arquivos PDF, execute:

`python mayor_proposals.py --download-proposals`

Os PDFs baixados estarão na subpasta `pdfs`, separados por estado e cidade.

Caso queira continuar um download parcial (por exemplo, que tenha sido
interrompido manualente ou que tenha falhado por conexão de rede), use:

`python mayor_proposals.py --continue-from arquivo-parcial.csv`
