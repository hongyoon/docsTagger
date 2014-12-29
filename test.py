from folderClass import Folder, photo, video
from tkinter import *
from tkinter import ttk, filedialog
from random import randint
from gui import taggerFrame, getMenubar

# path = filedialog.askdirectory()
# print(path)

path = 'C:/Users/hongyoon/Desktop/DOCS/imageTagger/'


def runTagger():
	#Declare empty GUI
	root = Tk()
	#Define Title
	root.title("Tagger")
	#Define Menubar
	root.config(menu=getMenubar(root))
	#Define Mainframe
	taggerFrame(root)
	#lunch GUI
	root.mainloop()

runTagger()