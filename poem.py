import nltk, pronouncing
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import wordnet
from word_expert import WordExpert
from formatting_expert import FormattingExpert 
from line import Line

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

        #aesthetic: line length ("negative mood" -> choppier, shorter lines)
        avg_line_length = self.f_ex.get_avg_line_length(self)
        
        #subtle rewards and punishment for line length 
        if target < 0:
            if avg_line_length <= 5:
                combined_fitness *= (1 + (avg_line_length / 10))
            else:
                combined_fitness /= (1 - (avg_line_length / 100)) 
        else:
            if avg_line_length > 5:
                combined_fitness *= (1 + (avg_line_length) / 10)
            else:
                combined_fitness /= (1 - (avg_line_length / 100)) 

        if not hasattr(self, 'fitness'):
            self.fitness = combined_fitness * 10
        return combined_fitness * 10

    def fittest_lines(self, num_lines=5):
        top_5 = {}
        for l in range(len(self.lines)):
            p = Poem([self.lines[l]])
            p.get_fitness(0.5, [44.5, "Clouds"])
            print(p.fitness)
            top_5[l] = p.fitness
        sort_list = (sorted(top_5.items(), key=lambda item: item[1]))
        print("hi")
        print(sort_list)

        if len(sort_list) >= num_lines:
            new_list = sort_list[-num_lines:]
            return list(dict(new_list).keys())

        return list(sort_list.keys())


    def update_fitness(self, target, weather):
        self.fitness = self.get_fitness(target, weather)
    
    def __str__(self):
        return"{0}".format(self.text)
        
    def __repr__(self):
        return "Poem({0})".format(self.lines)

def main():
    l = Line("Roses are terrible")
    l2 = Line("Violets are awful and blue")
    l3 = Line("Sugar is blown away in rain")
    l4 = Line("And so are")
    l5 = Line("choppy choppy yay the storm hurricane wind")
    l6 = Line("Thank you, thank you, unpaid labor")

    p = Poem([l,l2,l3,l4,l5, l6])
    print(p.fittest_lines())

    new_poem = []
    #can work on this 
    for line in reversed(sorted(p.fittest_lines())):
        new_poem.append(p.lines[line])
    
    np = Poem(new_poem)
    print(np)

main()