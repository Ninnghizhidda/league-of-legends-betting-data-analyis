from scripts.data_collection import concat_dataframes
from scripts.data_visualization import plot_category_statistics

# Contrói a base de dados para análises
df = concat_dataframes(('data/lla_urls.csv'))
print(df)

# Parâmetros
#filtered_category_names = ['T1', 'Kwang']
filtered_category_names = ['Estra', 'The K']

#cols = ['Abates do Time', 'Abates Contra', 'Torres do Time', 'Torres Contra', 'Dragões do Time', 'Dragões Contra']
#cols = ['Torres do Time', 'Torres Contra', 'Dragões do Time', 'Dragões Contra']
cols = ['Abates do Time', 'Abates Contra']
stats = ['mean', 'median', 'min', 'max']

# Chama a função plot_stats_by_category com o filtro de nomes de time
plot_category_statistics(df, 'Nome do Time', categories_to_highlight=filtered_category_names, cols_to_plot=cols
                         , stats=stats, sort_column='mean')
