import argparse
import os
from VectorSpace import VectorSpace
from Parser import Parser
from Parser import Jieba
from Parser import Blob
import csv

def task1(documents, query):
    parser = Blob()
    vs = VectorSpace(parser, documents)
    print("task1: ")
    print("--------------------------------------------------")
    print("Query string: ", query, " , TF, Cosine Similarity")
    print("NewsID/Score")
    for key, value in list(vs.search(query, "TF", "Cosine").items())[:10]:
        print(f"{key}: {value}")
    print("--------------------------------------------------")
    print("Query string: ", query, ", TF-IDF, Cosine Similarity")
    print("NewsID/Score")
    for key, value in list(vs.search(query, "TF-IDF", "Cosine").items())[:10]:
        print(f"{key}: {value}")
    print("--------------------------------------------------")
    print("Query string: ", query, ", TF, Euclidean Distance")
    print("NewsID/Score")
    for key, value in list(vs.search(query, "TF", "Euclidean").items())[:10]:
        print(f"{key}: {value}")
    print("--------------------------------------------------")
    print("Query string: ", query, ", TF-IDF, Euclidean Distance")
    print("NewsID/Score")
    for key, value in list(vs.search(query, "TF-IDF", "Euclidean").items())[:10]:
        print(f"{key}: {value}")
    print("--------------------------------------------------")
    return vs

def task2(vs, query):
    print("task2: ")
    print("--------------------------------------------------")
    print("Query string: ", query, ", TF-IDF, Cosine Similarity")
    print("NewsID/Score")
    for key, value in list(vs.pseudo_feedback_search(query, "TF-IDF", "Cosine").items())[:10]:
        print(f"{key}: {value}")
    print("--------------------------------------------------")

def task3(documents, query):
    parser = Jieba()
    #print(query)
    #print(documents)
    vs = VectorSpace(parser, documents)
    print("task3: ")
    res = list(vs.search(query, "TF", "Cosine").items())[:10]
    print("--------------------------------------------------")
    print("Query string: ", query, " , TF, Cosine Similarity")
    print("NewsID/Score")
    for key, value in res:
        print(f"{key}: {value}")
    res = list(vs.search(query, "TF-IDF", "Cosine").items())[:10]
    print("--------------------------------------------------")
    print("Query string: ", query, ", TF-IDF, Cosine Similarity")
    print("NewsID/Score")
    for key, value in res:
        print(f"{key}: {value}")
    print("--------------------------------------------------")

def task4(documents, queries, solution):
    parser = Blob()
    vs = VectorSpace(parser, documents)
    #res = {key: (list(vs.pseudo_feedback_search(query, "TF-IDF", "Cosine").items())[:10]) for key, query in queries.items()}
    res = {key: [row[0] for row in (list(vs.search(query, "TF-IDF", "Cosine").items())[:10])] for key, query in queries.items()}
    res = {key: [s[1:] if s.startswith('d') else s for s in value] for key, value in res.items()}
    #print(res)
    MRR_cnt = 0
    MAP_cnt = 0
    recall_cnt = 0
    for query, pred in res.items():
        relevant_docs = solution.get(query, [])
        #print("query: ", query, ", ", relevant_docs)
        #print("pred: ", pred)
        reciprocal_rank = 0
        for rank, doc_id in enumerate(pred):
            if doc_id in relevant_docs:
                reciprocal_rank = 1 / (rank+1)
                break
        MRR_cnt += reciprocal_rank

        relevant_cnt = 0
        precision_sum = 0
        for rank, doc_id in enumerate(pred):
            if doc_id in relevant_docs:
                relevant_cnt += 1
                precision_sum += relevant_cnt / (rank+1)
        if relevant_cnt > 0:
            MAP_cnt += precision_sum / relevant_cnt
        
        recall_cnt += relevant_cnt / len(relevant_docs)
    print("task4: ")
    print("--------------------------------------------------")
    print("Query string: ", ", TF-IDF, Cosine Similarity")
    print("MRR@10: ", MRR_cnt / len(res))
    print("MRR@10: ", MAP_cnt / len(res))
    print("MRR@10: ", recall_cnt / len(res))
    print("--------------------------------------------------")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Eng_query", type=str)
    parser.add_argument("--Chi_query", type=str)
    args = parser.parse_args()
    eng_documents = {}
    for filename in os.listdir("./EnglishNews"):
        file_path = os.path.join("./EnglishNews", filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            eng_documents[filename.split(".")[0]] = f.read()
    vs = task1(eng_documents, args.Eng_query)
    task2(vs, args.Eng_query)
    chi_documents = {}
    for filename in os.listdir("./ChineseNews"):
        file_path = os.path.join("./ChineseNews", filename)
        #print(file_path)
        with open(file_path, 'r') as f:
            chi_documents[filename.split(".")[0]] = f.read()
    #print(chi_documents)
    task3(chi_documents, args.Chi_query)
    smaller_documents = {}
    for filename in os.listdir("./smaller_dataset/collections"):
        file_path = os.path.join("./smaller_dataset/collections", filename)
        with open(file_path, 'r') as f:
            smaller_documents[filename.split(".")[0]] = f.read()
    smaller_queries = {}
    for filename in os.listdir("./smaller_dataset/queries"):
        file_path = os.path.join("./smaller_dataset/queries", filename)
        with open(file_path, 'r') as f:
            smaller_queries[filename.split(".")[0]] = f.read()
    solution = {}
    with open("./smaller_dataset/rel.tsv", 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            solution[row[0]] = row[1].strip('[]').split(', ')
    #print(solution)
    task4(smaller_documents, smaller_queries, solution)



if __name__ == "__main__":
    main()