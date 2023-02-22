import matplotlib.pyplot as plt
from scripts.data_collection import concat_dataframes
import seaborn as sns

# Contrói a base de dados para análises
df = concat_dataframes(('data/urls.csv'))

# Calcula a matriz de correlação
corr_matrix = df[df.columns].corr(numeric_only=True)
print(corr_matrix)

# Visualiza a matriz de correlação com um heatmap
sns.heatmap(corr_matrix, annot=True)
plt.show()
