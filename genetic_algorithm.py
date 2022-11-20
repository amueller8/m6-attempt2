
from weather_call import WeatherCall
from word_expert import WordExpert
from poem import Poem
from line import Line
import random
import glob
import nltk
from nltk.tokenize import word_tokenize
import mlconjug3
import os
from os.path import exists
import datetime

"""
Names: Abby (with some code used from PQ2 group project)
CSCI 3725
M6 Poetry Slam
11/20/22


File sets up a genetic algorithm to create
weather inspired poems partly informed by the flamenca 
spanish poetry style.
"""
class GeneticAlgorithm:

    def __init__(self, iterations, city_name, state_name=""):
        """
        Creates a genetic algorithm 
        params
            iterations (int): number of iterations
            city_name (string): city for seed weather/mood
            state_name (optional): to specify US state of city (XX format)
        """
        
        self.iterations = iterations
        self.inspiring_set = []
        self.stats = str(datetime.date.today())
        
        
        self.weather_call = WeatherCall()
        if state_name != "":
            weather = self.weather_call.query_city_for_weather(city_name,\
                state_name)
        else:
            weather = self.weather_call.query_city_for_weather(city=city_name)
        
        self.weather = weather
        self.target_mood = \
            self.weather_call.determine_weather_sentiment(weather)
        
        #process files
        for filename in glob.glob("weather_poems/*.txt"):
            lines = self.process_poem_file(filename)
            poem = Poem(lines[3:])
            self.inspiring_set.append(poem)
        
        self.conjugator = mlconjug3.Conjugator(language='en')
                          
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
        Selections poems proportionally to fitness.
        returns the selections
        
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

        fittest_poem = self.inspiring_set[-1]
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
                if probability < 60:
                    mutation_choice = random.randint(1, 2)
                   
                    if mutation_choice == 1:
                        #mutate synonyms, nouns
                        self.mutate_synonym_noun(poem)
                    elif mutation_choice == 2:
                        #put in verb synonyms
                        options = self.find_synonym_verb(poem)
                        self.mutate_synonym_verbs(poem, options)
                    
                poem.update_poem_text()
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
            fittest_poem = self.inspiring_set[-1]

            best_fitness = fittest_poem.fitness
            print("ITERATION: " + str(num_iteration + 1) +
                "\nFittest poem title:\n" +  str(self.inspiring_set[-1].title))
                      
            split_best = fittest_poem.split_poem_in_pairs(self.target_mood,\
                 self.weather)
            #we need 5 LINES from split_best , so worst case 5 selections
            split_best = reversed(split_best[-5:])
            split_dict = dict(split_best)

            final_poem_lines = []
            lines_added = 0
            for val in split_dict.values():
                if lines_added >= 5:
                    break
                if len(val.lines) == 2:
                    final_poem_lines.append(val.lines[0])
                    final_poem_lines.append(val.lines[1])
                    lines_added += 2
                    if lines_added == 5:
                        break
                else:
                    final_poem_lines.append(val.lines[0])
                    lines_added += 1
                    if lines_added == 5:
                        break

            final = Poem(final_poem_lines)
            if final.title:
                #os stuff;\
                # https://www.pythontutorial.net/python-basics/python-check-if-file-exists/
                if os.path.exists("generated_poems/"+final.title + ".txt"):
                    with open("generated_poems/"+final.title + \
                        str(num_iteration) + ".txt", "w") as file:
                        file.write(final.title + ":\n")
                        file.write(final.text)
                else:
                    with open("generated_poems/"+final.title + ".txt", "w") \
                        as file:
                        file.write(final.title + ":\n")
                        file.write(final.text)
            else:
                with open("generated_poems/poem" + \
                    str(num_iteration) + ".txt", "w") as file:
                    file.write(final.text)

            final_fitness = final.get_fitness(self.target_mood, self.weather)

            #add to stats sheet
            with open("stats/stats" + self.stats +".txt", "a") as f:
                w_str =  "Iteration\n" + str(num_iteration) + "\nPoem fitness\n" +\
                     str(best_fitness) + "\nfinal version fitness\n" + \
                        str(final_fitness)  + "\n"
                f.write(w_str)

            #flamenca inspiration improvement/lack of improvement

            num_iteration += 1

    def mutate_synonym_noun(self,poem):
        """
        Mutates in synonyms of a chosen noun into a poem.
        Tries to pick a meaningful noun and if not defaults to random.
        Param:
            poem (Poem to be mutated)
        
        """
        if poem.title != "":
            noun = random.choice(poem.title.split(" "))
        else:
            #find a noun in the poem
            line_tags = random.choice(poem.lines).tags
            noun = ""
            its = 0
            while noun == "" or its < len(line_tags):
                for lt in line_tags:
                    if len(lt) >= 2 and lt[1] == "NN" or lt[1] == "NNS":
                        noun = lt[0]
                        break
                    its += 1
        
            if noun == "":
                return 
        syns = poem.w_ex.get_synonyms(noun)

        if len(syns) == 0:
            return 
        #choose a random word
        syn = random.choice(syns)
        syn_pos = nltk.pos_tag(nltk.word_tokenize(syn))

        #find noun in all places, sub in system
        for line in poem.lines:
            for token in line.tokens:
                if token == noun:
                    token_index = line.tokens.index(token)
                    line.tags[token_index] = syn_pos
                    line.tokens[token_index] = syn
                    line.update_text(noun, syn)
        
        #$update poem fitness, text
        poem.update_fitness(self.target_mood, self.weather)
        poem.update_poem_text()
    
    def find_synonym_verb(self, poem):
        """
        Finds verbs in poems as well as synonym options for substitution.
        Param:
            poem (Poem to be mutated)
        
        return Options,dict  in form:
            line num: [verb_choice, synonym, "<POS TAG>"]
        
        """
        l = 0
        options = {}
        for line in poem.lines:
            options[l] = []
            tags = []
            for t in line.tags:
                if len(t) >= 2:
                    tags.append(t[1])

            #find "VBP" or "VB"  in tags
            try:
                tag_index = tags.index("VBP")
            except ValueError:
                tag_index = -1
            try:
                tag_index2 = tags.index("VBZ")
            except ValueError:
                tag_index2 = -1
            try:
                tag_index3 = tags.index("VBD")
            except ValueError:
                tag_index3 = -1

            
            #first we try for VBP
            if tag_index != -1 :
                verbs = poem.w_ex.get_synonyms(line.tags[tag_index][0])
                iters = 0
                while iters < len(verbs):
                    verb = random.choice(verbs)
                    if poem.w_ex.possible_verb(verb):
                        vbp = self.conjugator.conjugate(verb).conjug_info["indicative"]["indicative present"]["1p"]
                        options[l] = [verb, vbp, "VBP"]
                        break
                    iters += 1
            
            #then VDB
            if tag_index3 != -1:
                verbs2 = poem.w_ex.get_synonyms(line.tags[tag_index3][0])
                iters = 0
                while iters < len(verbs2):
                    verb2 = random.choice(verbs2)
                    if poem.w_ex.possible_verb(verb2):
                        vbd = self.conjugator.conjugate(verb2).conjug_info["indicative"]["indicative past tense"]["1p"]
                        options[l] = [verb2, vbd, "VBD"]
                        break
                    iters += 1
               
            #finally VBZ
            if tag_index2 != -1:
                verbs3 = poem.w_ex.get_synonyms(line.tags[tag_index2][0])
                iters = 0
                while iters < len(verbs3):
                    verb3 = random.choice(verbs3)
                    if poem.w_ex.possible_verb(verb3):
                        vbz = self.conjugator.conjugate(verb3).conjug_info["indicative"]["indicative present"]["3p"]
                        options[l] = [verb3, vbz, "VBZ"]
                        break
                    iters += 1
            
            l += 1
        
        return options
    
    def mutate_synonym_verbs(self, poem, options):
        """
        Mutates in synonyms of a verb into a poem.
        Param:
            poem (Poem to be mutated)
            options (dict of verb options from find_synonym_verb)

        """
        valid_options = []
        for k,v in options.items():
            if v != []:
                valid_options.append((k,v))
       #enforce validity by making sure all necessary info is provided 
        if valid_options:
            verb = random.choice(valid_options)
            line_index = verb[0]
            og_verb = verb[1][0]
            sub_verb = verb[1][1]
            line = poem.lines[line_index]

            for token in line.tokens:
                    if token == og_verb:
                        token_index = line.tokens.index(token)
                        line.tags[token_index] = verb[1][2]
                        line.tokens[token_index] = sub_verb
                        
                        line.update_text(og_verb, sub_verb)
            
            #$update poem fitness, text
            poem.update_fitness(self.target_mood, self.weather)
            poem.update_poem_text()
