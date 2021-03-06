#ZAID VAKIL

import speech_recognition as speech 
from gtts import gTTS 
import playsound 
import os 
import random
import webbrowser 
from time import ctime
import time
import yfinance
import mysql.connector
from mysql.connector import Error

# DB connection function
def dbConnection(host_name, user_name, user_password, db_name):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    except Error as e:
        print(f"The error '{e}' occurred")

    return conn

conn = dbConnection("localhost", "root", os.environ.get('DBPassword'), "jarvis") #establishing db connection

#function for db queries
def execute_read_query(conn, query):
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

select_users = "SELECT usrName from name" #executing query
myName = execute_read_query(conn, select_users) #retrieving my name


# checker function that checks for specific words/phrases in voice data
def checker(terms):
    for term in terms:
        if term in voice_data:
            return True

r = speech.Recognizer() #initializing variable 'r' to function as speech recognizer

def record_audio(ask=False):
    with speech.Microphone() as source: #default mic as audio source
        if ask:
            speak(ask)
        audio = r.listen(source)  #listening to audio 
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio) # converting to text
        except speech.UnknownValueError:
            speak("I didn't quite catch that")
        except speech.RequestError:
            speak('Sorry, the service is down') 
        print(f"-- {voice_data.lower()}") #print what the user said
        return voice_data.lower()

#function that converts a string to audio file
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') #google text to speech
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file) #play the file
    print(f"Jarvis: {audio_string}") #print what was played
    os.remove(audio_file) # delete the audio file

def respond(voice_data):
   

   # various greetings
    if checker(['hey','hi','hello', 'sup']):
        greetings = [f"hey, how can I help you {myName}", f"hey, what's up {myName}?", f"I'm listening master {myName}", f"how can I help you? {myName}", f"hello {myName}"]
        greet = greetings[random.randint(0,len(greetings)-1)]
        speak(greet)

    # pleasantries
    if checker(["how are you","how are you doing", "how's life", "how's it hanging"]):
        speak(f"I'm doing fantastic, thanks for asking {myName}!")
    
    
    if checker(['what is your name',"what's your name",'tell me your name', 'who are you', 'tell me who you are' ]):
        if myName:
            speak("my name is Jarvis")
        else:
            speak("my name is Jarvis. what's your name?")

    if checker(["my name is"]):
        new_name = voice_data.split("is")[-1].strip()
        speak(f"So very nice to meet you {new_name}")

   #time
    if checker(["what's the time","tell me the time","what time is it"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)

    #will google search if 'youtube' is not spoken
    if checker(["search for"]) and 'youtube' not in voice_data:
        search = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search} on google')

    #will youtube search the phrase if youtube is spoken
    if checker(["youtube"]):
        search = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search} on youtube')

    #stock price retrieval (limited for now)
    if checker(["price of"]):
        search = voice_data.lower().split(" of ")[-1].strip() 
        stocks = {
            "apple":"AAPL",
            "bitcoin":"BTC-USD",
            "facebook":"FB",
            "microsoft":"MSFT",
            "tesla":"TSLA"
           
        }
        try:
            stock = stocks[search]
            stock = yfinance.Ticker(stock)
            price = stock.info["regularMarketPrice"]

            speak(f'price of {search} is {price} {stock.info["currency"]} {myName}')
        except:
            speak('oops, something went wrong')
    if checker(["exit", "quit", "goodbye", "see you later", "see ya later", "later gator"]):
        speak("goodbye")
        exit()

time.sleep(6)

while(1):
    voice_data = record_audio() 
    respond(voice_data) 