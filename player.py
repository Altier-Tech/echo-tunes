import os
import tkinter as tk
from tkinter import END
import pygame
import speech_recognition as sr
import threading

# Initialize speech recognizer
r = sr.Recognizer()

# Initialize Pygame and Tkinter
pygame.mixer.init()
root = tk.Tk()
root.title("Echo Tunes")

# Create frames for playlist and controls
playlist_frame = tk.Frame(root)
playlist_frame.pack(pady=20)

control_frame = tk.Frame(root)
control_frame.pack()

# Create playlist listbox
playlist = tk.Listbox(playlist_frame, selectmode=tk.SINGLE)
playlist.pack(fill=tk.BOTH, expand=True)

# Add songs to playlist
songs_dir = 'songs'  # replace with your songs directory
songs = os.listdir(songs_dir)
for song in songs:
    filename, extension = os.path.splitext(song)
    if extension == '.mp3':
        song_path = os.path.join(songs_dir, song)
        playlist.insert(END, song_path)


# Define player control functions
def play_song():
    current_selection = playlist.curselection()
    if current_selection:  # if a song is selected
        song = playlist.get(current_selection[0])
    else:  # if no song is selected, default to the first song
        song = playlist.get(0)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    status_label.config(text="Status: Playing")


def pause_song():
    pygame.mixer.music.pause()
    status_label.config(text="Status: Paused")


def stop_song():
    pygame.mixer.music.stop()
    status_label.config(text="Status: Stopped")


def next_song():
    current_selection = playlist.curselection()
    if current_selection:  # if a song is selected
        current_index = current_selection[0]
    else:  # if no song is selected, default to the first song
        current_index = 0
    next_index = current_index + 1 if current_index + 1 < playlist.size() else 0
    playlist.select_clear(current_index)
    playlist.select_set(next_index)
    play_song()


def previous_song():
    current_selection = playlist.curselection()
    if current_selection:  # if a song is selected
        current_index = current_selection[0]
    else:  # if no song is selected, default to the first song
        current_index = 0
    prev_index = current_index - 1 if current_index > 0 else playlist.size() - 1
    playlist.select_clear(current_index)
    playlist.select_set(prev_index)
    play_song()


# Define volume control function
def set_volume(val):
    volume = int(val) / 100  # we need to normalize our value to be between 0 and 1
    pygame.mixer.music.set_volume(volume)


# Modify volume_scale to call set_volume when the scale is moved
volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=set_volume)
volume_scale.set(50)  # Set default volume to 50%
volume_scale.pack()

# Create control buttons
play_button = tk.Button(control_frame, text="Play", command=play_song)
play_button.pack(side=tk.LEFT)

pause_button = tk.Button(control_frame, text="Pause", command=pause_song)
pause_button.pack(side=tk.LEFT)

stop_button = tk.Button(control_frame, text="Stop", command=stop_song)
stop_button.pack(side=tk.LEFT)

next_button = tk.Button(control_frame, text="Next", command=next_song)
next_button.pack(side=tk.LEFT)

prev_button = tk.Button(control_frame, text="Previous", command=previous_song)
prev_button.pack(side=tk.LEFT)

# Create status label and volume control
status_label = tk.Label(root, text="Status: Idle")
status_label.pack()


# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text.lower()
        except:
            return ""


def on_exit():
    # Stop the song if it's playing
    pygame.mixer.music.stop()

    # Stop the voice command listening thread
    if voice_thread.is_alive():
        # Set a flag that will cause the thread to exit
        # Note: You'll need to check this flag in your `handle_voice_commands` function
        global exit_flag
        exit_flag = True

    # Destroy the tkinter window
    root.destroy()

    # Force terminate the Python script
    os._exit(0)


# Set the flag to False initially
exit_flag = False

# Bind the exit function to the window close button
root.protocol("WM_DELETE_WINDOW", on_exit)


# Function to handle voice commands
def handle_voice_commands():
    while True:
        if exit_flag:
            break
        command = recognize_speech()
        if command == 'play song':
            play_song()
        elif command == 'pause song':
            pause_song()
        elif command == 'next song':
            next_song()
        elif command == 'previous song':
            previous_song()


# Start voice command handler in a separate thread
voice_thread = threading.Thread(target=handle_voice_commands)
voice_thread.start()

# Run the main loop
root.mainloop()
