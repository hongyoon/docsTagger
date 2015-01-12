from folderClass import Folder, photo, video
from tkinter import *
from tkinter import ttk, filedialog
from random import randint
from gui import taggerFrame, getMenubar
import glob

# path = filedialog.askdirectory()
# print(path)

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