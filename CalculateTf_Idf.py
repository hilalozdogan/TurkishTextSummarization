import numpy as np
from Preprocessing import PreprocessingClass

class CalculateTfIdfClass():

    def calculate(self,sentences,word_stems):
        self.sentences = sentences
        self.word_stems = word_stems

        word_stems = sorted(list(set(word_stems)))

        bowMatrix, word_of_sent = self.bag_of_words(sentences, word_stems)
        tfMatrix=self.compute_tf(sentences,word_stems,bowMatrix,word_of_sent)
        idfScore=self.compute_idf(sentences,word_stems,bowMatrix)
        tfIdfMatrix=self.compute_tf_idf(sentences,word_stems,tfMatrix,idfScore)

        return tfIdfMatrix,bowMatrix


    def bag_of_words(self,sentences,word_stems):

        word_of_sent=[]
        bag = np.zeros((len(sentences),len(word_stems)))
        for x,sentence in enumerate(sentences):
            stems = PreprocessingClass().word_stemmer(sentence)
            word_of_sent.append(len(stems))
            for word in stems:
                for y,st_word in enumerate(word_stems):
                    if st_word == word:
                        bag[x][y] += 1

        bow_matrix=np.array(bag)

        return bow_matrix,word_of_sent

    def compute_tf(self,sentences,word_stems,bowMatrix,word_of_sent):

        tf = np.zeros((len(sentences), len(word_stems)))
        for i in range(0, len(sentences)):
            for j in range(0, len(word_stems)):
                    freq=bowMatrix[i][j]
                    if freq != 0.0:
                        tf[i][j] = freq/word_of_sent[i]
                    else :
                        tf[i][j] = 0.0

        tf_matrix= np.array(tf)

        return tf_matrix

    def compute_idf(self,sentences,word_stems,bowMatrix):
        exist=0.0
        idf = np.zeros(len(word_stems))
        for i in range (0,len(word_stems)):
            for j in range(0, len(sentences)):
                freq=bowMatrix[j][i]
                if freq != 0.0 :
                    exist += 1

            idf[i]=(np.log10(len(sentences) / exist))
            exist=0.0

        idf = np.array(idf)
        return idf

    def compute_tf_idf(self,sentences,word_stems,tfMatrix,idfScore):

        tfidf_matrix = np.zeros((len(sentences), len(word_stems)))
        for i in range(0,len(sentences)):
            for j in range(0, len(word_stems)):
                tfidf_matrix[i][j]=tfMatrix[i][j]*idfScore[j]

        tf_idf_matrix = np.asarray(tfidf_matrix)
       # X = np.transpose(X)
        return tf_idf_matrix


