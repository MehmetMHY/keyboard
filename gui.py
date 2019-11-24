from tkinter import *
from enum import Enum
import tkinter as tk 
import os

bgColor = "white"
bgButton = "ghost white"

listeners = []

def hitButton():
	global currentMode
	currentMode = v.get()

def openREADME():
	os.system("xdg-open README.md")

def optionMenuValue(selection):
	global playSong
	playSong = str(selection)

def sendIt():
	for listener in listeners:
		listener.onSubmitEvent(
			{
				1: Mode.FREEPLAY,
				2: Mode.RECORD,
				3: Mode.PLAYBACK
			}[currentMode],
			str(entry.get()),
			str(playSong)
		)
	print(str(currentMode) + "/" + str(entry.get()) + "/" + str(playSong))

def addListener(listener):
	listeners.append(listener)

def delListener(listener):
	listeners.remove(listener)

def getDirNames():
	global musicFileNames
	cv = []

	for root, dirs, files in os.walk("."):
		for filename in files:
			cv.append(filename)

	fileType = ".song"
	for i in range(len(cv)):
		if(cv[i][-5:] == fileType):
			musicFileNames.append(cv[i])

class Mode(Enum): 
    FREEPLAY = 1,
    RECORD = 2,
    PLAYBACK = 3

root = Tk() 
v = IntVar()

imgicon = PhotoImage(file=os.path.join(sp, 'favicon.ico'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)

musicFileNames = []
currentMode = 0
playSong = ""

root.title('RaspPI Keyboard')
root.configure(background=bgColor)
root.resizable(width=False, height=False)
root.geometry("335x550")

photo = PhotoImage(file = r"GUI_Icon.png") 
Button(root, image = photo, highlightbackground=bgColor).pack(side = TOP) 

readmeLabel = Label(root, text='Learn More', bg='DarkGoldenrod2').pack(fill=tk.BOTH)
submit = tk.Button(root, text='README', bg=bgButton, width=25, command=openREADME, highlightbackground=bgColor).pack()

modeLabel = Label(root, text='Modes', bg='gold').pack(fill=tk.BOTH)

Radiobutton(root, text='Free-Play	', bg=bgColor, variable=v, value=1, command=hitButton, highlightbackground=bgColor).pack(anchor=W) 
Radiobutton(root, text='Record	', bg=bgColor, variable=v, value=2, command=hitButton, highlightbackground=bgColor).pack(anchor=W) 
Radiobutton(root, text='Play-Back	', bg=bgColor, variable=v, value=3, command=hitButton, highlightbackground=bgColor).pack(anchor=W)

modeTwoLabel = Label(root, text='Record Name', bg='lightblue').pack(fill=tk.BOTH)
entry = Entry(root)
entry.pack()

modeThreeLabel = Label(root, text='Play Song', bg='lightblue').pack(fill=tk.BOTH)

variable = StringVar(root)

getDirNames()

if(len(musicFileNames) == 0):
	musicFileNames.append("NA")

variable.set(musicFileNames[0])
w = OptionMenu(root, variable, *musicFileNames, command=optionMenuValue)
w.pack()
w.config(bg=bgButton, highlightbackground=bgColor)


modeThreeLabel = Label(root, text='Send It', bg='lightgreen').pack(fill=tk.BOTH)
submit = tk.Button(root, text='Submit', width=25, command=sendIt, highlightbackground=bgColor, bg=bgButton).pack()

leaveLabel = Label(root, text='Close', bg='red').pack(fill=tk.BOTH)
exit = tk.Button(root, text='Exit', width=25, command=root.destroy, highlightbackground=bgColor, bg=bgButton).pack() 

root.mainloop()
