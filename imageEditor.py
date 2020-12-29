#!/bin/python

from PIL import ImageTk,Image
import tkinter as tk 
from tkinter import filedialog as fd
from tkinter import colorchooser
import os, sys, io
import pyautogui


class Application(tk.Frame):
	def __init__(self, image, master=None ):
		super().__init__(master)
		self.master = master
		self.imagePath = image
		self.resize = True


	
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

		self.master.pencilColor = None
		self.master.rectangleColor = None
		self.master.rectangle_frameColor = None
		self.master.color_picker = None
		self.master.ovalColor = None
		self.master.ovalFilledColor = None
		self.master.button1 = None

		self.master.xrec =  None
		self.master.yrec =  None
		self.master.rect = None
		self.master.line = None

		
	def window_config(self):

		self.master.geometry(f"{self.width}x{self.height+22}")
		self.master.title("imageEditor")
		

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
		#when save as ctrl+shift +s
		self.master.bind('<Control-Shift-KeyPress-S>', self.save_img_as)
		#when want to escape
		self.master.bind('<Escape>', self.close)
		self.master.bind('<Key-q>', self.close)
		#make brush bigger
		self.master.bind('<Key-plus>', self.bigger_brush)
		self.master.bind('<Key-equal>', self.bigger_brush)
		#make brush smaller
		self.master.bind('<Key-minus>', self.smaller_brush)
		#when window size changes
		self.master.bind('<Configure>', self.resizeWindow)

	def resizeWindow(self, event):

		self.width = self.master.winfo_width() 
		self.height = self.master.winfo_height()-22

	
		self.canvas.config(width=self.width, height=self.height)

	
	def convert_image(self, img):
		try:
			self.bgImage = ImageTk.PhotoImage(Image.open(img), master=self.master)
			self.get_sizes()
		except:

			self.height = 300
			self.width = 450

		self.set_bg_image()
		#self.window_config()
		self.pack(padx=0, pady=0)



	def get_sizes(self):
		self.height = self.bgImage.height()
		self.width = self.bgImage.width()
		


	def set_bg_image(self):

		self.canvas = tk.Canvas(root, width=self.width, heigh=self.height, bg="white")
		try:
			self.canvas.create_image(0,0,anchor="nw", image=self.bgImage)
			self.canvas.pack(fill="both", expand="yes")
		except:

			self.canvas.pack(fill="both", expand="yes")

	def key_pressed(self, event):
		x, y = event.x, event.y 
 
		if self.master.pencilColor == "red":
			Draw(self.master, self.canvas).line( x, y)


		elif self.master.rectangleColor == "red":
			Draw(self.master, self.canvas).rectangle( x, y)
		
		elif self.master.rectangle_frameColor == "red":
			Draw(self.master, self.canvas).rectangle_frame( x, y)

		elif self.master.ovalColor == "red":
			Draw(self.master, self.canvas).oval( x, y)

		elif self.master.ovalFilledColor == "red":
			Draw(self.master, self.canvas,self.imagePath).ovalFilled(x, y)
			
		elif self.master.color_picker == "red":
			Draw(self.master, self.canvas,self.imagePath).get_pixel_val( x, y)
			self.master.button1.configure(bg = self.canvas.lineColor)

	
	def key_released(self, event):
		self.canvas.keyDraw =  False
		Draw(self.master, self.canvas).key_released()

		

	def save_img(self, event):
		bgImage = ImageTk.PhotoImage(Image.new("RGB", (self.width, self.height), color="#ffffff" ), master=self.master)
		self.canvas.pack(fill="both", expand="yes")
		if self.imgSave == None:
			self.save_img_as()
		ps = self.canvas.postscript(colormode="color", height=self.height, width=self.width) 
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		img.save(self.imgSave, 'png')

	def save_img_as(self, event=None):
		bgImage = ImageTk.PhotoImage(Image.new("RGB", (self.width, self.height), color="#ffffff" ), master=self.master)
		self.canvas.pack(fill="both", expand="yes")
		f = fd.asksaveasfile(mode='w', defaultextension=".png")
		self.imgSave = f.name
		ps = self.canvas.postscript(colormode="color", height=self.height, width=self.width) 
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		img.save(self.imgSave, 'png')

	def undo(self, event):
		Draw(self.master, self.canvas).undo()

	def close(self, event):
		self.master.destroy()

	def bigger_brush(self, event):
		self.canvas.lineWidth = self.canvas.lineWidth + 1
		if self.canvas.lineWidth > 15:
			self.canvas.lineWidth = 15
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)

	def smaller_brush(self, event):

		self.canvas.lineWidth = self.canvas.lineWidth - 1
		if self.canvas.lineWidth <= 0:
			self.canvas.lineWidth = 1
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)


class Draw():
	def __init__(self, master=None, canvas=None, imagePath=None):
		self.master = master
		self.canvas = canvas
		self.imagePath = imagePath

				

	def line(self, x, y):
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
		self.master.bind('<Motion>', self.motion)


	def rectangle(self, x, y):
		
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
		self.master.bind('<Motion>', self.motion)

	def rectangle_frame(self, x, y):
		
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
		self.master.bind('<Motion>', self.motion)

	def oval(self, x, y):
		
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
		self.master.bind('<Motion>', self.motion)

	def ovalFilled(self, x, y):
		
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
		self.master.bind('<Motion>', self.motion)


	def get_pixel_val(self, x, y):
		
		im = Image.open(self.imagePath).convert('RGB')	
		pixlist = list()	
		#TODO highlighter	

		r, g, b = im.getpixel((x, y))	
	
		if r > 255 : r = 255 	
		if g > 255: g = 255	
		if b > 255: b = 255 	
		a = "#{:02x}{:02x}{:02x}".format(r,g,b)	
		self.canvas.lineColor = a	


	def key_released(self):
		self.keyDraw = False
		self.canvas.keyDraw = False
		self.master.rect = None
		self.master.oval = None
		self.master.ovalFilled = None
		self.master.xrec =  None
		self.master.yrec = None

		self.canvas.undoList.append(list(self.canvas.lastMoves))
		self.canvas.lastMoves = []

		
	def undo(self):
		try:
			for elem in self.canvas.undoList[-1:][0]:				
				self.canvas.delete(elem)			
			del self.canvas.undoList[-1:]
		except:
			del self.canvas.undoList[-1:]


	def motion(self, event):
		
		#draw line
		if self.canvas.keyDraw and self.master.pencilColor == "red" :
			
			x, y = event.x, event.y
			self.master.line = self.canvas.create_line(self.x, self.y,x, y,  \
					fill=self.canvas.lineColor, width=self.canvas.lineWidth)

			self.x ,self.y = x, y
			self.canvas.lastMoves.append(self.master.line)

		#draw filled rectangle		
		elif self.canvas.keyDraw and self.master.rectangleColor == "red":
			self.canvas.delete(self.master.rect)
			if self.master.xrec ==  None:
					self.master.xrec =  event.x
					self.master.yrec =   event.y


			x, y = event.x, event.y
			self.master.rect = self.canvas.create_rectangle(self.master.xrec, \
				self.master.yrec,x, y, fill=self.canvas.lineColor,\
				outline=self.canvas.lineColor, width=self.canvas.lineWidth,)
			self.x ,self.y = x, y
			self.canvas.lastMoves.append(self.master.rect)

		#draw unfilled rectangle
		elif self.canvas.keyDraw and self.master.rectangle_frameColor == "red":
			
			self.canvas.delete(self.master.rect)
			if self.master.xrec ==  None:
					self.master.xrec =  event.x
					self.master.yrec =   event.y

			x, y = event.x, event.y

			self.master.rect = self.canvas.create_rectangle(self.master.xrec, \
				self.master.yrec,x, y, outline=self.canvas.lineColor, 
			 	width=self.canvas.lineWidth)
			self.x ,self.y = x, y

			self.canvas.lastMoves.append(self.master.rect)

		#draw oval
		elif self.canvas.keyDraw and self.master.ovalColor == "red":
			try:
				self.canvas.delete(self.master.oval)
			except:
				pass
			if self.master.xrec ==  None:
					self.master.xrec =  event.x
					self.master.yrec =   event.y

			x, y = event.x, event.y
						
			self.master.oval = self.canvas.create_oval(self.master.xrec, \
				self.master.yrec,x, y, outline=self.canvas.lineColor, 
				width=self.canvas.lineWidth)

			self.x ,self.y = x, y
			
			self.canvas.lastMoves.append(self.master.oval)

		elif self.canvas.keyDraw and self.master.ovalFilledColor == "red":
			try:
				self.canvas.delete(self.master.ovalFilled)
			except:
				pass
			if self.master.xrec ==  None:
					self.master.xrec =  event.x
					self.master.yrec =   event.y

			x, y = event.x, event.y

						
			self.master.ovalFilled = self.canvas.create_oval(self.master.xrec, \
				self.master.yrec,x, y, outline=self.canvas.lineColor, 
				width=self.canvas.lineWidth, fill=self.canvas.lineColor)

			self.x ,self.y = x, y
			
			self.canvas.lastMoves.append(self.master.ovalFilled)


class Sidebar():
	def __init__(self, master=None, canvas=None):
		self.master = master
		self.canvas = canvas
		self.sidebar = None
	
		self.canvas.pencilButtonClicked = False

		self.sidebarObj()
		self.color_change()
		self.brush_size()
		self.pencil()
		self.rectangle()
		self.rectangle_frame()
		self.oval()
		self.ovalFilled()
		self.color_picker_button()

	def brush_size(self):
		self.canvas.lineWidthLabel = tk.StringVar()

		self.brush_size_label = tk.Label(self.sidebar, width=3, height=1,
					bg="white", relief="sunken")
		
		self.canvas.lineWidthLabel.set("1")
		self.brush_size_label["textvariable"] = self.canvas.lineWidthLabel
		self.brush_size_label.pack(side="right", anchor="ne")

	def sidebarObj(self):
		self.sidebar = tk.Frame(self.master, width=self.master.width,bd=0, bg='white', 
					height=30,  borderwidth=0, highlightcolor="blue",  
					highlightbackground="yellow", cursor="arrow", relief="raised")

		self.sidebar.pack(expand=False, fill='both', side='bottom', anchor='s', padx=0, pady=0)

	def color_change(self):
		self.icon = tk.PhotoImage(width=1, height=1)


		self.master.button1 = tk.Button(self.sidebar, width=1, heigh=1.2, bg=self.canvas.lineColor,
								image = self.icon, highlightcolor="green",  
								cursor="arrow", command=self.color_changer,
								compound="left", relief="sunken")
		
		self.master.button1.pack(expand=False, side="left", anchor="nw")

		self.master.button1.configure(height=22, width=20)

	def pencil(self):

		self.draw_icon = tk.PhotoImage(width=1, height=1)
		self.pencil = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.draw_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_pencil,
								compound="center", text="\u270E", fg="black")
		self.pencil.pack(side="left", anchor="nw")
		self.pencil.configure(height=15, width=5)

	def rectangle(self):

		self.rectangle_icon = tk.PhotoImage(width=1, height=1)
		self.rectangle = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.rectangle_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_rectangle,
								compound="center", text="\u25A0", fg="black")
		self.rectangle.pack(side="left", anchor="nw")
		self.rectangle.configure(height=15, width=5)

	def rectangle_frame(self):

		self.rectangle_frame_icon = tk.PhotoImage(width=1, height=1)
		self.rectangle_frame = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.rectangle_frame_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_rectangle_frame,
								compound="center", text="\u25A1", fg="black",)

		self.rectangle_frame.pack(side="left", anchor="nw")
		self.rectangle_frame.configure(height=15, width=5)

	def oval(self):
		# unicode filled circle
		self.oval_icon = tk.PhotoImage(width=1, height=1)
		self.oval = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.oval_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_oval,
								compound="center", text="\u25CB", fg="black",)

		self.oval.pack(side="left", anchor="nw")
		self.oval.configure(height=15, width=5)

	def ovalFilled(self):
		#\u25CF unicode filled circle
		self.ovalFilled_icon = tk.PhotoImage(width=1, height=1)
		self.ovalFilled = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.ovalFilled_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_oval_filled,
								compound="center", text="\u25CF", fg="black",)

		self.ovalFilled.pack(side="left", anchor="nw")
		self.ovalFilled.configure(height=15, width=5)

	def color_picker_button(self):
		self.color_picker_icon = tk.PhotoImage(width=1, height=1)
		self.color_picker = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.color_picker_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_color_picker,
								compound="center", text="c", fg="black")
		
		self.color_picker.pack(side="left", anchor="nw")
		self.color_picker.configure(height=15, width=5)

	def color_changer(self):

		self.canvas.lineColor = colorchooser.askcolor(title ="Choose color",
								color=self.canvas.lineColor)[-1:][0]
		self.master.button1.configure(bg = self.canvas.lineColor)

	
	def set_config_buttons(self, pencil=None, rectangle=None,
		rectangle_frame=None, color_picker=None, oval=None, ovalFilled=None):

		if rectangle_frame == None:
			self.rectangle_frame.configure(bg="white")
			self.rectangle_frame.configure(fg="black")
		else:
			self.rectangle_frame.configure(bg="#f9ffbd")
			self.rectangle_frame.configure(fg="red")
				

		if pencil == None:
			self.pencil.configure(bg="white")
			self.pencil.configure(fg="black")
		else:
			self.pencil.configure(bg="#f9ffbd")
			self.pencil.configure(fg="red")


		if rectangle == None:
			self.rectangle.configure(bg="white")
			self.rectangle.configure(fg="black")
		else:
			self.rectangle.configure(bg="#f9ffbd")
			self.rectangle.configure(fg="red")


		if color_picker == None:
			self.color_picker.configure(bg="white")
			self.color_picker.configure(fg="black")
		else:
			self.color_picker.configure(bg="#f9ffbd")
			self.color_picker.configure(fg="red")


		if oval == None:
			self.oval.configure(bg="white")
			self.oval.configure(fg="black")
		else:
			self.oval.configure(bg="#f9ffbd")
			self.oval.configure(fg="red")

		if ovalFilled == None:
			self.ovalFilled.configure(bg="white")
			self.ovalFilled.configure(fg="black")
		else:
			self.ovalFilled.configure(bg="#f9ffbd")
			self.ovalFilled.configure(fg="red")


		self.master.pencilColor = self.pencil["fg"]
		self.master.rectangleColor = self.rectangle["fg"]
		self.master.rectangle_frameColor = self.rectangle_frame["fg"]
		self.master.color_picker = self.color_picker["fg"]
		self.master.ovalColor = self.oval["fg"]
		self.master.ovalFilledColor = self.ovalFilled["fg"]

	def set_pencil(self):
		
		if self.pencil["fg"] == "black":		
			self.set_config_buttons(pencil=True)

	def set_rectangle(self):
		
		if self.rectangle["fg"] == "black":		
			self.set_config_buttons(rectangle=True)
	
	def set_rectangle_frame(self):

		if self.rectangle_frame["fg"] == "black":		
			self.set_config_buttons(rectangle_frame=True)


	def set_oval(self):
		if self.oval["fg"] == "black":		
			self.set_config_buttons(oval=True)

	def set_oval_filled(self):
		if self.ovalFilled["fg"] == "black":		
			self.set_config_buttons(ovalFilled=True)


	def set_color_picker(self):
		if self.color_picker["fg"] == "black":		
			self.set_config_buttons(color_picker=True)			


def show_help():
	print("""./imageEditor.py
		usage ./imageEditor.py {path to file} {path to save file}
			  ./imageEditor.py {path to file} (file will be replaced) if no image, will be created

		""")

		

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
pencilDraw = None
#root.eval('tk::PlaceWindow . center')

app = Application(img, master=root)
app.imgSave = imgSave

app.mainloop()


