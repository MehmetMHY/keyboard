from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
import pb

class Song:

    def __init__(self, song = None):
        self.notes = []
        self.durations = []
        self.sheetmusic = None
        
    def addNotes(self, notes, duration):
        self.notes.append(notes)
        self.durations.append(duration)

    def save(self, name):
        pb.runLilyPond(self.getSheetMusic(), name=name)

    def optimize(self):
        i = 0
        while(True):
            if(len(self.notes) >= i):
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
        
        self.__approximateDurations(accuracy)
        shortestDur = sys.maxint
        for i in range(len(self.durations)):
            self.durations[i] += -1*remainder if remainder < accuracy / 2 else remainder
        self.__approximateDurations(shortestDur)
        
        sheetmusic = ""
        for i in range(len(self.durations)):
            note = self.__generateNote(i)
            durations = self.__generateDurations(i)
            for dur in durations:
                sheetmusic += note + duration + " "
        return sheetmusic
            
    def __generateNote(self, i):
        if(type(self.notes[i]) is int):
            return self.notes[i].getName()
        returnVal = "<"
        for note in self.notes[i]:
            returnVal += note.getName() + " "
        returnVal += ">"
        return returnVal
    
    def __generateDurations(self, i):
        origVal = self.durations[i]
        durations = []
        while(self.durations[i] > 4):
            durations.append(4)
            self.durations[i] -= 4
        if(self.durations[i] == 3):
            durations.append(2)
            durations.append(1)
        else:
           durations.append(self.durations[i])
        self.durations[i] = origVal
        return durations
    
    def __approximateDurations(self, accuracy):
        for i in range(len(self.durations)):
            remainder = self.durations[i] % accuracy
            self.durations[i] += -1*remainder if remainder < accuracy / 2 else remainder

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
    
    def getName(self):
        return {
            Position.D: "d"
            Position.D_SHARP: "ds"
            Position.E: "e"
            Position.F: "f"
            Position.F_SHARP: "fs"
            Position.G: "g"
            Position.G_SHARP: "gs"
            Position.A: "a'"
            Position.A_SHARP: "as'"
            Position.B: "b'"
            Position.C: "c'"
            Position.C_SHARP: "cs'"
            Position.D2: "d'"
        }[self.getPosition]

    def getFrequency(self):
        val = self.octave.value*(2**(1/12))**self.position.value
        print(val)
        return val

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
    C = 3
    C_SHARP = 4
    D2 = 5

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
