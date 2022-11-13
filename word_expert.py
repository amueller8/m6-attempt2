import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import wordnet

class WordExpert:
    def __init__():
        self.corpus = ""

    def get_synonyms(self, word):
        """
        https://www.holisticseo.digital/python-seo/nltk/wordnet
        """
        synonyms = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())

    
    def get_antonyms(self, word):
        antonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        return list(set(antonyms))
        
