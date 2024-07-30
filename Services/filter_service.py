import google.generativeai as genai
import google.api_core.exceptions
from Constants.constants import API_KEYS_FILEPATH
from Logging.logger import apply_log_around


# Function to read API keys from a text file
def read_api_keys(file_path):
    with open(file_path, 'r') as file:
        keys = [line.strip() for line in file]
    return keys


# Read the API keys from the text file
api_keys = read_api_keys(API_KEYS_FILEPATH)


@apply_log_around
class Filter:
    @staticmethod
    def AIfilter(df):
        model_name = 'gemini-1.5-flash'
        subset = ['id', 'pci', 'skills', 'classification']
        df_subset = df[subset]
        api_key_index = 0  # Start with the first key
        genai.configure(api_key=api_keys[api_key_index])
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat()
        #TODO add prompt to constant

        for index in range(len(df_subset)):
            if not df_subset.classification[index]:
                s = f'Give me most suitable job Roles (max 5) for a candidate based on previous company experience as:'\
                    f'{str(df_subset.pci[index])} And skills as {str(df_subset.skills[index])}.' \
                    f'Make do with whatever is available, cant provide more information.' \
                    f'If you cant understand experience, classify based on skills.' \
                    f'No Extra symbols or explanation, just roles in a comma separated manner.' \
                    f'Maybe add a tag like senior, lead or similar titles before roles based on their duration ' \
                    f'IF MENTIONED.' \
                    f'CONSTRAINT: Make SURE all the titles together dont exceed 255 characters in total' \
                    f'(Including whitespaces and commas).'

                success = False
                while not success:
                    try:
                        response = chat.send_message(s)
                        df.loc[index, 'classification'] = response.text
                        success = True
                    except (google.api_core.exceptions.ResourceExhausted, google.api_core.exceptions.InvalidArgument):
                        api_key_index = (api_key_index + 1) % len(api_keys)
                        genai.configure(api_key=api_keys[api_key_index])
                        model = genai.GenerativeModel(model_name)
                        chat = model.start_chat(history=[])
                        # print(f"API key exhausted. Switching to key index {api_key_index}.")

        return df
