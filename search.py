songs_dict = {}


def add_song(title, index):
    songs_dict[index] = title


def search_song(search_term):
    search_term = search_term.lower()

    search_term_words = search_term.split(" ")
    search_term_words = [word for word in search_term_words if word != "the"]
    search_term_words = [word for word in search_term_words if word != "song"]
    search_term_words = [word for word in search_term_words if word != "play"]

    for song in songs_dict.keys():
        song_words = song.split(" ")
        song_words = [word for word in song_words if word != "the"]

        if set(search_term_words).issubset(set(song_words)):
            return songs_dict[song]

    return None
