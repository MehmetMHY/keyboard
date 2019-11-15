import RPi.GPIO as GPIO
import time
import pigpio
import threading
import time
from enum import Enum


# Listener template class
class Listener:
    # Simple listener priority enum
    class Order(Enum):
        FIRST = 0
        NORMAL = 1
        LAST = 2

    def onStartEvent(self, keyboardData):
        return

    def onPlayEvent(self, keyboardData):
        return

    def onStopEvent(self, keyboardData):
        return


# The keyboard class (the REAL meat and potatoes of this shi*)
class Keyboard:
    # Play thread class to allow for multi-threaded note playing
    class __PlayThread(threading.Thread):
        # Initialize with a reference of keyboard class using the playThread class
        def __init__(self, keyboard, updateDuration):
            threading.Thread.__init__(self)
            self.keyboard = keyboard
            self.pause = updateDuration

        # Run method that plays notes on a loop while keyboard is playing (overroad from threading.Thread)
        def run(self):
            # Calls start event
            keyboardData = self.keyboard.data
            for oList in self.keyboard.listeners.copy():
                for l in oList:
                    l.onStartEvent(keyboardData)

            # Loop while is playing, play
            while (self.keyboard.isPlaying):
                self.play()
                time.sleep(self.pause)

            # Calls stop event
            for oList in self.keyboard.listeners.copy():
                for l in oList:
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
            for oList in self.keyboard.listeners.copy():
                for l in oList:
                    l.onPlayEvent(keyboardData)

            # Loop through all pressed keys and play corresponding frequency
            for i in range(len(keyboardData.pressedKeys)):
                self.keyboard.pig.hardware_PWM(
                    keyboardData.speakers[i].getPin(),
                    keyboardData.pressedKeys[i].getNote().getFrequency(),
                    int(0.25e6)
                )

    # Keyboard data class
    class __Data:

        # Data class so all data will be used directly (no encapsulation)
        # Initialize data
        def __init__(self, keys, speakers, duration):
            self.duration = duration
            self.keys = keys
            self.speakers = speakers

            self.pressedKeys = []

    # Initialize keyboard class
    def __init__(self, keys, speakers, updateDuration = 0.01):
        self.data = Keyboard.__Data(keys, speakers, updateDuration)

        self.isPlaying = False

        self.playThread = Keyboard.__PlayThread(self, updateDuration)
        self.pig = pigpio.pi(port = 8887)

        self.listeners = [[], [], []]

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
    def addListener(self, listener, order = Listener.Order.NORMAL):
        self.listeners[order.value].append(listener)

    # Delete listener
    def delListener(self, listener):
        for oL in self.listeners:
            if listener not in oL:
                continue
            oL.remove(listener)

# Key class
class Key:
    # Initialize key class with pin, note, and octave
    def __init(self, pin, note):
        self.pin = pin
        self.note = note

    # Set octave
    def setNote(self, note):
        self.note = note

    # Set note
    def getNote(self):
        return self.note

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