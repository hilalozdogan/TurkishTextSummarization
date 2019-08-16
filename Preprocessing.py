
from TurkishStemmer import TurkishStemmer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re


class PreprocessingClass():

    def _init_(self,text):
        self.text=text

    def preprocessing(self,text):

        self.clean_text(text)
        sentences=self.sentence_tokenize(text)
        self.filter_sentences(text)
        word_tokens=self.word_tokenize(text)
        word_stems=self.word_stemmer(text)

        return sentences,word_tokens,word_stems

    def clean_text(self,text):

        cleaned_text = ' '.join(text.strip().split('\n'))
        cleaned_text.replace(u"\u201c", "").replace(u"\u201d", "")  #tırnak işaretleri kaldırma

        return cleaned_text


    def sentence_tokenize(self,text):

        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.tokenize(self.clean_text(text))

        return sentences


    def filter_sentences(self, text):

        sentences=self.sentence_tokenize(text)
        filtered_sentences=[]
        for s in sentences:
            s = s.lower()
            s = re.sub(r'\d+', '', s)  #sayılar
            s = re.sub(r'[^\w\s]', '', s)  #karakterler
            filtered_sentences.append(s)

        return filtered_sentences

    def word_tokenize(self,text):

        filtered_sentences = self.filter_sentences(text)
        words=[]
        for s in filtered_sentences:
            word = word_tokenize(s)
            words.append(word)

        return words


    def word_stemmer(self,text):

        words = self.word_tokenize(text)
        stopword = stopwords.words('turkish')

        word_stems=[]
        title_stems=[]
        ts = TurkishStemmer()
        for word in words:
            for w in word:
               if w not in stopword:
                 word_stems.append(ts.stem(w))

        return word_stems









