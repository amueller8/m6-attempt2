import random
from line import Line
from word_expert import WordExpert 
import pronouncing

class FormattingExpert():

    def __init__(self):
       self.name = "Expert :)"
       self.word_ex = WordExpert()
    
    def get_avg_line_length(self, poem):

        avg_line_length = 0
        for line in poem.lines:
            avg_line_length += len(line.tokens)
        avg_line_length /= len(poem.lines)
        
        return avg_line_length
    

    
        
        return num_syllables
    def change_line_syllables(self, line, six):
        current_syllables = line.count_syllables_in_line()
        if six:
            if current_syllables > 6:
                #which to chop
                line1, line2 = self.split_line_in_half(line)
                #find closest difference to 6
                if abs(line1.count_syllables_in_line() - 6) < \
                abs(line2.count_syllables_in_line() - 6):
                    return line1
                else:
                    return line2

    def make_six_syllables(self, line):
        sylls = line.count_syllables_in_line()
        if sylls < 6:
            diff = abs(sylls - 6)
            #find a synonym
            noun = self.word_ex.get_nouns(line)
            old = ""
            choice = ""
            if type(noun) == None:
                word = random.choice(line.input.strip().split(" "))
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
            return line

    
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


    def split_line_in_half(self, line):
        og_line = line
        words = og_line.input.split(" ")
        
        part_1 = words[0:len(words)//2]

        part_2 = words[(len(words)//2):]

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


