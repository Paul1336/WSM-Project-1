#http://tartarus.org/~martin/PorterStemmer/python.txt
from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb
from PorterStemmer import PorterStemmer
import jieba

class Parser:

	#A processor for removing the commoner morphological and inflexional endings from words in English
	stemmer=None

	stopwords=[]

	def __init__(self,):
		self.stemmer = PorterStemmer()

		#English stopwords from ftp://ftp.cs.cornell.edu/pub/smart/english.stop
		self.stopwords = open('english.stop', 'r').read().split()


	def clean(self, string):
		""" remove any nasty grammar tokens from string """
		string = string.replace(".","")
		string = string.replace(r"\s+"," ")
		string = string.lower()
		return string
	

	def removeStopWords(self,list):
		""" Remove common words which have no search value """
		return [word for word in list if word not in self.stopwords ]


	def tokenise(self, string):
		""" break string up into tokens and stem words """
		string = self.clean(string)
		words = string.split(" ")
		remove_chars = str.maketrans('', '', ',()\'"”“‘’:?')
		cleaned_list = [s.translate(remove_chars) for s in words]
		cleaned_list = [item.strip().lower() for item in cleaned_list]
		cleaned_list = [s.strip() for s in cleaned_list if s.strip()]
		return [self.stemmer.stem(word,0,len(word)-1) for word in words]
		return [self.stemmer.stem(word,0,len(word)-1) for word in cleaned_list]

class Jieba:

	#A processor for removing the commoner morphological and inflexional endings from words in English
	stemmer=None

	stopwords=[]

	def __init__(self,):
		self.stemmer = PorterStemmer()

		#English stopwords from ftp://ftp.cs.cornell.edu/pub/smart/english.stop
		#self.stopwords = open('english.stop', 'r').read().split()


	def clean(self, string):
		""" remove any nasty grammar tokens from string """
		string = string.replace("。","").replace("、","").replace("，","").replace("「","").replace("」","").replace("『","").replace("』","")
		string = string.replace(r"\s+"," ")
		#string = string.lower()
		return string
	

	def removeStopWords(self,list):
		""" Remove common words which have no search value """
		return [word for word in list if word not in self.stopwords ]


	def tokenise(self, string):
		""" break string up into tokens and stem words """
		string = self.clean(string)
		words = list(jieba.cut(string))
		#print(list(words))
		remove_chars = str.maketrans('', '', ',()\'"”“‘’:?')
		cleaned_list = [s.translate(remove_chars) for s in words]
		cleaned_list = [item.strip().lower() for item in cleaned_list]
		cleaned_list = [s.strip() for s in cleaned_list if s.strip()]
		return [self.stemmer.stem(word,0,len(word)-1) for word in words]
		return [self.stemmer.stem(word,0,len(word)-1) for word in cleaned_list]
	
	# with open("documentFrequency.txt", "a") as file:
            # file.write(" ".join(map(str, documentFrequency)) + "\n")

class Blob:

	#A processor for removing the commoner morphological and inflexional endings from words in English
	stemmer=None

	stopwords=[]

	def __init__(self,):
		self.stemmer = PorterStemmer()

		#English stopwords from ftp://ftp.cs.cornell.edu/pub/smart/english.stop
		self.stopwords = open('english.stop', 'r').read().split()


	def clean(self, string):
		""" remove any nasty grammar tokens from string """
		string = string.replace(".","")
		string = string.replace(r"\s+"," ")
		string = string.lower()
		return string
	

	def removeStopWords(self,list):
		""" Remove common words which have no search value """
		return [word for word in list if word not in self.stopwords ]


	def tokenise(self, string):
		""" break string up into tokens and stem words """
		string = self.clean(string)

		blob = tb(string)
		words = []
		for word in blob.words:
			words.append(word)

		#words = string.split(" ")
		remove_chars = str.maketrans('', '', ',()\'"”“‘’:?')
		cleaned_list = [s.translate(remove_chars) for s in words]
		cleaned_list = [item.strip().lower() for item in cleaned_list]
		cleaned_list = [s.strip() for s in cleaned_list if s.strip()]
		return [self.stemmer.stem(word,0,len(word)-1) for word in words]
		return [self.stemmer.stem(word,0,len(word)-1) for word in cleaned_list]
	