from genetic_algorithm import GeneticAlgorithm
import glob
import os, os.path
from gtts import gTTS

#mkae/run ga


def main():
 
    ga = GeneticAlgorithm(15, "Dallas")
    print("Target mood for city is ",ga.target_mood, ga.weather)
     
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
    list_of_files = glob.glob('generated_poems/*') 
    latest_files = sorted(list_of_files, key=os.path.getctime)
    return latest_files
    

main()
#take fittest poem
#read out loud