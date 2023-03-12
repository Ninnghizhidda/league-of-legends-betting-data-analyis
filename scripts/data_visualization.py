import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import webbrowser
import tempfile


def correlation_matrix(dataframe):
    # Calcula a matriz de correlação
    corr_matrix = dataframe[dataframe.columns].corr(numeric_only=True)

    # Visualiza a matriz de correlação com um heatmap
    sns.heatmap(corr_matrix, annot=True)
    plt.show()


def plot_grid(dataframe, value_column, category_column, plot_type='hist', bins='scott', column_number=2, row_number=2):
    # Agrupa os dados por nome de time
    grouped_data = dataframe.groupby(category_column)

    # Calcula o número de subplots necessários
    num_subplots = len(grouped_data)

    # Define as dimensões dos subplots
    rows = row_number
    cols = column_number

    # Cria a figura e os subplots
    fig, axs = plt.subplots(rows, cols, figsize=(12, 6))

    # Itera sobre os grupos e plota o tipo de gráfico selecionado para cada grupo como um subplot separado
    for i, (name, group) in enumerate(grouped_data):
        row = int(i / cols)
        col = i % cols
        if plot_type == 'hist':
            axs[row, col].hist(group[value_column], bins=bins)
            axs[row, col].set_title(f'Histograma de {name} (método de {bins})', fontsize=5)
        elif plot_type == 'box':
            axs[row, col].boxplot(group[value_column])
            axs[row, col].set_title(f'Boxplot de {name}', fontsize=5)

    plt.tight_layout()
    plt.show()


def bars_graphs(dataframe, group_column, data_column, agg_func='sum', ax=None):
    # Agrupa os dados pela coluna especificada e aplica a função de agregação especificada
    grouped_data = dataframe.groupby(group_column)[data_column].agg(agg_func)

    # Plota o gráfico de barras
    if ax is None:
        # se o eixo não for especificado, use o eixo atual
        ax = plt.gca()
    grouped_data.plot(kind='bar', ax=ax)
    ax.set_title(f'{agg_func.capitalize()} de {data_column} por {group_column}')
    ax.set_xlabel(group_column)
    ax.set_ylabel(f'{agg_func.capitalize()} de {data_column}')


def plot_category_statistics(df, category_column, categories_to_highlight=None, cols_to_plot=None, stats=None,
                             sort_column=None, font_size=5):
    # Parâmetros
    font_size = font_size

    # Filtra as linhas do adjust_dataframe para vitórias e derrotas
    df_victory = df.loc[df['result'] == 'Victory']
    df_defeat = df.loc[df['result'] == 'Defeat']

    # Calcula as estatísticas para cada coluna numérica agrupada pela coluna de categoria
    stats_df_victory = df_victory.groupby(category_column)[cols_to_plot].agg(stats)
    stats_df_defeat = df_defeat.groupby(category_column)[cols_to_plot].agg(stats)

    # Plota os gráficos para cada coluna numérica
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:gray']
    fig, axs = plt.subplots(nrows=2, ncols=len(cols_to_plot), figsize=(45, 10))

    for i, col in enumerate(cols_to_plot):
        if sort_column is not None:
            stats_df_victory = stats_df_victory.sort_values([(col, sort_column)], ascending=True)
            stats_df_defeat = stats_df_defeat.sort_values([(col, sort_column)], ascending=True)

        for j, stat in enumerate(stats):
            if stat == 'count':
                axv1 = axs[0][i]
                axv2 = axv1.twinx()
                axd1 = axs[1][i]
                axd2 = axd1.twinx()
                stats_df_victory[col][stat].plot(kind='line', ax=axv2, color=colors[j], alpha=0.7, linestyle='--',
                                                 linewidth=2)
                stats_df_defeat[col][stat].plot(kind='line', ax=axd2, color=colors[j], alpha=0.7, linestyle='--',
                                                linewidth=2)
            else:
                stats_df_victory[col][stat].plot(kind='bar', ax=axs[0][i], color=colors[j], alpha=0.7, width=0.15,
                                                 position=j)
                stats_df_defeat[col][stat].plot(kind='bar', ax=axs[1][i], color=colors[j], alpha=0.7, width=0.15,
                                                position=j)
        # Adiciona valor da coluna para cada categoria no gráfico em si
        for rect in axv1.containers:
            axv1.bar_label(rect, fontsize=font_size/2, padding=3, labels=[f"{v:.1f}" for v in rect.datavalues],
                           label_type="edge", rotation=90, alpha=0.7)

        axv1.set_title(f'{col} por {category_column} (win)', fontsize=font_size)
        axv1.set_ylabel(col, fontsize=font_size)
        axv1.set_xlabel(category_column, fontsize=font_size)
        axv1.tick_params(axis='both', labelsize=font_size)
        axv1.set_xticklabels(axs[0][i].get_xticklabels(), rotation=90)
        axv1.grid(axis='y', alpha=0.5, linestyle='--', linewidth=0.5)

        # define as linhas de grade secundárias (sub-ticks)
        axv1.yaxis.set_minor_locator(plt.MultipleLocator(0.5))
        axv1.grid(axis='y', alpha=0.5, linestyle='--', linewidth=0.75, which='minor')

        axv2.tick_params(axis='both', labelsize=font_size)

        # Adiciona valor da coluna para cada categoria no gráfico em si
        for rect in axd1.containers:
            axd1.bar_label(rect, fontsize=font_size/2, padding=3, labels=[f"{v:.1f}" for v in rect.datavalues],
                           label_type="edge", rotation=90, alpha=0.7)

        axd1.set_title(f'{col} por {category_column} (lose)', fontsize=font_size)
        axd1.set_ylabel(col, fontsize=font_size)
        axd1.set_xlabel(category_column, fontsize=font_size)
        axd1.tick_params(axis='both', labelsize=font_size)
        axd1.set_xticklabels(axs[1][i].get_xticklabels(), rotation=90)
        axd1.grid(axis='y', alpha=0.5, linestyle='--', linewidth=0.5)

        # define as linhas de grade secundárias (sub-ticks)
        axd1.yaxis.set_minor_locator(plt.MultipleLocator(0.5))
        axd1.grid(axis='y', alpha=0.5, linestyle='--', linewidth=0.75, which='minor')

        axd2.tick_params(axis='both', labelsize=font_size)

        if categories_to_highlight is not None:
            for row in axs:
                for ax in row:
                    for tick in ax.get_xticklabels():
                        if tick.get_text() is not None and tick.get_text() in categories_to_highlight:
                            tick.set_weight('bold')

    # Ajusta o espaçamento entre os subplots
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    plt.tight_layout()

    # Exibe os gráficos
    plt.show()


def plot_category_statistics_by_team(df, category_column, cols_to_plot=None, stats=None,
                                     sort_column=None):
    font_size = 5

    stats_df = df.groupby([category_column, 'team'])[cols_to_plot].agg(stats)

    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:gray']
    fig, axs = plt.subplots(nrows=1, ncols=len(cols_to_plot), figsize=(16, 12))

    for i, col in enumerate(cols_to_plot):
        if sort_column is not None:
            stats_df = stats_df.sort_values([(col, sort_column)], ascending=True)

        for j, stat in enumerate(stats):
            stats_df[col][stat].plot(kind='bar', ax=axs[i], alpha=0.7, position=j)

        axs[i].set_title(f'{col} por {category_column}', fontsize=font_size)
        axs[i].set_ylabel(col, fontsize=font_size)
        axs[i].set_xlabel(category_column, fontsize=font_size)
        axs[i].tick_params(axis='both', labelsize=font_size)
        axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation=90)

    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    plt.tight_layout()

    plt.show()


def show_pivot_tables(df, category_column, cols_to_plot, team_name=None, lower_position=0, upper_position=99,
                      weeks=None):
    # Filtra as posições dos times de acordo com o confronto a ser realizado
    df = df.query(f"{lower_position} <= position <= {upper_position}")

    # Filtra apenas as semanas definidas
    if weeks is not None:
        df = df[df['week'].isin(weeks)]

    # Calcula a média por time e por resultado
    mean_stats_df = df.pivot_table(index=category_column, columns='result', values=cols_to_plot, aggfunc='mean')

    # Ordena os dados pelo parâmetro 'cat'
    mean_stats_df = mean_stats_df.sort_values(by=category_column)

    # Renomeia as colunas para melhorar a visualização
    mean_stats_df.columns = [f'{col}_{res}' for res, col in mean_stats_df.columns]
    mean_stats_df.columns = mean_stats_df.columns.str.replace('_', '\n')

    # Arredonda os valores para uma casa decimal
    mean_stats_df = mean_stats_df.round(decimals=1)

    # Converte os DataFrames em strings HTML
    mean_html_string = mean_stats_df.to_html()

    # Coloca em negrito os valores referentes aos times especificados em team_names
    if team_name is not None:
        if team_name in mean_stats_df.index:
            team_row = mean_stats_df.loc[team_name]
            for col_idx, cell in team_row.items():
                if isinstance(cell, (int, float)):
                    cell_str = f'{cell:.1f}'
                else:
                    cell_str = str(cell)
                mean_stats_df.loc[team_name, col_idx] = f'<strong>{cell_str}</strong>'

        # Lê o arquivo CSS
        with open('C:\\npm\\league-of-legends-betting-data-analyis\\outputs\\assets\\pivot.css') as f:
            css = f.read()

        # Convert the DataFrames to HTML strings
        mean_html_string = mean_stats_df.to_html(escape=False, classes='table', index=True)
        mean_html_string = f'<style>{css}</style>' + mean_html_string

    # Salva as strings HTML em arquivos temporários
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as mean_f:
        mean_f.write(mean_html_string.encode('utf-8'))

    # Abre os arquivos temporários no navegador padrão
    webbrowser.open(mean_f.name)
