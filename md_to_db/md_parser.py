# md_parser.py

import pandas as pd
import re
import os
from io import StringIO
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import markdown

# Load environment variables from .env
load_dotenv()

# Path to the Markdown file
markdown_file = os.path.join(os.path.dirname(__file__), 'techniques_table.md')

# Read the Markdown table from the file
try:
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
except FileNotFoundError:
    print(f"Error: The file '{markdown_file}' was not found.")
    exit(1)
except Exception as e:
    print(f"Error reading '{markdown_file}': {e}")
    exit(1)

# Function to extract the Markdown table
def extract_markdown_table(md_text):
    # Match the table by looking for the header row starting with '| **Technique**'
    table_pattern = re.compile(
        r'(\| \*\*Technique\*\*.*?\|(?:\n\|.*?)*\n)',
        re.DOTALL
    )
    match = table_pattern.search(md_text)
    if not match:
        raise ValueError("Markdown table not found in the provided file.")
    return match.group()

try:
    table_string = extract_markdown_table(markdown_content)
except ValueError as ve:
    print(f"Error: {ve}")
    exit(1)

# Convert Markdown table to HTML
html = markdown.markdown(table_string, extensions=['tables'])

# Parse HTML to extract table using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table')

if not table:
    print("Error: No table found in the Markdown content.")
    exit(1)

# Convert HTML table to pandas DataFrame using StringIO to handle the HTML string
html_table = str(table)
html_io = StringIO(html_table)
df = pd.read_html(html_io, flavor='bs4')[0]

# Clean column names by stripping whitespace and removing asterisks
df.columns = [col.strip().replace('**', '') for col in df.columns]

# Function to replace slashes with semicolons and strip whitespace
def replace_slash(text):
    if pd.isna(text):
        return ''
    return '; '.join([item.strip() for item in text.split('/')])

# Apply the function to 'Category' and 'Sub-Category' columns
df['Categories'] = df['Category'].apply(replace_slash)
df['Sub-Categories'] = df['Sub-Category'].apply(replace_slash)

# Drop the original 'Category' and 'Sub-Category' columns
df.drop(['Category', 'Sub-Category'], axis=1, inplace=True)

# Function to split 'Scope' into 'Scope Global' and 'Scope Local'
def split_scope(scope):
    scope_global = 'Yes' if 'Global' in scope else 'No'
    scope_local = 'Yes' if 'Local' in scope else 'No'
    return pd.Series([scope_global, scope_local])

# Apply the function to create new columns
df[['Scope Global', 'Scope Local']] = df['Scope'].apply(split_scope)

# Drop the original 'Scope' column
df.drop(['Scope'], axis=1, inplace=True)

# Function to generate Tags based on Categories, Sub-Categories, and other fields
def generate_tags(row):
    tags = set()
    
    # Add tags based on Categories
    if 'Feature Analysis' in row['Categories']:
        tags.add('Feature Importance')
    if 'Visualisation Techniques' in row['Categories']:
        tags.add('Visualisation')
    if 'Model Approximation' in row['Categories']:
        tags.add('Surrogate Models')
    if 'Example-Based Methods' in row['Categories']:
        tags.add('Example-Based')
    if 'Rule Extraction' in row['Categories']:
        tags.add('Rule Extraction')
    if 'Uncertainty and Reliability' in row['Categories']:
        tags.add('Uncertainty')
    if 'Fairness Explanations' in row['Categories']:
        tags.add('Fairness')
    if 'Model Simplification' in row['Categories']:
        tags.add('Model Simplification')
    
    # Add tags based on Sub-Categories
    sub_categories = row['Sub-Categories'].split('; ')
    for sub in sub_categories:
        if sub == 'Importance and Attribution':
            tags.add('Attribution')
        elif sub == 'Feature Visualisation':
            tags.add('Feature Visualisation')
        elif sub == 'Model Behavior Visualisation':
            tags.add('Model Behavior Visualisation')
        elif sub == 'Dimensionality Reduction Visualisation':
            tags.add('Dimensionality Reduction')
        elif sub == 'Interaction Analysis':
            tags.add('Interaction Analysis')
        elif sub == 'Local Surrogates':
            tags.add('Local Surrogate')
        elif sub == 'Global Surrogates':
            tags.add('Global Surrogate')
        elif sub == 'Counterfactual Explanations':
            tags.add('Counterfactual')
        elif sub == 'Causal Analysis':
            tags.add('Causal Analysis')
        elif sub == 'Decision Rules':
            tags.add('Decision Rules')
        elif sub == 'Decision Trees':
            tags.add('Decision Trees')
        elif sub == 'Confidence Estimation':
            tags.add('Confidence Estimation')
        elif sub == 'Out-of-Distribution Detection':
            tags.add('Out-of-Distribution Detection')
        elif sub == 'Uncertainty Quantification':
            tags.add('Uncertainty Quantification')
        elif sub == 'Bias Detection and Mitigation':
            tags.add('Bias Mitigation')
        elif sub == 'Fairness Metrics Visualisation':
            tags.add('Fairness Metrics Visualisation')
        elif sub == 'Model Pruning':
            tags.add('Model Pruning')
        elif sub == 'Model Distillation':
            tags.add('Model Distillation')
    
    # Add tags based on Model-Dependency
    if row['Model-Dependency'] == 'Model-Agnostic':
        tags.add('Model-Agnostic')
    elif row['Model-Dependency'] == 'Model-Specific':
        tags.add('Model-Specific')
    
    # Add tags based on Scope
    if row['Scope Global'] == 'Yes':
        tags.add('Global Scope')
    if row['Scope Local'] == 'Yes':
        tags.add('Local Scope')
    
    return '; '.join(sorted(tags))

# Generate Tags column
df['Tags'] = df.apply(generate_tags, axis=1)

# Reorder and select the columns as per the improved schema
final_columns = [
    'Technique',
    'Description',
    'Categories',
    'Sub-Categories',
    'Scope Global',
    'Scope Local',
    'Model-Dependency',
    'Example Use-Case',
    'Tags'
]

# Ensure all required columns are present
missing_columns = set(final_columns) - set(df.columns)
if missing_columns:
    print(f"Error: Missing columns in the DataFrame: {missing_columns}")
    exit(1)

# Select and reorder the columns
df_final = df[final_columns]

# Handle any missing or inconsistent data
# For example, replace NaN with empty strings
df_final.fillna('', inplace=True)

# Define the output CSV path (same directory as the script)
output_csv = os.path.join(os.path.dirname(__file__), '../api/management/commands/techniques_data.csv')

# Clean and standardize Sub-Categories
df_final['Sub-Categories'] = df_final['Sub-Categories'].apply(lambda x: '; '.join(sorted(set([sub.strip().title() for sub in x.split(';') if sub.strip()]))))

# Save the DataFrame to a CSV file
df_final.to_csv(output_csv, index=False)
print(f"DataFrame saved to '{output_csv}'.")