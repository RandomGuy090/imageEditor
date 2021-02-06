from PIL import ImageTk,Image
import tkinter as tk 
from tkinter import filedialog as fd
from tkinter import colorchooser
import os, sys, io
import screeninfo
from math import sqrt

import  vars 



class Sidebar():
	def __init__(self, master=None, canvas=None):

		self.master = master
		self.canvas = canvas
		self.sidebar = None


		self.buttonHeight =  vars.sidebarHeight
		self.buttonWidth =  vars.sidebarWidth

		

		self.sidebarObj()
		self.color_change()
		self.brush_size()
		self.pencil()
		self.rectangle()
		self.rectangle_frame()
		self.oval()
		self.ovalFilled()
		self.color_picker_button()
		self.text()

		self.sidebar.configure(height=vars.sidebarHeight);

	def sidebarObj(self):
		self.sidebar = tk.Frame(bd=0, bg='white', 
					height=100,  borderwidth=1, highlightcolor="blue",  
					highlightbackground="yellow", cursor="arrow", relief="raised")
		self.sidebar.pack(expand=False, fill='both', padx=0, pady=0)


	def brush_size(self):
		self.canvas.lineWidthLabel = tk.StringVar()

		self.brush_size_label = tk.Label(self.sidebar, width=5, height=self.buttonHeight,
					bg="white", relief="sunken")
		
		self.canvas.lineWidthLabel.set(self.canvas.lineWidth)
		self.brush_size_label["textvariable"] = self.canvas.lineWidthLabel
		

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

	def text(self):

		self.text_icon = tk.PhotoImage(width=1, height=1)
		self.text_frame = tk.Button(self.sidebar, width=1, heigh=0.8, bg="white",
								image = self.text_icon, highlightcolor="green",  
								cursor="arrow", command=self.set_text,
								compound="center", text="T", fg="black",)

		self.text_frame.pack(side="left", anchor="nw")
		self.text_frame.configure(height=self.buttonHeight, width=self.buttonWidth)
		self.add_button_to_list(self.text_frame, "text_frame")

	def color_changer(self):
		self.canvas.lineColor = colorchooser.askcolor(title ="Choose color",
								color=self.canvas.lineColor)[-1:][0]
		self.master.button1.configure(bg = self.canvas.lineColor)
		self.master.button1.configure(height=self.buttonHeight, width=self.buttonWidth)

	def add_button_to_list(self, button, name):
		
		vars.buttons_list[name] = button
		if name not in vars.draw_Item_list:
			vars.draw_Item_list.append(name)

	def set_config_buttons(self):

		if vars.draw_Item != vars.draw_Item_list[6]:
			
			self.canvas.delete(vars.textBoxFrame)
			tmp = []
			tmp.append(vars.text_object)
			self.canvas.undoList.append(tmp)

			vars.text_object = None
			text_font = 0
			vars.total_text = ""

		for elem in vars.buttons_list:
			
			if vars.draw_Item == elem:
				vars.buttons_list[elem].configure(bg="#f9ffbd")
				vars.buttons_list[elem].configure(fg="red")
				vars.input_text = False

			else:
				self.set_unclicked(elem)
			
			


	def set_unclicked(self, Id):
		
		vars.buttons_list[Id].configure(bg="white")
		vars.buttons_list[Id].configure(fg="black")
		

		try:
			self.canvas.delete(self.master.textbox)
		except:
			pass



	def set_pencil(self):
		
		print("PENCIL")
		if vars.draw_Item == vars.draw_Item_list[0]:
			vars.draw_Item = None
			self.set_unclicked(vars.draw_Item_list[0])
		else:
			vars.draw_Item = vars.draw_Item_list[0]
			self.set_config_buttons()

	def set_rectangle(self):
		
		if vars.draw_Item == vars.draw_Item_list[1]:
			vars.draw_Item = None
			self.set_unclicked(vars.draw_Item_list[1])
			
		else:
			vars.draw_Item = vars.draw_Item_list[1]
			self.set_config_buttons()
	
	def set_rectangle_frame(self):

		
		if vars.draw_Item == vars.draw_Item_list[2]:
			vars.draw_Item = None
			self.set_unclicked(vars.draw_Item_list[2])
		else:
			vars.draw_Item = vars.draw_Item_list[2]
			self.set_config_buttons()

	def set_oval(self):
		
		if vars.draw_Item == vars.draw_Item_list[3]:
			vars.draw_Item = None
			self.set_unclicked(vars.draw_Item_list[3])
		else:
			vars.draw_Item = vars.draw_Item_list[3]
			self.set_config_buttons()

	def set_oval_filled(self):
		
		if vars.draw_Item == vars.draw_Item_list[4]:
			vars.draw_Item = None
			self.set_unclicked(vars.draw_Item_list[4])
		else:
			vars.draw_Item = vars.draw_Item_list[4]
			self.set_config_buttons()



	def set_color_picker(self):
		
		if vars.draw_Item == vars.draw_Item_list[5]:
			vars.draw_Item = None
			self.set_unclicked(vars.draw_Item_list[5])
		else:
			vars.draw_Item = vars.draw_Item_list[5]
			self.set_config_buttons()

	def set_text(self):
		
		# vars.input_text = True

		if vars.draw_Item == vars.draw_Item_list[6]:
			
			self.canvas.delete(vars.textBoxFrame)
			text_font = 0
			vars.total_text = ""
			
			tmp = []
			tmp.append(vars.text_object)
			self.canvas.undoList.append(tmp)
			
			vars.text_object = None
			vars.draw_Item = None

			self.set_unclicked(vars.draw_Item_list[6])
			
		else:
			vars.draw_Item = vars.draw_Item_list[6]
			self.set_config_buttons()