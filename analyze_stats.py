import matplotlib
from matplotlib import pyplot as plt
import random

"""
Name: Abby
CSCI 3725
M6 Poetry Slam
11/20/22


Analyzes fitness stats from poem and "final" flamenca-format version.
Creates and saves matplotlib graphs to aid in determining ideal # generations.
"""


def analyze():

    filename = input("Which file to analyze? ")
    with open("stats/" + filename) as f:
        data = f.readlines()
        x = [line.split("\n") for line in data]
        #print(x)
        #0, 1, 2 = iteration, poem, final
        
        iters = []
        poem = []
        final = []
        even = x[1::2]
        #print(even)
        for i in range(0, len(even), 3):
            iters.append(int(even[i][0]))
            poem.append(float(even[i+1][0]))
            final.append(float(even[i+2][0]))
        
        poem_tuples = []
        final_tuples  = []
        for e in iters:
            poem_tuples.append((iters[e], poem[e]))
            final_tuples.append((iters[e], final[e]))
        #plotting
        #https://stackoverflow.com/questions/18458734/how-do-i-plot-list-of-tuples-in-python
        plt.rcParams["figure.autolayout"] = True
        plt.xlabel('Iterations')
        plt.ylabel('Fitness')
        plt.xlim = max(iters)
        plt.ylim = max(max(poem), max(final))
        plt.plot(*zip(*poem_tuples))
        plt.plot(*zip(*final_tuples))
        plt.savefig('stats/plots/plot' + str(random.randint(0, 40000)) + '.png')

        plt.show()

        #https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
        #plt.savefig('stats/plots/plot' + str(random.randint(0, 40000)) + '.png')

        
def main():
    
    analyze()

main()