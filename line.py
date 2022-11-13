import nltk

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

class Line:

    def __init__(self, input):
        self.input = input
        self.tokens = nltk.word_tokenize(input)
        self.tags = nltk.pos_tag(self.tokens)

    def update_text(self, old_word, new_word):
        #if new word has _, change it
        start = self.input.find(old_word)
        new_word = new_word.split("_")
        new_w_str = ""
        if len(new_word) > 1:
            for w in new_word:
                new_w_str += w + " "
        else:
             new_w_str = new_word[0] + " "

        self.input = self.input[0:start] + new_w_str + self.input[start+len(old_word):]
    
    def get_input(self):
        return self.input
    
    def get_tokens(self):
        return self.tokens

    def get_tags(self):
        return self.tags
        
    def __str__(self):
        return f'{self.input}'
    
    def __repr__(self):
        return "Line({0})".format(self.get_input())
        
        