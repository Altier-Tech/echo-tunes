import os
import tkinter as tk
from tkinter import END
import pygame

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
    global current_song
    song = playlist.get(tk.ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    status_label.config(text="Status: Playing")


def pause_song():
    pygame.mixer.music.pause()
    status_label.config(text="Status: Paused")


def stop_song():
    pygame.mixer.music.stop()
    status_label.config(text="Status: Stopped")


# Create control buttons
play_button = tk.Button(control_frame, text="Play", command=play_song)
play_button.pack(side=tk.LEFT)

pause_button = tk.Button(control_frame, text="Pause", command=pause_song)
pause_button.pack(side=tk.LEFT)

stop_button = tk.Button(control_frame, text="Stop", command=stop_song)
stop_button.pack(side=tk.LEFT)

# Create status label and volume control
status_label = tk.Label(root, text="Status: Idle")
status_label.pack()

volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume")
volume_scale.set(50)  # Set default volume to 50%
volume_scale.pack()

# Run the main loop
root.mainloop()
