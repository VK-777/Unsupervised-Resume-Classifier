import nltk
import re
from nltk.corpus import stopwords
from Logging.logger import custom_logger
from Utils.CustomSingleton import SingletonMeta


class TextPreprocessor(metaclass=SingletonMeta):
    def __init__(self):
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
        self.introductory_phrases = ['worked', 'working', 'role and responsibilities']

    def preprocess_text(self, text):
        if text is None:
            return ""

        text = text.lower()  # Lowercase
        text = re.sub(r'\d+', '', text)  # Remove numbers
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        for phrase in self.introductory_phrases:
            text = text.replace(phrase.lower(), '')
        words = text.split()  # Tokenize
        words = [word for word in words if word not in self.stop_words]  # Remove stopwords
        return ' '.join(words)
