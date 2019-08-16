from TurkishStemmer import TurkishStemmer
from Preprocessing import PreprocessingClass
import math
from collections import Counter
import numpy as np

ts = TurkishStemmer()
ideal_length = 20.0

class SentenceFeaturesClass():

    def calculate_sent_scores(self,sentences,word_stems,word_tokens,title):

        lengthScore=self.sent_length_score(sentences)
        keywordScore=self.keywords_score(sentences,word_stems)
        posScore,negScore=self.positive_negative_words(sentences,word_tokens)
        titleScore=self.title_score(title,sentences)

        total_score=(lengthScore+keywordScore+posScore+negScore+titleScore)/10

        return total_score



    def sent_length_score(self, sentences):
        self.sentences=sentences

        length_score = np.zeros(len(sentences))

        for i, sentence in enumerate(sentences):

            difference = math.fabs(ideal_length - len(sentences[i]))
            score=difference / ideal_length
            length_score[i]=score

        return length_score*0.01


    def keywords_score(self,sentences,word_stems):
        self.sentences=sentences
        self.word_stems=word_stems

        freq_sent_scores = np.zeros(len(sentences))

        percent=round(len(word_stems)*0.1)
        freq = Counter(word_stems).most_common(percent)
        for i, sentence in enumerate(sentences):
            stems = PreprocessingClass().word_stemmer(sentence)
            for word in stems:
                for j in range(len(freq)):
                    if word == freq[j][0]:
                        freq_sent_scores[i] += 0.10

        return freq_sent_scores


    def positive_negative_words(self,sentences,word_tokens):
        positive_words=["özetle","sonuçta","neticede","kısacası","böylece"]
        negative_words=["çünkü","ancak","öyleyse","örneğin","ayrıca","ama","artık","halbuki","sonra","bu","şu"]

        pos_sent_score = np.zeros(len(sentences))
        neg_sent_score=np.zeros(len(sentences))

        for x,sent_words in enumerate(word_tokens):
            for word in sent_words:
                for pword in positive_words:
                    if pword == word :
                        pos_sent_score[x] += 0.20
                for nword in negative_words:
                    if nword == word:
                        neg_sent_score[x] -= 0.20


        return pos_sent_score,neg_sent_score


    def title_score(self,title,sentences):

        title_sent_score=np.zeros(len((sentences)))
        title_stems = PreprocessingClass().word_stemmer(title)

        for i, sentence in enumerate(sentences):
            stems = PreprocessingClass().word_stemmer(sentence)
            for word in stems:
                for tword in title_stems:
                    if tword == word:
                        title_sent_score[i] += 0.20

        return title_sent_score


    def sent_position_score(self,sentences):

        pos_score=np.zeros(len(sentences))

        for i,sentence in enumerate(sentences):

            relative_position = i / len(sentence)

            if 0 < relative_position <= 0.1:
                score=0.17
            elif 0.1 < relative_position <= 0.2:
                score=0.23
            elif 0.2 < relative_position <= 0.3:
                score=0.14
            elif 0.3 < relative_position <= 0.4:
                score=0.08
            elif 0.4 < relative_position <= 0.5:
                score=0.05
            elif 0.5 < relative_position <= 0.6:
                score=0.04
            elif 0.6 < relative_position <= 0.7:
                score=0.06
            elif 0.7 < relative_position <= 0.8:
                score=0.04
            elif 0.8 < relative_position <= 0.9:
                score=0.04
            elif 0.9 < relative_position <= 1.0:
                score=0.02
            else:
                score=0

            pos_score[i]=score

        return pos_score














