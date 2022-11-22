from genetic_algorithm import GeneticAlgorithm
import glob
import os, os.path
from gtts import gTTS

"""
Name: Abby
CSCI 3725
M6 Poetry Slam
11/20/22


File creates and runs an instance of a genetic algorithm,
then presents the top 3 most recent results for user to pick from.
Saves the file to an mp3 format and reads aloud.
"""

def main():
    """
    Creates GA and seeks input for stats file title as well as which poem is
    read at the end.
    """
    city = input("Which city would you like to use?")
 
    ga = GeneticAlgorithm(15, city)
    print("Target mood for" + str(ga.city) + " is ",ga.target_mood, "Weather is", ga.weather)
    stats = input("please give a title for stats file "+
     "(will have the word stats appended to front): ")
    ga.stats = stats
     
    ga.run()

    which_poem = print("Which of the following poems would you like to hear\
         read? (1,2 or 3")
    #options
    sorted_files = sort_files()
    for i in range(len(sorted_files)):
        sorted_files[i] = sorted_files[i].replace("generated_poems/", "")
        sorted_files[i] = sorted_files[i].replace(".txt", "")
    
    last_3 = sorted_files[-3:]
    print(last_3)

    answer = int(input("Enter number: "))

    file = "generated_poems/" + sorted_files[-answer] + ".txt"

    language = "en"
    text = ""
    with open(file, "r") as f:
        lines = f.readlines()
        text += "\n" 
        for line in lines:
            text += line + "\n"

    toSpeech = gTTS(text=text, lang=language, slow=False)
    #compress
    name_words = sorted_files[-answer].split()
    name = "-".join(name_words)
    toSpeech.save("generated_poems/" + name + ".mp3")
   
    #play
    poem = "generated_poems/" + name + ".mp3"
    print(poem)
    os.system("afplay " + poem )
  

    
def sort_files():
    """
    Sorts the files bu when there were added to generated_poems to find
    most recent.
    return:
    latest_files (creation time sorted list)
    """
    list_of_files = glob.glob('generated_poems/*') 
    latest_files = sorted(list_of_files, key=os.path.getctime)
    return latest_files
    

main()
#take fittest poem
#read out loud