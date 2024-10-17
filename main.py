import speech_recognition as al
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import subprocess
import moviepy
from moviepy.editor import *
from tkinter.filedialog import *
from pytube import YouTube






numbers = {'dk': '+27661713535',
          } # a dictionary of contacts to send a message to through whatsApp
applications = {"microsoft edge" : "taskkill /f /im msedge.exe", 
                "chrome" : "taskkill /f /im chrome.exe",
                "notepad":"taskkill /f /im notepad.exe",
                "word":"taskkill /f /im WINWORD.EXE",
                "visual studio":"taskkill /f /im devenv.exe",
                "settings":"taskkill /f /im SystemSettings.exe",
                "file explorer":"taskkill /f /im explorer.exe",
                } # a dictionary of applications to close
application_open = {"calculator" : "calc.exe", 
                    "chrome":"C://Program Files//Google//Chrome//Application//chrome.exe",
                    "visual studio":"C://Program Files//Microsoft Visual Studio//2022//Community//Common7//IDE//devenv.exe",
                    "word":"C://Program Files//Microsoft Office//root//Office16//WINWORD.EXE","settings":"C://Windows//ImmersiveControlPanel//SystemSettings.exe",
                    "file explorer":"explorer.exe",
                   } # a dictionary of applications to open

listener = al.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command(): # a method that initiates listening for the bot
    command = ""
    try:
        with al.Microphone() as source:
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "alexa" in command:
                command = command.replace("alexa", "")
                print(command)
    except:
        pass
    return command

def Download(link, name): # a method of downloading a youtube video/audio from youtube
    youtubeObj = YouTube(link)
    youtubeObj = youtubeObj.streams.get_highest_resolution()
    try:
        video = youtubeObj.download()
    except:
        print("Error, could not download the video")
        pass
    print("yay!!, video successfully downloaded")
    talk("video downloaded successfully")
    talk("would you like to convert the downloaded video into an audio file")
    convert = take_command()
    if "yes" in convert:
        video = moviepy.editor.VideoFileClip(video)
        audio = video.audio
        audio.write_audiofile(name + ".mp3")
        print("Success!!!")
        talk("video converted successfuly")
    elif "no" in convert:
        talk("okay, enjoy your video. Anything else can i do for you")
        talk("what else can i do for you")
    else:
        talk("i am not really sure of what you want me to do, so i will leave it as it is")
        talk("what else can i do for you")

def shutdown(): # a method of shutting down
        tym = datetime.datetime.now().strftime("%I:%M %p")
        talk("i hope i helped")
        if tym > "12:00 PM" or tym < "06:00 PM":
            talk("bye, enjoy the rest of the day")
            print("shutting down")
        elif tym > "12:00 AM" or tym < "12:00 PM":
            talk("bye, enjoy the rest of the morning")
            print("shutting down")
        else:
            talk("bye, enjoy the rest of the evening")
            print("shutting down")
        


def run_alexa():
    command = take_command()
    x = 0
    tym = datetime.datetime.now().strftime("%I:%M %p")
    print(command)

#------------------------playing videos from YouTube--------------------------------
    if "play" in command:
        talk("would you like to type out the name of the video or use voice command")
        choice1 = take_command()
        if "type" in choice1:
            talk("you can enter the name of the video now")
            video = input("Enter the name of the video: ")
        else:
            talk("what is the name of the video you want me to play for you")
            video = take_command()
            print(video)
        talk("playing" + video)
        pywhatkit.playonyt(video)
        talk ("anything else i can do for you")

#----------------asking for the current time-----------------------------

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        print("the time is " + time)
        talk ("the current time is " + time)
        talk ("what else can i do for you")

#----------------searching--------------------------------

    elif "who is" in command:
        person = command.replace("who is","")
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
        talk("what else can i do for you")

#----------------searching--------------------------------

    elif "what is" in command:
        obj = command.replace("what is","")
        info = wikipedia.summary(obj, 1)
        print(info)
        talk(info)
        talk("what else can i do for you")

#------------------asking how the bot is doing-------------

    elif "how are you" in command:
        rsp = command.replace("how are you","")
        talk("i am good, how are you")
        rsp = take_command()
        if "good" in rsp:
            talk("that's great, i am so looking forward into assisting you today")
            talk("how can i help you")
        elif "not okay" in rsp:
            talk("sorry, i hope interacting with me will make you feel better")
            talk("what can i do for you")
        else:
            talk("i did'nt quite understand that, but i hope you are doing well")
            talk("how can i help you")
   

#------------------Google searching---------------------------------------
   
    elif "search" in command:
        talk("would you like to type what you want me to search or you will just use voice commands instead")
        choice2 = take_command()

        if "type" in choice2:
            talk("you can type now")
            search = input("search here: ")
            pywhatkit.search(search)
            talk("done")
            talk("anything else?")

        elif "voice command" in choice2:
            talk("say what you want me to search for you")
            search = take_command()
            print(search)
            pywhatkit.search(search)
            talk("done")
            talk("anything else")

        else:
            talk("sorry i don't understand what you just said")
            talk("anything else i can do for you")

   
   
#-----------------sending a WhatsApp message---------------------------------

    elif "send a message" in command:
        nmsg= command.replace("send a message","")
        talk("would you like to type the name of the person you want me to send the message to or you will just use a voice command")
        TorV = take_command()
        print(TorV)
        if "type" in TorV:
            talk("Enter the name of the person")
            name = input("Enter the name of the person: ").casefold()
            print(name)

        elif "voice command" in TorV:
            talk("who do you want to send the message to")
            name = take_command()
            print(name)
        else:
            talk("i did not hear you properly, but i assume you meant voice command")
            talk("so, who would you like to send the message to")
            name = take_command()
            print(name)

        if name not in numbers:
            talk("the name stated is currently not in my system")
            talk("anything else?")
        
        else:
            receiver = numbers[name]
            print(receiver)
            talk("would you like to type the message or use a voice command")
            choice = take_command()
            if "type" in choice:
                talk("you can type the message now")
                msg = input("Enter the message: ")
            elif "voice command" in choice:
                talk("what do you want to say to" + name)
                msg = take_command()
                print(msg)
            else:
                talk("i couldn't hear that properly so i assume you would like to use a voice command")
                talk("what do you want to say to" + name)
                msg = take_command()
                print(msg)

            talk("enter the hour of which you want to send the message")
            hrs = int(input("enter the hour"))
            talk ("enter the minutes")
            mnts =int(input("enter the minute(s)"))
            pywhatkit.sendwhatmsg(receiver,msg, hrs,mnts)
            talk("sending message to"+ name)
            talk("what else can i help you with")
  
  #----------------------Closing an application------------------------------------
    
    elif "close" in command:
        appc = command.replace("close", "")
        talk("which application do you want to close")
        app = take_command()
        if app not in applications:
            talk("unfortunately i do not have access to the app you want me to close")
            talk("anything else i can do for you?")
        else:
            talk("consider that done!")
            app_close = applications[app]
            talk("closing " + app)
            os.system(app_close)
            talk("anything else i can do for you?")
            
#----------------------opening an application-----------------------------

    elif "open" in command:
        open = command.replace("open","")
        talk("which application do want to open")
        app = take_command()
        print(app)
        if app not in application_open:
            talk("unfortunately i do not have access to the app you want me to open")
            talk("what else can i do for you")
        else:
            talk("consider that done!")
            app_open = application_open[app]
            print(app_open)
            talk("opening "+ app)
            subprocess.call(app_open)
            talk("what else can i do for you")

#----------------------converting a video file(mp4) to an audio file(mp3)------------------------------
        
    elif "convert" in command:
        convert = command.replace("convert", "")
        talk("select the video you want to convert")
        video = askopenfilename()
        video = moviepy.editor.VideoFileClip(video)
        audio = video.audio
        talk("enter the name of the song")
        name = input("what would you like name the audio file: ")
        audio.write_audiofile(name + ".mp3")
        print("video successfully converted")
        talk("video converted successfully, what else can i do for you")

#-----------------------downloding a video from YouTube-------------------------------------------------------

    elif "download" in command:
        talk("enter the name of the video that you want to download")
        name = input("enter the name of the video: ")
        talk("enter the URL of the video you want to download")
        link = input("Enter the last part of the URL after 'v=': ")
        if (len(link) == 43):
            vid_link = link
        elif (len(link) < 43):
            vid_link = "https://www.youtube.com/watch?v=" + link
        else:
            print("invalid url entered")
        Download(vid_link, name)

#------------------------if you don't say anything-----------------------------------------------

    elif command == "":
        x = 1
        talk("you did not say anything so i assume you are not around")
        talk("i am going to sleep now as i wait for you to return")
        print("shutting down")

#----------------------------shut down---------------------------------------------------------

    elif "shutdown" in command:
       x = 1
       shutdown()
    elif "bye" in command:
        x = 1
        shutdown()

#----------------------what alexa says if she didn't hear you properly-------------------
        
    else:
        talk("sorry, i did not understand that, try again")

    return x



talk("hy, i am casper, how can i help")



while run_alexa() != 1:
    run_alexa()

    


   
   
   
     