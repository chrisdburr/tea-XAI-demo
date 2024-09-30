# md_to_db/mdtable_parser.py

import pandas as pd
import re
import os
import sys
from io import StringIO
from bs4 import BeautifulSoup
import markdown
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert Markdown table to CSV.')
    parser.add_argument('markdown_file', help='Path to the Markdown file containing the table.')
    parser.add_argument('output_csv', help='Path to the output CSV file.')
    args = parser.parse_args()

    markdown_file = args.markdown_file
    output_csv = args.output_csv

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

    # Function to extract the first Markdown table
    def extract_markdown_table(md_text):
        # Match the first table in the markdown content
        table_pattern = re.compile(
            r'(\|.*?\|(?:\n\|.*?)*\n)',
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

    # Convert HTML table to pandas DataFrame using StringIO to avoid deprecation warning
    html_table = str(table)
    html_io = StringIO(html_table)
    df = pd.read_html(html_io)[0]

    # Clean column names by stripping whitespace and removing asterisks
    df.columns = [col.strip().replace('**', '') for col in df.columns]

    # Fill NaN with empty strings
    df.fillna('', inplace=True)

    # Handle 'Scope' column if it exists
    if 'Scope' in df.columns:
        # Function to split 'Scope' into 'Scope Global' and 'Scope Local'
        def split_scope(scope):
            scope_global = 'Yes' if 'Global' in scope else 'No'
            scope_local = 'Yes' if 'Local' in scope else 'No'
            return pd.Series([scope_global, scope_local])
        # Apply the function to create new columns
        df[['Scope Global', 'Scope Local']] = df['Scope'].apply(split_scope)
        # Drop the original 'Scope' column
        df.drop(['Scope'], axis=1, inplace=True)

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    print(f"DataFrame saved to '{output_csv}'.")

if __name__ == '__main__':
    main()