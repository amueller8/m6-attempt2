import os


def read_text(text):
    os.system("say -v Serena " + text)

def read_poem(poem):
    for line in poem.lines:
        os.system("say -v Serena " + str(line.input))