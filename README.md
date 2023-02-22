Projeto de Análise de Dados de League of Legends para Apoio em Apostas

Este projeto tem como objetivo coletar dados por meio de web scraping das páginas de detalhamento do placar de partidas oficiais da Riot Games armazenadas no site lol.fandom.com. Em seguida, ele realiza análises estatísticas de probabilidade para apoiar na tomada de decisões de entrada e saída nas apostas e compara o risco com as odds abertas no site da Rivalry, que também são coletadas por meio de web scraping.

Arquivos:

data/urls.csv: arquivo com uma lista de URLs do lol.fandom que serão coletados os dados.
main.py: arquivo que centraliza todas as etapas de coleta, normalização, pré-processamento e análises dos dados coletados.
data_collection.py: funções responsáveis pelo web scraping no lol.fandom.
