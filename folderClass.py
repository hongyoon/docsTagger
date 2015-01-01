# folderClass
import os 
import os.path
import glob
import ntpath
from PIL import Image, ImageTk, ExifTags
import vlc

class Folder(object):
	"""class for an Folder"""
	def __init__(self, dirPath):
		# dirPath = directory path;
		self.dirPath = dirPath

		# empty list of entries (obj)
		self.entries = []

		photoExtensions = ["/*.JPG", "/*.PNG", "/*.GIF","/*JPEG"]
		for extension in photoExtensions:
			# glob.glob function return list of paths of a chosen extension
			photoPaths = glob.glob(dirPath + extension)

			# for each image path, create a image obj., then append to images (list of obj.)
			for photoPath in photoPaths:
				self.entries.append(photo(photoPath))

		videoExtensions = ["/*.AVI", "/*.MOV","/*.MTS", "/*.MPEG", "/*.WMV"]
		for extension in videoExtensions:
			# glob.glob function return list of paths of a chosen extension
			videoPaths = glob.glob(dirPath + extension)

			# for each image path, create a image obj., then append to images (list of obj.)
			for videoPath in videoPaths:
				self.entries.append(video(videoPath))

	def renameEntries(self):
		for entry in self.entries:
			entry.rename()

	def printEntries(self):
		for entry in self.entries:
			entry.printEntry()

#photo class
class entry(object):
	def __init__(self, entryPath):
		dirPath, nameExtension = ntpath.split(entryPath)
		name, extension = os.path.splitext(nameExtension)
		self.entryPath = entryPath
		self.dirPath = dirPath
		self.name = name
		self.targetName = ""
		self.extension = extension

		self.date = ""
		self.event = ""
		self.eventSub = ""
		self.action = ""
		self.actors = ""
		self.comment1 = ""
		self.comment2 = ""
		self.comment3 = ""

	def rename(self):
		# if name and target name are diff., then rename the image
		if (self.targetName):
			newPath = self.dirPath + "\ "  + self.targetName + self.extension

			# check to see if a file with the same number exists in dirPath
			if os.path.isfile(newPath): 
				# if yes, add '_int' to differentiate each file 
				i = 0
				newPath = self.dirPath + "\ "  + self.targetName + '_' + str(i) + self.extension
				while os.path.isfile(newPath):
					i += 1
					newPath = self.dirPath + "\ "  + self.targetName + '_' + str(i) + self.extension
					self.targetName = self.targetName + '_' + str(i)
			
			#rename it
			os.rename(self.entryPath, newPath)
		
	def setTargetName(self,targetName):
		if targetName:
			self.targetName = targetName 
		else:
			pass

	def printEntry(self):
		print('directory path is ', self.dirPath)
		print('entry name is ', self.name)
		print('target name is ', self.targetName)
		print('extension is ', self.extension)
		print('type is ', self.type)

class photo(entry):
	def __init__(self,entryPath):
		#generate thumbnail
		super().__init__(entryPath)
		self.type = 'photo'
		thumbnail = Image.open(entryPath)

		#rotate thumbnail if vertical orientation
		#- Exif Tags are jpeg metadata format
		#- reference: http://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
		
		#search through exif to find an orientation tag
		try:

			for orientation in ExifTags.TAGS.keys() : 
				if ExifTags.TAGS[orientation]=='Orientation' : break 


			exif=dict(thumbnail._getexif().items())
			if   exif[orientation] == 3 : thumbnail=thumbnail.rotate(180, expand=True)
			elif exif[orientation] == 6 : thumbnail=thumbnail.rotate(270, expand=True)
			elif exif[orientation] == 8 : thumbnail=thumbnail.rotate(90, expand=True)
			
		except:
			pass
		else:
			pass

		#reduce size 
		maxSize = 960, 540  #maximum size
		thumbnail.thumbnail(maxSize, Image.ANTIALIAS)

		#assign attributes
		self.thumbnail = thumbnail

class video(entry):
	def __init__(self,entryPath):
		super().__init__(entryPath)
		self.type = 'video'
		self.vlcMedia = vlc.Instance().media_new(self.entryPath)