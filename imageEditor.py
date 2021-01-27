#!/bin/python

from PIL import ImageTk,Image
import tkinter as tk 
from tkinter import filedialog as fd
from tkinter import colorchooser
import os, sys, io
import screeninfo
from math import sqrt


draw_Item_list = list()
draw_Item = 0
buttons_list = dict()
maxLineWidth = 50

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

		self.canvas.keyOverlay = False
		self.canvas.lineWidth = 1
		self.canvas.lineColor = "#ff0000"
		self.canvas.lastMoves = list()
		self.canvas.undoList = []

		
		self.master.button1 = None
		self.master.shift = False

		self.master.xrec =  None
		self.master.yrec =  None
		self.master.rect = None
		self.master.line = None

		
	def window_config(self):
		global sidebarHeight
		self.master.geometry(f"{self.width}x{self.height+sidebarHeight}")
		self.master.title("imageEditor")


		

	def keybinds(self):
		#when mouse button pressed		
		self.canvas.bind('<ButtonPress-1>', self.key_pressed)
		#when mouse button pressed		
		self.canvas.bind('<Shift-ButtonPress-1>', self.key_pressed_Shift)
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
		global sidebarHeight
		self.width = self.master.winfo_width() 
		self.height = self.master.winfo_height()-22
		self.canvas.config(width=self.width, height=self.height-sidebarHeight)

	def convert_image(self, img):
		try:
			self.bgImage = ImageTk.PhotoImage(Image.open(img), master=self.master)
			self.get_sizes()
		except:
			global sidebarHeight, sidebarWidth
			self.height = int((screeninfo.get_monitors()[0].height *50) / 100)
			self.width = int((screeninfo.get_monitors()[0].width *40) / 100)

		self.set_bg_image()
		self.window_config()
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
		
		global draw_Item, draw_Item_list
		if draw_Item == None:
			return

		if draw_Item == draw_Item_list[0]:
			Draw(self.master, self.canvas).line( x, y)

		elif draw_Item == draw_Item_list[1]:
			Draw(self.master, self.canvas).rectangle( x, y)
		
		elif draw_Item == draw_Item_list[2]:
			Draw(self.master, self.canvas).rectangle_frame( x, y)

		elif draw_Item == draw_Item_list[3]:
			Draw(self.master, self.canvas).oval( x, y)

		elif draw_Item == draw_Item_list[4]:
			Draw(self.master, self.canvas,self.imagePath).ovalFilled(x, y)
	
		elif draw_Item == draw_Item_list[5]:
			Draw(self.master, self.canvas,self.imagePath).get_pixel_val( x, y)
			self.master.button1.configure(bg = self.canvas.lineColor)


	def key_pressed_Shift(self, event):
		global draw_Item, draw_Item_list
		self.master.shift = True
		x, y = event.x, event.y 
		if draw_Item == draw_Item_list[0]:
			Draw(self.master, self.canvas).line( x, y)

		elif draw_Item == draw_Item_list[1]:
			Draw(self.master, self.canvas).rectangle( x, y)
		
		elif draw_Item == draw_Item_list[2]:
			Draw(self.master, self.canvas).rectangle_frame( x, y)

		elif draw_Item == draw_Item_list[3]:
			Draw(self.master, self.canvas).oval( x, y)

		elif draw_Item == draw_Item_list[4]:
			Draw(self.master, self.canvas,self.imagePath).ovalFilled(x, y)
	
		elif draw_Item == draw_Item_list[5]:
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
	
		ps = self.canvas.postscript(colormode="color", pagewidth=self.width-1,\
		 pageheight=self.height-1 ,height=self.height, width=self.width) 
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		img.save(self.imgSave, 'png')
		
	def save_img_as(self, event=None):
		bgImage = ImageTk.PhotoImage(Image.new("RGB", (self.width, self.height), color="#ffffff" ), master=self.master)
		self.canvas.pack(fill="both", expand="yes")
		f = fd.asksaveasfile(mode='w', defaultextension=".png")
		self.imgSave = f.name
		ps = self.canvas.postscript(colormode="color", height=self.height, width=self.width, \
			pagewidth=self.width-1, pageheight=self.height-1) 
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		img.save(self.imgSave, 'png')

	def undo(self, event):
		Draw(self.master, self.canvas).undo()

	def close(self, event):
		self.master.destroy()

	def bigger_brush(self, event):
		global maxLineWidth
		self.canvas.lineWidth = self.canvas.lineWidth + 1
		if self.canvas.lineWidth > maxLineWidth:
			self.canvas.lineWidth = maxLineWidth
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)

	def smaller_brush(self, event):

		self.canvas.lineWidth = self.canvas.lineWidth - 1
		if self.canvas.lineWidth <= 0:
			self.canvas.lineWidth = 1
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)


class Draw(Application):
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
		# asd
		self.x = x
		if not self.master.shift:
			self.y = x
		else:
			self.y = y

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
		try:
			im = Image.open(self.imagePath).convert('RGB')	
		except:
			return 
		pixlist = list()	

		r, g, b = im.getpixel((x, y))	
	
		if r > 255 : r = 255 	
		if g > 255: g = 255	
		if b > 255: b = 255 	
		a = "#{:02x}{:02x}{:02x}".format(r,g,b)	
		self.canvas.lineColor = a	

	def key_released(self):
		self.canvas.keyDraw = False
		self.master.shift = False

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
		global draw_Item, draw_Item_list
		
		#draw line
		if self.canvas.keyDraw and draw_Item == draw_Item_list[0]:
			
			x, y = event.x, event.y
			if self.canvas.lineWidth >5:
				self.master.line = self.canvas.create_oval(x,y,\
					x+self.canvas.lineWidth-4, y+self.canvas.lineWidth-4,\
					 outline=self.canvas.lineColor,width=self.canvas.lineWidth-3, 
					 fill=self.canvas.lineColor)
			else:
				self.master.line = self.canvas.create_line(x,y,\
			
			self.x, self.y, width=self.canvas.lineWidth, fill=self.canvas.lineColor)


			self.x ,self.y = x, y
			self.canvas.lastMoves.append(self.master.line)

		#draw filled rectangle		
		elif self.canvas.keyDraw and draw_Item == draw_Item_list[1]:
			self.canvas.delete(self.master.rect)
			
			self.master.xrec, self.master.yrec = self.set_xrec(event.x, event.y)

			x, y = self.make_shifted(event.x, event.y)   
				
			self.master.rect = self.canvas.create_rectangle(self.master.xrec, \
				self.master.yrec,x, y, fill=self.canvas.lineColor,\
				outline=self.canvas.lineColor, width=self.canvas.lineWidth,)
			self.x ,self.y = x, y
			self.canvas.lastMoves.append(self.master.rect)

		#draw unfilled rectangle
		elif self.canvas.keyDraw and draw_Item == draw_Item_list[2]:
			
			self.canvas.delete(self.master.rect)
			self.master.xrec, self.master.yrec = self.set_xrec(event.x, event.y)

			x, y = self.make_shifted(event.x, event.y)   

			self.master.rect = self.canvas.create_rectangle(self.master.xrec, \
				self.master.yrec,x, y, outline=self.canvas.lineColor, 
			 	width=self.canvas.lineWidth)
			self.x ,self.y = x, y

			self.canvas.lastMoves.append(self.master.rect)

		#draw oval
		elif self.canvas.keyDraw and draw_Item == draw_Item_list[3]:
			try:
				self.canvas.delete(self.master.oval)
			except:
				pass
			self.master.xrec, self.master.yrec = self.set_xrec(event.x, event.y)
			x, y = self.make_shifted(event.x, event.y)   
						
			self.master.oval = self.canvas.create_oval(self.master.xrec, \
				self.master.yrec,x, y, outline=self.canvas.lineColor, 
				width=self.canvas.lineWidth)

			self.x ,self.y = x, y
			
			self.canvas.lastMoves.append(self.master.oval)
		
		#draw filled oval
		elif self.canvas.keyDraw and draw_Item == draw_Item_list[4]:
			try:
				self.canvas.delete(self.master.ovalFilled)
			except:
				pass

			self.master.xrec, self.master.yrec = self.set_xrec(event.x, event.y)

			x, y = self.make_shifted(event.x, event.y)   
		
			self.master.ovalFilled = self.canvas.create_oval(self.master.xrec, \
				self.master.yrec,x, y, outline=self.canvas.lineColor, 
				width=self.canvas.lineWidth, fill=self.canvas.lineColor)

			self.x ,self.y = x, y
			self.canvas.lastMoves.append(self.master.ovalFilled)

	def make_shifted(self, x, y):
		if self.master.shift:
			if x > self.master.xrec and y < self.master.yrec:
				y = (x - self.master.xrec) - self.master.yrec
				y = -1 * y
			
			elif x < self.master.xrec and y < self.master.yrec:
				y = (x - self.master.xrec) + self.master.yrec
			elif x < self.master.xrec and y > self.master.yrec:
				x = (y - self.master.yrec) - self.master.xrec
				x = x *-1
			elif x > self.master.xrec and y > self.master.yrec:
				x = (y - self.master.yrec) + self.master.xrec
		return x, y

	def set_xrec(self,x, y):
		if self.master.xrec == None:
			xrec = x
			yrec = y
			return xrec, yrec
		return self.master.xrec, self.master.yrec


class Sidebar(Application):
	def __init__(self, master=None, canvas=None):

		self.master = master
		self.canvas = canvas
		self.sidebar = None
		# self.buttonHeight =  master.winfo_screenwidth()
		# self.buttonWidth =  master.winfo_screenheight()
		global sidebarHeight, sidebarWidth
		self.buttonHeight =  sidebarHeight
		self.buttonWidth =  sidebarWidth

		print(self.buttonHeight);
		print(self.buttonWidth);

		self.sidebarObj()
		self.color_change()
		self.brush_size()
		self.pencil()
		self.rectangle()
		self.rectangle_frame()
		self.oval()
		self.ovalFilled()
		self.color_picker_button()

		self.sidebar.configure(height=sidebarHeight);

	def sidebarObj(self):
		self.sidebar = tk.Frame(bd=0, bg='white', 
					height=100,  borderwidth=1, highlightcolor="blue",  
					highlightbackground="yellow", cursor="arrow", relief="raised")
		self.sidebar.pack(expand=False, fill='both', padx=0, pady=0)


	def brush_size(self):
		self.canvas.lineWidthLabel = tk.StringVar()

		self.brush_size_label = tk.Label(self.sidebar, width=3,
					bg="white", relief="sunken")
		
		self.canvas.lineWidthLabel.set("1")
		self.brush_size_label["textvariable"] = self.canvas.lineWidthLabel
		# self.brush_size_label.config(height=int((self.buttonHeight*9)/100))

		self.brush_size_label.pack(side="right", anchor="ne")


	def color_change(self):
		self.icon = tk.PhotoImage(width=1, height=1)


		self.master.button1 = tk.Button(self.sidebar, bg=self.canvas.lineColor,
								image = self.icon, highlightcolor="green",  
								cursor="arrow", command=self.color_changer,
								compound="left", relief="sunken")
		
		self.master.button1.pack(expand=False, side="left", anchor="nw")

		self.master.button1.configure(height=self.buttonHeight, width=self.buttonWidth)

	def pencil(self):

		self.draw_icon = tk.PhotoImage(width=1, height=1)
		self.pencil = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.draw_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_pencil,
								compound="center", text="\u270E", fg="black")
		self.pencil.pack(side="left", anchor="nw")
		self.pencil.configure(height=self.buttonHeight, width=self.buttonWidth)

		self.add_button_to_list(self.pencil, "pencil")
		
	def rectangle(self):

		self.rectangle_icon = tk.PhotoImage(width=1, height=1)
		self.rectangle = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.rectangle_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_rectangle,
								compound="center", text="\u25A0", fg="black")

		self.rectangle.pack(side="left", anchor="nw")
		self.rectangle.configure(height=self.buttonHeight, width=self.buttonWidth)
		self.add_button_to_list(self.rectangle, "rectangle")

	def rectangle_frame(self):

		self.rectangle_frame_icon = tk.PhotoImage(width=1, height=1)
		self.rectangle_frame = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.rectangle_frame_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_rectangle_frame,
								compound="center", text="\u25A1", fg="black",)

		self.rectangle_frame.pack(side="left", anchor="nw")
		self.rectangle_frame.configure(height=self.buttonHeight, width=self.buttonWidth)
		self.add_button_to_list(self.rectangle_frame, "rectangle_frame")

	def oval(self):
		# unicode filled circle
		self.oval_icon = tk.PhotoImage(width=1, height=1)
		self.oval = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.oval_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_oval,
								compound="center", text="\u25CB", fg="black",)

		self.oval.pack(side="left", anchor="nw")
		self.oval.configure(height=self.buttonHeight, width=self.buttonWidth)
		self.add_button_to_list(self.oval, "oval")

	def ovalFilled(self):
		#\u25CF unicode filled circle
		self.ovalFilled_icon = tk.PhotoImage(width=1, height=1)
		self.ovalFilled = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.ovalFilled_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_oval_filled,
								compound="center", text="\u25CF", fg="black",)

		self.ovalFilled.pack(side="left", anchor="nw")
		self.ovalFilled.configure(height=self.buttonHeight, width=self.buttonWidth)
		
		self.add_button_to_list(self.ovalFilled, "ovalFilled")

	def color_picker_button(self):
		self.color_picker_icon = tk.PhotoImage(width=1, height=1)
		self.color_picker = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.color_picker_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_color_picker,
								compound="center", text="c", fg="black")
		
		self.color_picker.pack(side="left", anchor="nw")
		self.color_picker.configure(height=self.buttonHeight, width=self.buttonWidth)

		self.add_button_to_list(self.color_picker, "color_picker")

	def color_changer(self):

		self.canvas.lineColor = colorchooser.askcolor(title ="Choose color",
								color=self.canvas.lineColor)[-1:][0]
		self.master.button1.configure(bg = self.canvas.lineColor)
		self.master.button1.configure(height=self.buttonHeight, width=self.buttonWidth)

	def add_button_to_list(self, button, name):
		global buttons_list, draw_Item_list
		buttons_list[name] = button
		if name not in draw_Item_list:
			draw_Item_list.append(name)

	def set_config_buttons(self):
		global buttons_list, draw_Item
					
		for elem in buttons_list:
			if draw_Item == elem:
				buttons_list[elem].configure(bg="#f9ffbd")
				buttons_list[elem].configure(fg="red")
			else:
				self.set_unclicked(elem)

	def set_unclicked(self, Id):
		global buttons_list
		buttons_list[Id].configure(bg="white")
		buttons_list[Id].configure(fg="black")

	def set_pencil(self):
		global draw_Item, draw_Item_list
		
		if draw_Item == draw_Item_list[0]:
			draw_Item = None
			self.set_unclicked(draw_Item_list[0])
		else:
			draw_Item = draw_Item_list[0]
			self.set_config_buttons()

	def set_rectangle(self):
		global draw_Item, draw_Item_list
		if draw_Item == draw_Item_list[1]:
			draw_Item = None
			self.set_unclicked(draw_Item_list[1])
			
		else:
			draw_Item = draw_Item_list[1]
			self.set_config_buttons()
	
	def set_rectangle_frame(self):

		global draw_Item, draw_Item_list
		if draw_Item == draw_Item_list[2]:
			draw_Item = None
			self.set_unclicked(draw_Item_list[2])
		else:
			draw_Item = draw_Item_list[2]
			self.set_config_buttons()

	def set_oval(self):
		global draw_Item, draw_Item_list		
		if draw_Item == draw_Item_list[3]:
			draw_Item = None
			self.set_unclicked(draw_Item_list[3])
		else:
			draw_Item = draw_Item_list[3]
			self.set_config_buttons()

	def set_oval_filled(self):
		global draw_Item, draw_Item_list
		if draw_Item == draw_Item_list[4]:
			draw_Item = None
			self.set_unclicked(draw_Item_list[4])
		else:
			draw_Item = draw_Item_list[4]
			self.set_config_buttons()

	def set_color_picker(self):
		global draw_Item, draw_Item_list
		if draw_Item == draw_Item_list[5]:
			draw_Item = None
			self.set_unclicked(draw_Item_list[5])
		else:
			draw_Item = draw_Item_list[5]
			self.set_config_buttons()


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
sidebarHeight = int((screeninfo.get_monitors()[0].height *2) / 100)
sidebarWidth = int((screeninfo.get_monitors()[0].width *3) / 100)


app = Application(img, master=root)
app.imgSave = imgSave

app.mainloop()


