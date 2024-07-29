import re
import pandas as pd
from Logging.logger import apply_log_around
from Utils.CustomSingleton import SingletonMeta


class SkillPreprocessor(metaclass=SingletonMeta):
    @staticmethod
    def preprocess_skills(ss):
        if pd.isna(ss):
            return ''
        if not isinstance(ss, str):
            ss = str(ss)
        processed = ss.strip('"')
        pattern = re.compile(r'([a-z]+)([A-Z]) | ([A-Z][a-z]+)')
        processed = pattern.sub(r'\1 \2', processed)
        return processed

    @staticmethod
    def process_tokens(df):
        tokenized_skills = [skills.split(',') if skills != '' else [] for skills in df['skills'].fillna('')]
        tokenized_skills = list(map(
            lambda sublist: [s.strip().replace('*', '').replace('\\n', '').replace('\\u', '').replace('\n', '') for s in
                             sublist if s.strip().replace('*', '').replace('\\n', '').replace('\\u', '') != ''],
            tokenized_skills))
        return tokenized_skills
