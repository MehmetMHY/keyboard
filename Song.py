from enum import Enum
import matplotlib.pyplot as plt

#TODO add comments

class Song:

    def __init__(self, song = None):
        self.notes = [[], []] if song is None else song.notes

    def addNotes(self, notes, duration):
        absDuration = duration if len(self.notes) == 0 else self.notes[len(self.notes) - 1][1] + duration
        for note in notes:
            self.notes[0].append(note)
            self.notes[1].append(absDuration)

    #TODO optimize notes
    def optimize(self):
        
        for i in range(1, len(self.notes[1])):
            if(not (self.notes[1][i] == self.notes[1][i-1])):
                continue
            self

    #TODO finish adding display
    def display(self, name):
        plt.figure(figsize=(15, 5))

        # plt.plot(self.notes[1], self.notes[0], 'b')
        # plt.title("Song" if len(name) == 0 else name)

        plt.show()

    #TODO add ability to write to file
    def write(self, file):
        return


class Note:

    def __init__(self, position, octave):
        self.position = position
        self.octave = octave

    def setPosition(self, position):
        self.position = position

    def setOctave(self, octave):
        self.octave = octave

    def getPosition(self):
        return self.position

    def getOctave(self):
        return self.octave

    def getFrequency(self):
        return self.octave*(2**(1/12))**self.position

# Notes enum
# Map of note and corresponding half-step movement
class Position(Enum):
    D = -7
    D_SHARP = -6
    E = -5
    F = -4
    F_SHARP = -3
    G = -2
    G_SHARP = -1
    A = 0
    A_SHARP = 1
    B = 2

# Octaves enum
# Map of octave and corresponding A frequency
class Octave(Enum):
    ZERO = 27.50
    ONE = 55.00
    TWO = 110.00
    THREE = 220.00
    FOUR = 440.00
    FIVE = 880.00
    SIX = 1760.00
    SEVEN = 3520.00
    EIGHT = 7040.00
