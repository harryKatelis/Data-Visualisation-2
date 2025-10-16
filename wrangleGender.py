import pandas as pd

# URLs
url_2011 = "https://raw.githubusercontent.com/harryKatelis/FIT3179-Vega-lite/refs/heads/main/genderstate2011.csv"
url_2017 = "https://raw.githubusercontent.com/harryKatelis/FIT3179-Vega-lite/refs/heads/main/genderstate2017%232.csv"

# Load CSVs
df_2011 = pd.read_csv(url_2011)
df_2017 = pd.read_csv(url_2017)

# Add Year column
df_2011['Year'] = 2011
df_2017['Year'] = 2017

# Keep relevant columns (Total, Male, Female numbers + proportion + population)
df_2011 = df_2011[['Name', 'Number', 'Proportion (%)', 'Population', 'Number2', 'Proportion (%)2', 'Number3', 'Proportion (%)3', 'Year']]
df_2017 = df_2017[['Name', 'Number', 'Proportion (%)', 'Population', 'Number2', 'Proportion (%)2', 'Number3', 'Proportion (%)3', 'Year']]

# Remove commas and convert numbers to int
for col in ['Number', 'Number2', 'Number3', 'Population']:
    df_2011[col] = df_2011[col].str.replace(',', '').astype(int)
    df_2017[col] = df_2017[col].str.replace(',', '').astype(int)

# Rename columns
df_2011.rename(columns={
    'Name':'State',
    'Number':'Total',
    'Proportion (%)':'Total_Prop',
    'Number2':'Male',
    'Proportion (%)2':'Male_Prop',
    'Number3':'Female',
    'Proportion (%)3':'Female_Prop'
}, inplace=True)

df_2017.rename(columns={
    'Name':'State',
    'Number':'Total',
    'Proportion (%)':'Total_Prop',
    'Number2':'Male',
    'Proportion (%)2':'Male_Prop',
    'Number3':'Female',
    'Proportion (%)3':'Female_Prop'
}, inplace=True)

# Combine both years
df_combined = pd.concat([df_2011, df_2017], ignore_index=True)

# Reshape to long format
long_rows = []
for _, row in df_combined.iterrows():
    population = row['Population']  # same for all genders
    long_rows.append({'State': row['State'], 'Year': row['Year'], 'Gender':'Total', 'Value': row['Total'], 'Proportion': row['Total_Prop'], 'Population': population})
    long_rows.append({'State': row['State'], 'Year': row['Year'], 'Gender':'Male', 'Value': row['Male'], 'Proportion': row['Male_Prop'], 'Population': population})
    long_rows.append({'State': row['State'], 'Year': row['Year'], 'Gender':'Female', 'Value': row['Female'], 'Proportion': row['Female_Prop'], 'Population': population})

df_long = pd.DataFrame(long_rows)

# Save to CSV
df_long.to_csv('merged_gender_state_final.csv', index=False)

print("Merged CSV ready for Vega-Lite with a single Population per state-year:")
print(df_long.head())