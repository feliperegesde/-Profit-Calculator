import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo Excel
file_path = "C:/Users/User/Downloads/Growth-Internship-Test.xlsx - BY AGE.csv"  # Substitua pelo caminho correto
data = pd.read_csv(file_path)

# Converter colunas monetárias e métricas relevantes para valores numéricos
columns_to_clean = [
    'Amount Spent (USD)', 'Link Clicks', 'Purchase Conversion Value (Facebook Pixel)'
]

# Função para limpar e converter colunas numéricas
def clean_numeric_columns(df, columns):
    for column in columns:
        df[column] = pd.to_numeric(
            df[column].replace({'\$': '', ',': '', '': '0'}, regex=True), errors='coerce'
        ).fillna(0)
    return df

data = clean_numeric_columns(data, columns_to_clean)

# Agrupar por faixa etária e calcular métricas
age_analysis = data.groupby('Age').agg({
    'Amount Spent (USD)': 'sum',
    'Link Clicks': 'sum',
    'Purchase Conversion Value (Facebook Pixel)': 'sum'
}).reset_index()

# Calcular métricas adicionais
age_analysis['Average CPC (USD)'] = age_analysis['Amount Spent (USD)'] / age_analysis['Link Clicks']
age_analysis['ROI'] = age_analysis['Purchase Conversion Value (Facebook Pixel)'] / age_analysis['Amount Spent (USD)']

# Tratar valores nulos e infinitos
age_analysis.fillna(0, inplace=True)
age_analysis.replace([float('inf'), -float('inf')], 0, inplace=True)

# Alocar orçamento baseado no ROI (10.000 euros)
total_budget = 10000
roi_total = age_analysis['ROI'].sum()
age_analysis['Budget Allocation (EUR)'] = (age_analysis['ROI'] / roi_total) * total_budget

# Gráfico: ROI e Orçamento por Faixa Etária
plt.figure(figsize=(10, 6))
plt.bar(age_analysis['Age'], age_analysis['ROI'], label='ROI', alpha=0.7, color='blue')
plt.plot(age_analysis['Age'], age_analysis['Budget Allocation (EUR)'], label='Budget Allocation (EUR)', color='red', marker='o', linewidth=2)

# Adicionar legendas, títulos e rótulos
plt.title('ROI e Orçamento Alocado por Faixa Etária')
plt.xlabel('Faixa Etária')
plt.ylabel('Valores')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Exibir o gráfico
plt.show()
