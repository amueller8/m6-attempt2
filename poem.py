import nltk, pronouncing
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import wordnet
from word_expert import WordExpert
from formatting_expert import FormattingExpert 
from line import Line
import random

class Poem:
    def __init__(self, lines):
        self.lines = lines
        self.sia = SentimentIntensityAnalyzer()
        self.w_ex = WordExpert()
        self.f_ex = FormattingExpert()
        self.text = ""
        for line in self.lines:
                self.text += line.input + "\n"
        self.sentiment = self.analyze_sentiment()
        
        #self.nlp = spacy.load("en_core_web_sm")
        
        self.api_weather_options = ["thunderstorm", "drizzle", "rain",
            "snow", "clouds", "mist", "smoke","haze","dust","fog",
            "sand", "ash", "squall", "tornado", "clear", "extreme"
        ]
        self.other_weather_options = ["sunshine", "sunny", "foggy", "misty",
        "snowy", "cloudy", "drizzling", "raining", "pouring", "downpour",
        "smoky", "hazy", "windy", "wind", "stormy", "thunder", "thundering",
        "lightning", "hurricane", "tornado", "storms", "showers", "sun", 
        "cloud", "bright", "light", "dark", "breeze", "freeze", "ice", "icy",
        "darkness"
        ]

        top_3_nouns = self.w_ex.get_nouns(self)
        try:
            if len(top_3_nouns) >= 2 :
                self.title = " ".join(top_3_nouns)
            else:
                self.title = self.lines[0].input
        except TypeError:
            self.title = self.lines[0].input

    
    def analyze_sentiment(self):
        sentiment = self.sia.polarity_scores(self.text)['compound']
        return sentiment 
    

    def update_poem_text(self):
        self.text = ""
        for line in self.lines:
                self.text += line.input + "\n"
        
        #update fitness too?
        #self.fitness = self.get_fitness(target, weather)
    
    def get_fitness(self, target, weather):
        """
        Determines fitness based on target mood and weather.
        """
        sent_fitness = abs(self.sentiment - target)
        #weather fitness
        #count weather related words in text, including the word itself
        weather1= weather[1].lower()
        synonyms = self.w_ex.get_synonyms(weather1)
        synonyms.append(weather1)
        weather_words = 0
        for word in self.text.split():
            word = word.lower()
            if word in synonyms or word in self.api_weather_options or \
                word in self.other_weather_options:
                weather_words += 1
                #may make the boost for a weather word much bigger like 5
            #make a list of weather words (like the options from API)
            #including sun, sunshine, etc
 
        #composite fitness: we will subtract sentiment scores from 1, 
        #so smaller --> bigger
        sent_decimal = 1 - sent_fitness
        if weather_words != 0:
            combined_fitness = sent_decimal * weather_words
        else: 
            combined_fitness = sent_decimal

        #aesthetic: targeting ~6 syllable lines
        avg_syllables = self.f_ex.get_avg_line_length(self)
        
        #subtle rewards and punishment for line length 
        if avg_syllables == 6:
            combined_fitness *= (1 + avg_syllables/7 )
        elif avg_syllables == 5 or avg_syllables == 7:
            combined_fitness /= (1 + (avg_syllables) / 15)
        elif avg_syllables < 5:
            combined_fitness /= (1 - (avg_syllables / 80)) 
        elif avg_syllables > 7:
            combined_fitness /= (1 - (avg_syllables / 80)) 

        if not hasattr(self, 'fitness'):
            self.fitness = combined_fitness * 10
        return combined_fitness * 10

    def fittest_lines(self, target_mood, weather, num_lines=5):
        top_5 = {}
        for l in range(len(self.lines)):
            p = Poem([self.lines[l]])
            p.get_fitness(target_mood, weather)
            #print(p.fitness)
            top_5[l] = p.fitness
        sort_list = (sorted(top_5.items(), key=lambda item: item[1]))
        print("hi")
        print(sort_list)

        #if len(sort_list) >= num_lines:
            #new_list = sort_list[-num_lines:]
            #return list(dict(new_list).keys())

        return list(dict(sort_list).keys())


    def update_fitness(self, target, weather):
        self.fitness = self.get_fitness(target, weather)
    
    def __str__(self):
        return"{0}".format(self.text)
        
    def __repr__(self):
        return "Poem({0})".format(self.lines)

    def split_poem_in_pairs(self, target, weather):
        linez = []
        pairs = []
        index = 0
        for l in self.lines:
            if l.count_syllables_in_line() >= 8:
                l1, l2 = self.f_ex.split_line_in_half(l)
                linez.append(l1)
                linez.append(l2)
                pairs.append(index)
                pairs.append(index + 1)
                index += 1
            index += 1
        
        new_p = Poem(linez)
        fitnesses = []
        for i in range(len(new_p.lines)):
            if i in pairs and i+1 in pairs and i+1 < len(new_p.lines):
                g_fit = Poem([new_p.lines[i], new_p.lines[i+1]])
                g_fit.get_fitness(target, weather)
                fitnesses.append((g_fit.fitness, g_fit))
                i += 1
            else:
                g_fit = Poem([new_p.lines[i]])
                g_fit.get_fitness(target, weather)
                fitnesses.append((g_fit.fitness, g_fit))
        #print("POEM BY FITNESSES",fitnesses)
        sort_list = (sorted(dict(fitnesses).items(), key=lambda item: item[0]))
        #print("HERE IS SORTLIST\n",sort_list)
        return sort_list

def main():
    l = Line("Roses are terrible")
    l2 = Line("Violets are awful and blue")
    l3 = Line("Sugar is blown away in rain")
    l4 = Line("And so are")
    l5 = Line("choppy choppy yay the storm hurricane wind")
    l6 = Line("Thank you, thank you, unpaid labor")

    p = Poem([l,l2,l3,l4,l5, l6])
    #print(p.fittest_lines())

    linz = []
    pairs = []
    index = 0
    for l in p.lines:
        
        if l.count_syllables_in_line() > 6:
            l1, l2 = p.f_ex.split_line_in_half(l)
            linz.append(l1)
            linz.append(l2)
            pairs.append(index)
            pairs.append(index + 1)
            index += 1
        index += 1
        
    new_p = Poem(linz)
    fitnesses = []
    
    for i in range(len(new_p.lines)):
        if i in pairs and i+1 in pairs and i+1 < len(new_p.lines) and i < len(new_p.lines) :
            g_fit = Poem([new_p.lines[i], new_p.lines[i+1]])
            g_fit.get_fitness(0.6, [41.0, "Cloudy"])
            fitnesses.append((g_fit.fitness, g_fit))
            i += 1
        else:
            g_fit = Poem([new_p.lines[i]])
            g_fit.get_fitness(0.6, [41.0, "Cloudy"])
            fitnesses.append((g_fit.fitness, g_fit))

    print(fitnesses)
    print(new_p)
    
  
#main()