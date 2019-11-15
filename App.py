import time
import Keyboard
import KeyPlayback
import KeyHelper
from listeners import KeyRecord
from listeners import OctaveSetter

# TODO add keys/speakers
# Set keys
keys = []
speakers = []

# Initialize components
recorder = KeyRecord.KeyRecord()
playback = KeyPlayback.KeyPlayback(speakers)
keyHelper = KeyHelper.KeyHelper(keys)

# Initialize keyboard and add its listeners
keyboard = Keyboard.Keyboard(keys, speakers)
keyboard.addListener(OctaveSetter.OctaveSetter())
keyboard.addListener(recorder, Keyboard.Listener.Order.LAST)

# Play and record keyboard
keyboard.play()
time.sleep(3)
recorder.record()
time.sleep(10)
recorder.stop()
time.sleep(2)
keyboard.stop()

# Playback recorded song
playback.play(recorder.getSong())

time.sleep(2)

# Play keyboard with key helper playing the recorded song
keyboard.play()
keyHelper.start(recorder.getSong())
keyboard.stop()

time.sleep(2)

# Display recorded song on sheet music
recorder.getSong().display()
