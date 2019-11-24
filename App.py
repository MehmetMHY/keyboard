



# Play and record keyboard
keyboard.play()
recorder.record()
time.sleep(3)
recorder.stop()
keyboard.stop()

# Display recorded song on sheet music
recorder.getSong().save(name = "test")

# Playback recorded song
playback.play(Song.load("test"))