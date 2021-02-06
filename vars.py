import screeninfo


global text_object
global textBoxFrame 
global total_text
global input_text
global buttons_list 
global maxLineWidth 
global coords 
global last_coords 
global draw_Item 
global draw_Item_list 
global sidebarWidth
global sidebarHeight
global pencilDraw 

pencilDraw = None

sidebarHeight = int((screeninfo.get_monitors()[0].height *2) / 100)
sidebarWidth = int((screeninfo.get_monitors()[0].width *3) / 150)

draw_Item_list = list()
draw_Item = 0


text_object = None
textBoxFrame = None
total_text = " "
input_text = False

buttons_list = dict()
maxLineWidth = 50

coords = (0,0)
last_coords = (None,None)
