import os
import threading

import tkinter as tk
from tkinter import END

import pygame

eyed3

from static import *
from voice import recognize_speech

# Initialize Pygame and Tkinter
pygame.mixer.init()
root = tk.Tk()
root.title("Echo Tunes")

# Set window size and background color
root.geometry('720x480')
root.configure(bg='#7E84F7')

# Create title label
title_label = tk.Label(root, text="Echo Tunes", bg='#7E84F7', font=("Helvetica", 16))
title_label.place(x=0, y=10, width=720, height=50)

# Create frames for playlist and controls
playlist_frame = tk.Frame(root, bg='#7E84F7')
playlist_frame.place(x=60, y=85, width=590, height=225)

control_frame = tk.Frame(root, bg='#7E84F7')
control_frame.place(x=60, y=310, width=590, height=100)

# Create playlist listbox
playlist = tk.Listbox(playlist_frame, selectmode=tk.SINGLE, bg='#7E84F7')
playlist.pack(fill=tk.BOTH, expand=True)

# Create status label and volume control
status_label = tk.Label(root, text="Status: Idle", bg='#7E84F7')
status_label.place(x=0, y=460, width=720, height=20)

# Add songs to playlist
songs_dir = 'songs'  # replace with your songs directory
songs = os.listdir(songs_dir)
for song in songs:
    filename, extension = os.path.splitext(song)
    if extension == '.mp3':
        playlist.insert(END, filename)


# Define player control functions
def play_song():
    current_selection = playlist.curselection()
    if current_selection:  # if a song is selected
        song = playlist.get(current_selection[0])
    else:  # if no song is selected, default to the first song
        song = playlist.get(0)
    song_path = os.path.join(songs_dir, song + '.mp3')
    pygame.mixer.music.load(song_path)
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


# Create control buttons
prev_button = tk.Button(control_frame, text="Previous", command=previous_song, bg='#7E84F7')
prev_button.pack(side=tk.LEFT)

stop_button = tk.Button(control_frame, text="Stop", command=stop_song, bg='#7E84F7')
stop_button.pack(side=tk.LEFT)

play_button = tk.Button(control_frame, text="Play", command=play_song, bg='#7E84F7')
play_button.pack(side=tk.LEFT)

pause_button = tk.Button(control_frame, text="Pause", command=pause_song, bg='#7E84F7')
pause_button.pack(side=tk.LEFT)

next_button = tk.Button(control_frame, text="Next", command=next_song, bg='#7E84F7')
next_button.pack(side=tk.LEFT)

# Modify volume_scale to call set_volume when the scale is moved
volume_scale = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=set_volume,
                        bg='#7E84F7')
volume_scale.set(50)  # Set default volume to 50%
volume_scale.pack(side=tk.RIGHT)


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
        if command in play_commands:
            play_song()
        elif command in stop_commands:
            pause_song()
        elif command in next_song_commands:
            next_song()
        elif command in previous_song_commands:
            previous_song()
        elif command in stop_commands:
            stop_song()
        elif command in volume_up_commands:
            current_volume = volume_scale.get()
            new_volume = current_volume + 10 if current_volume + 10 < 100 else 100
            volume_scale.set(new_volume)
        elif command in volume_down_commands:
            current_volume = volume_scale.get()
            new_volume = current_volume - 10 if current_volume - 10 > 0 else 0
            volume_scale.set(new_volume)
        else:
            print("Command not recognized: " + command)


# Start voice command handler in a separate thread
voice_thread = threading.Thread(target=handle_voice_commands)
voice_thread.start()

# Run the main loop
root.mainloop()
