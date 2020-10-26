import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from natsort import natsorted
import string
from bs4 import BeautifulSoup
from urllib.request import urlopen

def write_file(filename, data):
    with open(filename, 'w') as f:
        stuff = f.write(data)
    f.close()

    return stuff

def read_file(filename):
    with open(filename, 'r', encoding='ASCII', errors="surrogateescape") as f:
        stuff = f.read()
    f.close()
    return stuff

def preprocessing(final_string):
    # Tokenize.
    tokenizer = TweetTokenizer()
    token_list = tokenizer.tokenize(final_string)

    # Remove punctuations.
    table = str.maketrans('', '', '\t')
    token_list = [word.translate(table) for word in token_list]
    punctuations = (string.punctuation).replace("'", "")
    trans_table = str.maketrans('', '', punctuations)
    stripped_words = [word.translate(trans_table) for word in token_list]
    token_list = [str for str in stripped_words if str]



    # Change to lowercase.
    token_list = [word.lower() for word in token_list]

    # stopword removal.
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in token_list if not w in stop_words]
    filtered_sentence = []

    for w in token_list:
	    if w not in stop_words:
		    filtered_sentence.append(w)

    return filtered_sentence


review_list=[]
url = 'https://www.rottentomatoes.com/m/tenet'
webpage = urlopen(url)

source = BeautifulSoup(webpage,'html.parser',from_encoding='utf-8')
reviews = source.find_all('blockquote',{'class': 'media-body quote_bubble__quote'})

for review in reviews:
    review_list.append(review.get_text().strip().replace('\n','').replace('\t','').replace('\r',''))
    i = -1
    for review in review_list:
        i = i + 1
        write_file("D:\GitHub\IR\documents\dec{0}.txt".format(i), review)

# In this example, we create the positional index for only 1 folder.
folder_names = ["documents"]

# Initialize the stemmer.
stemmer = PorterStemmer()

# Initialize the file no.
fileno = 0

# Initialize the vocabulary.
pos_index = {}

# Initialize the file mapping (fileno -> file name).
file_map = {}

for folder_name in folder_names:

    # Open files.
    file_names = natsorted(os.listdir("D:\GitHub\IR/" + folder_name))

    # For every file.
    for file_name in file_names:

        # Read file contents.
        stuff = read_file("D:\GitHub\IR/" + folder_name + "/" + file_name)

        # This is the list of words in order of the text.
        # We need to preserve the order because we require positions.
        # 'preprocessing' function does some basic punctuation removal,
        # stopword removal etc.
        final_token_list = preprocessing(stuff)

        # For position and term in the tokens.
        for pos, term in enumerate(final_token_list):

            # First stem the term.
            term = stemmer.stem(term)

            # If term already exists in the positional index dictionary.
            if term in pos_index:

                # Increment total freq by 1.
                pos_index[term][0] = pos_index[term][0] + 1

                # Check if the term has existed in that DocID before.
                if fileno in pos_index[term][1]:
                    pos_index[term][1][fileno].append(pos)

                else:
                    pos_index[term][1][fileno] = [pos]

            # If term does not exist in the positional index dictionary
            # (first encounter).
            else:

                # Initialize the list.
                pos_index[term] = []
                # The total frequency is 1.
                pos_index[term].append(1)
                # The postings list is initially empty.
                pos_index[term].append({})
                # Add doc ID to postings list.
                pos_index[term][1][fileno] = [pos]

                # Map the file no. to the file name.
        file_map[fileno] = "D:\GitHub\IR/" + folder_name + "/" + file_name

        # Increment the file no. counter for document ID mapping
        fileno += 1

# Sample positional index to test the code.
find_text = "work"
sample_pos_idx = pos_index[find_text]
print("indexed word :", find_text)
print("Positional Index")
print(sample_pos_idx)

file_list = sample_pos_idx[1]
print("Filename, [Positions]")
for fileno, positions in file_list.items():
    print(file_map[fileno], positions)


    