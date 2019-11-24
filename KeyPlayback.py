import Keyboard
import time
import pigpio

class KeyPlayback(Keyboard.Listener):

    def __init__(self, speakers):
        self.speakers = speakers
        self.pig = pigpio.pi(port = 8887)
    
    def play(self, song):
        notes = song.getNotes().copy()
        durs = song.getDurations().copy()
        for i in range(len(notes)):
            for speaker in self.speakers:
                self.pig.hardware_PWM(speaker.getPin(), 0, 0)
            if (not (type(notes[i]) is list)):
                self.pig.hardware_PWM(
                    self.speakers[0].getPin(),
                    int(notes[i].getFrequency()),
                    int(0.25e6)
                )
            else:
                for j in range(len(notes[i])):
                    self.pig.hardware_PWM(
                        self.speakers[int(j/Keyboard.Speaker.NOTES_PER_SPEAKER)%len(self.speakers)].getPin(),
                        int(notes[i][j].getFrequency()),
                        int(0.25e6)
                    )
            time.sleep(durs[i])
        
        for speaker in self.speakers:
                self.pig.hardware_PWM(speaker.getPin(), 0, 0)
                

