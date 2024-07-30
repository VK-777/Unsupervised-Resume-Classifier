import re
import spacy
from Constants.constants import REGEX_PATTERNS

nlp = spacy.load('en_core_web_sm')


class JobTitleExtractor:
    def __init__(self):
        self.nlp = nlp

    def extract_job_title(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "WORK_OF_ART":
                return ent.text

        regex_patterns = REGEX_PATTERNS

        for pattern in regex_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0).title()
        return "Unknown"
