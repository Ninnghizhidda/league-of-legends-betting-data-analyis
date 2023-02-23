from scripts.data_collection import concat_dataframes
from scripts.data_visualization import bars_graphs

# Contrói a base de dados para análises
df = concat_dataframes(('data/urls.csv'))

# Plota o número total de abates por equipe
bars_graphs(df, 'Nome do Time', 'Abates do Time', 'sum')
