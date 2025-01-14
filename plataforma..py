import pandas as pd


file_path = "C:/Users/User/Downloads/Growth-Internship-Test.xlsx - BY PLATFORM.csv"  
data = pd.read_csv(file_path)


columns_to_clean = [
    'CPC (Link) (USD)', 'CPC (All) (USD)', 'Cost per 1,000 People Reached (USD)',
    'Cost per Add To Cart (Facebook Pixel) (USD)', 'Cost per Initiate Checkout (Facebook Pixel) (USD)',
    'Cost per Purchase (Facebook Pixel) (USD)', 'Amount Spent (USD)', 'Purchase Conversion Value (Facebook Pixel)'
]


def clean_numeric_columns(df, columns):
    for column in columns:
        df[column] = (
            df[column]
            .replace({'\$': '', '\.': '', ',': '.', ' ': ''}, regex=True)
            .replace('^$', '0', regex=True)  
            .astype(float)  
        )
    return df

data = clean_numeric_columns(data, columns_to_clean)


platform_analysis = data.groupby('Platform').agg({
    'Amount Spent (USD)': 'sum',
    'Link Clicks': 'sum',
    'Purchase Conversion Value (Facebook Pixel)': 'sum'
}).reset_index()


platform_analysis['Average CPC (USD)'] = platform_analysis['Amount Spent (USD)'] / platform_analysis['Link Clicks']
platform_analysis['ROI'] = platform_analysis['Purchase Conversion Value (Facebook Pixel)'] / platform_analysis['Amount Spent (USD)']


platform_analysis.fillna(0, inplace=True)
platform_analysis.replace([float('inf'), -float('inf')], 0, inplace=True)


best_platform = platform_analysis.sort_values(by='ROI', ascending=False)
total_budget = 10000
roi_total = best_platform['ROI'].sum()
best_platform['Budget Allocation (EUR)'] = (best_platform['ROI'] / roi_total) * total_budget

print("\nOrçamento Alocado por Plataforma:")
print(best_platform[['Platform', 'ROI', 'Budget Allocation (EUR)']])


print("Melhor plataforma com base no ROI:")
print(best_platform)