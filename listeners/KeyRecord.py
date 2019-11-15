import Keyboard
import Song

class KeyRecord(Keyboard.Listener):

    def __init__(self, song = None):
        self.isRecording = False
        self.song = Song.Song() if song is None else song

    def record(self):
        self.isRecording = True

    def stop(self):
        self.isRecording = False
        self.song.optimize()

    def erase(self):
        self.song.notes.clear()

    def onPlayEvent(self, keyboardData):
        if(not self.isRecording):
            return
        self.song.addNotes(keyboardData.pressedKeys, keyboardData.duration)
