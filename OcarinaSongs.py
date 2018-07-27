PLAYBACK_START = 0xB781DC
PLAYBACK_LENGTH = 0xA0
ACTIVATION_START = 0xB78E5C
ACTIVATION_LENGTH = 0x09

ACTIVATION_TO_PLAYBACK_NOTE = {
    0: 0x02, # A
    1: 0x05, # Down
    2: 0x09, # Right
    3: 0x0B, # Left
    4: 0x0E, # Up
    0xFF: 0xFF, # Rest
}

import random

# checks if one list is a sublist of the other (in either direction)
# python is magic.....
def subsong(song1, song2):
    # convert both lists to strings
    s1 = ''.join( map(chr, song1.activation))
    s2 = ''.join( map(chr, song2.activation))
    # check if either is a substring of the other
    return (s1 in s2) or (s2 in s1)

# give random durations and volumes to the notes
def fast_playback(activation):
    playback = []
    for note_index, note in enumerate(activation):
        playback.append( {'note': note, 'duration': 0x03, 'volume': 0x57} )
    return playback

# give random durations and volumes to the notes
def random_playback(activation):
    playback = []
    for note_index, note in enumerate(activation):
        duration = random.randint(0x8, 0x20)
        # make final note longer on average
        if( note_index + 1 >= len(activation) ):
            duration = random.randint(0x10, 0x30)
        volume = random.randint(0x40, 0x60)
        playback.append( {'note': note, 'duration': duration, 'volume': volume} )
        # randomly rest
        if( random.random() < 0.1 ):
            duration = random.randint(0x8, 0x18)
            playback.append( {'note': 0xFF, 'duration': duration, 'volume': 0} )
    return playback

# gives random volume and duration to the notes of piece
def random_piece_playback(piece):
    playback = []
    for note in piece:
        duration = random.randint(0x8, 0x20)
        volume = random.randint(0x40, 0x60)
        playback.append( {'note': note, 'duration': duration, 'volume': volume} )
    return playback

# takes the volume/duration of playback, and notes of piece, and creates a playback piece
# assumes the lists are the same length
def copy_playback_info(playback, piece):
    return [ { 'note': n, 'volume': p['volume'], 'duration': p['duration']} for (p, n) in zip(playback, piece) ]

def identity(x):
    return x

def random_piece(count, allowed=range(0,5)):
    return random.choices(allowed, k=count)

def invert_piece(piece):
    return [4 - note for note in piece]

def reverse_piece(piece):
    return piece[::-1]

def clamp(val, low, high):
    return max(low, min(high, val))

def transpose_piece(amount):
    def transpose(piece):
        return [clamp(note + amount, 0, 4) for note in piece]
    return transpose

def compose(f, g):
    return lambda x: f(g(x))

def add_transform_to_piece(piece, transform):
    return piece + transform(piece)

def repeat(piece):
    return 2 * piece

# a Song contains it's simple note data, as well as the data to be stored into the rom
class Song():

    def increase_duration_to(self, duration):
        if self.total_duration >= duration:
            return

        duration_needed = duration - self.total_duration
        last_note_duration = self.playback[-1]['duration']
        last_note_adds = 0x7F - last_note_duration

        if last_note_adds >= duration_needed:
            self.playback[-1]['duration'] += duration_needed
            self.format_playback_data()
            return
        else:
            self.playback[-1]['duration'] = 0x7F
            duration_needed -= last_note_adds
        while duration_needed >= 0x7F:
            self.playback.append( {'note': 0xFF, 'duration': 0x7F, 'volume': 0} )
            duration_needed -= 0x7F
        self.playback.append( {'note': 0xFF, 'duration': duration_needed, 'volume': 0} )
        self.format_playback_data()


    def two_piece_playback(self, piece, extra_position='none', activation_transform=identity, playback_transform=identity):
        piece_length = len(piece)
        piece2 = activation_transform( piece )
        # add playback parameters
        playback_piece1 = random_piece_playback(piece)
        playback_piece2 = copy_playback_info(playback_transform(playback_piece1), piece2)
        if extra_position == 'none':
            self.length = 2 * piece_length
            self.activation = piece + piece2
            # add a rest between
            duration = random.randint(0x8, 0x18)
            rest = {'note': 0xFF, 'duration': duration, 'volume': 0}
            self.playback = playback_piece1 + [rest] + playback_piece2
        else:
            self.length = 2 * piece_length + 1
            extra = random_piece(1)
            extra_playback = random_piece_playback(extra)
            if extra_position == 'start':
                self.activation = extra + piece + piece2
                self.playback = extra_playback + playback_piece1 + playback_piece2
            elif extra_position == 'middle':
                self.activation = piece + extra + piece2
                self.playback = playback_piece1 + extra_playback + playback_piece2
            elif extra_position == 'end':
                self.activation = piece + piece2 + extra
                self.playback = playback_piece1 + playback_piece2 + extra_playback

    # add rests between repeated notes in the playback so that they work in-game
    def break_repeated_notes(self, duration=0x08):
        new_playback = []
        for note_index, note in enumerate(self.playback):
            new_playback.append(note)
            if ( note_index + 1 < len(self.playback) ) and \
               ( self.playback[note_index]['note'] == self.playback[note_index + 1]['note'] ):
                new_playback.append( {'note': 0xFF, 'duration': duration, 'volume': 0} )
        self.playback = new_playback

    # create the list of bytes that will be written into the rom for the activation
    def format_activation_data(self):
        # data is 1 byte for the song length,
        # len bytes for the song, and the remainder is padding
        padding = [0] * (ACTIVATION_LENGTH - (self.length + 1))
        self.activation_data = [self.length] + self.activation + padding

    # create the list of byte that will  be written in to the rom for the playback
    def format_playback_data(self):
        self.playback_data = []

        self.total_duration = 0
        for note in self.playback:
            pitch = ACTIVATION_TO_PLAYBACK_NOTE[ note['note'] ]
            self.playback_data += [pitch, 0, 0, note['duration'], note['volume'], 0, 0, 0]
            self.total_duration += note['duration']
        # add a rest at the end
        self.playback_data += [0xFF, 0, 0, 0, 0x5A, 0, 0, 0]
        # pad the rest of the song
        padding = [0] * (PLAYBACK_LENGTH - len(self.playback_data))
        self.playback_data += padding

    def display(self):
        activation_string = 'Activation Data:\n\t' + ' '.join( map( "{:02x}".format, self.activation_data) )
        # break playback into groups of 8...
        index = 0
        broken_up_playback = []
        while index < len(self.playback_data):
            broken_up_playback.append( self.playback_data[index:index + 8])
            index += 8
        playback_string = 'Playback Data:\n\t' + '\n\t'.join( map( lambda line: ' '.join( map( "{:02x}".format, line) ), broken_up_playback ) )
        return activation_string + '\n' + playback_string

    # create a song, based on a given scheme
    def __init__(self, rand_song=True, piece_size=3, extra_position='none', starting_range=range(0,5), activation_transform=identity, playback_transform=identity, activation=None):
        if activation:
            self.length = len(activation)
            self.activation = activation
            self.playback = fast_playback(self.activation)
            self.break_repeated_notes(0x03)
            self.format_playback_data()
            self.increase_duration_to(45)
            return

        if rand_song:
            self.length = random.randint(4, 8)
            self.activation = random.choices(range(0,5), k=self.length)
            self.playback = random_playback(self.activation)
        else:
            if extra_position != 'none':
                piece_size = 3
            piece = random_piece(piece_size, starting_range)
            self.two_piece_playback(piece, extra_position, activation_transform, playback_transform)

        self.break_repeated_notes()
        self.format_activation_data()
        self.format_playback_data()

    __str__ = __repr__ = display

# randomly choose song parameters
def get_random_song():

    rand_song = random.choices([True, False], [1, 9])[0]
    piece_size = random.choices([3, 4], [5, 2])[0]
    extra_position = random.choices(['none', 'start', 'middle', 'end'], [12, 1, 1, 1])[0]
    activation_transform = identity
    playback_transform = identity
    weight_damage = 0
    should_transpose = random.choices([True, False], [1, 4])[0]
    starting_range=range(0,5)
    if should_transpose:
        weight_damage = 2
        direction = random.choices(['up', 'down'], [1, 1])[0]
        if direction == 'up':
            starting_range=range(0,4)
            activation_transform = transpose_piece(1)
        elif direction == 'down':
            starting_range=range(1,5)
            activation_transform = transpose_piece(-1)
    should_invert = random.choices([True, False], [3 - weight_damage, 6])[0]
    if should_invert:
        weight_damage += 1
        activation_transform = compose(invert_piece, activation_transform)
    should_reflect = random.choices([True, False], [5 - weight_damage, 4])[0]
    if should_reflect:
        activation_transform = compose(reverse_piece, activation_transform)
        playback_transform = reverse_piece


    # print([rand_song, piece_size, extra_position, starting_range, should_transpose, should_invert, should_reflect])

    song = Song(rand_song, piece_size, extra_position, starting_range, activation_transform, playback_transform)

    # rate its difficulty
    difficulty = 0
    difficulty = piece_size * 12
    if extra_position != 'none':
        difficulty += 12
    if should_transpose:
        difficulty += 25
    if should_reflect:
        difficulty += 10
    if should_invert:
        difficulty += 20
    if rand_song:
        difficulty = 11 * len(song.activation)

    song.difficulty = difficulty
    return song


# create a list of 12 songs, none of which are sub-strings of any other song
def generate_song_list(scarecrow_song=None):
    songs = []

    for _ in range(12):
        while True:
            # generate a completely random song
            song = get_random_song()
            # test the song against all existing songs
            is_good = True

            for other_song in songs + [scarecrow_song] if scarecrow_song else songs:
                if subsong(song, other_song):
                    is_good = False
            if is_good:
                songs.append(song)
                break

    # sort the songs by length
    songs.sort(key=lambda s: s.difficulty)
    return songs



# replace the playback and activation requirements for the ocarina songs
def replace_songs(rom, scarecrow_song=None):
    songs = generate_song_list(scarecrow_song)

    #print('\n\n'.join(map(str, songs)))

    song_order = [
        8, # zelda's lullaby
        6, # saria's song
        7, # epona's song
        11, # song of storms
        10, # song of time
        9, # sun's song
        5, # prelude of light
        0, # minuet of forest
        1, # bolero of fire
        2, # serenade of water
        3, # requiem of spirit
        4, # nocturne of shadow
    ]

    for index, song in enumerate(songs):

        # fix the song of time
        if song_order[index] == 10:
            song.increase_duration_to(260)

        # write the song to the activation table
        cur_offset = ACTIVATION_START + song_order[index] * ACTIVATION_LENGTH
        rom.write_bytes(cur_offset, song.activation_data)

        # write the songs to the playback table
        song_offset = PLAYBACK_START + song_order[index] * PLAYBACK_LENGTH
        rom.write_bytes(song_offset, song.playback_data)