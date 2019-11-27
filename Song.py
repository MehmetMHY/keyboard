from enum import Enum
from threading import Thread
import numpy as np
import pb
import sys
import os

# Load song file from SONGS folder
def load(fileName):
        if( not os.path.exists("SONGS")):
            raise IOError("File not found")
        
        file = np.load("SONGS/" + str(fileName))
        
        return Song(file[0], file[1])

class Song:

    # Initialize song object
    def __init__(self, notes = None, durations = None):
        self.notes = [] if notes is None else notes
        self.durations = [] if durations is None else durations
        self.sheetmusic = None

    # Add notes to song
    def addNotes(self, note, duration):
        self.notes.append(note)
        self.durations.append(duration)

    # Save song
    def save(self, name="song"):
        self.__saveSong__(name)
        self.__saveLily__(name)
        
    # Save song to npy file
    def __saveSong__(self, name):
        if( not os.path.exists("SONGS")):
            os.makedirs("SONGS")
        np.save("SONGS/" + name + ".npy", np.array([self.notes, self.durations]))

    # Save song as a lilypond file
    def __saveLily__(self, name):
        Thread(target = pb.runLilyPond, args = (self.getSheetMusic(), name)).start()

    # Optimize the song size
    def optimize(self):
        i = 0
        while(True):
            if(len(self.notes) <= i):
                break
            if(self.notes[i-1] != self.notes[i]):
                i += 1
                continue
            self.durations[i-1] += self.durations[i]
            del self.notes[i]
            del self.durations[i]

    # Get song notes
    def getNotes(self):
        return self.notes

    # Get song duration
    def getDurations(self):
        return self.durations

    # Get sheet music (as a string)
    def getSheetMusic(self, accuracy = 0.2):
        if(self.sheetmusic == None):
            self.updateSheetMusic(accuracy)
        return self.sheetmusic

    # Update sheet music
    def updateSheetMusic(self, accuracy = 0.2):
        self.sheetmusic = self.__generateSheetMusic__(accuracy)

    # Generate sheet music
    def __generateSheetMusic__(self, accuracy):
        self.optimize()

        durs = self.durations.copy()
        shortestDur = self.__approximate(durs, accuracy)
        for i in range(len(durs)):
            durs[i] = round(durs[i]/shortestDur)

        lowestOctave = self.__findLowestOctave__()

        sheetmusic = ""
        for i in range(len(durs)):
            note = self.__generateCord__(self.notes[i], lowestOctave)
            durations = self.__convertDuration__(durs[i])
            for dur in durations:
                sheetmusic += note + str(dur) + " "
                
        return sheetmusic

    def __findLowestOctave__(self):
        lowestOctave = Octave.EIGHT
        for note in self.notes:
            if (type(note) is list):
                for rN in note:
                    if (rN.getOctave().num < lowestOctave.num):
                        lowestOctave = rN.getOctave()
            elif(note.getOctave().num < lowestOctave.num):
                lowestOctave = note.getOctave()
        return lowestOctave

    def __generateCord__(self, note, lowestOctave):
        if(not (type(note) is list)):
            return note.getPosition().name + ("'" * (note.getOctave().num + 1 - lowestOctave.num))
        if(len(note) == 0):
            return "r"
        cord = "<"
        for rN in note:
            cord += rN.getPosition().name + ("'" * (rN.getOctave().num + 1 - lowestOctave.num)) + " "
        cord += ">"
        return cord

    # Convert time duration to note duration
    def __convertDuration__(self, time):
        durations = []

        while (time >= 4):
            durations.append(1)
            time -= 4

        for i in {
                3: [2, 4],
                2: [2],
                1: [4],
                0: []
        }[time]:
            durations.append(i)

        return durations

    def __approximate(self, vals, accuracy):
        i = 0
        shortestVal = sys.maxsize
        while (True):
            if (len(vals) <= i):
                break

            remainder = vals[i] % accuracy
            vals[i] += -1 * remainder if remainder < accuracy / 2 else accuracy - remainder

            if (vals[i] <= 0):
                del vals[i]
                continue

            if (vals[i] <= shortestVal and (self.notes[i] is not type(list) or len(self.notes[i]) > 0)):
                shortestVal = vals[i]

            i += 1
        return shortestVal


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
        return self.octave.frequency*(2**(1/12))**self.position.halfsteps
    
    def toString(self):
        return self.__str__()
    
    def __str__(self):
        return "[" + self.position.name + ", " + str(self.octave.num) + "]"

# Notes enum
# Map of note and corresponding half-step movement
class Position(Enum):
    
    D = -7, "d"
    D_SHARP = -6, "dis"
    E = -5, "e"
    F = -4, "f"
    F_SHARP = -3, "fis"
    G = -2, "g"
    G_SHARP = -1, "gis"
    A = 0, "a"
    A_SHARP = 1, "ais"
    B = 2, "b"
    C = 3, "c'"
    C_SHARP = 4, "cis'"
    D2 = 5, "d'"
    
    def __init__(self, halfsteps: int = None, name: str = None):
        self._halfsteps_ = halfsteps
        self._name_ = name
    
    @property
    def halfsteps(self):
        return self._halfsteps_
    
    @property
    def name(self):
        return self._name_

# Octaves enum
class Octave(Enum):
    
    ZERO = 27.50, 0
    ONE = 55.00, 1
    TWO = 110.00, 2
    THREE = 220.00, 3
    FOUR = 440.00, 4
    FIVE = 880.00, 5
    SIX = 1760.00, 6
    SEVEN = 3520.00, 7
    EIGHT = 7040.00, 8
    
    def __init__(self, frequency: int = None, num: int = None):
        self._frequency_ = frequency
        self._num_ = num
        
    @property
    def frequency(self):
        return self._frequency_
    
    @property
    def num(self):
        return self._num_
