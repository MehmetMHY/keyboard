from enum import Enum
import pb
import sys

class Song:

    def __init__(self, song = None):
        self.notes = []
        self.durations = []
        self.sheetmusic = None
        
    def addNotes(self, notes, duration):
        self.notes.append(notes)
        self.durations.append(duration)

    def save(self, name):
        pb.runLilyPond(self.getSheetMusic(), fileName=name)

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
            
    def getSheetMusic(self, accuracy = 0.2):
        if(self.sheetmusic == None):
            self.updateSheetMusic(accuracy)
        return self.sheetmusic
        
    def updateSheetMusic(self, accuracy = 0.2):
        self.sheetmusic = self.__generateSheetMusic(accuracy)
        
    def __generateSheetMusic(self, accuracy):
        self.optimize()

        durs = self.durations.copy()
        shortestDur = self.__approximate(durs, accuracy)
        for i in range(len(durs)):
            durs[i] = round(durs[i]/shortestDur)

        lowestOctave = self.__findLowestOctave()

        sheetmusic = ""
        for i in range(len(durs)):
            note = self.__generateCord(self.notes[i], lowestOctave)
            durations = self.__generateDurations(durs[i])
            for dur in durations:
                sheetmusic += note + dur + " "

        return sheetmusic

    def __findLowestOctave(self):
        lowestNote = Octave.EIGHT
        for note in self.notes:
            if (type(note) is list):
                for rN in note:
                    if (rN.getOctave().num < lowestOctave.getOctave().num):
                        lowestOctave = rN
                continue
            if(note.getOctave().num < lowestOctave.getOctave().num):
                lowestOctave = note
        return lowestNote

    def __generateCord(self, note, lowestOctave):

        if(type(note) is list):
            cord = "<"
            for rN in note:
                cord += rN.getPosition().name + ("'" * (rN.getOctave().num - lowestOctave.getOctave().num)) + " "
            cord += ">"
            return cord

        return note.getPosition().name + ("'" * (note.getOctave().num - lowestOctave.getOctave().num))

    def __generateDurations(self, time):
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
        shortestVal = sys.maxint
        while (True):
            if (len(vals) <= i):
                break

            remainder = vals[i] % accuracy
            vals[i] += -1 * remainder if remainder < accuracy / 2 else accuracy - remainder

            if (vals[i] <= 0):
                del vals[i]
                continue

            if (vals[i] <= shortestVal):
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

# Notes enum
# Map of note and corresponding half-step movement
class Position(Enum):
    
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj
    
    def __init__(self, halfsteps, name):
        self.halfsteps = halfsteps
        self.name = name
    
    D = -7, "d"
    D_SHARP = -6, "ds"
    E = -5, "e"
    F = -4, "f"
    F_SHARP = -3, "fs"
    G = -2, "g"
    G_SHARP = -1, "gs"
    A = 0, "a'"
    A_SHARP = 1, "as'"
    B = 2, "b'"
    C = 3, "c'"
    C_SHARP = 4, "cs'"
    D2 = 5, "d'"

# Octaves enum
# Map of octave and corresponding A frequency
class Octave(Enum):
    
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj
    
    def __init__(self, frequency, num):
        self.frequency = frequency
        self.num = num
    
    ZERO = 27.50, 0
    ONE = 55.00, 1
    TWO = 110.00, 2
    THREE = 220.00, 3
    FOUR = 440.00, 4
    FIVE = 880.00, 5
    SIX = 1760.00, 6
    SEVEN = 3520.00, 7
    EIGHT = 7040.00, 8
