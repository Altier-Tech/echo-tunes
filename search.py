songs_dict = {}


def add_song(title, index):
    songs_dict[index] = title


def search_songs(search_term):
    search_term = search_term.lower()

    search_term_words = search_term.split(" ")
    search_term_words = [word for word in search_term_words if word != "the"]
    search_term_words = [word for word in search_term_words if word != "play"]

    
