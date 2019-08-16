import numpy as np


class CosineSimilarityClass():

    def cosine_similarity(self,sentence,sentences_vectors):
        self.sentence = sentence
        self.sentences_vectors = sentences_vectors

        cosSim = []

        for sentence_vector in sentences_vectors:
            cosSim.append(np.dot(sentence_vector, sentence) / (np.sqrt(
                np.sum(sentence_vector * sentence_vector)) * np.sqrt(np.sum(sentence * sentence))))

        return np.array(cosSim)



