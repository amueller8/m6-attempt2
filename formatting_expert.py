

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
        original_lines = poem.lines

        """
        negative sentiment target -> short, choppy
        positive sentiment (highly positive, longer "flowy" lines)

        #basically chop up the negative ones, make the poem have
        more shorter lines 
        
        """



