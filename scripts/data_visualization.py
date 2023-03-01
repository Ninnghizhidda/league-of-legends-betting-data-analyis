import matplotlib.pyplot as plt
import seaborn as sns
import textwrap


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


def plot_category_statistics(df, category_column, categories_to_highlight=None, cols_to_plot=None, stats=None,
                             sort_column=None):
    #Parâmetros
    font_size = 5

    # Filtra as linhas do dataframe para vitórias e derrotas
    df_victory = df.loc[df['Resultado do Time'] == 'Victory']
    df_defeat = df.loc[df['Resultado do Time'] == 'Defeat']

    # Calcula as estatísticas para cada coluna numérica agrupada pela coluna de categoria
    stats_df_victory = df_victory.groupby(category_column)[cols_to_plot].agg(stats)
    stats_df_defeat = df_defeat.groupby(category_column)[cols_to_plot].agg(stats)

    # Plota os gráficos para cada coluna numérica
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:gray']
    fig, axs = plt.subplots(nrows=2, ncols=len(cols_to_plot), figsize=(16, 12))

    for i, col in enumerate(cols_to_plot):
        if sort_column is not None:
            stats_df_victory = stats_df_victory.sort_values([(col, sort_column)], ascending=True)
            stats_df_defeat = stats_df_defeat.sort_values([(col, sort_column)], ascending=True)

        for j, stat in enumerate(stats):
            if stat == 'count':
                stats_df_victory[col][stat].plot(kind='line', ax=axs[0][i], color=colors[j], alpha=0.7, linestyle='--',
                                                 linewidth=2)
                stats_df_defeat[col][stat].plot(kind='line', ax=axs[1][i], color=colors[j], alpha=0.7, linestyle='--',
                                                linewidth=2)
            else:
                stats_df_victory[col][stat].plot(kind='bar', ax=axs[0][i], color=colors[j], alpha=0.7, width=0.15,
                                                 position=j)
                stats_df_defeat[col][stat].plot(kind='bar', ax=axs[1][i], color=colors[j], alpha=0.7, width=0.15,
                                                position=j)

        axs[0][i].set_title(f'{col} por {category_column} (vitória)', fontsize=font_size)
        axs[0][i].set_ylabel(col, fontsize=font_size)
        axs[0][i].set_xlabel(category_column, fontsize=font_size)
        axs[0][i].tick_params(axis='both', labelsize=font_size)
        axs[0][i].set_xticklabels(axs[0][i].get_xticklabels(), rotation=90)

        axs[1][i].set_title(f'{col} por {category_column} (derrota)', fontsize=font_size)
        axs[1][i].set_ylabel(col, fontsize=font_size)
        axs[1][i].set_xlabel(category_column, fontsize=font_size)
        axs[1][i].tick_params(axis='both', labelsize=font_size)
        axs[1][i].set_xticklabels(axs[1][i].get_xticklabels(), rotation=90)

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
