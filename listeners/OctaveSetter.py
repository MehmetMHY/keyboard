import Keyboard
import adcUtil as adc
import Song

class OctaveSetter(Keyboard.Listener):

    def __init__(self, channel=0):
        self.channel = channel
        self.octave = self.__calcOctave()
        self.count = 0
        self.isOn = True

    def turnOn(self):
        self.isOn = True

    def turnOff(self):
        self.isOn = False

    def __calcOctave(self):
        numOct = int(float(adc.readADC(self.channel)/3.3)*8.5)
        for octave in Song.Octave:
            if(numOct == octave.num):
                return octave
        return None

    def onPlayEvent(self, keyboardData):
        if (not self.isOn):
            return

        if(self.count % 10 == 0):
            self.octave = self.__calcOctave()
        self.count += 1

        for key in keyboardData.pressedKeys:
            note = key.getNote()
            note.setOctave(self.octave)
            key.setNote(note)
