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
		#self.canvas.PencilDraw = False

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
		self.master.bind('<Control-c>', self.save_img)
		self.master.bind('<space>', self.save_img)
		#when want to escape
		self.master.bind('<Escape>', self.close)
		self.master.bind('<Key-q>', self.close)
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
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)

	def smaller_brush(self, event):

		self.canvas.lineWidth = self.canvas.lineWidth - 1
		print(f"self.canvas.lineWidth {self.canvas.lineWidth}")
		if self.canvas.lineWidth <= 0:
			self.canvas.lineWidth = 1
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)





class Draw():
	def __init__(self, master=None, canvas=None):
		self.master = master
		self.canvas = canvas

		#self.canvas.keyDraw = False
		
		#TODO image Handler
		#self.imagePath = "gutman.jpg"
				

	def line(self, x, y):
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
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

		print(f"{self.master.pencilColor}  xx  {self.canvas.keyDraw}")
		
		if self.canvas.keyDraw and self.master.pencilColor == "red" :
			x, y = event.x, event.y
			rect = self.canvas.create_line(x, y, self.x, self.y, \
					fill=self.canvas.lineColor, width=self.canvas.lineWidth,)
			self.x ,self.y = x, y
			self.canvas.lastMoves.append(rect)




	

class Sidebar():
	def __init__(self, master=None, canvas=None):
		self.master = master
		self.canvas = canvas
		self.sidebar = None
		self.draw_icon = None
		self.canvas.pencilButtonClicked = False



		
		self.sidebarObj()
		self.color_change()
		self.brush_size()
		self.pencil()

	def brush_size(self):
		self.canvas.lineWidthLabel = tk.StringVar()

		self.brush_size_label = tk.Label(self.sidebar, width=3, height=1,
					bg="white", relief="sunken")
		#self.brush_size_label["text"] = self.canvas.lineWidth
		self.canvas.lineWidthLabel.set("1")
		self.brush_size_label["textvariable"] = self.canvas.lineWidthLabel
		self.brush_size_label.pack(side="right", anchor="ne")

	def sidebarObj(self):
		self.sidebar = tk.Frame(self.master, width=self.master.width,bd=0, bg='white', 
					height=40,  borderwidth=0, highlightcolor="blue", 
					highlightbackground="yellow", cursor="arrow", relief="flat")

		self.sidebar.pack(expand=True, fill='both', side='top', anchor='n', padx=0, pady=0)


	def color_change(self):
		try:
			self.icon = tk.PhotoImage(file="palette.png")
		except:
			self.icon = tk.PhotoImage(width=1, height=1)


		self.button1 = tk.Button(self.sidebar, width=1, heigh=1, bg="white",
								image = self.icon, highlightcolor="green",  
								cursor="arrow", command=self.turn_red,
								compound="left")
		
		self.button1.pack(side="left", anchor="nw")

		self.button1.configure(height=15, width=20)


	def pencil(self):

		self.draw_icon = tk.PhotoImage(width=1, height=1)
		self.pencil = tk.Button(self.sidebar, width=1, heigh=1, bg="white",
								image = self.draw_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_pencil,
								compound="center", text="\u270E", fg="black")
		self.pencil.pack(side="left", anchor="nw")
		self.pencil.configure(height=15, width=5)

	def turn_red(self):
		print("CLICKED")
		self.canvas.lineColor = colorchooser.askcolor(title ="Choose color",
								color=self.canvas.lineColor)[-1:][0]

	def set_pencil(self):
		
		if self.pencil["fg"] == "black":		
			#print(f"self.canvas.PencilDraw {self.canvas.PencilDraw}" )
			self.pencil.configure(bg="#f9ffbd")
			self.pencil.configure(fg="red")
		else:
			#print(f"self.canvas.PencilDraw {self.canvas.PencilDraw}" )
			self.pencil.configure(bg="white")
			self.pencil.configure(fg="black")

		self.master.pencilColor = self.pencil["fg"]



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
pencilDraw = None
#root.eval('tk::PlaceWindow . center')

app = Application(img, master=root)
app.imgSave = imgSave

app.mainloop()
