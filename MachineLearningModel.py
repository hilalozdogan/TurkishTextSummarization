import pickle

from sklearn.model_selection import train_test_split
from Preprocessing import PreprocessingClass
import pandas as pd
from nltk.tokenize.punkt import PunktSentenceTokenizer
from TurkishStemmer import TurkishStemmer
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfTransformer


class MachineLearningClass():

        ts = TurkishStemmer()
        sentenceDict = {}
        sentenceDictLen = {}
        sentenceDictLabel = {}

        no_of_inputs = 10    #Number of training files
        no_of_testSet = 10  #Number of test files


        for x in range(1, no_of_inputs+1):
            sentenceList = ''
            sentenceListSum = ''
            fileName = 'Veriseti/Text' + str(x) + ".txt"
            fileNameSummary = 'Veriseti/Summary' + str(x) + ".txt"
            openText = open(fileName,"r")
            readText = openText.read()
            openSummary = open(fileNameSummary,"r")
            readSummary = openSummary.read()

            sentenceList=PreprocessingClass().filter_sentences(readText)

            sentenceListSum=PreprocessingClass().filter_sentences(readSummary)

            no_of_sentence = len(sentenceList)

            for y in range(0, no_of_sentence):
                sentId = str(x) + '.' + str(y)
                sentenceDict[sentId] = sentenceList[y]

                if (sentenceDict[sentId] in sentenceListSum):
                    sentenceDictLabel[sentId] = 1
                else:
                    sentenceDictLabel[sentId] = 0

                stems=PreprocessingClass().word_stemmer(sentenceDict[sentId])
                sentenceDict[sentId]=' '.join(stems)


        df=pd.DataFrame(sentenceDict.items(), columns=['SentenceId', 'Sentence'])
        dfSum=pd.DataFrame(sentenceDictLabel.items(),columns=['SentenceId','Label'])
        label=dfSum.iloc[:,-1].values
        sentence=df.iloc[:,-1].values

        with open('X.pickle','wb') as f:
            pickle.dump(sentence,f)

        with open('y.pickle', 'wb') as f:
            pickle.dump(label, f)

        dfLabel=pd.DataFrame(data=label,index=range(len(sentence)),columns=["Label"])
        dfData=pd.concat([df,dfLabel],axis=1)

        vectorizer=CountVectorizer(max_features=50)
        X=vectorizer.fit_transform(sentence).toarray()

        transformer=TfidfTransformer()
        X=transformer.fit_transform(X).toarray()
        y=dfSum.iloc[:,-1].values

        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=0)

        gnb=GaussianNB()
        gnb.fit(X_train,y_train)
        y_pred=gnb.predict(X_test)
        cm=confusion_matrix(y_test,y_pred)
        print(cm)


        with open('classifier.pickle','wb') as f:
            pickle.dump(gnb,f)

        with open('tfidfmodel.pickle','wb') as f:
            pickle.dump(transformer,f)

        with open('vectorize.pickle','wb') as f:
            pickle.dump(vectorizer, f)



        def newPred(self,text):
            sentence_tokenizer = PunktSentenceTokenizer()
            sentences = sentence_tokenizer.tokenize(text)
            print(len(sentences))
            predList = PreprocessingClass().filter_sentences(text)

            with open('classifier.pickle','rb') as f:
                clf=pickle.load(f)

            with open('vectorize.pickle','rb') as f:
                vect=pickle.load(f)

            with open('tfidfmodel.pickle', 'rb') as f:
                tfidf=pickle.load(f)

            predText = vect.fit_transform(predList).toarray()
            predText = tfidf.transform(predText).toarray()
            new_pred = clf.predict(predText)
            finalSum = [ ]
            for i,j in enumerate(new_pred):
                if j == 1 :
                    finalSum.append(sentences[i])

            return finalSum





