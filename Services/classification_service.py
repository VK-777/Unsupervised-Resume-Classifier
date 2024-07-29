import json
import re
import spacy
import pandas as pd

from Constants.constants import JOB_SKILLS_FILEPATH, JOB_TITLES_FILEPATH
from Logging.logger import apply_log_around
from Utils.text_preprocessor_utils import TextPreprocessor
from Utils.data_processor_utils import DataProcessor
from Utils.job_titles_processor_utils import JobTitleProcessor
from Utils.skill_preprocessor_utils import SkillPreprocessor

from Services.job_classifier_service import JobClassifier
from Services.filter_service import Filter

job_skills_filepath = JOB_SKILLS_FILEPATH
# Load job skills JSON
with open(JOB_TITLES_FILEPATH, 'r') as f:
    job_titles = json.load(f)

nlp = spacy.load('en_core_web_sm')


class JobTitleExtractor:
    def __init__(self):
        self.nlp = nlp

    def extract_job_title(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "WORK_OF_ART":
                return ent.text

        regex_patterns = [
            r'\b(?:[a-z]+\s){0,2}(?:engineer|developer|lead|manager|administrator|consultant|technician|scientist'
            r'|analyst|coordinator|director|specialist|officer|architect|strategist|executive|advisor|designer'
            r'|programmer|supervisor|trainer|planner|controller|assistant|operator|agent|representative|clerk'
            r'|inspector|instructor|apps developer|attendant)\b',
        ]

        for pattern in regex_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0).title()
        return "Unknown"


@apply_log_around
class Classify:

    @staticmethod
    def classify_resume(df):
        data_processor = DataProcessor()
        df = data_processor.preprocess_data(df)
        df1 = data_processor.process_data(df)

        title = JobTitleProcessor()
        df1 = title.process_job_titles_0(df1)

        text_processor = TextPreprocessor()
        df1['jobRoleAndResponsibilities'] = df1['jobRoleAndResponsibilities'].apply(text_processor.preprocess_text)

        extractor = JobTitleExtractor()
        df1['Extracted_Job_Title'] = df1['jobRoleAndResponsibilities'].apply(extractor.extract_job_title)
        df1['Duration'] = pd.to_numeric(df1['Duration'], errors='coerce')
        df1['Total_Experience_Years'] = df1.groupby('candidate_name_encoded')['Duration'].transform(
            lambda x: x.sum() / 12)

        my_dict = title.process_job_titles_1(df1)
        my_dict = title.process_job_titles_2(my_dict)
        Titles = {key: ', '.join(value.keys()) for key, value in my_dict.items()}

        df = df.reset_index(drop=True)
        df['classification'] = df['classification'].astype('object')
        for i in range(len(df)):
            df.loc[i, 'classification'] = Titles.get(df.candidate_name[i])

        skill_preprocessor = SkillPreprocessor()
        df['processed'] = df['skills'].apply(skill_preprocessor.preprocess_skills)
        df['processed'] = skill_preprocessor.process_tokens(df)

        skills_list = df.processed.tolist()
        skills_list = [[i.strip('"') for i in skill] for skill in skills_list]

        job_classifier = JobClassifier(job_skills_filepath)

        similarity_scores = job_classifier.calculate_similarity(skills_list, job_titles)
        dataf = pd.DataFrame(similarity_scores)

        df = job_classifier.final_title(df, dataf.job_title.tolist())
        df.classification = [job_classifier.map_to_predefined(list(i.strip().split(','))) for i in df.classification]

        fil = Filter()
        df = fil.AIfilter(df)
        return df
