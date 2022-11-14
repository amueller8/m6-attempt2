
from weather_call import WeatherCall
from word_expert import WordExpert
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

    def recombination(self, selected_poems):
        """
        The selected poems are recombined through single point crossover to
        form one child. At the completion of selection we are left with just
        one child per two parents.

        Args:
            selected_poems (Poem[]): A list of the poems produced by
            selection, which is double the size of the initial population.
        """
        new_poems = []
        for i in range(0, len(selected_poems), 2):
            if selected_poems[i].get_fitness(self.target_mood, self.weather) < \
                    selected_poems[i + 1].get_fitness(self.target_mood, \
                        self.weather):
                random_index = random.randint(0, int(
                    selected_poems[i].get_fitness(self.target_mood, \
                        self.weather)))
            else:
                random_index = random.randint(0, int(
                    selected_poems[i + 1].get_fitness(self.target_mood, \
                        self.weather)))
            first_half = selected_poems[i].lines[0:random_index]
            second_half = selected_poems[i + 1].lines[random_index:]
            combined_list = first_half + second_half
            new_poem = Poem(lines=combined_list)
            new_poems.append(new_poem)
            #recalcuate fitness of the new one 
            new_poem.update_fitness(self.target_mood, self.weather)
        self.inspiring_set= new_poems
    
    def run(self):
        """
        The method that controls the entire overview of the GA process, running
        it the iterations of selection, recombination, and mutation, as well as
        printing useful information at the end of each iteration.
        """
        num_iteration = 0
        
        # Start iterations
        while num_iteration < self.iterations:
            for poem in self.inspiring_set:
                poem.update_fitness(self.target_mood, self.weather)
            original_list = self.inspiring_set
            selected = self.selection()
            self.recombination(selected)
            # Mutation
            for poem in self.inspiring_set:
                old_fitness = poem.get_fitness(self.target_mood, self.weather)
                probability = random.randint(0, 100)
                if probability < 80:
                    mutation_choice = random.randint(1, 3)
                   
                    if mutation_choice == 1:
                        #mutate synonyms
                        print(1)
                        #self.mutate_ingredient_name(rec)
                    elif mutation_choice == 2:
                        #mutate antonyms
                        print(2)
                        #self.mutate_add_recipe_ingredient(rec)
                    elif mutation_choice == 3:
                        print(3)
                        #mutate line length or form?
                        #self.mutate_remove_recipe_ingredient(rec)

                    #poem.update_fitness(self.target_mood, self.weather)
                    
                    
                poem.update_fitness(self.target_mood, self.weather)

            # Combining top 50% of new and original recipes
            self.inspiring_set.sort(key=lambda x: x.fitness)
            original_list.sort(key=lambda x: x.fitness)
            new_gen = self.inspiring_set[(len(self.inspiring_set) // 2):]+ \
                            original_list[(len(original_list) // 2):]
            self.inspiring_set = new_gen
            # Iteration print statements
            self.inspiring_set.sort(key=lambda x: x.fitness)
            #self.inspiring_set = new_gen
            print("ITERATION: " + str(num_iteration + 1) +
                "\nFittest poem:\n" + str(self.inspiring_set[-1]) +
                "\nFitness: " + \
                str(self.inspiring_set[-1].get_fitness(self.target_mood,\
                     self.weather)))
            #print(self.recipes[-1])
            num_iteration += 1



def main():
    ga = GeneticAlgorithm(2, "Boston")
    print("Target mood for Boston is ",ga.target_mood, ga.weather)
    print(ga.weather)
    #print(ga.inspiring_set)
    x = random.choice(ga.inspiring_set)
    print(x)
    print(x.get_fitness(ga.target_mood, ga.weather))
    print(x.fitness)
    #w = WordExpert()
    #print(w.get_nouns(x))
    #ga.run()

main()