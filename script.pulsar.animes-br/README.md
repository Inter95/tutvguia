script.pulsar.animes-br
===========================

Brazilian Portuguese content
- one piece (aliançaPROJECT)
- naruto shippuuden (aliançaPROJECT)
- hunter x hunter - 2011 (aliançaPROJECT)

===========================
LEIA-ME
- Modifique o arquivo resources\data.json para adicionar novos animes, se der certo me avise para atualizar o repositório ou se souber como crie um pull request.
- Só vai funcionar com trackers abertos
- Instruções sobre o arquivo resources\data.json:
  - desc: Descrição da entrada.
  - tvdb_id: Código do anime (vide http://thetvdb.com/).
  - search_string: String usada para busca, onde %EPISODE% será substituído pelo número do episódio.
  - tracker_engine: Valores aceitos atualmente -> 'generic' ou 'btdigg_api'.
  - base_url: Parte da URL que fica antes da "String de Busca".

Atenção não se esqueça das virgulas, aspas e chaves.
O tracker_engine "generic" só funciona com pesquisas que retornem o link magnético direto.
