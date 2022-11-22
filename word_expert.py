import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import wordnet

"""
Name: Abby
CSCI 3725
M6 Poetry Slam
11/20/22


File creates a "word expert" class that handles knowledge about 
getting synonyms for a word, getting antonyms (ultimately not 
included as mutation), and getting nouns, the nouns in a line,
finding adjectives/adverbs, and verbs.

"""

class WordExpert:
    def __init__(self):
        self.corpus = ""

    def get_synonyms(self, word):
        """
        Gets synonyms given a word.
        Inspiration and nltk known how from:
        https://www.holisticseo.digital/python-seo/nltk/wordnet
        Param: word, word to search for synonyms of
        Return: list of synonyms
        """
        synonyms = []

        for syn in wordnet.synsets(str(word)):
            for l in syn.lemmas():
                synonyms.append(l.name())
        
        return list(set(synonyms))

    
    def get_antonyms(self, word):
        """
        Gets antonyms given a word.
        Inspiration and nltk known how from:
        https://www.holisticseo.digital/python-seo/nltk/wordnet
        Param: word, word to search for antonyms of
        Return: list of antonyms
        """
        antonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        return list(set(antonyms))

    def get_nouns(self, poem):
        """
        Gets the 3 most common nouns of a poem, or 2/1 if only that many.
        Param: poem
        Return: up to 3 most common nouns in list
        """

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
        """
        Gets the 3 most common nouns of a line, or as many as there are.
        Param: line
        Return: up to 3 most common nouns in list
        """

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
        """
        Sees if a word canbe interpreted as a verb.
        """
        #https://www.reddit.com/r/LanguageTechnology/comments/\
        # egh7jk/how_to_check_if_a_word_can_be_interpreted_as_a/
        return ('v' in set(s.pos() for s in wordnet.synsets(word)) and "_" \
            not in word)
    

    def find_adjectives_adverbs(self, line):
        """
        Finds adjs and adverbs in a line.
        Param: line
        Return: adjective and adverb tokens list.
        """

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



