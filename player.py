import os
import threading

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Listbox

import pickle

import eyed3
import pygame

from search import add_song, search_song
from static import *
from voice import recognize_speech

eyed3.log.setLevel("ERROR")

playlists = []

# Initialize Pygame and Tkinter
pygame.mixer.init()
root = tk.Tk()
root.title("Echo Tunes")

# Set window size and background color
root.geometry('720x600')
root.configure(bg='#7E84F7')

# Create title label
title_label = tk.Label(root, text="Echo Tunes", bg='#7E84F7', font=("Helvetica", 16))
title_label.place(x=0, y=10, width=720, height=50)

# Create frames for playlist and controls
playlist_frame = tk.Frame(root, bg='#7E84F7')
playlist_frame.place(x=60, y=185, width=590, height=225)

playlist_control_frame = tk.Frame(root, bg='#7E84F7')
playlist_control_frame.place(x=60, y=145, width=590, height=40)

control_frame = tk.Frame(root, bg='#7E84F7')
control_frame.place(x=60, y=410, width=590, height=100)

# Create Treeview with four columns
columns = ('#1', '#2', '#3', '#4')
playlist = ttk.Treeview(playlist_frame, columns=columns, show='headings')
playlist.heading('#1', text='#')
playlist.heading('#2', text='Song')
playlist.heading('#3', text='Artist')
playlist.heading('#4', text='Album')
playlist.column('#1', width=40)
playlist.pack(fill=tk.BOTH, expand=True)

# Create status label and volume control
status_label = tk.Label(root, text="Status: Idle", bg='#7E84F7')
status_label.place(x=0, y=560, width=720, height=20)


# Function to update the songs list when a playlist is selected
def update_songs(evt):
    # Get the selected playlist
    selected_playlist = playlists[playlists_listbox.curselection()[0]]
    # Clear the songs list
    playlist.delete(*playlist.get_children())
    # Add songs from the selected playlist
    songs = os.listdir(selected_playlist)
    for i, song in enumerate(songs, start=1):
        filename, extension = os.path.splitext(song)
        if extension == '.mp3':
            try:
                audiofile = eyed3.load(os.path.join(selected_playlist, song))
                artist = audiofile.tag.artist
                album = audiofile.tag.album
                add_song(filename, i)
                playlist.insert('', 'end', values=(i, filename, artist, album))
            except Exception as e:
                print(f"Error loading file {song}: {e}")


# Function to add a playlist
def add_playlist():
    # Open a directory chooser dialog
    directory = filedialog.askdirectory()
    # Check if the selected directory is already in the playlists list
    if directory not in playlists:
        # Add the selected directory to the playlists list
        playlists.append(directory)
        # Update the playlists list box
        update_playlists()
    else:
        print("This directory is already in the playlists.")


def search_playlist(playlist_name):
    for i, playlist in enumerate(playlists, start=1):
        if playlist_name.lower() in os.path.basename(playlist).lower():
            return i - 1  # return the index of the playlist
    return None  # return None if no match is found


# Create a button for adding playlists
add_playlist_button = tk.Button(playlist_control_frame, text="Add Playlist", command=add_playlist, bg='#7E84F7')
add_playlist_button.pack(side=tk.LEFT)

# Create a list box for displaying playlists
playlists_listbox = Listbox(root, bg='white')
playlists_listbox.place(x=60, y=60, width=590, height=80)  # Adjusted height
playlists_listbox.bind('<<ListboxSelect>>', update_songs)

# Add songs to playlist
songs_dir = 'songs'  # replace with your songs directory
songs = os.listdir(songs_dir)
for i, song in enumerate(songs, start=0):
    filename, extension = os.path.splitext(song)
    if extension == '.mp3':
        try:
            audiofile = eyed3.load(os.path.join(songs_dir, song))
            artist = audiofile.tag.artist
            album = audiofile.tag.album
            add_song(filename, i)
            playlist.insert('', 'end', values=(i, filename, artist, album))
        except Exception as e:
            print(f"Error loading file {song}: {e}")

# Define player control functions
is_paused = False


def save_playlists():
    with open('playlists.pkl', 'wb') as f:
        pickle.dump(playlists, f)


def load_playlists():
    try:
        with open('playlists.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []


# Function to delete a playlist
def delete_playlist():
    # Check if a playlist is selected
    if playlists_listbox.curselection():
        # Get the selected playlist
        selected_playlist = playlists[playlists_listbox.curselection()[0]]
        # Remove the selected playlist from the playlists list
        playlists.remove(selected_playlist)
        # Update the playlists list box
        update_playlists()
    else:
        print("No playlist selected.")


# Create a button for deleting playlists
delete_playlist_button = tk.Button(playlist_control_frame, text="Delete Playlist", command=delete_playlist,
                                   bg='#7E84F7')
delete_playlist_button.pack(side=tk.LEFT)


# Function to update the playlists list box
def update_playlists():
    # Clear the list box
    playlists_listbox.delete(0, tk.END)
    # Add each playlist to the list box
    for i, playlist in enumerate(playlists, start=1):
        playlists_listbox.insert(tk.END, f"{i}. {os.path.basename(playlist)}")


# Load playlists at the start of the program
playlists = load_playlists()

# Update the playlists list box
update_playlists()


# Function to update the playlists list box
def update_playlists():
    # Clear the list box
    playlists_listbox.delete(0, tk.END)
    # Add each playlist to the list box
    for playlist in playlists:
        playlists_listbox.insert(tk.END, os.path.basename(playlist))


# Define player control functions
def play_song():
    global is_paused  # Add this line to access the global variable
    if is_paused:  # If the song is paused
        pygame.mixer.music.unpause()  # Unpause the song
        status_label.config(text="Status: Playing")
        is_paused = False  # Update the is_paused status
    else:
        current_selection = playlist.selection()
        if current_selection:  # if a song is selected
            song = playlist.item(current_selection[0])['values'][1]
        else:  # if no song is selected, default to the first song
            song = playlist.item(playlist.get_children()[0])['values'][1]
        # Get the selected playlist
        selected_playlist = playlists[playlists_listbox.curselection()[0]]
        song_path = os.path.join(selected_playlist, song + '.mp3')
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        status_label.config(text="Status: Playing")


def play_by_index(index):
    song = playlist.item(playlist.get_children()[index])['values'][1]
    song_path = os.path.join(songs_dir, song + '.mp3')
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    status_label.config(text="Status: Playing")


def next_song():
    current_selection = playlist.selection()
    if current_selection:  # if a song is selected
        current_index = playlist.get_children().index(current_selection[0])
    else:  # if no song is selected, default to the first song
        current_index = 0
    next_index = current_index + 1 if current_index + 1 < len(playlist.get_children()) else 0
    playlist.selection_set(playlist.get_children()[next_index])
    play_song()


def previous_song():
    current_selection = playlist.selection()
    if current_selection:  # if a song is selected
        current_index = playlist.get_children().index(current_selection[0])
    else:  # if no song is selected, default to the first song
        current_index = 0
    prev_index = current_index - 1 if current_index > 0 else len(playlist.get_children()) - 1
    playlist.selection_set(playlist.get_children()[prev_index])
    play_song()


def pause_song():
    global is_paused  # Add this line to access the global variable
    pygame.mixer.music.pause()
    status_label.config(text="Status: Paused")
    is_paused = True  # Update the is_paused status


def stop_song():
    pygame.mixer.music.stop()
    status_label.config(text="Status: Stopped")


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
    # Save playlists when the application is closed
    save_playlists()

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
        command = parse_voice_command()
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
        elif any(cmd in command for cmd in search_playlist_commands):
            playlist_name = command.split(" ", 2)[2]
            playlist_index = search_playlist(playlist_name)
            if playlist_index is not None:
                print("Found playlist ", playlist_index, ": ", playlist_name)
                playlists_listbox.selection_set(playlist_index)
                update_songs(None)
            else:
                print("Playlist not found: " + playlist_name)
        elif command.split(" ")[0] == "play" and command.split(" ")[1] == "song" and len(command.split(" ")) > 2:
            song_name = command.split(" ", 2)[2]
            song_index = search_song(command)
            if song_index is not None:
                print("Playing song ", i, ": ", song_name)
                play_by_index(song_index)
            else:
                print("Song not found: " + song_name)
        else:
            print("Command not recognized: " + command)


# Start voice command handler in a separate thread
voice_thread = threading.Thread(target=handle_voice_commands)
voice_thread.start()

# Run the main loop
root.mainloop()
