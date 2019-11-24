import Keyboard
import Song
import RPi.GPIO as GPIO

class KeyRecord(Keyboard.Listener):
    
    NO_PIN = -1

    def __init__(self, pin = NO_PIN, song = None):
        self.isRecording = False
        self.song = Song.Song() if song is None else song
        
        self.pin = pin
        if (self.pin != KeyRecord.NO_PIN):
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(pin, GPIO.OUT)

    def record(self):
        self.isRecording = True
        if(self.pin != KeyRecord.NO_PIN):
            GPIO.output(self.pin, GPIO.LOW)

    def stop(self):
        self.isRecording = False
        self.song.optimize()
        if(self.pin != KeyRecord.NO_PIN):
            GPIO.output(self.pin, GPIO.HIGH)
        
    def erase(self):
        self.song.notes.clear()

    def onPlayEvent(self, keyboardData):
        if(not self.isRecording):
            return
        self.song.addNotes([key.getNote() for key in keyboardData.pressedKeys], keyboardData.duration)
        
    def getSong(self):
        return self.song
