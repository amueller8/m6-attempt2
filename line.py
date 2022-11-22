import nltk
import pronouncing 
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')


"""
Abby
CSC3725
11/21/22
Line class with updating and syllable counting methods.

"""
class Line:

    def __init__(self, input):
        self.input = input
        self.tokens = nltk.word_tokenize(input)
        self.tags = nltk.pos_tag(self.tokens)
        self.syllables = self.count_syllables_in_line()

    """
    def count_syllables_in_line(self):
        num_syllables = 0
        for word in self.tokens:
            pronunciation_list = pronouncing.phones_for_word(word)
            #for now just picking first of list 
            if pronunciation_list:
                num_syllables += pronouncing.syllable_count(pronunciation_list[0])
            else:
                num_syllables += 0
        
        return num_syllables
    """

    def update_text(self, old_word, new_word):
        """
        Updates line input text.
        Param:
            old_word, word to be replaced
            new_word, replacement word/token (if tokenized and 2 words, splits)
        """
        #if new word has _, change it
        start = self.input.find(old_word)
        new_word = new_word.split("_")
        new_w_str = ""
        if len(new_word) > 1:
            for w in new_word:
                new_w_str += w + " "
        else:
             new_w_str = new_word[0] + " "

        if new_word == "":
            self.input[0:start] + self.input[start+len(old_word):]
        else:
            self.input = self.input[0:start] + new_w_str + self.input[start+len(old_word):]
    
    def count_syllables_in_line(self):
        """
        Counts syllables in a line.
        There is a duplicate method in f_ex.
        """
        num_syllables = 0
        for word in self.tokens:
            pronunciation_list = pronouncing.phones_for_word(word)
            #for now just picking first of list 
            if pronunciation_list:
                num_syllables += pronouncing.syllable_count(pronunciation_list[0])
            else:
                num_syllables += 0
        
        return num_syllables

    def split_line_in_half(self):
        """
        Splits line in half. Similar method in f_ex.
        """
        og_line = self
        words = og_line.input.strip().split(" ")
        
        part_1 = words[0:len(words)//2]
        " ".join(part_1)

        part_2 = words[(len(words)//2):]
        " ".join(part_2)

        return Line(part_1), Line(part_2)
    
    def remove_word(self, word):
        """
        Remove_word takes out a given word.
        This mutation was taken out of final version bc I needed more time.
        """
        new_line = self.input.replace(word, "")


    def get_input(self):
        """
        Gives line input.
        """
        return self.input
    
    def get_tokens(self):
        """
        Getter for tokens.
        """
        return self.tokens

    def get_tags(self):
        """
        Getter for tags.
        """
        return self.tags
        
    def __str__(self):
        return f'{self.input}'
    
    def __repr__(self):
        return "Line({0})".format(self.get_input())
        