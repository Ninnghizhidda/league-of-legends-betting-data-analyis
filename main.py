from scripts.data_collection import concat_dataframes
from scripts.data_visualization import plot_category_statistics

# Contrói a base de dados para análises
df = concat_dataframes(('data/cblol_academy_urls.csv'))
print(df)

# Parâmetros
#filtered_category_names = ['Fluxo Academy', 'LOUD Academy']
#filtered_category_names = ['Liberty [...]', 'FURIA Academy']
filtered_category_names = ['RED Academy', 'paiN Academy']
cols = ['Abates do Time', 'Abates Contra']
stats = ['mean', 'median', 'min', 'max', 'count']

# Chama a função plot_stats_by_category com o filtro de nomes de time
plot_category_statistics(df, 'Nome do Time', categories_to_highlight=filtered_category_names, cols_to_plot=cols, stats=stats)
