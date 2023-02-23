import matplotlib.pyplot as plt
import seaborn as sns


def correlation_matrix(dataframe):
    # Calcula a matriz de correlação
    corr_matrix = dataframe[dataframe.columns].corr(numeric_only=True)

    # Visualiza a matriz de correlação com um heatmap
    sns.heatmap(corr_matrix, annot=True)
    plt.show()


def bars_graphs(dataframe, group_column, data_column, agg_func='sum'):
    # Agrupa os dados pela coluna especificada e aplica a função de agregação especificada
    grouped_data = dataframe.groupby(group_column)[data_column].agg(agg_func)

    # Plota o gráfico de barras
    grouped_data.plot(kind='bar')
    plt.title(f'{agg_func.capitalize()} de {data_column} por {group_column}')
    plt.xlabel(group_column)
    plt.ylabel(f'{agg_func.capitalize()} de {data_column}')
    plt.show()
