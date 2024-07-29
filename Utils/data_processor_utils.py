import pandas as pd
import ast
import re
import json
from Logging.logger import apply_log_around
from Utils.CustomSingleton import SingletonMeta


@apply_log_around
class DataProcessor(metaclass=SingletonMeta):
    @staticmethod
    def clean_json_string(s):
        # Fix common JSON issues such as missing values after keys
        s = s.replace(',}', '}')  # Remove trailing commas before closing braces
        s = s.replace(',]', ']')  # Remove trailing commas before closing brackets
        s = re.sub(r'(?<=:)(\s*[,}\]])', 'null\\1', s)  # Add 'null' for missing values
        return s

    @staticmethod
    def safe_literal_eval(val):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            try:
                return json.loads(val)
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON: {e}')
                return None

    @staticmethod
    def preprocess_data(df):
        # df = df.drop_duplicates('candidate_name', inplace=True)

        # Fill NaN values with an empty list string representation
        df['previous_company_information'] = df['previous_company_information'].fillna('[]')

        # Clean and parse JSON-like strings
        df['previous_company_information'] = df['previous_company_information'].apply(
            lambda x: DataProcessor.safe_literal_eval(DataProcessor.clean_json_string(x))
        )

        # Copy the parsed data to 'pci' column
        df['pci'] = df['previous_company_information'].apply(
            lambda x: DataProcessor.safe_literal_eval(x) if isinstance(x, str) else x
        )

        return df

    @staticmethod
    def process_data(df):
        # Create an empty list to hold the flattened data
        flattened_data = []

        # Iterate through each row
        for index, row in df.iterrows():
            candidate_name = row['candidate_name']
            companies_info = row['pci']

            # Ensure companies_info is treated as a list of dictionaries
            if isinstance(companies_info, list):
                # Iterate through each dictionary in the list
                for company_info in companies_info:
                    if isinstance(company_info, dict):
                        # Handle potential missing keys with default values or error handling
                        try:
                            flattened_entry = {
                                'candidate_name': candidate_name,
                                'Company_Name': company_info.get('Company_Name') or company_info.get('CompanyName'),
                                'start_date': company_info.get('start_date') or company_info.get('Start_date'),
                                'end_date': company_info.get('end_date') or company_info.get('endDate'),
                                'Duration': company_info.get('Duration') or company_info.get('duration'),
                                'jobRoleAndResponsibilities': company_info.get(
                                    'jobRoleAndResponsibilities') or company_info.get('workRoleAndResponsibilities'),
                                'Project_Name': company_info.get('Project_Name') or company_info.get('ProjectName')
                            }
                        except KeyError as e:
                            print(f"KeyError: {e} in {company_info}. Skipping entry.")
                            continue

                    # Append the flattened entry to the list
                    flattened_data.append(flattened_entry)

        # Create a new DataFrame from the flattened data
        df1 = pd.DataFrame(flattened_data)
        return df1
