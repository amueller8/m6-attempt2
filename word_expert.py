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

        for syn in wordnet.synsets(str(word)):
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
                if len(line.tags[t]) < 2:
                    continue
                token = line.tokens[t]
                if line.tags[t][1] == "NN":
                    noun_tokens[token] = noun_tokens.get(token, 0) + 1
                if line.tags[t][1] == "NNP":
                    noun_tokens_plural[token] = \
                        noun_tokens_plural.get(token, 0) + 1
        
        #most common nouns = 
        most_common = sorted(noun_tokens.items(), key=lambda x:x[1])
        #select up to 3 most common 
        if len(most_common) >= 3:
            return [most_common[-1][0], most_common[-2][0], most_common[-3][0] ]
        elif len(most_common) == 2:
            return [most_common[-1][0], most_common[-2][0] ]
        elif len(most_common) == 1:
            return most_common[-1][0]
        else:
            return
    
    def get_nouns_line(self, line):

        noun_tokens = {}
        noun_tokens_plural = {}
    
        for t in range(len(line.tokens)):
            if len(line.tags[t]) < 2:
                continue
            token = line.tokens[t]
            if line.tags[t][1] == "NN":
                noun_tokens[token] = noun_tokens.get(token, 0) + 1
            if line.tags[t][1] == "NNP":
                noun_tokens_plural[token] = \
                    noun_tokens_plural.get(token, 0) + 1
        
        #most common nouns = 
        most_common = sorted(noun_tokens.items(), key=lambda x:x[1])
        #select up to 3 most common 
        if len(most_common) >= 3:
            return [most_common[-1][0], most_common[-2][0], most_common[-3][0] ]
        elif len(most_common) == 2:
            return [most_common[-1][0], most_common[-2][0] ]
        elif len(most_common) == 1:
            return most_common[-1][0]
        else:
            return
    
    def possible_verb(self,word): 
        #https://www.reddit.com/r/LanguageTechnology/comments/egh7jk/how_to_check_if_a_word_can_be_interpreted_as_a/
        return ('v' in set(s.pos() for s in wordnet.synsets(word)) and "_" not in word)
    

    def find_adjectives_adverbs(self, line):

        adj_adverb_tokens = []
        for t in range(len(line.tokens)):
            if len(line.tags[t]) < 2:
                continue
            token = line.tokens[t]
            if line.tags[t][1] == "JJ" or line.tags[t][1] == "JJS" :
                adj_adverb_tokens.append(token)
            if line.tags[t][1] == "RB"  or line.tags[t][1] == "RBS":
                adj_adverb_tokens.append(token)

        return adj_adverb_tokens



