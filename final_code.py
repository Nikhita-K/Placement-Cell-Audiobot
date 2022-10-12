from tkinter import *
import time
import datetime
import pyttsx3
import speech_recognition as sr
from threading import Thread
import requests
from bs4 import BeautifulSoup
import nltk
# other packages required for this Program
import random
import string  # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import mysql.connector
warnings.filterwarnings('ignore')

def shut_down():
    p1 = Thread(target=speak, args=("Shutting down. Thankyou For Using Our Sevice. Take Care, Good Bye.",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    time.sleep(7)
    root.destroy()


def transition2():
    global img1
    global flag
    global flag2
    global frames
    global canvas
    local_flag = False
    for k in range(0, 5000):
        for frame in frames:
            if flag == False:
                canvas.create_image(0, 0, image=img1, anchor=NW)
                canvas.update()
                flag = True
                return
            else:
                canvas.create_image(0, 0, image=frame, anchor=NW)
                canvas.update()
                time.sleep(0.1)


def chatbot(sent):
    global flag2
    global loading
    # answer is the variable to be used to store the response to be displayed
    # t = Label(root, text="Hi", font=("Candara Light", 18), bg="#7D1935", fg="white").place(x=1010, y=30)
    f = open('chatbot.txt', 'r', errors='ignore')
    raw = f.read()
    raw = raw.lower()  # converts to lowercase

    # sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences
    sent_tokens = raw.split("\n")
    word_tokens = nltk.word_tokenize(raw)  # converts to list of words
    # print(sent_tokens)
    # print(word_tokens)

    lemmer = nltk.stem.WordNetLemmatizer()

    # WordNet is a semantically-oriented dictionary of English included in NLTK.
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    # Keyword Matching
    GREETING_INPUTS = (
    "hello", "hi", "greetings", "sup", "hey", "good morning", "good afternoon", "good evening", "good night")
    GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

    def greeting(sentence):
        """If user's input is a greeting, return a greeting response"""
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)

    def response(user_response):
        bot_response = ''
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            bot_response = bot_response + "I am sorry! I don't understand you"
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="chatbot"
            )
            my_cursor = mydb.cursor()
            sql = "INSERT INTO queries(query,resolved,date) values (%s,%s,NOW())"
            attach = (user_response, 0)
            my_cursor.execute(sql, attach)
            mydb.commit()
            return bot_response
        else:
            bot_response = bot_response + sent_tokens[idx]
            return bot_response
    user_response = sent.lower()
    if greeting(user_response) is not None:
        answer = greeting(user_response)
    else:
        answer = response(user_response)
        sent_tokens.remove(user_response)
    # return bot
    # answer = chatbot(user_response)
    canvas2.create_text(10, 225, anchor=NW, text=answer, font=('Candara Light', -25, 'bold italic'), fill="white",
                        width=350)
    flag2 = False
    loading.destroy()

    p1 = Thread(target=speak, args=(answer,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def speak(text):
    global flag
    engine.say(text)
    engine.runAndWait()
    flag = False


def wishme():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning. I am C M R I T placement bot."
    elif 12 <= hour < 18:
        text = "Good Afternoon. I am C M R I T placement bot."
    else:
        text = "Good Evening. I am C M R I T placement bot."

    canvas2.create_text(10, 10, anchor=NW, text=text, font=('Candara Light', -25, 'bold italic'), fill="white",
                        width=350)
    p1 = Thread(target=speak, args=(text,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def takecommand():
    global loading
    global flag
    global flag2
    global canvas2
    global query
    global img4
    if flag2 == False:
        canvas2.delete("all")
        canvas2.create_image(0, 0, image=img4, anchor="nw")

    speak("I am listening.")
    flag = True
    r = sr.Recognizer()
    # r.dynamic_energy_threshold = False
    # r.energy_threshold = 4000
    with sr.Microphone() as source:
        print("Listening...")
        # r.pause_threshold = 3
        audio = r.listen(source) #, timeout=10, phrase_time_limit=4

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user Said :{query}\n")
        query = query.lower()
        canvas2.create_text(490, 120, anchor=NE, justify=RIGHT, text=query, font=('Comic Sans MS', -30,'bold'), fill="#FF5C58",
                            width=350)
        global img3
        loading = Label(root, image=img3, bd=0)
        loading.place(x=900, y=622)

    except Exception as e:
        print(e)
        speak("Say that again please")
        return "None"

def q1():
    global canvas2
    global query
    global img4
    canvas2.delete("all")
    canvas2.create_image(0, 0, image=img4, anchor="nw")
    ques_1 = "Is there any contact no?"
    ans_1= "Contact us : Tel => +91 80 28524466/77 , Email => info@cmrit.ac.in"
    canvas2.create_text(10, 120, anchor=NW, text=ques_1, font=('Candara Light', -25, 'bold italic'), fill="white",
                        width=350)
    canvas2.create_text(490, 225, anchor=NE, justify=RIGHT, text=ans_1, font=('Comic Sans MS', -20, 'bold'),
                        fill="#FF5C58",
                        width=350)
    p1 = Thread(target=speak, args=(ques_1+ans_1,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    next_btn = Button(root, image=img_next, bd=0, command=q2)
    next_btn.place(x=1000, y=625)

def q2():
    # lambda: okVar.set(1)
    global canvas2
    global query
    global img4
    canvas2.delete("all")
    canvas2.create_image(0, 0, image=img4, anchor="nw")
    ques_2 = "What are all the departments at CMRIT ?"
    ans_2 = "Departments at CMRIT : CSE, ISE, TCE, ECE, EEE, CIVIL, MECH, CS AND AI, CS AND ML."
    canvas2.create_text(10, 120, anchor=NW, text=ques_2, font=('Candara Light', -25, 'bold italic'), fill="white",
                        width=350)
    canvas2.create_text(490, 225, anchor=NE, justify=RIGHT, text=ans_2, font=('Comic Sans MS', -20, 'bold'),
                        fill="#FF5C58",
                        width=350)
    p1 = Thread(target=speak, args=(ques_2+ans_2,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    next_btn = Button(root, image=img_next, bd=0, command=q3)
    next_btn.place(x=1000, y=625)

def q3():
    # lambda: okVar.set(1)
    global canvas2
    global query
    global img4
    canvas2.delete("all")
    canvas2.create_image(0, 0, image=img4, anchor="nw")
    ques_3 = "What are all the companies visiting CMRIT ?"
    ans_3 = "Companies visiting CMRIT are Amazon, Cimpress, Ellucian, HP, Accenture, Capgemini, Deloitte, Infosys,and foreign companies like Canbright, Tokyo, Andpad, Aucfan, Cretors Match from Japan"
    canvas2.create_text(10, 120, anchor=NW, text=ques_3, font=('Candara Light', -25, 'bold italic'), fill="white",
                        width=350)
    canvas2.create_text(490, 225, anchor=NE, justify=RIGHT, text=ans_3, font=('Comic Sans MS', -20, 'bold'),
                        fill="#FF5C58",
                        width=350)
    p1 = Thread(target=speak, args=(ques_3+ans_3,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    next_btn = Button(root, image=img_next, bd=0, command=end)
    next_btn.place(x=1000, y=625)
    # lambda: okVar.set(1)
    # next_btn.destroy()

def end():
    # q3.next_btn.destroy()
    # lambda: okVar.set(1)
    global canvas2
    global query
    global img4
    canvas2.delete("all")
    canvas2.create_image(0, 0, image=img4, anchor="nw")
    end_txt = "These were some of the FAQ's asked, if you have more queries pleas click on the ask me a Question button"
    speak(end_txt)


def faq():
    q1()
    # q2()
    # q3.next_btn.destroy()


def main_window():
    global query
    global canvas2
    global img4
    wishme()
    while True:
        if query != None:
            if 'shutdown' in query or 'quit' in query or 'stop' in query or 'goodbye' in query or 'bye' in query:
                shut_down()
                break
            else:
                chatbot(query)
                query = None




if __name__ == "__main__":
    loading = None
    query = None
    flag = True
    flag2 = True

    engine = pyttsx3.init()  # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 10)

    root = Tk()
    root.title("Intelligent Chatbot")
    root.geometry('1360x690+-5+0')
    root.configure(background='white')

    img1 = PhotoImage(file='chatbot-image.png')
    img2 = PhotoImage(file='button.png')
    img2_2 = PhotoImage(file = 'FAQ_btn.png')
    img_next = PhotoImage(file = 'next.png')
    img3 = PhotoImage(file='icon.png')
    img4 = PhotoImage(file='try4.png')
    background_image = PhotoImage(file="last.png")

    f = Frame(root, width=1360, height=690)
    f.place(x=0, y=0)
    f.tkraise()
    front_image = PhotoImage(file="front.png")
    okVar = IntVar()
    btnOK = Button(f, image=front_image, command=lambda: okVar.set(1))
    btnOK.place(x=39, y=52)
    f.wait_variable(okVar)
    f.destroy()

    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0)

    frames = [PhotoImage(file='chatgif.gif', format='gif -index %i' % (i)) for i in range(20)]
    canvas = Canvas(root, width=800, height=596)
    canvas.place(x=10, y=10)
    canvas.create_image(0, 0, image=img1, anchor=NW)
    question_button = Button(root, image=img2, bd=0, command=takecommand)
    question_button.place(x=100, y=625)
    question_button2 = Button(root, image=img2_2, bd=0, command=faq)
    question_button2.place(x=500, y=625)

    frame = Frame(root, width=500, height=596)
    frame.place(x=825, y=10)
    canvas2 = Canvas(frame, bg='#FFFFFF', width=500, height=596, scrollregion=(0, 0, 500, 900))
    vbar = Scrollbar(frame, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canvas2.yview)
    canvas2.config(width=500, height=596, background="black")
    canvas2.config(yscrollcommand=vbar.set)
    canvas2.pack(side=LEFT, expand=True, fill=BOTH)
    canvas2.create_image(0, 0, image=img4, anchor="nw")

    task = Thread(target=main_window)
    task.start()
    root.mainloop()