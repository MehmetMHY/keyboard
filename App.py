import time
import Keyboard
import KeyPlayback
import KeyHelper
import Song
from listeners import KeyRecord
from listeners import OctaveSetter

# TODO add keys/speakers
# Set keys
keys = [
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
speakers = [
    Keyboard.Speaker(12),
    Keyboard.Speaker(18),
    Keyboard.Speaker(19)
]

# Initialize components
recorder = KeyRecord.KeyRecord()
playback = KeyPlayback.KeyPlayback(speakers)
# keyHelper = KeyHelper.KeyHelper(keys)

# Initialize keyboard and add its listeners
keyboard = Keyboard.Keyboard(keys, speakers)
keyboard.addListener(OctaveSetter.OctaveSetter())
keyboard.addListener(recorder, Keyboard.Listener.Order.LAST)

# Play and record keyboard
keyboard.play()
time.sleep(3)
recorder.record()
time.sleep(50)
recorder.stop()
time.sleep(2)
keyboard.stop()

# Playback recorded song
#playback.play(recorder.getSong())

#time.sleep(2)

# Play keyboard with key helper playing the recorded song
#keyboard.play()
#keyHelper.start(recorder.getSong())
#keyboard.stop()

#time.sleep(2)

# Display recorded song on sheet music
#recorder.getSong().display()
