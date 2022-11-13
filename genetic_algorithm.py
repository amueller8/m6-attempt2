
from weather_call import WeatherCall
from poem import Poem
from line import Line
import random
import glob

class GeneticAlgorithm:

    def __init__(self, iterations, city_name, state_name=""):
        
        self.iterations = iterations
        self.inspiring_set = []
        
        weather_call = WeatherCall()
        if state_name != "":
            weather = weather_call.query_city_for_weather(city_name,\
                state_name)
        else:
            weather = weather_call.query_city_for_weather(city=city_name)
        
        self.weather = weather
        self.target_mood = weather_call.determine_weather_sentiment(weather)
        for filename in glob.glob("weather_poems/*.txt"):
            lines = self.process_poem_file(filename)
            poem = Poem(lines[3:])
            self.inspiring_set.append(poem)
                          
    def process_poem_file(self,file):
        lines = []
        with open(file, 'r') as f:
            my_line = f.readline()#may need to convert from one line to 
            while my_line:
                if my_line != "" and my_line != "\n":
                    lines.append(Line(my_line))
                
                my_line = f.readline()

        return lines
            
    def selection(self):
        """
        Does selection.
        Casting to int.
        
        """
        selected_poems = []
        total = 0
        for p in range(len(self.inspiring_set)):
            total += int(self.inspiring_set[p].get_fitness(self.target_mood,\
                 self.weather)) 

        self.inspiring_set.sort(key=lambda x: (x.fitness))
        count = 0
        
        for i in range(2 * len(self.inspiring_set)):
            count = 0
            random_number = random.randint(0,total)
            #random_number = random.SystemRandom().uniform(0,total)
            for z in range(len(self.inspiring_set)):
                count += int(self.inspiring_set[z].get_fitness(self.target_mood,\
                 self.weather))
                if random_number <= count:
                    selected_poems.append(self.inspiring_set[z])
                    break
        return selected_poems

def main():
    ga = GeneticAlgorithm(2, "Boston")
    print("Target mood for Boston is ",ga.target_mood, ga.weather)
    print(ga.inspiring_set)

main()