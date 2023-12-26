import os
import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()


# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            return text.lower()
        except:
            return ""


# Function to launch script
def launch_script():
    os.system('python player.py')


# Main loop
while True:
    command = recognize_speech()
    if command == 'launch music player':
        launch_script()
