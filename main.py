from scripts.data_collection import concat_dataframes
from scripts.data_visualization import plot_stats_by_category

# Contrói a base de dados para análises
df = concat_dataframes(('data/lpl_urls.csv'))

# Filtra apenas as linhas que contenham os nomes de Time especificados
team_names = ['FunPlus Phoenix','LGD Gaming']

# Chama a função plot_stats_by_category com o filtro de nomes de time
plot_stats_by_category(df, 'Nome do Time', team_names_to_display=team_names)
