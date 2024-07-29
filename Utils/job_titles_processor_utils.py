import pandas as pd
import numpy as np
import warnings
from sklearn.preprocessing import LabelEncoder
from Logging.logger import apply_log_around
from Utils.CustomSingleton import SingletonMeta


@apply_log_around
class DataParser(metaclass=SingletonMeta):

    @staticmethod
    def parse_duration_to_months(start_date, end_date):
        warnings.filterwarnings("ignore", "Parsing dates in %d-%m-%Y format", UserWarning)
        # Check if end_date is None or "Present"
        if end_date is None or end_date.lower() == 'present' or end_date.lower() == 'till date':
            end_date = pd.Timestamp.now()
        else:
            # Attempt to parse end_date in multiple formats
            try:
                end_date = pd.to_datetime(end_date, format='%b-%Y', errors='raise')
            except ValueError:
                try:
                    end_date = pd.to_datetime(end_date, format='%m-%Y', errors='raise')
                except ValueError:
                    end_date = pd.to_datetime(end_date, errors='coerce')  # Try with default parsing

        # Attempt to parse start_date in multiple formats
        try:
            start_date = pd.to_datetime(start_date, format='%b-%Y', errors='raise')
        except ValueError:
            try:
                start_date = pd.to_datetime(start_date, format='%m-%Y', errors='raise')
            except ValueError:
                start_date = pd.to_datetime(start_date, errors='coerce')  # Try with default parsing

        # Return the difference in months if both dates are valid, otherwise return NaN
        if pd.isnull(start_date) or pd.isnull(end_date):
            return np.nan
        else:
            return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)


@apply_log_around
class JobTitleProcessor(metaclass=SingletonMeta):
    @staticmethod
    def process_job_titles_0(df1):
        # Fill missing job roles with 'Unknown'
        df1['jobRoleAndResponsibilities'].fillna('Unknown', inplace=True)

        # Encode categorical variables
        le_name = LabelEncoder()
        df1['candidate_name_encoded'] = le_name.fit_transform(df1['candidate_name'])

        le_company = LabelEncoder()
        df1['Company_Name_encoded'] = le_company.fit_transform(df1['Company_Name'])

        for i in range(len(df1)):
            df1.loc[i, 'Duration'] = DataParser.parse_duration_to_months(df1.start_date[i], df1.end_date[i])

        return df1

    @staticmethod
    def process_job_titles_1(df):
        u_codes = df['candidate_name'].unique()
        titles_dict = {key: {} for key in u_codes}
        for i in range(len(df)):
            code = df.candidate_name[i]
            if (df.Extracted_Job_Title[i]) == 'Unknown':
                df.loc[i, 'Extracted_Job_Title'] = 'Experienced'
            titles_dict[code].update({df.Extracted_Job_Title[i]: df.Duration[i]})

        def sort_inner_dict(d):
            return dict(sorted(d.items(), key=lambda item: (item[1] is float('nan'), item[1]), reverse=True))

        titles_dict = {k: sort_inner_dict(v) for k, v in titles_dict.items()}
        for i, jobs in titles_dict.items():
            if len(titles_dict[i]) > 2:
                if 'Experienced' in titles_dict[i]:
                    titles_dict[i].pop('Experienced')
            else:
                if 'Experienced' in titles_dict[i]:
                    new_dict = {'Experienced': titles_dict[i].get('Experienced')}
                    titles_dict[i].pop('Experienced')
                    new_dict.update(titles_dict[i])
                    titles_dict[i] = new_dict
        return titles_dict

    @staticmethod
    def process_job_titles_2(my_dict):
        new_dict = {}
        for key, jobs in my_dict.items():
            updated_jobs = {}
            for job, duration in jobs.items():
                if job == 'Experienced':
                    duration /= 12
                    if duration <= 3:
                        updated_job = 'Junior'
                    elif 3 < duration <= 5:
                        updated_job = 'Mid-Level'
                    elif 5 < duration <= 8:
                        updated_job = 'Senior'
                    elif 8 < duration <= 15:
                        updated_job = 'Lead'
                    elif 15 < duration <= 18:
                        updated_job = 'Specialist'
                    else:
                        updated_job = 'Executive'
                else:
                    updated_job = job
                updated_jobs[updated_job] = duration
            new_dict[key] = updated_jobs
        return new_dict
