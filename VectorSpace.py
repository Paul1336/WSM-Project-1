# from pprint import pprint
import util
from typing import List, Dict
import itertools
import numpy as np


class VectorSpace:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """
    vectorKeywordIndex = []
    IDF_Vector = []
    parser=None

    TF_vectors: Dict[str, List[float]] = {}
    TF_IDF_vectors: Dict[str, List[float]] = {}
    tokenized_documents: Dict[str, List[str]] = {}

    def __init__(self, parser, documents=[]):
        self.parser = parser
        self.vectorKeywordIndex = []
        if(len(documents)>0):
            self.build(documents)

    def build(self,documents):
        """ Create the vector space for the passed document strings """
        self.tokenized_documents = {key: self.parser.tokenise(document) for key, document in documents.items()}
        self.vectorKeywordIndex = self.getVectorKeywordIndex(self.tokenized_documents)
        self.TF_vectors = {key: self.makeVector(document) for key, document in self.tokenized_documents.items()}
        freq_vectors = np.zeros(len(self.vectorKeywordIndex))
        for _, vector in self.TF_vectors.items():
            for idx, val in enumerate(vector):
                if(val > 0):
                    freq_vectors[idx] += 1
        self.IDF_Vector = np.log(len(documents) / freq_vectors)
        self.TF_IDF_vectors = {key: np.array(vector) * np.array(self.IDF_Vector) for key, vector in self.TF_vectors.items()}
        # print(self.vectorKeywordIndex)
        # print(self.documentVectors)
    
    def getVectorKeywordIndex(self, tokenList):
        """ create the keyword associated to the position of the elements within the document vectors """

        #Mapped documents into a single word string	
        merged_list = list(itertools.chain(*tokenList.values()))
        #Remove common words which have no search value
        vocabularyList = self.parser.removeStopWords(merged_list)
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)

        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)


    def makeVector(self, wordList):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            if word in self.vectorKeywordIndex:
                vector[self.vectorKeywordIndex[word]] += 1
        return vector


    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(self.parser.tokenise(termList))
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def search(self,searchList, weighting, distance):
        """ search for documents that match based on a list of terms """
        queryVector = np.array(self.buildQueryVector(searchList))
        if(weighting == "TF"):
            weighting_vectors = self.TF_vectors
        else:
            weighting_vectors = self.TF_IDF_vectors
            queryVector = queryVector * self.IDF_Vector
        if(distance == "Cosine"):
            ratings = {key: util.cosine(queryVector, np.array(vector)) for key, vector in weighting_vectors.items()}
            return dict(sorted(ratings.items(), key=lambda item: item[1], reverse=True))
        else:
            ratings = {key: util.euclidean_distance(queryVector, np.array(vector)) for key, vector in weighting_vectors.items()}
            return dict(sorted(ratings.items(), key=lambda item: item[1], reverse=False))
        
    def pseudo_feedback_search(self,searchList, weighting, distance):
        best_query = list(self.search(searchList, weighting, distance).items())[0]
        print("original best query: ", best_query[0], ", score: ", best_query[1])
        queryVector = np.array(self.buildQueryVector(searchList)) * self.IDF_Vector + 0.5* self.TF_IDF_vectors[best_query[0]]
        ratings = {key: util.cosine(queryVector, np.array(vector)) for key, vector in self.TF_IDF_vectors.items()}
        return dict(sorted(ratings.items(), key=lambda item: item[1], reverse=True))

if __name__ == '__main__':
    #test data
    documents = ["The cat in the hat disabled",
                 "A cat is a fine pet ponies.",
                 "Dogs and cats make good pets.",
                 "I haven't got a hat."]

    vectorSpace = VectorSpace(documents)

    #print(vectorSpace.vectorKeywordIndex)

    #print(vectorSpace.documentVectors)

    print(vectorSpace.related(1))

    #print(vectorSpace.search(["cat"]))

###################################################
