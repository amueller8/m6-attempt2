import random
from line import Line
from word_expert import WordExpert 
import pronouncing

"""
Name: Abby
CSCI 3725
M6 Poetry Slam
11/20/22


File creates a "formatting expert" class that handles knowledge about 
average poem syllables, changing line syllables accordingly,
splitting/joining and generally altering some format stuff
(some stuff handled in poem too.s)
"""

class FormattingExpert():
    """
    File creates a "formatting expert" class that handles knowledge about 
    syllables and changing poem line formatting to change # syllables.
    """

    def __init__(self):
       self.name = "Expert :)"
       self.word_ex = WordExpert()
    
    def get_avg_line_length(self, poem):
        """
        Gets average words in poem. This is deprecated.
        """
        avg_line_length = 0
        for line in poem.lines:
            avg_line_length += len(line.tokens)
        avg_line_length /= len(poem.lines)
        
        return avg_line_length
    
    def get_avg_syllables(self, poem):
        """
        Counts average syllables in poem. Useful for fitness.
        param: poem, Poem to be counted
        return: avg_syllables int
        """
        avg_syllables = 0
        for line in poem.lines:
            avg_syllables+= line.syllables

        avg_syllables /= len(poem.lines)
        
        return avg_syllables
    

    def change_line_syllables(self, line, six):
        current_syllables = line.count_syllables_in_line()
        if six:
            if current_syllables > 6:
                #which to chop
                line1, line2 = self.split_line_in_half(line)
        
                if line1.count_syllables_in_line() > 6:
                    return self.change_line_syllables(line1, True)
                elif line2.count_syllables_in_line() > 6:
                    return self.change_line_syllables(line2, True)

                #find closest difference to 6
                if abs(line1.count_syllables_in_line() - 6) < \
                abs(line2.count_syllables_in_line() - 6):
                    return self.make_six_syllables(line)
                else:
                    return self.make_six_syllables(line)
            else:

                return self.make_six_syllables(line)

    def cut_to_six_sylls(self, line):
        """
        Reduces a line to 6 or fewer syllables (closest to 6 wins)
        param: line to be cut to 6
        return: new line
        """
        sylls = line.count_syllables_in_line()
        if sylls > 6:
            to_remove = sylls - 6
            #try cutting in half??

            line1, line2 = self.split_line_in_half(line)
            sylls1 = line1.count_syllables_in_line()
            sylls2 = line2.count_syllables_in_line()
            print("OLD: ", line, " (sylls ", sylls,")\n NEW:",\
                 line1, "\n", line2, "sylls: ", sylls1, sylls2)

            #return closest
            line1diff = abs(sylls1 - 6)
            line2diff = abs(sylls2 - 6)
            if line1diff <= line2diff:
                return line1
            else:
                return line2
            
   
    def make_six_syllables(self, line):
        """
        Another attempt to make a line 6 syllables. will probably delete
        """
        sylls = line.count_syllables_in_line()
        if sylls < 6:
            diff = abs(sylls - 6)
            #find a synonym
            noun = self.word_ex.get_nouns_line(line)
            old = ""
            choice = ""
            print(type(noun), "type noun")
            if noun is None:
                word = random.choice(line.input.strip().split(" "))
                old = word
                sub_word = random.choice(self.word_ex.get_antonyms(word) + \
                    self.word_ex.get_synonyms(word))
                for word in sub_word:
                    pronounce = pronouncing.phones_for_word(word)
                    if pronounce:
                        sylls = pronouncing.syllable_count(pronounce[0])
                        if sylls == diff:
                            choice = word
                            break
            else:
                word = random.choice(noun)
                old = word
                sub_word = random.choice(self.word_ex.get_antonyms(word), \
                    self.word_ex.get_synonyms(word))
                for word in sub_word:
                    pronounce = pronouncing.phones_for_word(word)
                    if pronounce:
                        sylls = pronouncing.syllable_count(pronounce[0])
                        if sylls == diff:
                            choice = word
                            break

            line.update_text(old, choice)
            print("MAKE SIX SYLLS???",line)
            return line


    def change_poem_line_length_2(self, poem):
        #choose least fit line?? maybe later
        line = random.choice(poem.lines)
        new_line = self.change_line_length_2(line)
        index = poem.lines.index(line)
        poem.lines[index] = new_line

        
    def change_poem_line_length(self, poem, target, weather):
        """
        Based on mood, alter poem line lengths (shorter for negative mood)
        (longer for positive mood)
        """
        original_lines = poem.lines
        new_lines = []

        if target < 0:
            #choppiest if very negative 
            if abs(target) >= 0.5:
                chop_threshold = 0.25
            else:
                chop_threshold = 0.75
            
            for line in original_lines:
                chop_factor = random.random()
                if len(line.tokens) > 5:
                    if chop_factor > chop_threshold:
                        line1, line2 = self.split_line_in_half(line)
                        new_lines.append(line1)
                        new_lines.append(line2)
                else:
                    new_lines.append(line)
        
            poem.lines = new_lines
        else:
            if abs(target) >= 0.5:
                chop_threshold = 0.25
            else:
                chop_threshold = 0.75
            
            for i in range(0,len(original_lines),2):
                chop_factor = random.random()
                try:
                    if len(original_lines[i].tokens) <= 5:
                        if len(original_lines[i+1].tokens) <= 5 and \
                            chop_factor > chop_threshold:
                            new_line = self.join_lines(original_lines[i],
                                original_lines[i+1])
                            new_lines.append(new_line)
                    else:
                        new_lines.append(original_lines[i])
                        new_lines.append(original_lines[i+1])
                except IndexError:
                    new_lines.append(original_lines[i])
                    #new_lines.append(original_lines[i+1])
        
            poem.lines = new_lines

    def change_line_length_2(self, line):
        line1, line2 = self.split_line_in_half(line)
        #pick closest to 6 syll
        sylls1 = line1.count_syllables_in_line()
        sylls2 = line2.count_syllables_in_line()
        if abs(sylls1 - 6) == 0:
            return line1
        elif abs(sylls2 - 6) == 0:
            return line2
        else: #return closest to 6
            if abs(sylls1 - 6) <  abs(sylls2 - 6):
                return line1
            else:
                return line2

        
                        

    def split_line_in_half(self, line):
        og_line = line
        words = og_line.input.strip().split(" ")
        
        part_1 = words[0:len(words)//2]
        part_1 = " ".join(part_1)

        part_2 = words[(len(words)//2):]
        part_2 = " ".join(part_2)
        print(part_1, part_2)
        return Line(part_1), Line(part_2)
        """
        negative sentiment target -> short, choppy
        positive sentiment (highly positive, longer "flowy" lines)

        #basically chop up the negative ones, make the poem have
        more shorter lines 
        
        """
    def join_lines(self, line1,line2):
        text1 = line1.input
        text2 = line2.input

        if line1.input.strip()[-1] in ",.!?":
            new_line = Line(text1.strip()+ " " + text2.strip())
        else:
            new_line = Line(text1.strip() + ", " + text2.strip())
        
        return new_line


def main():
    f = FormattingExpert()
    l = Line("Roses are terrible")
    l2 = Line("Violets are awful and blue")
    l3 = Line("Sugar is blown away in rain")
    l4 = Line("And so are")
    l5 = Line("choppy choppy yay the storm hurricane wind")
    l6 = Line("Thank you, thank you, unpaid labor")

    p =  [l, l2, l3,l4,l5, l6]
    for i in p:
        line = f.cut_to_six_sylls(i)
        print("FINAL LINE: ", line)

#main()