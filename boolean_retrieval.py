import os
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
from natsort import natsorted
import string


def read_file(filename):
	with open(filename, 'r', encoding="ascii", errors="surrogateescape") as f:
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
	return token_list


# In this example, we create the positional index for only 1 folder.
folder_names = ["documents"]  # Coding/Classes/boolean_query/

# Initialize the stemmer.
stemmer = PorterStemmer()

# Initialize the file no.
fileno = 0

# Initialize the vocabulary.
pos_index = {}

# Initialize the file mapping (fileno -> file name).
file_map = {}

file_names = []

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

# # Sample positional index to test the code.
# sample_pos_idx = pos_index["tropic"]
# print("Positional Index")
# print(sample_pos_idx)

# file_list = sample_pos_idx[1]
# print("Filename, [Positions]")
# for fileno, positions in file_list.items():
#     print(file_map[fileno], positions)

# print()

# Start of Boolean Queries
query = "schizophrenia and drug"
# query = "schizophrenia or new"
# query = "schizophrenia and new NOT drug"



# Tokenizing the the query
normalized_query = preprocessing(query)
print("Boolean Query after normalization:", normalized_query)

# 'connecting_words' means operations (and, or, not)
connecting_terms = []
cnt = 1

# 'different_words' means search words
different_terms = []

# Splitting the search terms and boolean operations (and, not, or)
for term in normalized_query:
	# First stem the query terms
	term = stemmer.stem(term)

	if term != "and" and term != "or" and term != "not":
		different_terms.append(term)
	else:
		connecting_terms.append(term)

print("Separated terms:", different_terms)
print("Boolean operators:", connecting_terms)
print()

# get all unique words from inverted index dictionary
unique_words_all = set(pos_index.keys())
print("unique_words_all : ",unique_words_all)
print()

# number of documents
total_files = fileno + 1  # len(files_with_index)

# index of documents, if search word occurs 1, else 0.
zeroes_and_ones = []

# index of documents for all search words
zeroes_and_ones_of_all_terms = []

# index of documents for all search words
pos_idx_of_all_terms = []

list_terms = []

# Find ids for each search word

for term in (different_terms):
	if term in unique_words_all:
		# First set 0 to all documents
		zeroes_and_ones = [0] * total_files
		sample_pos_idx = pos_index[term]
		pos_idx_of_all_terms.append(sample_pos_idx)
		# Set 1 for document index, if search word occurs
		for docId in sample_pos_idx[1].keys():
			zeroes_and_ones[docId] = 1

		zeroes_and_ones_of_all_terms.append(zeroes_and_ones)

	else:
		print(term, " not found")
		sys.exit()

print("list_terms", list_terms)
print("pos idx of all terms", pos_idx_of_all_terms)
print("Vectors for query terms", zeroes_and_ones_of_all_terms)
print("connecting_terms", connecting_terms)
print()

# Checking intersections
for term in connecting_terms:

	# Results of search word after or before operation
	word_list1 = zeroes_and_ones_of_all_terms[0]
	word_list2 = zeroes_and_ones_of_all_terms[1]

	if term == "and": #0 & 0 = 0 1 & 1 = 1 0 & 1 = 0 1 & 0 = 0
		bitwise_op = [w1 & w2 for (w1, w2) in zip(word_list1, word_list2)]
		zeroes_and_ones_of_all_terms.remove(word_list1)
		zeroes_and_ones_of_all_terms.remove(word_list2)
		zeroes_and_ones_of_all_terms.insert(0, bitwise_op)

	elif term == "or":
		bitwise_op = [w1 | w2 for (w1, w2) in zip(word_list1, word_list2)]
		zeroes_and_ones_of_all_terms.remove(word_list1)
		zeroes_and_ones_of_all_terms.remove(word_list2)
		zeroes_and_ones_of_all_terms.insert(0, bitwise_op)

	elif term == "not":
		bitwise_op = [not w1 for w1 in word_list2]
		bitwise_op = [int(b == True) for b in bitwise_op]
		zeroes_and_ones_of_all_terms.remove(word_list2)
		zeroes_and_ones_of_all_terms.remove(word_list1)
		bitwise_op = [w1 & w2 for (w1, w2) in zip(word_list1, bitwise_op)]
		zeroes_and_ones_of_all_terms.insert(0, bitwise_op)

Proximity_matche = []

#intersecting two posting list

word_index1 = pos_idx_of_all_terms[0][1]
word_index2 = pos_idx_of_all_terms[1][1]

for i in range(len(word_index1)):
	for j in range(len(word_index2)):
		if i == j:
			if (word_index1[i][0] + 1) == word_index2[i][0]:
				Proximity_matche.append(i)
				print("Proximity_matche : ", Proximity_matche)

intersections = zeroes_and_ones_of_all_terms[0]
print("Intersections", intersections)
print()

files = []
cnt = 0
for index in intersections:
	if index == 1:
		files.append(file_names[cnt])
	cnt = cnt + 1

print("Search words were found in ", files)


files2 = []
cnt = 0
for index in Proximity_matche:
	if index == 1:
		files2.append(file_names[cnt])
	cnt = cnt + 1

print(" Search Proximity_matche words were found in ", files2)



