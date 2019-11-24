
from tkinter import *
from enum import Enum
import tkinter as tk 
import os

root = Tk() 
v = IntVar()

musicFileNames = []
listeners = []
currentMode = 0
playSong = ""

def hitButton():
	global currentMode
	currentMode = v.get()

def openREADME():
	# TODO
	print("Open README file - PI ONLY - TODO")

def optionMenuValue(selection):
	global playSong
	playSong = str(selection)

class Mode(Enum): 
    FREEPLAY = 1,
    RECORD = 2,
    PLAYBACK = 3

def sendIt():
	for listener in listeners:
		listener.onSubmitEvent(
			# MODE (Perfer enums) (enum),
			# NAME (str),
			# SONG NAME (str)
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


root.title('RaspPI Keyboard') 
root.resizable(width=False, height=False)

root.geometry("335x575")

photo = PhotoImage(file = r"GUI_Icon.png") 
Button(root, text = 'Click Me !', image = photo).pack(side = TOP) 

readmeLabel = Label(root, text='Learn More', bg='DarkGoldenrod2').pack(fill=tk.BOTH)
submit = tk.Button(root, text='README', width=25, command=openREADME).pack()

modeLabel = Label(root, text='Modes', bg='gold').pack(fill=tk.BOTH)

Radiobutton(root, text='Free-Play', variable=v, value=1, command=hitButton).pack(anchor=W) 
Radiobutton(root, text='Record', variable=v, value=2, command=hitButton).pack(anchor=W) 
Radiobutton(root, text='Play-Back', variable=v, value=3, command=hitButton).pack(anchor=W)

modeTwoLabel = Label(root, text='Record Name', bg='lightblue').pack(fill=tk.BOTH)
entry = Entry(root)
entry.pack()

modeThreeLabel = Label(root, text='Play Song', bg='lightblue').pack(fill=tk.BOTH)

variable = StringVar(root)

getDirNames()

if(len(musicFileNames) == 0):
	variable.set("NA")
	w = OptionMenu(root, variable, "NA", command=optionMenuValue).pack()
else:
	variable.set(musicFileNames[0])
	w = OptionMenu(root, variable, *musicFileNames, command=optionMenuValue).pack()

modeThreeLabel = Label(root, text='Send It', bg='lightgreen').pack(fill=tk.BOTH)
submit = tk.Button(root, text='Submit', width=25, command=sendIt).pack()

leaveLabel = Label(root, text='Close', bg='red').pack(fill=tk.BOTH)
exit = tk.Button(root, text='Exit', width=25, command=root.destroy).pack() 

root.mainloop()
