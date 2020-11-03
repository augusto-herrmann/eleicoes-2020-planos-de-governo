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

### Experimentando com chamadas à API

Para experimentar com a definição da API no formato Open API, copie o conteúdo
do arquivo [divulgacandcontas-swagger.yml](divulgacandcontas-swagger.yml) e
cole-o em [editor.swagger.io](https://editor.swagger.io/). Será criada uma
interface web para que você possa preencher os parâmetros e experimentar com
as consultas.

Todavia, a API do TSE possui dois problemas que impedirão as consultas de
funcionar pelo navegador: a API não suporta
*[Cross Origin Resource Sharing](https://pt.wikipedia.org/wiki/Cross-origin_resource_sharing)*
(CORS), o que faz com que o navegador bloqueie chamadas à API a partir de
outros domíníos (como o editor Swagger, por exemplo).

Uma possível solução, para quem usa Firefox, é instalar a extensão
[CORS Everywhere](https://addons.mozilla.org/en-US/firefox/addon/cors-everywhere/)
e configurar o "*activation whitelist*" para `/^https:\/\/editor.swagger.io/`.
Ative a extensão na aba do editor de Swagger para que as chamadas à API passem
a funcionar no Firefox.

Você pode encontrar exemplos de scripts para acessar essa API no diretório
[`examples`](examples/).

## Como contribuir

Essa documentação está em construção e contém apenas uma pequena fração do
que está disponível na API. Caso você encontre alguma outra chamada à API que
seja útil para você, não hesite em enviar o *pull request* com a sua
complementação.
