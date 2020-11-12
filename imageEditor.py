#!/bin/python


from PIL import ImageTk,Image
import tkinter as tk 
import os, sys, io
import pyautogui
	



class Application(tk.Frame):
	def __init__(self, image, master=None ):
		super().__init__(master)
		self.master = master
		self.master.title("imageEditor")
		
		image = Image.open(img)
		self.canvas_config()
		self.keybinds()


	def canvas_config(self):
		self.convert_image(img)
		
		self.keyDraw = False
		self.canvas.lineWidth = 1
		self.canvas.lineColor = "#ff0000"


	def keybinds(self):
		#when mouse button pressed		
		self.master.bind('<ButtonPress-1>', self.key_pressed)
		#when mouse button released
		self.master.bind('<ButtonRelease-1>', self.key_released)
		#when want to save CTRL+S
		self.master.bind('<Control-s>', self.save_img)
		#when want to escape
		self.master.bind('<Escape>', self.close)
		self.master.bind('<Key-q>', self.close)
		self.master.bind('<Control-c>', self.close)
		#make brush bigger


		self.master.bind('<Key-plus>', self.bigger_brush)
		self.master.bind('<Key-equal>', self.bigger_brush)

		self.master.bind('<Key-minus>', self.smaller_brush)



	
	def convert_image(self, img):
		self.bgImage = ImageTk.PhotoImage(Image.open(img), master=self.master)
		self.height, self.width = self.get_sizes()
		self.set_bg_image()	
		self.set_sizes()
		self.pack()

	  
	def get_sizes(self):
		height = self.bgImage.height()
		width = self.bgImage.width()
		return height, width

	def set_sizes(self):
		self.master.geometry(f"{self.width}x{self.height}")
		#self.master.overrideredirect(1)



	def set_bg_image(self):
		self.canvas = tk.Canvas(root, width=self.width, heigh=self.height)
		self.canvas.create_image(0,0,anchor="nw", image=self.bgImage)
		self.canvas.grid()
		self.canvas.pack()

	def key_pressed(self, event):
		x, y = event.x, event.y 
		Draw(self.master, self.canvas).line( x, y)
	
	def key_released(self, event):
		self.canvas.keyDraw =  False
		Draw(self.master).key_released()

	def save_img(self, event):
		print("SAVE")
		self.canvas.pack()
		ps = self.canvas.postscript(colormode="color") 
		
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		img.save(self.imgSave, 'png')

	def close(self, event):
		self.master.destroy()

	def bigger_brush(self, event):
		self.canvas.lineWidth = self.canvas.lineWidth + 1
		print(f"self.canvas.lineWidth {self.canvas.lineWidth}")

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

		
	def line(self, x, y):
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
		self.master.bind('<Motion>', self.motion)


	def key_released(self):
		self.keyDraw = False
		self.canvas.keyDraw = False


	def motion(self, event):
		print(self.canvas.keyDraw)
		if self.canvas.keyDraw:
			print(f"cursor {event.x}, {event.y}")
			print(f"olf cursor {self.x}, {self.y}\n")
			x, y = event.x, event.y
			rect = self.canvas.create_line(x, y, self.x, self.y, \
					fill=self.canvas.lineColor, width=self.canvas.lineWidth)
			self.x ,self.y = x, y


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


app = Application(img, master=root)
app.imgSave = imgSave

app.mainloop()