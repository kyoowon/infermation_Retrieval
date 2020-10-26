import spacy
from spacy.lang.en.stop_words import STOP_WORDS
STOP_WORDS -= {"Test_One","Test_Two"}

print(len(STOP_WORDS))
print(STOP_WORDS)