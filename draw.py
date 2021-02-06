from PIL import ImageTk,Image
import tkinter as tk 
from tkinter import filedialog as fd
from tkinter import colorchooser

import vars

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

	def text(self, x, y):
		
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
		vars.last_coords = (None,None)

		self.canvas.undoList.append(list(self.canvas.lastMoves))
		self.canvas.lastMoves = []
		# 
		# 
	
	def undo(self):
		try:
			for elem in self.canvas.undoList[-1:][0]:				
				self.canvas.delete(elem)			
			del self.canvas.undoList[-1:]
		except:
			del self.canvas.undoList[-1:]

	def motion(self, event):
		
		
		#draw line
		if self.canvas.keyDraw and vars.draw_Item == vars.draw_Item_list[0]:
			
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
		elif self.canvas.keyDraw and vars.draw_Item == vars.draw_Item_list[1]:
			self.canvas.delete(self.master.rect)
			
			vars.last_coords = self.set_xrec(event.x, event.y)

			x, y = self.make_shifted(event.x, event.y)   
				
			self.master.rect = self.canvas.create_rectangle(vars.last_coords[0], \
				vars.last_coords[1],x, y, fill=self.canvas.lineColor,\
				outline=self.canvas.lineColor, width=self.canvas.lineWidth,)
			self.x ,self.y = x, y
			self.canvas.lastMoves.append(self.master.rect)

		#draw unfilled rectangle
		elif self.canvas.keyDraw and vars.draw_Item == vars.draw_Item_list[2]:
			
			self.canvas.delete(self.master.rect)
			vars.last_coords = self.set_xrec(event.x, event.y)

			x, y = self.make_shifted(event.x, event.y)   

			self.master.rect = self.canvas.create_rectangle(vars.last_coords[0], \
				vars.last_coords[1],x, y, outline=self.canvas.lineColor, 
			 	width=self.canvas.lineWidth)
			self.x ,self.y = x, y

			self.canvas.lastMoves.append(self.master.rect)

		#draw oval
		elif self.canvas.keyDraw and vars.draw_Item == vars.draw_Item_list[3]:
			try:
				self.canvas.delete(self.master.oval)
			except:
				pass
			vars.last_coords = self.set_xrec(event.x, event.y)
			x, y = self.make_shifted(event.x, event.y)   
						
			self.master.oval = self.canvas.create_oval(vars.last_coords[0], \
				vars.last_coords[1],x, y, outline=self.canvas.lineColor, 
				width=self.canvas.lineWidth)

			self.x ,self.y = x, y
			
			self.canvas.lastMoves.append(self.master.oval)
		
		#draw filled oval
		elif self.canvas.keyDraw and vars.draw_Item == vars.draw_Item_list[4]:
			try:
				self.canvas.delete(self.master.ovalFilled)
			except:
				pass

			vars.last_coords = self.set_xrec(event.x, event.y)

			x, y = self.make_shifted(event.x, event.y)   
		
			self.master.ovalFilled = self.canvas.create_oval(vars.last_coords[0], \
				vars.last_coords[1],x, y, outline=self.canvas.lineColor, 
				width=self.canvas.lineWidth, fill=self.canvas.lineColor)

			self.x ,self.y = x, y
			self.canvas.lastMoves.append(self.master.ovalFilled)
		
		# draw textbox
		elif self.canvas.keyDraw and vars.draw_Item == vars.draw_Item_list[6]:
			
			try:
				self.canvas.delete(self.master.textbox)
			except:
				pass

			vars.last_coords = self.set_xrec(event.x, event.y)
			x, y = self.make_shifted(event.x, event.y)   
		
			self.master.textbox = self.canvas.create_rectangle(vars.last_coords[0], \
				vars.last_coords[1],x, y, outline=self.canvas.lineColor, 
				width=2, dash=(10, 10))

			# self.master.vars.input_text = True
			
			vars.input_text = True

			vars.coords = x, y
			self.x ,self.y = x, y
			text_font = vars.last_coords[1] - y
			vars.textBoxFrame = self.master.textbox
			
			self.master.ex_coords = vars.last_coords

	def input_text(self, font):
		ex_coords = self.master.ex_coords
		
		coords = vars.coords
			
		if vars.input_text == False:
			return


		self.canvas.delete(vars.text_object)
		
		if coords[1] > ex_coords[1]:
			y = coords[1]
		else:
			y = ex_coords[1]


		if coords[0] < ex_coords[0]:
			x = coords[0]
		else:
			x = ex_coords[0]

		if coords[0] > ex_coords[0]:
			width = coords[0] - ex_coords[0]
		else:
			width = ex_coords[0] - ex_coords[0]

		if font <0:
			font = font*-1

		vars.text_object = self.canvas.create_text(x, y, font=("Purisa", self.canvas.lineWidth),
			text=vars.total_text, anchor="sw", width=width, fill=self.canvas.lineColor)


	def make_shifted(self, x, y):
		if self.master.shift:
			
			if x > vars.last_coords[0] and y < vars.last_coords[1]:
				y = (x - vars.last_coords[0]) - vars.last_coords[1]
				y = -1 * y
			elif x < vars.last_coords[0] and y < vars.last_coords[1]:
				y = (x - vars.last_coords[0]) + vars.last_coords[1]
			elif x < vars.last_coords[0] and y > vars.last_coords[1]:
				x = (y - vars.last_coords[1]) - vars.last_coords[0]
				x = x *-1
			elif x > vars.last_coords[0] and y > vars.last_coords[1]:
				x = (y - vars.last_coords[1]) + vars.last_coords[0]
		return x, y

	def set_xrec(self,x, y):
		
		
		if vars.last_coords[0] == None:
			xrec = x
			yrec = y
			return x, y
		return vars.last_coords