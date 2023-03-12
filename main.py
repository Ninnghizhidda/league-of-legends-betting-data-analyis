from scripts.data_collection import concat_dataframes
from scripts.data_visualization import show_pivot_tables

# Choose the league to analysis
league = "ljl"

# Get league data
filename = f"data/{league}_urls.csv"
df = concat_dataframes(filename)

# Parameters analysis
cols = ['kills', 'deaths', 'towers', 'given_towers', 'dragons', 'given_dragons', 'barons', 'given_barons', 'time']
stats = ['mean', 'median', 'min', 'max', 'count']

# Confrontations
teams = {
    'lpl': [['Anyone', 'EDward', 'FunPlu', 'Rare A', 'LNG', 'JD Gam'],
            [1, 12, 11, 11, 1, 1],
            [6, 17, 17, 17, 6, 6]],
    'ljl': [['Sengok', 'Detona', 'SoftBa', 'FENNEL'],
            [1, 1, 1, 1],
            [4, 4, 4, 4]],
    'lck': [['Dplus ', 'BRION', 'Gen. G', 'Kwangd'],
            [6, 1, 6, 1],
            [10, 5, 10, 5]],
    'vcs': [['SBTC', 'GAM', 'CERBER', 'Secret'],
            [1, 1, 5, 1],
            [4, 4, 8, 4]],
    'cbl': [['KaBuM!', 'Los Gr', 'FURIA', 'paiN', 'Libert', 'RED Ca', 'INTZ', 'LOUD', 'Vivo K', 'Fluxo'],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]],
    'lec': [['MAD Li', 'Team B', 'Excel', 'Team V', 'Fnatic', 'SK Gam', 'G2 Esp', 'Astral', 'Team H', 'KOI'],
            [1, 1, 1, 6, 1, 6, 6, 1, 6, 6],
            [5, 5, 5, 10, 5, 10, 10, 5, 10, 10]]
}

team_data = teams[league]

# Create html pivot_tables
for team, low, up in zip(team_data[0], team_data[1], team_data[2]):
    show_pivot_tables(df, category_column='team', cols_to_plot=cols, team_name=team, lower_position=low,
                      upper_position=up)
