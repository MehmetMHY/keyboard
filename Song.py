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
                    if (rN.getOctave()["num"] < lowestOctave.getOctave()["num"]):
                        lowestOctave = rN
                continue
            if(note["num"].getOctave() < lowestOctave.getOctave()["num"]):
                lowestOctave = note
        return lowestNote

    def __generateCord(self, note, lowestOctave):

        if(type(note) is list):
            cord = "<"
            for rN in note:
                cord += rN.getPosition()["name"] + ("'" * (rN.getOctave()["num"] - lowestOctave.getOctave()["num"])) + " "
            cord += ">"
            return cord

        return note.getPosition()["name"] + ("'" * (note.getOctave()["num"] - lowestOctave.getOctave()["num"]))

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
        return self.octave["frequency"]*(2**(1/12))**self.position["halfsteps"]

# Notes enum
# Map of note and corresponding half-step movement
class Position(Enum):
    D = {
        "halfsteps": -7,
        "name": "d"
    }
    D_SHARP = {
        "halfsteps": -6,
        "name": "ds"
    }
    E = {
        "halfsteps": -5,
        "name": "e"
    }
    F = {
        "halfsteps": -4,
        "name": "f"
    }
    F_SHARP = {
        "halfsteps": -3,
        "name": "fs"
    }
    G = {
        "halfsteps": -2,
        "name": "g"
    }
    G_SHARP = {
        "halfsteps": -1,
        "name": "gs"
    }
    A = {
        "halfsteps": 0,
        "name": "a'"
    }
    A_SHARP = {
        "halfsteps": 1,
        "name": "as'"
    }
    B = {
        "halfsteps": 2,
        "name": "b'"
    }
    C = {
        "halfsteps": 3,
        "name": "c'"
    }
    C_SHARP = {
        "halfsteps": 4,
        "name": "cs'"
    }
    D2 = {
        "halfsteps": 5,
        "name": "d'"
    }

# Octaves enum
# Map of octave and corresponding A frequency
class Octave(Enum):
    ZERO = {
        "frequency": 27.50,
        "num": 0
    }
    ONE = {
        "frequency": 55.00,
        "num": 1
    }
    TWO = {
        "frequency": 110.00,
        "num": 2
    }
    THREE = {
        "frequency": 220.00,
        "num": 3
    }
    FOUR = {
        "frequency": 440.00,
        "num": 4
    }
    FIVE = {
        "frequency": 880.00,
        "num": 5
    }
    SIX = {
        "frequency": 1760.00,
        "num": 6
    }
    SEVEN = {
        "frequency": 3520.00,
        "num": 7
    }
    EIGHT = {
        "frequency": 7040.00,
        "num": 8
    }
