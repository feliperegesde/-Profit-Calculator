import pandas as pd

# Carregar o arquivo Excel
file_path = "C:/Users/User/Downloads/Growth-Internship-Test.xlsx - BY COUNTRY.csv"  # Substitua pelo caminho correto
data = pd.read_csv(file_path)

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

# Agrupar por país e calcular métricas
country_analysis = data.groupby('Country').agg({
    'Amount Spent (USD)': 'sum',
    'Link Clicks': 'sum',
    'Purchase Conversion Value (Facebook Pixel)': 'sum'
}).reset_index()

# Calcular métricas adicionais
country_analysis['Average CPC (USD)'] = country_analysis['Amount Spent (USD)'] / country_analysis['Link Clicks']
country_analysis['ROI'] = country_analysis['Purchase Conversion Value (Facebook Pixel)'] / country_analysis['Amount Spent (USD)']

# Tratar valores nulos e infinitos
country_analysis.fillna(0, inplace=True)
country_analysis.replace([float('inf'), -float('inf')], 0, inplace=True)

# Ordenar por ROI para encontrar o país mais lucrativo
country_analysis = country_analysis.sort_values(by='ROI', ascending=False)

# Exibir a análise por país
print("Análise por País:")
print(country_analysis)

# Alocar orçamento baseado no ROI (10.000 euros)
total_budget = 10000
roi_total = country_analysis['ROI'].sum()
country_analysis['Budget Allocation (EUR)'] = (country_analysis['ROI'] / roi_total) * total_budget

print("\nOrçamento Alocado por País:")
print(country_analysis[['Country', 'ROI', 'Budget Allocation (EUR)']])
