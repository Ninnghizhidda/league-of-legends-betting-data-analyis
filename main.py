from scripts.data_collection import concat_dataframes
from scripts.data_visualization import plot_category_statistics
import pandas as pd

# Contrói a base de dados para análises
df = concat_dataframes(('data/lpl_urls.csv'))
#print(df.columns)
#print(df['week'].unique())
print(df['position'].unique())

# Parâmetros
#valor_central = 10
opponent_position = 7
df = df.query('position <= @opponent_position')
#df = df.query('@valor_central - @range_ <= position <= @valor_central + @range_')
#df = df.loc[df['Semana'].isin(['Week_5', 'Week_6', 'Week_7'])]
cat = ['Top E', 'LNG E']
cols = ['kills', 'deaths',
        #'towers', 'given_towers',
        #'dragons', 'given_dragons',
        'time']
stats = ['mean', 'median', 'min', 'max', 'count']


# Chama a função plot_stats_by_category com o filtro de nomes de time
plot_category_statistics(df, 'team', categories_to_highlight=cat, cols_to_plot=cols
                         , stats=stats, sort_column='mean', font_size=8)
