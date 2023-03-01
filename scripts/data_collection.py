from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import numpy as np


def get_time_from_scoreboard_match_time(scoreboard_match_time):
    data_time = []
    for time in scoreboard_match_time:
        # Encontra os valores de tempo no formato "mm:ss" usando regex
        time_text = time.text.strip()
        match = re.match(r"^\d{1,2}:\d{2}$", time_text)

        if match:
            # Adiciona o valor de tempo filtrado à lista de tempos
            minutes, seconds = time_text.split(":")
            time_filtered = f"{minutes.zfill(2)}:{seconds}"
            data_time.append(time_filtered)

    scoreboard_match_time = []

    for time in data_time:
        scoreboard_match_time.append(time)
        scoreboard_match_time.append(time)

    return scoreboard_match_time


def get_match_data_from_url(url):
    # Faz uma requisição GET para a URL e obtém o HTML da página
    response = requests.get(url)
    html_content = response.content

    # Analisa o HTML da página com BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extrai as informações que você deseja do HTML
    scoreboard_team_title = soup.find_all("a", {"class": "catlink-teams tWACM tWAFM tWAN to_hasTooltip"})
    scoreboard_match_result = soup.find_all("div", {"class": "sb-header-vertict"})
    scoreboard_match_gold = soup.find_all("div", {"class": "sb-header-Gold"})
    scoreboard_match_kills = soup.find_all("div", {"class": "sb-header-Kills"})
    scoreboard_match_towers = soup.find_all("div", {"class": "sb-footer-item sb-footer-item-towers"})
    scoreboard_match_inhibitors = soup.find_all("div", {"class": "sb-footer-item sb-footer-item-inhibitors"})
    scoreboard_match_barons = soup.find_all("div", {"class": "sb-footer-item sb-footer-item-barons"})
    scoreboard_match_dragons = soup.find_all("div", {"class": "sb-footer-item sb-footer-item-dragons"})
    scoreboard_match_heralds = soup.find_all("div", {"class": "sb-footer-item sb-footer-item-riftheralds"})

    scoreboard_match_time = soup.find_all("th", {"colspan": "2"})
    scoreboard_match_time = get_time_from_scoreboard_match_time(scoreboard_match_time)

    scoreboard_patch = soup.find_all(lambda tag: tag.name == 'a' and re.search(r'Patch 13', tag.text))
    scoreboard_match_patches = []
    for patch in scoreboard_patch:
        scoreboard_match_patches.append(patch.text)
        scoreboard_match_patches.append(patch.text)

    scoreboard_champions = soup.select('span.sprite.champion-sprite:not(.sb-footer-bans span.sprite.champion-sprite)')

    # Pivotar os campeões do time em 5 colunas diferentes
    champions = [champion.get('title') for champion in scoreboard_champions]
    champions_matrix = np.reshape(champions, (-1, 5))

    # Loop pelos elementos encontrados nas duas listas simultaneamente
    data = []
    for i, (team, result, gold, kills, towers, inhibitors, barons, dragons, heralds, times, patches) in \
            enumerate(zip(scoreboard_team_title, scoreboard_match_result,
                          scoreboard_match_gold, scoreboard_match_kills,
                          scoreboard_match_towers, scoreboard_match_inhibitors,
                          scoreboard_match_barons, scoreboard_match_dragons,
                          scoreboard_match_heralds, scoreboard_match_time,
                          scoreboard_match_patches)):
        # Adiciona um dicionário com os dados do time e do resultado à lista data
        row_data = {'Semana': url.split("/")[-1],
                    'Torneio': url.split("/")[4],
                    'Split': url.split("/")[6],
                    'Nome do Time': team.text,
                    'Resultado do Time': result.text,
                    'Ouro do Time': gold.text,
                    'Abates do Time': kills.text,
                    'Torres do Time': towers.text,
                    'Inibidores do Time': inhibitors.text,
                    'Barões do Time': barons.text,
                    'Dragões do Time': dragons.text,
                    'Arautos do Time': heralds.text,
                    'Tempo de Jogo': times,
                    'Patch do Jogo': patches
                    }
        for j, champion in enumerate(champions_matrix[i]):
            row_data[f'Campeão {j + 1}'] = champion
        data.append(row_data)

    # Cria o DataFrame do Pandas a partir da lista data
    df = pd.DataFrame(data)

    # Exibe o DataFrame
    return df


def concat_dataframes(caminho_arquivo):
    # Carrega o arquivo CSV em um DataFrame do Pandas
    df_urls = pd.read_csv(caminho_arquivo)

    df_list = []

    for url in df_urls['urls']:
        df_list.append(get_match_data_from_url(url))

    concatenated_df = dataframe(pd.concat(df_list))

    return concatenated_df


def dataframe(dataframe):
    # Mapeia os nomes antigos para os novos
    column_names = {'Campeão 1': 'Top', 'Campeão 2': 'Jungle', 'Campeão 3': 'Mid',
                    'Campeão 4': 'Bot', 'Campeão 5': 'Sup'}

    # Renomeia as colunas
    dataframe = dataframe.rename(columns=column_names)

    dataframe['Semana'] = dataframe['Semana'].replace('Scoreboards','Week_1')

    # Definindo as colunas para int32, verificando e substituindo valores não numéricos por 0
    int_cols = ['Abates do Time', 'Torres do Time', 'Inibidores do Time', 'Barões do Time', 'Dragões do Time',
                'Arautos do Time']
    for col in int_cols:
        dataframe[col] = pd.to_numeric(dataframe[col], errors='coerce').fillna(0).astype('int32')

    # Definindo as colunas para categoria
    cat_cols = ['Semana', 'Torneio', 'Split', 'Nome do Time', 'Resultado do Time', 'Patch do Jogo', 'Top', 'Jungle',
                'Mid', 'Bot', 'Sup']
    dataframe[cat_cols] = dataframe[cat_cols].astype('category')

    dataframe['Nome do Time'] = dataframe['Nome do Time'].str.slice(0, 5)

    # Verificando quais linhas têm o formato mm:ss e convertendo apenas as linhas com o formato mm:ss
    mm_ss_rows = dataframe['Tempo de Jogo'].str.contains(r'^\d{1,2}:\d{2}$')
    dataframe.loc[mm_ss_rows, 'Tempo de Jogo'] = pd.to_timedelta('00:' + dataframe.loc[mm_ss_rows, 'Tempo de Jogo'])

    # Remover último caractere da coluna e definindo para float64
    dataframe['Ouro do Time'] = dataframe['Ouro do Time'].str[:-1]
    dataframe['Ouro do Time'] = dataframe['Ouro do Time'].astype('float64')

    # Ajusta dados do time adversário
    dataframe['Abates Contra'] = dataframe['Abates do Time'].shift(-1).where(dataframe.index % 2 == 0,
                                                                           dataframe['Abates do Time'].shift(1))
    dataframe['Torres Contra'] = dataframe['Torres do Time'].shift(-1).where(dataframe.index % 2 == 0,
                                                                           dataframe['Torres do Time'].shift(1))
    dataframe['Dragões Contra'] = dataframe['Dragões do Time'].shift(-1).where(dataframe.index % 2 == 0,
                                                                           dataframe['Dragões do Time'].shift(1))

    dataframe['Total de Abates'] = dataframe['Abates Contra'] + dataframe['Abates do Time']
    dataframe['Total de Dragões'] = dataframe['Dragões Contra'] + dataframe['Dragões do Time']
    dataframe['Total de Torres'] = dataframe['Torres Contra'] + dataframe['Torres do Time']

    return dataframe
