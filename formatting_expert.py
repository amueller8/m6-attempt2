import random
from line import Line

class FormattingExpert():

    def __init__(self):
       self.name = "Expert :)"
    
    def get_avg_line_length(self, poem):

        avg_line_length = 0
        for line in poem.lines:
            avg_line_length += len(line.tokens)
        avg_line_length /= len(poem.lines)
        
        return avg_line_length
    
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
                if len(original_lines[i].tokens) <= 5:
                    if len(original_lines[i+1]) <= 5 and \
                        chop_factor > chop_threshold:
                        new_line = self.join_lines(original_lines[i] + \
                            original_lines[i+1])
                        new_lines.append(new_line)
                else:
                    new_lines.append(original_lines[i])
                    new_lines.append(original_lines[i+1])
        
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

        if line1.strip()[-1] in ",.!?":
            new_line = Line(text1 + " " + text2)
        else:
            new_line = Line(text1 + ", " + text2)
        
        return new_line


