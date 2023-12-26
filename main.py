import os
import speech_recognition as sr


# Function to launch script
def launch_script():
    os.system('python player.py')


# Main loop
while True:
    command = recognize_speech()
    if command == 'launch music player':
        launch_script()
