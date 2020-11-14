#!/bin/python


from PIL import ImageTk,Image
import tkinter as tk 
from tkinter import colorchooser
import os, sys, io
import pyautogui
	



class Application(tk.Frame):
	def __init__(self, image, master=None ):
		super().__init__(master)
		self.master = master
		self.imagePath = image

		image = Image.open(img)
	
		self.canvas_config()
		self.master.width = self.width
		self.master.height = self.height

		sidebar = Sidebar(self.master, self.canvas)
		self.keybinds()


	def canvas_config(self):
		self.convert_image(img)
		self.window_config()

		self.keyDraw = False
		self.canvas.keyOverlay = False
		self.canvas.lineWidth = 1
		self.canvas.lineColor = "#ff0000"
		self.canvas.lastMoves = list()
		self.canvas.undoList = []

	def window_config(self):
		self.master.geometry(f"{self.width}x{self.height+22}")
		self.master.title("imageEditor")
		#self.master.resizable(False, False)
		#frameless window
		#self.master.overrideredirect(True) 
	  

	def keybinds(self):
		#when mouse button pressed		
		self.canvas.bind('<ButtonPress-1>', self.key_pressed)
		#when mouse button released
		self.canvas.bind('<ButtonRelease-1>', self.key_released)
		#delete all when backspace
		#self.master.bind('<BackSpace>', self.clear_all)
		self.master.bind('<Control-z>', self.undo)
		#when want to save CTRL+S
		self.master.bind('<Control-s>', self.save_img)
		self.master.bind('<space>', self.save_img)
		#when want to escape
		self.master.bind('<Escape>', self.close)
		self.master.bind('<Key-q>', self.close)
		self.master.bind('<Control-c>', self.close)
		#make brush bigger
		self.master.bind('<Key-plus>', self.bigger_brush)
		self.master.bind('<Key-equal>', self.bigger_brush)
		#make brush smaller
		self.master.bind('<Key-minus>', self.smaller_brush)



	
	def convert_image(self, img):
		self.bgImage = ImageTk.PhotoImage(Image.open(img), master=self.master)
		self.get_sizes()
		self.set_bg_image()	
		#self.window_config()
		self.pack(padx=0, pady=0)



	def get_sizes(self):
		self.height = self.bgImage.height()
		self.width = self.bgImage.width()
		


	def set_bg_image(self):

		self.canvas = tk.Canvas(root, width=self.width, heigh=self.height)
		self.canvas.create_image(0,0,anchor="nw", image=self.bgImage)

		self.canvas.pack()

	def key_pressed(self, event):
		x, y = event.x, event.y 
		Draw(self.master, self.canvas).line( x, y)
		#Draw(self.master, self.canvas).overlay( x, y, self.imagePath)
	
	def key_released(self, event):
		self.canvas.keyDraw =  False
		Draw(self.master, self.canvas).key_released()

		

	def save_img(self, event):
		print("SAVED")
		#self.canvas.pack()
		ps = self.canvas.postscript(colormode="color", height=self.height, width=self.width) 
		
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		img.save(self.imgSave, 'png')

	def undo(self, event):
		print("Undo")
		Draw(self.master, self.canvas).undo()

	def close(self, event):
		self.master.destroy()

	def bigger_brush(self, event):
		self.canvas.lineWidth = self.canvas.lineWidth + 1
		print(f"self.canvas.lineWidth {self.canvas.lineWidth}")
		if self.canvas.lineWidth > 10:
			self.canvas.lineWidth = 10

	def smaller_brush(self, event):

		self.canvas.lineWidth = self.canvas.lineWidth - 1
		print(f"self.canvas.lineWidth {self.canvas.lineWidth}")
		if self.canvas.lineWidth <= 0:
			self.canvas.lineWidth = 1




class Draw():
	def __init__(self, master=None, canvas=None):
		self.master = master
		self.canvas = canvas
		self.canvas.keyDraw = False
		self.canvas.keyOverlay = False
		#TODO image Handler
		self.imagePath = "gutman.jpg"
				

	def line(self, x, y):
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
		self.master.bind('<Motion>', self.motion)

	def overlay(self, x, y,imagePath):
		self.y = y
		self.x = x
		self.canvas.keyOverlay = True
		self.imagePath = imagePath
		self.master.bind('<Motion>', self.motion)

	def key_released(self):
		self.keyDraw = False
		self.keyOverlay = False
		self.canvas.keyDraw = False
		self.canvas.undoList.append(list(self.canvas.lastMoves))
		self.canvas.lastMoves = []

		
	def undo(self):
		try:
			for elem in self.canvas.undoList[-1:][0]:				
				self.canvas.delete(elem)			
			del self.canvas.undoList[-1:]
		except:
			pass

	def motion(self, event):
		
		if self.canvas.keyDraw:
			print("LINE")
			print("LINE")
			print("LINE")

			x, y = event.x, event.y
			rect = self.canvas.create_line(x, y, self.x, self.y, \
					fill=self.canvas.lineColor, width=self.canvas.lineWidth,)
			self.x ,self.y = x, y
			self.canvas.lastMoves.append(rect)

		elif self.canvas.keyOverlay:

			self.get_pixel_val()
			x, y = event.x, event.y
			rect = self.canvas.create_rectangle(x, y, x+self.canvas.lineWidth, y+self.canvas.lineWidth,
					fill=self.canvas.lineColor, outline=self.canvas.lineColor)
			


			self.x ,self.y = x, y
			self.canvas.lastMoves.append(rect)

	
	def get_pixel_val(self):	
		im = Image.open(self.imagePath).convert('RGB')
		pixlist = list()
		#TODO highlighter


		r, g, b = im.getpixel((self.x, self.y))

		g = g+100
		b = b+100
		if r > 255 : r = 255 
		if g > 255: g = 255
		if b > 255: b = 255 
		a = "#{:02x}{:02x}{:02x}".format(r,g,b)
		self.canvas.lineColor = a
		print(a)


	

class Sidebar():
	def __init__(self, master=None, canvas=None):
		self.master = master
		self.canvas = canvas
		

		sidebar = tk.Frame(self.master, width=self.master.width,bd=0, bg='white', 
					height=40,  borderwidth=0, highlightcolor="blue", 
					highlightbackground="yellow", cursor="arrow", relief="flat")

		sidebar.pack(expand=True, fill='both', side='top', anchor='n', padx=0, pady=0)

		try:
			self.icon = tk.PhotoImage(file="palette.png")
		except:
			self.icon = tk.PhotoImage(width=1, height=1)


		self.button1 = tk.Button(sidebar, width=1, heigh=1, bg="white",
								image = self.icon, highlightcolor="green",  
								cursor="arrow", command=self.turn_red,
								compound="center")
		
		self.button1.pack(side="left", anchor="nw")

		self.button1.configure(height=15, width=20)
	
	def turn_red(self):
		print("CLICKED")
		self.canvas.lineColor = colorchooser.askcolor(title ="Choose color",
								color=self.canvas.lineColor)[-1:][0]
		print(self.canvas.lineColor)

def show_help():
	print("""./imageEditor.py
		usage ./imageEditor.py {path to file } {path to save file}
		""")

		

if "-h" in sys.argv or "--help" in sys.argv:
	show_help()
	sys.exit(0)
try:
	img = sys.argv[1]
except:
	img = "/tmp/sscopy.png"

try:
	imgSave = sys.argv[2]
except:
	imgSave = "/tmp/sscopy.png"


root = tk.Tk()

#root.eval('tk::PlaceWindow . center')
print("xDDDD")
app = Application(img, master=root)
app.imgSave = imgSave

app.mainloop()
