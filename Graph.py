from collections import defaultdict
from CosineSimilarity import CosineSimilarityClass
import numpy as np

class GraphClass():

    def get_graph(self,tf_idf_matrix, threshold):

        graph = defaultdict(list)
        n_sentences=len(tf_idf_matrix)
        for node in range(n_sentences-1):
            start_index = node + 1
            cos_sim=CosineSimilarityClass().cosine_similarity(tf_idf_matrix[node],
                                  tf_idf_matrix[start_index:])
            index_of_edges=np.asarray(np.where(cos_sim>threshold))+start_index
            if len(index_of_edges[0])>0:
                graph[node] += list(index_of_edges[0])
                for i in index_of_edges[0] :
                    graph[i].append(node)

        return graph





