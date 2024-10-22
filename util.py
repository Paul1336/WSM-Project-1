import sys
#http://www.scipy.org/
try:
	from numpy import dot
	from numpy.linalg import norm
	import numpy
except:
	print("Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?")
	sys.exit() 

def removeDuplicates(list):
	""" remove duplicates from a list """
	return set((item for item in list))


def cosine(vector1, vector2):
    """ related documents j and q are in the concept space by comparing the vectors :
    cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
    norm1 = numpy.linalg.norm(vector1)
    norm2 = numpy.linalg.norm(vector2)
    
    # 檢查是否有零範數的情況
    if norm1 == 0 or norm2 == 0:
        return 0.0  # 如果有一個向量是零向量，餘弦相似度設為0

    return float(numpy.dot(vector1, vector2) / (norm1 * norm2))

def euclidean_distance(vector1, vector2):
	return norm(vector1 - vector2)