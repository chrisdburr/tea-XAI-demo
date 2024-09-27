# verify_csv.py

import pandas as pd
import os

# Path to the CSV file
csv_file = os.path.join(os.path.dirname(__file__), 'techniques_data_2.csv')

# Read the CSV file
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"Error: The file '{csv_file}' was not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: The file '{csv_file}' is empty.")
    exit(1)
except pd.errors.ParserError as e:
    print(f"Error parsing '{csv_file}': {e}")
    exit(1)

# Define expected columns
expected_columns = [
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

# 1. Check for Missing Columns
missing_columns = set(expected_columns) - set(df.columns)
if missing_columns:
    print(f"Missing columns: {missing_columns}")
else:
    print("All expected columns are present.")

# 2. Check for Extra Columns
extra_columns = set(df.columns) - set(expected_columns)
if extra_columns:
    print(f"Extra columns detected: {extra_columns}")
else:
    print("No extra columns detected.")

# 3. Check for Correct Number of Columns in Each Row
expected_num_columns = len(expected_columns)
actual_num_columns = df.shape[1]
if actual_num_columns != expected_num_columns:
    print(f"Warning: Expected {expected_num_columns} columns, but found {actual_num_columns}.")
else:
    print("All rows have the correct number of columns.")

# 4. Check for Missing Values in Critical Columns
critical_columns = ['Technique', 'Description', 'Categories', 'Sub-Categories', 'Model-Dependency', 'Example Use-Case']
missing_values = df[critical_columns].isnull().sum()
if missing_values.any():
    print("Missing values detected in critical columns:")
    print(missing_values[missing_values > 0])
else:
    print("No missing values in critical columns.")

# 5. Validate 'Scope Global' and 'Scope Local' Columns
valid_scope_values = {'Yes', 'No'}
invalid_scope_global = df[~df['Scope Global'].isin(valid_scope_values)]
invalid_scope_local = df[~df['Scope Local'].isin(valid_scope_values)]

if not invalid_scope_global.empty:
    print("\nInvalid values found in 'Scope Global' column:")
    print(invalid_scope_global[['Technique', 'Scope Global']])
else:
    print("\nAll 'Scope Global' values are valid ('Yes' or 'No').")

if not invalid_scope_local.empty:
    print("\nInvalid values found in 'Scope Local' column:")
    print(invalid_scope_local[['Technique', 'Scope Local']])
else:
    print("\nAll 'Scope Local' values are valid ('Yes' or 'No').")

# 6. Check for Duplicate Techniques
duplicates = df[df.duplicated(subset=['Technique'], keep=False)]
if not duplicates.empty:
    print("\nDuplicate techniques found:")
    print(duplicates[['Technique']])
else:
    print("\nNo duplicate techniques found.")

# 7. Validate 'Model-Dependency' Column
valid_model_dependencies = {'Model-Agnostic', 'Model-Specific'}
invalid_model_dependency = df[~df['Model-Dependency'].isin(valid_model_dependencies)]
if not invalid_model_dependency.empty:
    print("\nInvalid values found in 'Model-Dependency' column:")
    print(invalid_model_dependency[['Technique', 'Model-Dependency']])
else:
    print("\nAll 'Model-Dependency' values are valid ('Model-Agnostic' or 'Model-Specific').")

# 8. Validate 'Categories' and 'Sub-Categories' Formatting
def validate_separated_values(series, separator='; '):
    return series.apply(lambda x: isinstance(x, str) and '; ' in x)

# Example: Check if multiple categories are properly separated
multi_categories = df[df['Categories'].str.contains('; ')]
print(f"\nNumber of techniques with multiple categories: {multi_categories.shape[0]}")

multi_sub_categories = df[df['Sub-Categories'].str.contains('; ')]
print(f"Number of techniques with multiple sub-categories: {multi_sub_categories.shape[0]}")

# 9. Check Tags Consistency
# Assuming tags should be a semicolon-separated list
tags_valid = df['Tags'].apply(lambda x: isinstance(x, str) and ';' in x)
invalid_tags = df[~tags_valid]
if not invalid_tags.empty:
    print("\nInvalid tags format found in the following techniques:")
    print(invalid_tags[['Technique', 'Tags']])
else:
    print("\nAll tags are properly formatted.")

# 10. Check Completeness Against Original Markdown (Optional)
# If you have access to the original Markdown table, you can compare the number of entries.
# For demonstration, we'll assume the Markdown has 50 techniques.
expected_num_techniques = 45  # Replace with the actual number
actual_num_techniques = df.shape[0]
if actual_num_techniques != expected_num_techniques:
    print(f"\nWarning: Expected {expected_num_techniques} techniques, but found {actual_num_techniques}.")
else:
    print(f"\nNumber of techniques matches the expected count: {expected_num_techniques}.")

# 11. Summary of Checks
print("\n--- Summary of CSV Verification ---")
print(f"Total techniques: {actual_num_techniques}")
print(f"Missing Columns: {missing_columns if missing_columns else 'None'}")
print(f"Extra Columns: {extra_columns if extra_columns else 'None'}")
print(f"Missing Values in Critical Columns: {missing_values[missing_values > 0].to_dict() if missing_values.any() else 'None'}")
print(f"Invalid 'Scope Global' Entries: {invalid_scope_global.shape[0]}")
print(f"Invalid 'Scope Local' Entries: {invalid_scope_local.shape[0]}")
print(f"Duplicate Techniques: {duplicates.shape[0]}")
print(f"Invalid 'Model-Dependency' Entries: {invalid_model_dependency.shape[0]}")
print(f"Techniques with Multiple Categories: {multi_categories.shape[0]}")
print(f"Techniques with Multiple Sub-Categories: {multi_sub_categories.shape[0]}")
print(f"Invalid Tags Format: {invalid_tags.shape[0]}")
print(f"Expected vs Actual Techniques Count: {'Mismatch' if actual_num_techniques != expected_num_techniques else 'Match'}")