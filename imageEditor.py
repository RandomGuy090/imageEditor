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





		sidebar = tk.Frame(root, width=self.width,bd=0, bg='blue', height=25,  borderwidth=0,
			highlightcolor="blue", highlightbackground="yellow", cursor="arrow", relief="sunken")

		sidebar.pack(expand=True, fill='both', side='top', anchor='n')

		self.button1 = tk.Button(sidebar, width=1, heigh=1, bg="green",
			highlightcolor="green", highlightbackground="green", cursor="arrow")
		
		self.button1.pack(side="left", anchor="nw")
		self.button1.bind("ButtonPress-1", self.turn_red)


		
		self.keybinds()





	def turn_red(self, event):
		event.widget["activeforeground"] = "red"

	def canvas_config(self):
		self.convert_image(img)
		
		self.keyDraw = False
		self.canvas.lineWidth = 1
		self.canvas.lineColor = "#ff0000"

		self.canvas.lastMoves = list()
		self.canvas.undoList = []


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
		self.height, self.width = self.get_sizes()
		self.set_bg_image()	
		self.set_sizes()
		self.pack()

	  
	def get_sizes(self):
		height = self.bgImage.height()
		width = self.bgImage.width()
		return height, width

	def set_sizes(self):
		self.master.geometry(f"{self.width}x{self.height+20}")

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
		print("SAVE")
		#self.canvas.pack()
		ps = self.canvas.postscript(colormode="color", height=self.height, width=self.width) 
		
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		img.save(self.imgSave, 'png')

	def undo(self, event):
		print("Undo")
		#"insert -4 chars", "insert")
		#Draw(self.master).clear_all()
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



		#self.canvas.lastMoves
				
	def line(self, x, y):
		
		self.y = y
		self.x = x
		self.canvas.keyDraw = True
		self.master.bind('<Motion>', self.motion)
		


	def key_released(self):
		self.keyDraw = False
		self.canvas.keyDraw = False
		


		print(f"self.canvas.lastMoves  {self.canvas.lastMoves}")
		print(f"self.canvas.undoList {self.canvas.undoList}")
		print(f"self.canvas.undoList {len(self.canvas.undoList)}")
		
		
		self.canvas.undoList.append(list(self.canvas.lastMoves))


		print(f"\nself.canvas.undoList {len(self.canvas.undoList)}")
		self.canvas.lastMoves = []
		print(f"self.canvas.undoList {self.canvas.undoList}")
		
	def undo(self):
		try:
			print(self.canvas.undoList[-1:])
			for elem in self.canvas.undoList[-1:][0]:
				print(elem)
				self.canvas.delete(elem)
			
			print(" ")
			print(" ")
			print(" ")
			print(self.canvas.undoList[0][-1:])
			
			del self.canvas.undoList[-1:]
		except:
			pass



	def motion(self, event):

		if self.canvas.keyDraw:
			print(f"cursor {event.x}, {event.y}")
			print(f"olf cursor {self.x}, {self.y}\n")
			x, y = event.x, event.y
			rect = self.canvas.create_line(x, y, self.x, self.y, \
					fill=self.canvas.lineColor, width=self.canvas.lineWidth,
					tags="main_line_tag",)
			self.x ,self.y = x, y
			self.canvas.lastMoves.append(rect)
	



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