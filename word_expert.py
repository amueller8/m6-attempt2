import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import wordnet

class WordExpert:
    def __init__(self):
        self.corpus = ""

    def get_synonyms(self, word):
        """
        https://www.holisticseo.digital/python-seo/nltk/wordnet
        """
        synonyms = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        
        return list(set(synonyms))

    
    def get_antonyms(self, word):
        antonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        return list(set(antonyms))

    def get_nouns(self, poem):
        noun_tokens = {}
        noun_tokens_plural = {}
        for line in poem.lines:
            for t in range(len(line.tokens)):
                token = line.tokens[t]
                print("Token ", token, "Tag ", line.tags[t][1])
                if line.tags[t][1] == "NN":
                    noun_tokens[token] = noun_tokens.get(token, 0) + 1
                if line.tags[t][1] == "NNP":
                    noun_tokens_plural[token] = \
                        noun_tokens_plural.get(token, 0) + 1
        
        #most common nouns = 
        most_common = sorted(noun_tokens.items(), key=lambda x:x[1])
        print(most_common)
        return(most_common)
        



        
