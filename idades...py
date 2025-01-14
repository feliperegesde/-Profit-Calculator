import pandas as pd


file_path = "C:/Users/User/Downloads/Growth-Internship-Test.xlsx - BY AGE.csv"  
data = pd.read_csv(file_path)


columns_to_clean = [
    'Amount Spent (USD)', 'Link Clicks', 'Purchase Conversion Value (Facebook Pixel)'
]


def clean_numeric_columns(df, columns):
    for column in columns:
        df[column] = pd.to_numeric(
            df[column].replace({'\$': '', ',': '', '': '0'}, regex=True), errors='coerce'
        ).fillna(0)
    return df

data = clean_numeric_columns(data, columns_to_clean)


age_analysis = data.groupby('Age').agg({
    'Amount Spent (USD)': 'sum',
    'Link Clicks': 'sum',
    'Purchase Conversion Value (Facebook Pixel)': 'sum'
}).reset_index()


age_analysis['Average CPC (USD)'] = age_analysis['Amount Spent (USD)'] / age_analysis['Link Clicks']
age_analysis['ROI'] = age_analysis['Purchase Conversion Value (Facebook Pixel)'] / age_analysis['Amount Spent (USD)']


age_analysis.fillna(0, inplace=True)
age_analysis.replace([float('inf'), -float('inf')], 0, inplace=True)


age_analysis = age_analysis.sort_values(by='ROI', ascending=False)


print("Análise por Faixa Etária:")
print(age_analysis)


total_budget = 10000
roi_total = age_analysis['ROI'].sum()
age_analysis['Budget Allocation (EUR)'] = (age_analysis['ROI'] / roi_total) * total_budget

print("\nOrçamento Alocado por Faixa Etária:")
print(age_analysis[['Age', 'ROI', 'Budget Allocation (EUR)']])
