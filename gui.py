from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from operator import truediv
from folderClass import Folder, photo, video
import math
import os
import vlc

def getMenubar(root):
	#de fine menubar
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="New")
	filemenu.add_command(label="Open Folder")
	filemenu.add_command(label="Save")
	filemenu.add_command(label="Save as ...")
	filemenu.add_command(label="Close")
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Undo")
	editmenu.add_separator()
	editmenu.add_command(label="Cut")
	editmenu.add_command(label="Copy")
	editmenu.add_command(label="Paste")
	editmenu.add_command(label="Delete")
	editmenu.add_command(label="Select All")
	menubar.add_cascade(label="Edit", menu=editmenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help Index")
	helpmenu.add_command(label="About...")
	menubar.add_cascade(label="Help", menu=helpmenu)

	return menubar

class taggerFrame(Frame):
	def __init__(self, master):
		#define a Frame object of tkinter
		Frame.__init__(self,master)

		#ask for a directory in a pop-up window
		self.dirPath = filedialog.askdirectory()

		#initialized Folder class
		self.Folder = Folder(self.dirPath)

		#change the tile
		master.title(self.dirPath)

		#reset focus to 'master'
		master.focus_force()

		#initial folder
		self.entryIndex = 0

		#tkinter setting
		self.grid(column=0, row=0, sticky=(N, W, E, S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		#generate widgets
		self.createWidgets()

		#display the first entry
		self.displayEntry(self.entryIndex)

		#disable 'previous' button
		self.previous_button.config(state='disabled')

		#set focus to date entry
		self.date_entry.focus_force()

	def createWidgets(self):
		#Define canvas display images
		entry_canvas = Canvas(self, width=800, height =500)
		entry_canvas.grid(column=1, row=1, rowspan = 18)
		self.entry_canvas = entry_canvas
		self.canvas_id = entry_canvas.winfo_id()

		#Declare string variable
		date_strVar = StringVar()
		event_strVar = StringVar()
		eventSub_strVar = StringVar()
		action_strVar = StringVar()
		actors_strVar = StringVar()
		comment1_strVar = StringVar()
		comment2_strVar = StringVar()
		comment3_strVar = StringVar()

		self.date_strVar = date_strVar
		self.event_strVar = event_strVar
		self.eventSub_strVar = eventSub_strVar
		self.action_strVar = action_strVar
		self.actors_strVar = actors_strVar
		self.comment1_strVar = comment1_strVar
		self.comment2_strVar = comment2_strVar
		self.comment3_strVar = comment3_strVar

		#Define Entry Fields
		date_entry = ttk.Entry(self, width=20, textvariable = date_strVar)
		event_entry = ttk.Entry(self, width=20, textvariable = event_strVar)
		eventSub_entry = ttk.Entry(self, width=20, textvariable = eventSub_strVar)
		action_entry = ttk.Entry(self, width=20, textvariable = action_strVar)
		actors_entry = ttk.Entry(self, width=20, textvariable = actors_strVar)
		comment1_entry = ttk.Entry(self, width=20, textvariable = comment1_strVar)
		comment2_entry = ttk.Entry(self, width=20, textvariable = comment2_strVar)
		comment3_entry = ttk.Entry(self, width=20, textvariable = comment3_strVar)

		self.date_entry = date_entry
		self.event_entry = event_entry
		self.eventSub_entry = eventSub_entry
		self.action_entry = action_entry
		self.actors_entry = actors_entry
		self.comment1_entry = comment1_entry
		self.comment2_entry = comment2_entry
		self.comment3_entry = comment3_entry

		#Define Entry Grids
		date_entry.grid(    column=2, columnspan=2, row=2,  sticky=(W, E))
		event_entry.grid(   column=2, columnspan=2, row=4,  sticky=(W, E))
		eventSub_entry.grid(column=2, columnspan=2, row=6,  sticky=(W, E))
		action_entry.grid(  column=2, columnspan=2, row=8,  sticky=(W, E))
		actors_entry.grid(  column=2, columnspan=2, row=10, sticky=(W, E))
		comment1_entry.grid(column=2, columnspan=2, row=12, sticky=(W, E))
		comment2_entry.grid(column=2, columnspan=2, row=14, sticky=(W, E))
		comment3_entry.grid(column=2, columnspan=2, row=16, sticky=(W, E))

		#Define Label
		ttk.Label(self, text="Date: #year_month_date (i.e., 2014_Nov_11)").grid(    column=2, columnspan=2, row=1,  sticky=(W, E))
		ttk.Label(self, text="Event name (i.e., undegraduateRetreat)").grid(   column=2, columnspan=2, row=3,  sticky=(W, E))
		ttk.Label(self, text="Event Section: day#_subsection (i.e., day1_sermon)" ).grid(column=2, columnspan=2, row=5,  sticky=(W, E))
		ttk.Label(self, text="Action: verb_adjective (i.e., pray_crazy)" ).grid(  column=2, columnspan=2, row=7,  sticky=(W, E))
		ttk.Label(self, text="Actors: group, LGname, people name" ).grid(  column=2, columnspan=2, row=9, sticky=(W, E))
		ttk.Label(self, text="Additional Comment 1 (i.e., moneyShot)" ).grid(column=2, columnspan=2, row=11, sticky=(W, E))
		ttk.Label(self, text="Additional Comment 2 (i.e., WaLauEh)").grid(column=2, columnspan=2, row=13, sticky=(W, E))
		ttk.Label(self, text="Additional Comment 3 (i.e., NoLah)").grid(column=2, columnspan=2, row=15, sticky=(W, E))

		#buttons
		self.previous_button = ttk.Button(self, text="previous", width=20, command = self.openPreviousEntry)
		self.previous_button.grid(row=18, column=2)
	
		self.next_button = ttk.Button(self, text="next", width=20, command=self.openNextEntry)
		self.next_button.grid(row=18, column=3)

		for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)
	
	def collectStrings(self):
		#input: -empty-
		#output: list of Strings
		#collect all string entries from user

		#assign in an attribute 'strings' to store user generated string val.
		entryObject = self.Folder.entries[self.entryIndex]
		entryObject.date = self.date_entry.get()
		entryObject.event = self.event_entry.get()
		entryObject.eventSub = self.eventSub_entry.get()
		entryObject.action = self.action_entry.get()
		entryObject.actors = self.actors_entry.get()
		entryObject.comment1 = self.comment1_entry.get()
		entryObject.comment2 = self.comment2_entry.get()
		entryObject.comment3 = self.comment3_entry.get()

		strings = [entryObject.date,entryObject.event,entryObject.eventSub,entryObject.action,entryObject.actors,entryObject.comment1,entryObject.comment2,entryObject.comment3]
		strings = [i for i in strings if i != '']
		return strings

	def concatenateStrings(self, strings):
		#input: a list of String
		#output: one string ('1String1_String2_ ...') 
		#concatenate a list of strings to one long string
		
		fileString = ""
		for i in range(len(strings)):
			if strings[i]:
				if i == (len(strings)-1):
					fileString = fileString + strings[i]
				else:
					fileString = fileString + strings[i] + '_'
		return fileString
		
	def makeTargetName(self):
		strings = self.collectStrings()
		targetName = self.concatenateStrings(strings)
		return targetName

	def openAnotherFolder(self):
		#ask for a directory in a pop-up window
		self.dirPath = filedialog.askdirectory()

		#initialized Folder class
		self.Folder = Folder(self.dirPath)

		#initial folder
		self.entryIndex = 0

		#display the first element
		self.displayEntry(self.entryIndex)

		#update the button
		self.updateButtons()

		#set focus to date entry
		self.date_entry.focus_force()

	def displayEntry(self, entryIndex):
		entryObject = self.Folder.entries[entryIndex]
		#update entry value

		#load previous date / event / eventSub if exists  
		currentStrs = [entryObject.date, entryObject.event, entryObject.eventSub]

		if entryIndex > 0:
			previousEntry = self.Folder.entries[entryIndex-1]
			previousStrs = [previousEntry.date, previousEntry.event, previousEntry.eventSub]

			for i in range(len(currentStrs)):
				if not currentStrs[i]:
					currentStrs[i] = previousStrs[i]

		self.date_strVar.set(currentStrs[0])
		self.event_strVar.set(currentStrs[1])
		self.eventSub_strVar.set(currentStrs[2])

		self.action_strVar.set(entryObject.action)
		self.actors_strVar.set(entryObject.actors)
		self.comment1_strVar.set(entryObject.comment1)
		self.comment2_strVar.set(entryObject.comment2)
		self.comment3_strVar.set(entryObject.comment3)

		#update photo / video canvas 
		if entryObject.type == 'photo':
			if 'vlcInstance' in self.__dict__:

				self.player.stop()
				self.vlcInstance.release()
				del self.vlcInstance

			global photo
			photo = ImageTk.PhotoImage(entryObject.thumbnail)
			item = self.entry_canvas.create_image(0,0, anchor=NW, image=photo)
			self.entry_canvas.itemconfigure(item, image=photo)

		elif entryObject.type == 'video':
			if not 'vlcInstance' in self.__dict__:

				#initialize vlc for video module
				self.vlcInstance = vlc.Instance()
				self.player = self.vlcInstance.media_player_new()
				self.player.set_hwnd(self.canvas_id)
			self.player.set_media(entryObject.vlcMedia)
			self.player.play()
		else :
			error('unknown type')

	def openNextEntry(self):
		#0 save target name
		entryObject = self.Folder.entries[self.entryIndex]
		targetName = self.makeTargetName()
		entryObject.setTargetName(targetName)

		if self.entryIndex < (len(self.Folder.entries)-1):
			#1 entriesIndex++
			self.entryIndex += 1

			#2 update the buttons
			self.updateButtons()

			#3 update String, Photo / Video
			self.displayEntry(self.entryIndex)

		#4 set focus to action field
		self.action_entry.focus_force()
		return

	def openPreviousEntry(self):

		#0 save target name
		entryObject = self.Folder.entries[self.entryIndex]
		targetName = self.makeTargetName()
		entryObject.setTargetName(targetName)

		if self.entryIndex > 0:
			#1 entriesIndex--
			self.entryIndex -= 1

			#2 update the buttons
			self.updateButtons()
			
			#3 update String, Photo / Video
			self.displayEntry(self.entryIndex)

		#4 set focus to action field
		self.action_entry.focus_force()
		return

	def renameFilesInFolder(self):
		if messagebox.askyesno("Are you sure?", "Do you want to rename files in folder?"):
			self.Folder.renameEntries()
			try:
				self.Folder.renameEntries()
				if messagebox.askyesno("Another Folder?", "Do you want to tag files in a new folder?"):
					self.openAnotherFolder()
				else:
					self.master.destroy()
			except:
				messagebox.showinfo("info", "oops something did not go well. send an email to 'hongyoon@umich.edu' to report an error")	
		else:
			self.focus_set()

	def updateLastEntryThenRename(self):
		#make a target name
		if 'vlcInstance' in self.__dict__:
			self.player.stop()
			self.vlcInstance.release()
			del self.vlcInstance
		targetName = self.makeTargetName()

		#assign in target name for the last entry
		entryObject = self.Folder.entries[self.entryIndex]
		entryObject.setTargetName(targetName)

		#rename all files in Folder
		self.renameFilesInFolder()

	def updateButtons(self):
		if self.entryIndex == 0:
			self.previous_button.config(text="first file!", state='disabled')
			self.next_button.config(text='next', command = self.openNextEntry)

		elif self.entryIndex == (len(self.Folder.entries)-1):
			self.previous_button.config(text='previous', state='normal')
			self.next_button.config(text="rename files", command=self.updateLastEntryThenRename)

		else:
			self.previous_button.config(text='previous', state='normal')
			self.next_button.config(text='next', state='normal', command=self.openNextEntry)