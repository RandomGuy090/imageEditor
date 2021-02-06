#!/bin/python


import tkinter as tk 
import os, sys, io


import vars
from application import Application


def show_help():
	print("""./imageEditor.py
		usage ./imageEditor.py {path to file} {path to save file}
			  ./imageEditor.py {path to file} (file will be replaced) if no image, will be created

		""")

if __name__ == "__main__": 

	if "-h" in sys.argv or "--help" in sys.argv:
		show_help()
		sys.exit(0)
	try:
		img = sys.argv[1]
	except:
		img = None

	try:
		imgSave = sys.argv[2]
	except:
		try:
			imgSave = sys.argv[1]
		except:
			imgSave = None


	root = tk.Tk()
	# root.resizable(False, False)
	
	#root.eval('tk::PlaceWindow . center')
	

	app = Application(img, master=root)
	app.imgSave = imgSave

	app.mainloop()


