import time
import Keyboard
import KeyPlayback
import KeyHelper
import Song
import gui
from listeners import KeyRecord, OctaveSetter

class App:
    
    def __init__(self):
        self.keys = [
            Keyboard.Key(20, Song.Note(Song.Position.D, Song.Octave.THREE)),
            Keyboard.Key(21, Song.Note(Song.Position.D_SHARP, Song.Octave.THREE)),
            Keyboard.Key(22, Song.Note(Song.Position.E, Song.Octave.THREE)),
            Keyboard.Key(23, Song.Note(Song.Position.F, Song.Octave.THREE)),
            Keyboard.Key(24, Song.Note(Song.Position.F_SHARP, Song.Octave.THREE)),
            Keyboard.Key(25, Song.Note(Song.Position.G, Song.Octave.THREE)),
            Keyboard.Key(26, Song.Note(Song.Position.G_SHARP, Song.Octave.THREE)),
            Keyboard.Key(27, Song.Note(Song.Position.A, Song.Octave.THREE)),
            Keyboard.Key(17, Song.Note(Song.Position.A_SHARP, Song.Octave.THREE)),
            Keyboard.Key(16, Song.Note(Song.Position.B, Song.Octave.THREE)),
            Keyboard.Key(13, Song.Note(Song.Position.C, Song.Octave.THREE)),
            Keyboard.Key(6, Song.Note(Song.Position.C_SHARP, Song.Octave.THREE)),
            Keyboard.Key(5, Song.Note(Song.Position.D2, Song.Octave.THREE))
        ]
        self.speakers = [
            Keyboard.Speaker(12),
            Keyboard.Speaker(18),
            Keyboard.Speaker(19)
        ]

        # Initialize components
        self.recorder = KeyRecord.KeyRecord(pin = 4)
        self.playback = KeyPlayback.KeyPlayback(self.speakers)

        # Initialize keyboard and add its listeners
        self.keyboard = Keyboard.Keyboard(self.keys, self.speakers)
        self.keyboard.addListener(OctaveSetter.OctaveSetter())
        self.keyboard.addListener(self.recorder, Keyboard.Listener.Order.LAST)
    
    def onSubmitEvent(self, mode, recordName, playbackName):
        self.recordName = recordName
        self.playbackName = playbackName
        
        if(mode == gui.Mode.FREEPLAY):
            self.keyboard.play()
        elif(mode == gui.Mode.RECORD):
            self.keyboard.play()
            self.recorder.record()
        elif(mode == gui.Mode.PLAYBACK):
            self.playback.play(Song.load(playbackName))
        elif(mode == gui.Mode.MUTE):
            self.keyboard.stop()
    
    def onStopEvent(self):
        self.recorder.stop()
        
        if self.recordName == "":
            self.recorder.getSong().save()
        else:
            self.recorder.getSong().save(self.recordName)
        
        # RESTART HERE
     
app = App()
gui.addListener(app)
gui.start()


        



