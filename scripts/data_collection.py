from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import numpy as np


def get_match_data_from_url(url):
    # Faz uma requisição GET para a URL e obtém o HTML da página
    print(url)
    response = requests.get(url)
    html_content = response.content

    # Analisa o HTML da página com BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extrai as informações que você deseja do HTML
    scoreboard_team_title = soup.find_all("a", {
        "class": ["catlink-teams tWACM tWAFM tWAN to_hasTooltip", "catlink-teams tWACM tWAFM tWAN"]})
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

    scoreboard_patch = soup.find_all("div", {"class": "sb-datetime-patch"})

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
        row_data = {'week': url.split("/")[-1],
                    'tournament': url.split("/")[4],
                    'split': url.split("/")[6],
                    'team': team.text,
                    'result': result.text,
                    'gold': gold.text,
                    'kills': kills.text,
                    'towers': towers.text,
                    'inhibitors': inhibitors.text,
                    'barons': barons.text,
                    'dragons': dragons.text,
                    'heralds': heralds.text,
                    'time': times,
                    'patch': patches
                    }
        for j, champion in enumerate(champions_matrix[i]):
            row_data[f'champion {j + 1}'] = champion
        data.append(row_data)

    # Cria o DataFrame do Pandas a partir da lista data
    df = pd.DataFrame(data)

    # Exibe o DataFrame
    return df


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


def concat_dataframes(caminho_arquivo):
    # Carrega o arquivo CSV em um DataFrame do Pandas
    df_urls = pd.read_csv(caminho_arquivo)

    # Carrega as posições dos times na semanas
    if df_urls.iloc[0][0].split("/")[4] == "LPL":
        url = df_urls.iloc[0][0]
        parts = url.split("/")
        desired_parts = parts[:7]
        desired_url = "/".join(desired_parts) + "/Results_Diagrams"
        week_df = weekly_team_position(desired_url)
        print('week: ' + week_df['week'].unique())
        print('opponents: ' + week_df['opponent'].unique())
        print('positions: ' + week_df['position'].unique())
    else:
        url = df_urls.iloc[0][0]
        parts = url.split("/")
        desired_parts = parts[:7]
        desired_url = "/".join(desired_parts)
        week_df = weekly_team_position(desired_url)

    match_list = []

    for url in df_urls['urls']:
        match_list.append(get_match_data_from_url(url))
    scoreboard = pd.concat(match_list)

    concatenated_df = adjust_dataframe(scoreboard)
    print(concatenated_df['week'].unique())
    print(concatenated_df['team'].unique())
    print(concatenated_df['opponent'].unique())

    # fazendo o join dos dataframes usando a coluna chave
    full_df = pd.merge(concatenated_df, week_df, on=['week', 'opponent'], how='left')
    full_df['#n'] = full_df.apply(lambda row: f"#_{row.name + 1}", axis=1)

    # Definindo as colunas para categoria
    cat_cols = ['week', 'opponent']
    full_df[cat_cols] = full_df[cat_cols].astype('category')

    full_df['position'] = pd.to_numeric(full_df['position'], errors='coerce').fillna(0).astype('int32')

    return full_df


def adjust_dataframe(dataframe):
    # Mapeia os nomes antigos para os novos
    column_names = {'champion 1': 'top', 'champion 2': 'jungle', 'champion 3': 'mid',
                    'champion 4': 'bot', 'champion 5': 'sup'}

    # Renomeia as colunas
    dataframe = dataframe.rename(columns=column_names)

    dataframe['week'] = dataframe['week'].replace('Scoreboards', 'Week_1')
    # Aplica uma expressão regular para remover números e parênteses
    dataframe['week'] = dataframe['week'].apply(lambda x: re.sub(r'(_\(\d+\))', '', x))

    # Definindo as colunas para int32, verificando e substituindo valores não numéricos por 0
    int_cols = ['kills', 'towers', 'inhibitors', 'barons', 'dragons',
                'heralds']
    for col in int_cols:
        dataframe[col] = pd.to_numeric(dataframe[col], errors='coerce').fillna(0).astype('int32')

    # Definindo as colunas para categoria
    cat_cols = ['tournament', 'split', 'team', 'result', 'patch', 'top', 'jungle',
                'mid', 'bot', 'sup']
    dataframe[cat_cols] = dataframe[cat_cols].astype('category')

    dataframe['team'] = dataframe['team'].str.slice(0, 5)

    # Verificando quais linhas têm o formato mm:ss e convertendo apenas as linhas com o formato mm:ss
    mm_ss_rows = dataframe['time'].str.contains(r'^\d{1,2}:\d{2}$')
    dataframe.loc[mm_ss_rows, 'time'] = pd.to_timedelta('00:' + dataframe.loc[mm_ss_rows, 'time'])
    dataframe['time'] = pd.to_timedelta(dataframe['time']).dt.total_seconds() / 60

    # Remover último caractere da coluna e definindo para float64
    dataframe['gold'] = dataframe['gold'].str[:-1]
    dataframe['gold'] = dataframe['gold'].astype('float64')

    # Ajusta dados do time adversário
    dataframe['opponent'] = dataframe['team'].shift(-1).where(dataframe.index % 2 == 0,
                                                              dataframe['team'].shift(1))
    dataframe['deaths'] = dataframe['kills'].shift(-1).where(dataframe.index % 2 == 0,
                                                             dataframe['kills'].shift(1))
    dataframe['given_towers'] = dataframe['towers'].shift(-1).where(dataframe.index % 2 == 0,
                                                                    dataframe['towers'].shift(1))
    dataframe['given_dragons'] = dataframe['dragons'].shift(-1).where(dataframe.index % 2 == 0,
                                                                      dataframe['dragons'].shift(1))

    dataframe['total_kills'] = dataframe['deaths'] + dataframe['kills']
    dataframe['total_dragons'] = dataframe['given_dragons'] + dataframe['dragons']
    dataframe['total_towers'] = dataframe['given_towers'] + dataframe['towers']

    return dataframe


def weekly_team_position(url):
    # Faz uma requisição GET para a URL e obtém o HTML da página
    response = requests.get(url)
    html_content = response.content

    # Analisa o HTML da página com BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extrai as informações que você deseja do HTML
    tables = soup.find_all("table", {"class": "wikitable timeline"})

    # Cria uma lista para armazenar os dados
    data = []

    # Percorre cada tabela que possui a classe "wikitable timeline"
    for table in tables:
        # Percorre cada linha da tabela
        for tr in table.find_all("tr"):
            if tr.th is not None and "Week" in tr.th.text:
                week_title = tr.th.text
            tds = tr.find_all("td")
            # Verifica se a linha contém informações de uma semana
            if len(tds) > 0:
                # Percorre cada linha da semana para extrair as informações do time
                team_position = tds[0].text.strip()
                team_name = tds[2].get("title")
                # Adiciona as informações na lista de dados
                data.append([week_title, team_name, team_position])

    # Cria um adjust_dataframe com os dados e imprime na tela
    df = pd.DataFrame(data, columns=["week", "opponent", "position"])

    df['week'] = df['week'].str.replace(' ', '_')
    df['opponent'] = df['opponent'].str.slice(0, 5)

    # Exibe o DataFrame
    return df
