from PIL import ImageTk,Image
import tkinter as tk 
import io
import vars 
from sidebar import Sidebar
from draw import Draw


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
		self.convert_image(self.imagePath)
		self.window_config()

		self.canvas.keyOverlay = False
		self.canvas.lineWidth = 10
		self.canvas.lineColor = "#ff0000"
		self.canvas.lastMoves = list()
		self.canvas.undoList = []

		
		self.master.button1 = None
		self.master.shift = False
		self.master.input_text = None
		

		self.master.ex_coords = vars.last_coords


		self.master.rect = None
		self.master.line = None
		self.master.text = None


		
	def window_config(self):

		self.master.geometry(f"{self.width}x{self.height+vars.sidebarHeight+vars.sidebarHeight}")
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

		#when every key else has been pressed
		self.master.bind("<Key>",self.text_inp_keys)
		self.master.bind("<space>",self.text_inp_keys)
		self.master.bind("<Return>",self.Enter)
		self.master.bind("<BackSpace>",self.Backspace)
		self.master.bind("<Control-BackSpace>",self.CtrlBackspace)

	def CtrlBackspace(self, event):
		
		self.canvas.delete(vars.text_object)

		try:
			for elem in vars.total_text[::-1]:
				if elem == " ":
					vars.total_text = vars.total_text[:-1]
				else:
					break
			
			vars.total_text = vars.total_text[:-(vars.total_text[::-1].index(" ")+1)]

		except:
			vars.total_text = ""

		vars.input_text = True
		Draw(self.master, self.canvas).input_text(self.canvas.lineWidth)

	def Backspace(self, event):
		
		self.canvas.delete(vars.text_object)
		vars.total_text = vars.total_text[:-1]
		vars.input_text = True
		Draw(self.master, self.canvas).input_text(self.canvas.lineWidth)

	def Enter(self, event):
		self.master.vars.input_text = True
		
		text_font = 0
		vars.total_text = ""
		self.canvas.delete(vars.textBoxFrame)
		tmp = []
		tmp.append(vars.text_object)
		self.canvas.undoList.append(tmp)
		
		vars.text_object = None

	def text_inp_keys(self, event):
		
		
		vars.draw_Item_list	
		if vars.draw_Item == vars.draw_Item_list[6]:
			vars.input_text = True
		else:
			vars.input_text = False
		if vars.input_text:
			vars.total_text += event.char	
			Draw(self.master, self.canvas).input_text(self.canvas.lineWidth)

	def resizeWindow(self, event):

		self.width = self.master.winfo_width() 
		self.height = self.master.winfo_height()-vars.sidebarHeight*2
		self.canvas.config(width=self.width, height=self.height)

	def convert_image(self, img):
		try:
			self.bgImage = ImageTk.PhotoImage(Image.open(img), master=self.master)
			self.get_sizes()
		except:

			self.height = int((screeninfo.get_monitors()[0].height *50) / 100)
			self.width = int((screeninfo.get_monitors()[0].width *40) / 100)

		self.set_bg_image()
		self.window_config()
		self.pack(padx=0, pady=0)

	def get_sizes(self):
		self.height = self.bgImage.height()
		self.width = self.bgImage.width()
		
	def set_bg_image(self):
		self.canvas = tk.Canvas(width=self.width, heigh=self.height, bg="white")
		try:
			self.canvas.create_image(0,0,anchor="nw", image=self.bgImage)
			self.canvas.pack(fill="both", expand="yes")
		except:
			self.canvas.pack(fill="both", expand="yes")

	def key_pressed(self, event):

		try:
			vars.draw_Item
		except NameError:
			vars.draw_Item = "pencil"
			  
		x, y = event.x, event.y 
		
		
		
		if vars.draw_Item == None:
			return

		if vars.draw_Item == vars.draw_Item_list[0]:
			Draw(self.master, self.canvas).line( x, y)

		elif vars.draw_Item == vars.draw_Item_list[1]:
			Draw(self.master, self.canvas).rectangle( x, y)
		
		elif vars.draw_Item == vars.draw_Item_list[2]:
			Draw(self.master, self.canvas).rectangle_frame( x, y)

		elif vars.draw_Item == vars.draw_Item_list[3]:
			Draw(self.master, self.canvas).oval( x, y)

		elif vars.draw_Item == vars.draw_Item_list[4]:
			Draw(self.master, self.canvas,self.imagePath).ovalFilled(x, y)
	
		elif vars.draw_Item == vars.draw_Item_list[5]:
			Draw(self.master, self.canvas,self.imagePath).get_pixel_val(x, y)
			self.master.button1.configure(bg = self.canvas.lineColor)

		elif vars.draw_Item == vars.draw_Item_list[6]:
			Draw(self.master, self.canvas,self.imagePath).text( x, y)



	def key_pressed_Shift(self, event):
		
		self.master.shift = True
		x, y = event.x, event.y 
		if vars.draw_Item == vars.draw_Item_list[0]:
			Draw(self.master, self.canvas).line( x, y)

		elif vars.draw_Item == vars.draw_Item_list[1]:
			Draw(self.master, self.canvas).rectangle( x, y)
		
		elif vars.draw_Item == vars.draw_Item_list[2]:
			Draw(self.master, self.canvas).rectangle_frame( x, y)

		elif vars.draw_Item == vars.draw_Item_list[3]:
			Draw(self.master, self.canvas).oval( x, y)

		elif vars.draw_Item == vars.draw_Item_list[4]:
			Draw(self.master, self.canvas,self.imagePath).ovalFilled(x, y)
	
		elif vars.draw_Item == vars.draw_Item_list[5]:
			Draw(self.master, self.canvas,self.imagePath).get_pixel_val( x, y)
			self.master.button1.configure(bg = self.canvas.lineColor)
		
	
	def key_released(self, event):

		self.canvas.keyDraw =  False
		Draw(self.master, self.canvas).key_released()

	def save_img(self, event):
		try:
			self.canvas.delete(self.master.textbox)
		except:
			pass
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
		try:
			self.canvas.delete(self.master.textbox)
		except:
			pass
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
		
		self.canvas.lineWidth = self.canvas.lineWidth + 1
		if self.canvas.lineWidth > vars.maxLineWidth:
			self.canvas.lineWidth = vars.maxLineWidth
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)

	def smaller_brush(self, event):

		self.canvas.lineWidth = self.canvas.lineWidth - 1
		if self.canvas.lineWidth <= 0:
			self.canvas.lineWidth = 1
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)

