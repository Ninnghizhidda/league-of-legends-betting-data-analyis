import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def correlation_matrix(dataframe):
    # Calcula a matriz de correlação
    corr_matrix = dataframe[dataframe.columns].corr(numeric_only=True)

    # Visualiza a matriz de correlação com um heatmap
    sns.heatmap(corr_matrix, annot=True)
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


def plot_stats_by_category(df, category_column, team_names_to_display=None):
    # Seleciona as colunas numéricas do dataframe
    num_cols = ['Abates do Time', 'Torres do Time', 'Dragões do Time']

    # Filtra as linhas do dataframe para vitórias e derrotas
    df_victory = df.loc[df['Resultado do Time'] == 'Victory']
    df_defeat = df.loc[df['Resultado do Time'] == 'Defeat']

    # Calcula as estatísticas para cada coluna numérica agrupada pela coluna de categoria
    stats_df_victory = df_victory.groupby(category_column)[num_cols].agg(['mean', 'median', 'min', 'max'])
    stats_df_defeat = df_defeat.groupby(category_column)[num_cols].agg(['mean', 'median', 'min', 'max'])

    # Plota os gráficos para cada coluna numérica
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    fig, axs = plt.subplots(nrows=2, ncols=len(num_cols), figsize=(16, 12))
    fig.subplots_adjust(wspace=0.1)

    for i, col in enumerate(num_cols):
        for j, stat in enumerate(['mean', 'median', 'min', 'max']):
            stats_df_victory[col][stat].plot(kind='bar', ax=axs[0][i], color=colors[j], alpha=0.7, width=0.15,
                                             position=j)
            stats_df_defeat[col][stat].plot(kind='bar', ax=axs[1][i], color=colors[j], alpha=0.7, width=0.15,
                                            position=j)

        axs[0][i].set_title(f'{col} por {category_column} (vitória)', fontsize=8)
        axs[0][i].set_xlabel(category_column, fontsize=8)
        axs[0][i].set_ylabel(col, fontsize=8)
        axs[0][i].tick_params(axis='both', labelsize=8)
        axs[0][i].set_xticklabels(axs[0][i].get_xticklabels(), rotation=90)

        axs[1][i].set_title(f'{col} por {category_column} (derrota)', fontsize=8)
        axs[1][i].set_xlabel(category_column, fontsize=8)
        axs[1][i].set_ylabel(col, fontsize=8)
        axs[1][i].tick_params(axis='both', labelsize=8)
        axs[1][i].set_xticklabels(axs[1][i].get_xticklabels(), rotation=90)

        for tick in axs[0][i].get_xticklabels():
            if tick.get_text() in team_names_to_display:
                tick.set_weight('bold')
            tick.set_rotation(90)

        for tick in axs[1][i].get_xticklabels():
            if tick.get_text() in team_names_to_display:
                tick.set_weight('bold')
            tick.set_rotation(90)

    # Ajusta o espaçamento entre os subplots
    plt.subplots_adjust(hspace=0.4, wspace=0.1)

    # Exibe os gráficos
    plt.show()
