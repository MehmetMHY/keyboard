import Keyboard
import adcUtil as adc
import Song

class OctaveSetter(Keyboard.Listener):

    def __init__(self, channel=0):
        self.channel = channel
        self.octave = self.getOctave()
        self.count = 0
        self.isOn = True

    def turnOn(self):
        self.isOn = True

    def turnOff(self):
        self.isOn = False

    def getOctave(self):
        return {
            0: Song.Octave.ZERO,
            1: Song.Octave.ONE,
            2: Song.Octave.TWO,
            3: Song.Octave.THREE,
            4: Song.Octave.FOUR,
            5: Song.Octave.FIVE,
            6: Song.Octave.SIX,
            7: Song.Octave.SEVEN,
            8: Song.Octave.EIGHT
        } [int(float(adc.readADC(self.channel)/3.3)*8.5)]

    def onPlayEvent(self, keyboardData):
        if (not self.isOn):
            return

        if(self.count % 10 == 0):
            self.octave = self.getOctave()
        self.count += 1

        for key in keyboardData.pressedKeys:
            note = key.getNote()
            note.setOctave(self.octave)
            key.setNote(note)
