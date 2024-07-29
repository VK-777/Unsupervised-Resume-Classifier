import re
import spacy

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
