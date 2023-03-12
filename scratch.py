from scripts.data_collection import concat_dataframes
import webbrowser
import tempfile

def show_pivot_table(df, category_column, cols_to_plot):
    # Calcula a média por time e por resultado
    stats_df = df.pivot_table(index=category_column, columns='result', values=cols_to_plot, aggfunc='mean')

    # Renomeia as colunas para melhorar a visualização
    stats_df.columns = [f'{col}_{res}' for res, col in stats_df.columns]
    stats_df.columns = stats_df.columns.str.replace('_', '\n')

    # Ordena os dados pelo parâmetro 'cat'
    stats_df = stats_df.sort_values(by=category_column)

    # Arredonda os valores para uma casa decimal
    stats_df = stats_df.round(decimals=1)

    # Converte o DataFrame em uma string HTML
    html_string = stats_df.to_html()

    # Salva a string HTML em um arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        f.write(html_string.encode('utf-8'))

    # Abre o arquivo temporário no navegador padrão
    webbrowser.open(f.name)

# Exemplo de uso:
dataframe = concat_dataframes(('data/lcs_urls.csv'))

