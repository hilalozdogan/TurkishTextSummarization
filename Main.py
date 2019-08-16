from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from Preprocessing import PreprocessingClass
from CalculateTf_Idf import CalculateTfIdfClass
from Pagerank import PagerankClass
from SentenceFeatures import SentenceFeaturesClass
from Graph import GraphClass
from MachineLearningModel import MachineLearningClass
import operator
from langdetect import detect


def dialog():
    var = messagebox.showinfo("Uyarı", "Özetlemek istenilen metin Türkçe dilinde değildir!")

def dialog2():
    var = messagebox.showinfo("Uyarı", "Özetlemek istenilen metnin başlığı Türkçe dilinde değildir!")

def dialog3():
    var = messagebox.showinfo("Uyarı", "Özet cümle sayısı,özetlenmek istenilen metindeki cümle sayısından fazla olamaz!")

def dialog4():
    var = messagebox.showinfo("Uyarı", "Özetlemek istenilen metnin boyutu çok uzun!")


def get_text():
    text = T1.get(1.0, "end-1c")
    return text


def get_title():
    title = Tittle.get(1.0, "end-1c")
    if (detect(title) != 'tr'):
        dialog2()
    return title

def clean():

    T1.delete(1.0, "end-1c")
    Tittle.delete(1.0, "end-1c")
    Number.delete(1.0,"end-1c")


def cleanSum():

    T2.delete(1.0, "end-1c")

def summarizeMl():

    cleanSum()
    text=get_text()
    if (detect(text) == 'tr'):
        summary=MachineLearningClass().newPred(text)
        for i in range(0,len(summary)):
            T2.insert(INSERT,summary[i])
    else:
        dialog()

    return summary

def summarize():

    cleanSum()
    threshold=0.01
    d=0.15
    n_iter=50
    SummaryNumber = int(Number.get(1.0, "end-1c"))
    text=get_text()
    if (detect(text) == 'tr'):
        title=get_title()
        sentences,word_tokens,word_stems=PreprocessingClass().preprocessing(text)
        if(len(sentences)<10):
            if (len(sentences) > SummaryNumber):
                tfIdfMatrix,bowMatrix=CalculateTfIdfClass().calculate(sentences,word_stems)
                graph=GraphClass().get_graph(tfIdfMatrix,threshold)
                pagerank_scores=PagerankClass().calculate_page_rank(graph,d,n_iter)
                sentence_scores=SentenceFeaturesClass().calculate_sent_scores(sentences,word_stems,word_tokens,title)


                ranked_sentences = sorted(((pagerank_scores[i], s) for i, s in enumerate(sentences)), reverse=True)

                print("PageRank")
                for i, s in enumerate(sentences):
                    print(ranked_sentences[i])

                ranked_sent_features = sorted(((sentence_scores[i], s) for i, s in enumerate(sentences)), reverse=True)

                print("Sentence Features Score")
                for i, s in enumerate(sentences):
                    print(ranked_sent_features[i])



                for i,s in enumerate(sentences):
                    pagerank_scores[i]=pagerank_scores[i]+sentence_scores[i]


                scores_sorted_bySimilarity = sorted(pagerank_scores.items(),
                                                    key=operator.itemgetter(1), reverse=True)[0:SummaryNumber]

                summary = [sentences[line] for line, sim in scores_sorted_bySimilarity]

                print("Final Score")
                for i, s in enumerate(sentences):
                        print(pagerank_scores[i],s)

                for i in range(0, SummaryNumber):
                    T2.insert(INSERT, summary[i])

            else :
                dialog3()
        else:
            dialog4()
    else:
        dialog()

root = Tk()
root.title("Metin Özetleyici")
root.geometry("970x600")
root.configure(background='lavender blush')

L1 = Label(text="Özetlemek İstediğiniz Metin",font=("Verdana", 13, "bold"),fg="gray40")
L1.configure(background='lavender blush')
Tittle = Text(bd=5,width=60,height=1)
Tittle.insert(INSERT,"Başlığı Giriniz...")
Tittle.configure(font=("Verdana 10 italic "),fg="VioletRed3")
T1 = ScrolledText(bd=5,width=100,height=10)
T1.configure(font=("Verdana 10 italic"),fg="gray40")
T1.insert(INSERT,"Metni Giriniz...")
L1.place(x=60,y=5)
T1.place(x=60,y=70)
Tittle.place(x=60,y=35)

L2 = Label(text="Metnin Özet Hali",font=("Verdana", 13,"bold"),fg="gray40")
L2.configure(background='lavender blush')
T2 = ScrolledText(bd=5, width=100,height=10)
T2.configure(font=("Verdana 10 italic"),fg="gray40")
L2.place(x=60,y=330)
T2.place(x=60,y=360)

B1=Button(text="ÖZETLE (TextRank)",bd=2,height=2,width=16,font=("Verdana", 11, "bold"),fg="white",command=summarize)
B2=Button(text="TEMİZLE",bd=2,height=1,width=9,font=("Verdana", 10, "bold"),fg="white",command=clean)
B3=Button(text="ÖZETLE (ML)",bd=2,height=2,width=16,font=("Verdana", 11, "bold"),fg="white",command=summarizeMl)
B4=Button(text="TEMİZLE",bd=2,height=1,width=9,font=("Verdana", 10, "bold"),fg="white",command=cleanSum)
B1.configure(background="skyblue")
B2.configure(background="chartreuse3")
B3.configure(background="skyblue")
B4.configure(background="chartreuse3")

B1.place(x=250,y=270)
B2.place(x=800,y=250)
B3.place(x=500,y=270)
B4.place(x=800,y=540)

Number = Text(bd=4,width=29,height=1)
Number.place(x=615,y=35)
Number.insert(INSERT,"Özetteki Cümle Sayısını Giriniz....")
Number.configure(font=("Verdana 10 italic "),fg="VioletRed3")

root.mainloop()




