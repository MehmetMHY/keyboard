import RPi.GPIO as GPIO
import time
import pigpio
import threading
import time
from enum import Enum

# The keyboard class (the REAL meat and potatoes of this shi*)
class Keyboard:
    # Play thread class to allow for multi-threaded note playing
    class __PlayThread(threading.Thread):
        # Initialize with a reference of keyboard class using the playThread class
        def __init__(self, keyboard):
            threading.Thread.__init__(self)
            self.keyboard = keyboard

        # Run method that plays notes on a loop while keyboard is playing (overroad from threading.Thread)
        def run(self):
            # Calls start event
            keyboardData = self.keyboard.data
            for l in self.keyboard.listeners.copy():
                l.onStartEvent(keyboardData)

            # Loop while is playing, play
            while (self.keyboard.isPlaying):
                self.play()
                time.sleep(0.01)

            # Calls stop event
            for l in self.keyboard.listeners.copy():
                l.onStopEvent(keyboardData)

        # play notes
        def play(self):
            # Create copy of keyboard data to prevent asynchronous change threading issues
            keyboardData = self.keyboard.data
            keyboardData.pressedKeys.clear()

            # Loop through all keys in keyboard data and check which are pressed
            for key in keyboardData.keys:
                if (len(keyboardData.pressedKeys) >= len(keyboardData.speakers)):
                    break
                if(key.isPressed()):
                    keyboardData.pressedKeys.append(key)

            # Calls Play event
            for l in self.keyboard.listeners.copy():
                l.onPlayEvent(keyboardData)

            # Loop through all pressed keys and play corresponding frequency
            for i in range(len(keyboardData.pressedKeys)):
                self.keyboard.pig.hardwar_PWM(
                    keyboardData.speakers[i].getPin(),
                    keyboardData.pressedKeys[i].getFrequency(),
                    int(0.25e6)
                )

    # Keyboard data class
    class __Data:

        # Data class so all data will be used directly (no encapsulation)
        # Initialize data
        def __init__(self, keys, speakers):
            self.pressedKeys = []
            self.keys = keys
            self.speakers = speakers

    # Initialize keyboard class
    def __init__(self, keys, speakers):
        self.data = Keyboard.__Data(keys, speakers)

        self.isPlaying = False

        self.playThread = Keyboard.__PlayThread(self)
        self.pig = pigpio.pi(port = 8887)

        self.listeners = []

        self.__setup()

    def __setup(self):
        GPIO.setmode(GPIO.BCM)

    # Tell play thread to begin playing
    def play(self):
        self.isPlaying = True

        if (not self.playThread.isAlive()):
            self.playThread.start()

    # Tell play thread to STOP
    def stop(self):
        self.isPlaying = False

    # Add listener
    def addListener(self, listener):
        self.listeners.append(listener)

    # Delete listener
    def delListener(self, listener):
        self.listeners.remove(listener)

# Listener template class
class Listener:
    def onStartEvent(self, keyboardData):
        return

    def onPlayEvent(self, keyboardData):
        return

    def onStopEvent(self, keyboardData):
        return

# Notes enum
# Map of note and corresponding half-step movement
class Note(Enum):
    D = -7
    D_sharp = -6
    E = -5
    F = -4
    F_sharp = -3
    G = -2
    G_sharp = -1
    A = 0
    A_sharp = 1
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

# Key class
class Key:
    # Initialize key class with pin, note, and octave
    def __init(self, pin, note, octave):
        self.pin = pin
        self.octave = octave
        self.note = note

    # Set octave
    def setOctave(self, octave):
        self.octave = octave

    # Set note
    def setNote(self, note):
        self.note = note

    # Get frequency using fn = f0 * (a)^n
    #   fn = frequency
    #   a = 2^1/12
    #   n = half-step movement from a
    def getFrequency(self):
        return self.octave*(2**(1/12))**self.note

    # Check if key is pressed
    def isPressed(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        isPressed = GPIO.input(self.pin) == 1
        GPIO.clear(self.pin)
        return isPressed

# Speaker class
class Speaker:
    # Initialize with pin
    def __init__(self, pin):
        self.pin = pin

    # Get pin of speaker
    def getPin(self):
        return self.pin