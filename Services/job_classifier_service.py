import json
import pandas as pd
from fuzzywuzzy import fuzz
import re


class JobClassifier:
    def __init__(self, job_skills_filepath):
        self.job_skills = self.load_job_skills(job_skills_filepath)
        self.common_skills = {
            "RESTful", "APIs", "Git", "Unit Testing", "CI/CD", "Containerization", "Cloud", "Platforms", "HTML", "CSS",
            "Java"
        }
        self.predefined_titles = list(self.job_skills.keys())

    def load_job_skills(self, filepath):
        with open(filepath, 'r') as file:
            job_skills = json.load(file)
        return job_skills

    @staticmethod
    def calculate_similarity(skills_list, job_titles):
        similarity_scores = []
        threshold = 70

        for skills in skills_list:
            max_score = 0
            best_match = ''

            for job in job_titles:
                required_skills = job.get("required_skills", [])
                preferred_skills = job.get("preferred_skills", [])
                job_title = job["job_title"]

                # Check if candidate has at least 50% of required skills
                required_skills_set = set(required_skills)
                candidate_skills_set = set(skills)

                # Compare each skill in skills_list with required and preferred skills
                total_weighted_score = 0
                total_weight = 0

                # Compare required skills
                for skill in skills:
                    max_required_score = max(
                        fuzz.ratio(skill.lower(), req_skill.lower()) for req_skill in required_skills
                    )
                    total_weighted_score += max_required_score
                    total_weight += 1

                # Compare preferred skills if they exist
                if preferred_skills:
                    for skill in skills:
                        max_preferred_score = max(
                            fuzz.ratio(skill.lower(), pref_skill.lower()) for pref_skill in preferred_skills
                        )
                        total_weighted_score += max_preferred_score
                        total_weight += 0.5  # Give less weight to preferred skills

                # Calculate average weighted score
                if total_weight > 0:
                    avg_weighted_score = total_weighted_score / total_weight
                else:
                    avg_weighted_score = 0

                # Update best match if current job has higher average score
                if avg_weighted_score > max_score and avg_weighted_score > threshold:
                    max_score = avg_weighted_score
                    best_match = job_title

            # Append the best match and its similarity score
            similarity_scores.append({
                "skills": skills,
                "job_title": best_match,
                "similarity_score": max_score
            })

        return similarity_scores

    def final_title(self, df, job_titles):
        for i in range(len(df)):
            try:
                title = str(job_titles[i])
                if title == None:
                    continue
                if pd.isnull(df['classification'][i]):
                    df.loc[i, 'classification'] = title
                else:
                    if title not in df.loc[i, 'classification']:
                        df.loc[i, 'classification'] += ', ' + title
            except KeyError:
                continue

        def joiner(titles, num):
            label = ""
            for j in range(num, len(titles)):
                label += titles[j] + ', '
            return label[:-2].strip()

        position = ['Junior', 'Mid-Level', 'Senior', 'Lead', 'Specialist', 'Executive']

        for i in range(len(df)):
            titles = list(df.classification[i].split(','))
            label = ""
            if titles[0] in position:
                if len(titles) > 2:
                    label = joiner(titles, 1)
                else:
                    for j in range(len(titles)):
                        label += titles[j]
            else:
                label = joiner(titles, 0)

            df.loc[i, 'classification'] = label

        return df

    def map_to_predefined(self, job_titles):
        mapped_titles = []
        seen_titles = set()  # To keep track of unique mapped titles

        def preprocess_text(text):
            if text is None:
                return ""
            text = text.lower()  # Lowercase
            text = re.sub(r'\d+', '', text)  # Remove numbers
            text = re.sub(r'[^\w\s]', '', text)
            return text

        predefined_lower = {preprocess_text(title): title for title in self.predefined_titles}

        for title in job_titles:
            title_lower = title.lower()

            for predefined_title in predefined_lower:
                if predefined_title in title_lower:
                    mapped_title = predefined_lower[predefined_title]
                    if mapped_title not in seen_titles:
                        mapped_titles.append(mapped_title)
                        seen_titles.add(mapped_title)
                    break
            else:
                if title not in seen_titles:
                    mapped_titles.append(title.strip())
                    seen_titles.add(title)

        mapped_titles = [title for title in mapped_titles if len(title.split()) > 1]

        return mapped_titles
