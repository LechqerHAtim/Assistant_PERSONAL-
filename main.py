import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import yfinance as yf # to fetch financial data
import ssl
import certifi
import time
from record import record
import datetime
import requests, json
import pprint 
import requests 
import os # to remove created audio files
import wikipedia
import smtplib
import time
import imaplib
import email
import traceback 
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "emailforprojecttest" + ORG_EMAIL 
FROM_PWD = "test123@" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993
my_dict = {'jhon':FROM_EMAIL, "alexa" :FROM_EMAIL,"alex" :FROM_EMAIL,"alexis" :FROM_EMAIL}


class person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True
r = sr.Recognizer()
r.energy_threshold = 500
# listen for audio and convert it to text:

#####################################################################################
def record_audio(ask=False):
    try:
        rec=record()
        rec.reco()
        data='output.wav'
        # define the recognizer

        # define the audio file
        audio_file = sr.AudioFile(data)
        # speech recognition
        with audio_file as source: 
            audio=r.record(source)
            result = r.recognize_google(audio)
            print(result)
        return result.lower()
    except :
        return 'i did not get that'
# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"0: {audio_string}") # print what app said
    os.remove(audio_file) # remove audio file
################# weather #############################
def get_weather(city):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = city
    API_KEY = "f50118cf8a114e59a12bc48f97a1a357"
    # upadting the URL
    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
    # HTTP request
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data['main']
        # getting temperature
        temperature = main['temp']
        # getting the humidity
        humidity = main['humidity']
        # getting the pressure
        pressure = main['pressure']
        # weather report
        report = data['weather']
        speak(f"Temperature: {temperature}")
        speak(f"Humidity: {humidity}")
        speak(f"Pressure: {pressure}")
        speak(f"Weather Report: {report[0]['description']}")
    else:
        # showing the error message
        speak("there is a problem make sure that you are connected")
################# Article ##############
def get_article(tile):
    if tile=='exit':
        exit()
    url = 'https://newsapi.org/v2/everything?'

    # Specify the query and 
    # number of returns 
    parameters = { 
        'q': 'merkel', # query phrase 
        'pageSize': 100, # maximum is 100 
        'apiKey': 'b7606d9935694125bd119401331fdbd8' # your own API key 
    } 

    # Make the request 

    response = requests.get(url, 
                            params = parameters) 

    # Convert the response to 
    # JSON format and pretty print it 
    response_json = response.json() 
    #pprint.pprint(response_json) 
    articlee ='' 
    for article in response_json['articles']:
        for word in tile.split():
             if word in article['title']:
                 articlee=article['title']
             break
    return articlee
    ####################### Read Email###################
def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        fromWho={}

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(1,10):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                try:
                    if isinstance(arr, tuple):
                
                        msg = email.message_from_string(str(arr[1],'utf-8'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        print('From : ' + email_from + '\n')
                        print('Subject : ' + email_subject + '\n')
                        fromWho[i]='from '+email_from+'  and the subject is  ' + email_subject
                except:
                    print('')
        return fromWho
    except Exception as e:
        traceback.print_exc() 
        print(str(e))
############ send email ################
def send_mail(receiver_email, msg):
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.sendmail(FROM_EMAIL, receiver_email, msg)
        mail.close()
        return True
    except Exception as e:
        print(e)
        return False
####################### top News #####################
def topnews():
    api_dict={
    "business":"http://newsapi.org/v2/top-headlines?country=ma&category=business&apiKey=b638e9087e644b8bb916b747c65ab141",
    "entertainment":"http://newsapi.org/v2/top-headlines?country=ma&category=entertainment&apiKey=b638e9087e644b8bb916b747c65ab141",
    "health":"http://newsapi.org/v2/top-headlines?country=ma&category=health&apiKey=b638e9087e644b8bb916b747c65ab141",
    "science":"http://newsapi.org/v2/top-headlines?country=ma&category=science&apiKey=b638e9087e644b8bb916b747c65ab141",
    "sports":"http://newsapi.org/v2/top-headlines?country=ma&category=sports&apiKey=b638e9087e644b8bb916b747c65ab141",
    "technology":"http://newsapi.org/v2/top-headlines?country=ma&category=technology&apiKey=b638e9087e644b8bb916b747c65ab141",
    "sports":"http://newsapi.org/v2/top-headlines?country=ma&category=sports&apiKey=b638e9087e644b8bb916b747c65ab141",

}
    content=None
    url=None
    con=True

    while con:

        speak('which field news do you want ?:')
        field=record_audio()
        print(field)


        for key,value in api_dict.items():

                if key in field:
                    url=value
                    print(value)
                    con=False
                    break
                else:
                    url=True
        

    news=requests.get(url).text
    news=json.loads(news)
    speak("here's the first news")
    arts=news['articles']
    for articles in arts:
        article=articles['title']
  
        if article is None:
            continue
        speak(article)
   
    print('here the top news end, thank you')
    speak('here the top news end, thank you')


################## remnider of medicine ############
def takeMedecine():
    now = datetime.datetime.now()
    if now.strftime("%I:%M")=="03:12":
        speak('take your medecine baby ')


def respond(voice_data):
    # 1: greeting
    if there_exists(['hey','hi','hello']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
        greet = greetings[random.randint(0,len(greetings)-1)]
        speak(greet)

###################################################################
    # 2: name
    if there_exists(["what is your name","what's your name","tell me your name"]):
        if person_obj.name:
            speak("my name is lobana")
        else:
            speak("my name is lobana. what's your name?")

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name) # remember name in person object

    # 3: greeting
    if there_exists(["how are you","how are you doing"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")

    # 4: time
    if there_exists(["what hour","what time","what's the time","tell me the time","what time is it"]):
        now = datetime.datetime.now()
        if str(now.hour)== "00":
            hours = '12'
        else:
            hours = str(now.hour)
        minutes = str(now.minute)
        time = f'{hours} {minutes}'
        print(time)
        speak(time)

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    # 6: search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')

    # 7: get stock price
    if there_exists(["price of"]):
        search_term = voice_data.lower().split(" of ")[-1].strip() #strip removes whitespace after/before a term in string
        stocks = {
            "apple":"AAPL",
            "microsoft":"MSFT",
            "facebook":"FB",
            "tesla":"TSLA",
            "bitcoin":"BTC-USD"
        }
        try:
            stock = stocks[search_term]
            stock = yf.Ticker(stock)
            price = stock.info["regularMarketPrice"]

            speak(f'price of {search_term} is {price} {stock.info["currency"]} {person_obj.name}')
        except:
            speak('oops, something went wrong')
    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        exit()
    
    #weather 
    if there_exists(["weather","tell me weather","how is outside"]):
        get_weather('tanger')





    if there_exists(["tell joke","joke"]):
        speak("ok listing  this is new jokeA woman gets on a bus with her baby. The driver says “Ugh – that’s the ugliest baby I’ve ever seen!” The woman walks to the back of the bus and sits down. She says to the man next to her: The driver just insulted me The man says: “You go up there and tell him off. Go on. I’ll hold your monkey for you.  ")
  
    if there_exists(["what news","article","news","read news","read article"]):
        topnews()
      

    if there_exists(["wikipedia","search in wikipedia","get info wikipedia"]):
       
        try:
            speak("what do you want to look for in wikipedia Baby")
            voice = record_audio()
            summary=wikipedia.summary(voice)            
            speak(summary)
        except :
            speak('i dont have such as information')
    if there_exists(["whats my new email","read gmail","read email"]):
        emails=read_email_from_gmail()
        for email in emails:
            speak("the email number"+str(email))
            speak(""+str(emails[email]))

    if there_exists(['i love you ','do you love me','love me','do you love me']):
        speak("i love you honey more than anythings,could you kiss me baby  ")
    if there_exists(['send email']):
        try:
            speak(' what is the message')
            msg=record_audio()
            print(msg)
            speak('Who will recive this email')
            txt=record_audio()
            for key in my_dict:
                if key==txt:
                    print(txt)
                    receiver_email=my_dict[key]
            send_mail(receiver_email,msg)
            speak('Email has been send successfully')
        except Exception as e:
            print(e)
            speak('Email has not been sent due to some error')

    if there_exists(['can you']):
        li_commands = {
            "open websites": "Example: 'open youtube.com",
            "time": "Example: 'what time it is?'",
            "date": "Example: 'what date it is?'",
            "launch applications": "Example: 'launch chrome'",
            "tell me": "Example: 'tell me about India'",
            "weather": "Example: 'what weather/temperature in Mumbai?'",
            "news": "Example: 'news for today' ",
        }
        ans = """I can do lots of things, for example you can ask me time, date, weather in your city,
        I can open websites for you, launch application and more. See the list of commands-"""
        print(ans)
    
        speak(ans)
    if there_exists(['play music','music']):
        music="C:/Users/Asus/Desktop/semster/IOTPROJECT/songs"
        songs=os.listdir(music)
        speak('I will play your favorite song')
        os.startfile(os.path.join(music,songs[0]))
    if there_exists(['write','note book']):
        speak('what should i write down')
        note=record_audio()
        remember=open("data.txt","w")
        remember.write(note)
        remember.close
        speak('I have noted that')

time.sleep(1)
person_obj = person()
i=0
while(True):
    takeMedecine()
    voice_data = record_audio() # get the voice input
    respond(voice_data) # respond
    i+=1


