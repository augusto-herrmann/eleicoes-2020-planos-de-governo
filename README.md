Documentação não oficial da API DivulgaCandContas do TSE

# Documentação não oficial da API DivulgaCandContas

O Tribunal Superior Eleitoral disponibiliza os dados sobre candidaturas em
eleições de três formas:

1. Para consulta pela web, no sistema
   [DivulgaCandContas](https://divulgacandcontas.tse.jus.br/divulga/);
2. Para download, em arquivos CSV, pelo
   [repositório de dados eleitorais](https://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais);
3. Por uma API do tipo REST.

A API é usada pelo sistema que faz a consulta pela web. Entretanto, ela não
está documentada. Tentativas de obter a documentação oficial junto ao TSE não
lograram êxito. Por isso, decidimos começar a criar uma documentação não
oficial para ajudar a quem mais esteja tentando utilizá-la.

## Como usar

Para usar a API, consulte a documentação no formato
[Open API 2.0](https://swagger.io/specification/v2/). Para mais informações
sobre o padrão Open API, consulte o site [swagger.io](https://swagger.io/).

A documentação está no arquivo
[divulgacandcontas-swagger.yml](divulgacandcontas-swagger.yml). Além disso,
o arquivo [divulgacandcontas.http](divulgacandcontas.http) possui alguns
exemplos de consultas prontas para uso.

## Como contribuir

Essa documentação está em construção e contém apenas uma pequena fração do
que está disponível na API. Caso você encontre alguma outra chamada à API que
seja útil para você, não hesite em enviar o *pull request* com a sua
complementação.
