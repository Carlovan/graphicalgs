import sys
import pygame
from pygame import gfxdraw
import math

pygame.init()
pygame.font.init()

#Used to render text
_font = pygame.font.SysFont("arial", 50)

class Node:
	'''Class to represent a node in a graph'''
	def __init__(self, name, x, y, size=30):
		'''name:	the label of the node
		   x:			x coordinate when drawing
		   y:			y coordinate when drawing
		   size:	diameter of the circle when drawing'''

		if not isinstance(x, int) or not isinstance(y, int):
			raise TypeError, "coordinates must be integers"
		if not isinstance(size, int):
			raise TypeError, "size must be an integer"
		self.name = str(name)
		self.x = x
		self.y = y
		self.size = size
	def draw(self, screen, color, width=2):
		'''Draws a Node object on the Surface, as a anti-aliased circle with its name inside.
		Returns the rectangle to be udpdated.'''
		if not isinstance(screen, pygame.Surface):
			raise TypeError, "you must give a Surface object"
		if not isinstance(width, int) or width < 1:
			raise TypeError("width must be an integer > 0")

		#Rectangle to be updated
		to_update = pygame.Rect(0,0,size,size)
		to_update.center = (x, y)

		#Node coordinates
		x = self.x
		y = self.y
		#Text inside the node
		text = self.name
		#Node size
		size = self.size
		#Draw the anti-aliasing circle (mutliple for line width)
		for i in range(width):
			pygame.gfxdraw.aacircle(screen, x, y, size/2-i, color)
		#Render the text very big
		txt = _font.render(str(text), True, color)
		#Get text size
		txtW = txt.get_width()
		txtH = txt.get_height()
		#Size inside the circle
		tempTxtSize = size*3/4
		#Get the bigger dimension of the text and calculate new dimensions to fit inside the circle
		#and with same rate
		if txtW > txtH:
			txtH = tempTxtSize*txtH/txtW
			txtW = tempTxtSize
		else:
			txtW = tempTxtSize*txtW/txtH
			txtH = tempTxtSize
		#Scale the text to calculated size
		txt = pygame.transform.smoothscale(txt, (txtW, txtH))
		#Draw the text on the surface inside the circle
		screen.blit(txt, (x-txtW/2, y-txtH/2))
		return to_update

class Edge:
	'''A class to represent an edge in a graph'''
	def __init__(self, nodeFrom, nodeTo, weight=-1):
		'''nodeFrom, nodeTo:	the starting and arriving nodes (Node objects)
			weight:					the weight of the edge (in case of weighted graph'''
		if not isinstance(nodeFrom, Node) or not isinstance(nodeTo, Node):
			raise TypeError, "required Node"
		if not isinstance(weight, int):
			raise TypeError, "required int"

		self.nodeFrom = nodeFrom
		self.nodeTo = nodeTo
		self.weight = weight

	def draw(self, screen, color, width=2, directed=False, weighted=False):
		'''Draws the Edge on the Surface with the specified color.
		Returns the ractangle to be updated'''
		if not isinstance(screen, pygame.Surface):
			raise TypeError, "required a pygame.Surface object"

		#The slope of the line
		tan = float(self.nodeTo.y-self.nodeFrom.y)/float(self.nodeTo.x-self.nodeFrom.x)

		#Angle of the line with y=0
		angle = math.atan(tan) + (math.pi if self.nodeTo.x < self.nodeFrom.x else 0)

		#Debug
		#print "angle {1} tan {0} cos {2} sin {3}".format(tan, math.degrees(angle), math.cos(angle), math.sin(angle))

		#Starting point
		startx = int(self.nodeFrom.x+math.cos(angle)*float(self.nodeFrom.size/2))
		starty = int(self.nodeFrom.y+math.sin(angle)*float(self.nodeFrom.size/2))

		#Ending point
		endx = int(self.nodeTo.x-math.cos(angle)*(self.nodeTo.size/2))
		endy = int(self.nodeTo.y-math.sin(angle)*(self.nodeTo.size/2))

		#Draw the line
		return pygame.draw.line(screen, color, (startx, starty), (endx, endy), width)

class Graph:
	'''Represent a graph, with nodes and edges'''
	def __init__(self, edges, directed=False, weighted=False):
		'''edges: a list of Edges'''
		if not isinstance(edges, (list, tuple)):
			raise TypeError, "required a list for the edges"
		if not all(isinstance(x, Edge) for x in edges):
			raise TypeError, "required a list of Edges"
		if not isinstance(directed, bool):
			raise TypeError, "required a bool for directed graph"
		if not isinstance(weighted, bool):
			raise TypeError, "required a bool for wieghted graph"

		self.edges = edges
		self.nodes = list(set(list(x.nodeFrom for x in edges) + list(x.nodeTo for x in edges)))
		self.directed = directed
		self.weighted = weighted

	def genAdjList(self):
		'''Generates an adjacent list as a dictionary indexed with the nodes' labels'''
		adj = {}
		for x in self.nodes:
			adj[x.name] = []

		#Add edges
		for x in self.edges:
			if self.weighted:
				adj[x.nodeFrom.name].append((x.nodeTo.weight, x.nodeTo.name))
				if not self.directed:
					adj[x.nodeTo.name].append((x.nodeFrom.weight, x.nodeFrom.name))
			else:
				adj[x.nodeFrom.name].append(x.nodeTo.name)
				if not self.directed:
					adj[x.nodeTo.name].append(x.nodeFrom.name)

		return adj

	def draw(self, screen, color, highlight=[], hlcolors=[]):
		'''Draws every Node and Edge in the Graph.
		   You can specify in the list highlight the nodes you want to highlight with a different color.
		   You can specify colors in hlcolors.
		   highlight[i] will be draw with color hlcolor[i]
		   If len(highlight) > len(hlcolors) the overflow nodes will be drawed with the last color (hlcolors[-1]).
		   Returns the list of the rectangle to be updated'''
		if not isinstance(highlight, (list, tuple)) or not isinstance(hlcolors, (list, tuple)):
			raise TypeError, "required a list or tuple"
		elif len(highlight) != len(hlcolors):
			raise ValueError, "highlight and hlcolors arguments must have the same dimension"
		#Converts to string
		map(str, highlight)

		#Rects to be updated
		to_update = []

		#Call the draw function for every edge
		for e in self.edges:
			to_update.append(e.draw(surf, color))
		#Call the draw function for every node
		for n in self.nodes:
			#Check if to be highlighted
			if n.name in highlight:
				to_update.append(n.draw(screen, hlcolors[highlight.index(n.name)]))
			else:
				to_update.append(n.draw(screen, color))
		return to_update


def _swap(screen, rect1, rect2, color1, color2, time, fps=25):
	'''This is an internal function to swap two rects'''

	#Refresh the screen
	pygame.display.flip()

	#If rect1 and rect2 are the same rect just draw it and wait
	#print rect1
	#print rect2
	if rect1.left == rect2.left and rect1.top == rect2.top and rect1.width == rect2.width and rect1.height == rect2.height:
		drawn_rect = pygame.draw.rect(screen, color1, rect1)
		#Update just the drawn rectangle
		pygame.display.update(drawn_rect)
		pygame.time.sleep(time)
		return

	#Saves the current surface
	surfTemp = screen.copy()
	rect1Temp = rect1.copy()
	rect2Temp = rect2.copy()

	#Total animation frames
	totFrames = int(fps*time)+1
	#Horizontal movement
	offsetX = rect1.left-rect2.left
	stepX = float(offsetX)/totFrames
	#Vertical movement
	offsetY = rect1.bottom-rect2.bottom
	stepY = float(offsetY)/totFrames

	#Rect to update on the screen
	to_update = []

	#Object for timing
	clock = pygame.time.Clock()
	#Iterate for every frame
	for i in range(totFrames+1):
		#Limit framerate
		clock.tick(fps)
		#Reset the surface and rectangles
		screen.blit(surfTemp, (0,0))
		rect1 = rect1Temp.copy()
		rect2 = rect2Temp.copy()
		#Set rectangles position to the current frame
		rect1.left -= int(stepX*i)
		rect1.bottom -= int(stepY*i)
		rect2.left += int(stepX*i)
		rect2.bottom += int(stepY*i)
		#Draws the frame
		to_update.append(pygame.draw.rect(screen, color1, rect1))
		to_update.append(pygame.draw.rect(screen, color2, rect2))
		#Refresh just the old rectangle (erase) and new (draw)
		pygame.display.update(to_update)
		#pygame.display.flip()
		#Remove the old ractangles
		to_update = to_update[-2:]

def drawArray(screen, array, color=(0,0,0), horizontal=False, highlight=[], hlcolors=[], swap=[], swap_time=500):
	'''This function draws on a Surface the content of a list of integers as rectangles.
	   You can specify in the list highlight the elements you want to highlight with a different color.
	   You can specify colors in hlcolors.
	   highlight[i] willbe drawed with color hlcolor[i]
	   If len(highlight) > len(hlcolors) the overflow nodes will be drawed with the last color (hlcolors[-1]).
	   horizontal is a bool to specify if you want horizontal rectangle instead of vertical.
	   swap is a list; it can contain 2 elements to swap. You can specify the swap time with the swap_time argument (in ms).
	   Returns the list of the rects to be updated.'''
	#Check arguments type
	if not isinstance(array, (list,tuple)):
		raise TypeError, "required a list or tuple"
	#if not _is_color(color):
	#	raise ValueError, "invalid color"
	for el in array:
		if not isinstance(el, int):
			raise TypeError, "required an integer"

	if not isinstance(screen, pygame.Surface):
		raise TypeError, "required a pygame.Surface object"

	if not isinstance(horizontal, bool):
		raise TypeError, "required bool"

	if not isinstance(highlight, list) or not isinstance(hlcolors, list):
		raise TypeError, "required a list"

	if not (isinstance(swap, (list, tuple)) and (len(swap) != 0 or len(swap) != 2)):
		raise TypeError, "swap must be a two elements list or tuple"

	if not isinstance(swap_time, int):
		raise TypeError, "swaptime must be an integer (milliseconds)"

	if len(swap) == 2 and (swap[0] == swap[1]):
		swap = []

	#Rectangles to update
	to_update = []

	#Surface dimensions
	if not horizontal:
		surfH = screen.get_height()
		surfW = screen.get_width()
	else:
		surfW = screen.get_height()
		surfH = screen.get_width()

	#Calculate maximum value in list
	maxVal = max(array)

	#Max height of the rectangle (15px blank on top)
	#The height of every rect is calculated using -> maxVal : maxHeight = actualVal : x -> x = (maxHeigh * actualVal)/maxVal
	maxHeight = (surfH - 15)

	#Width of every rectangle
	rectWidth = surfW/len(array)
	#Space between two rectangles
	spaceWidth = rectWidth/10

	toSwap = []

	#Iterate over the array
	for i in range(len(array)):
		#Calculate the height of the current element
		actualHeight = (maxHeight*array[i])/maxVal
		#Current elements size and position
		rectx = rectWidth*i+(spaceWidth/2)
		rectw = rectWidth-spaceWidth
		recth = actualHeight
		rect = 0
		if not horizontal:
			rect = pygame.Rect(rectx, 0, rectw, recth)
			rect.bottom = surfH
		else:
			rect = pygame.Rect(0, rectx, recth, rectw)
			rect.left = 0
		#Draw the current element if not to swap
		if i not in swap:
			#The color used to draw the element
			el_color = 0
			#If it's highlighted
			if i in highlight:
				#Select the color
				temp_index = highlight.index(i) if highlight.index(i) < len(hlcolors) else len(hlcolors)-1
				el_color = hlcolors[temp_index]
			else:
				el_color = color
			#Draw the rectangle
			to_update.append(pygame.draw.rect(screen, el_color, rect))
		#If to swap
		else:
			#Add the element's RECTANGLE to the list (and doesn't draw it)
			toSwap.append(rect)
	#If there are some elements to swap
	if(len(toSwap) == 2):
		#Select the colors
		c1 = (hlcolors[highlight.index(swap[0])] if swap[0] in highlight else color)
		c2 = (hlcolors[highlight.index(swap[1])] if swap[1] in highlight else color)
		#Animate the swap
		_swap(screen, toSwap[0], toSwap[1], c1, c2, swap_time/1000.0)
	return to_update
