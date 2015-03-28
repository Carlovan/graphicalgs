import sys
import pygame
from pygame import gfxdraw
import math

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("arial", 50)

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
	def draw(self, screen, color):
		'''Draws a Node object on the Surface, as a circle with its name inside'''
		if not isinstance(screen, pygame.Surface):
			raise TypeError, "you must give a Surface object"

		#Node coordinates
		x = self.x
		y = self.y
		#Text inside the node
		text = self.name
		#Node size
		size = self.size
		#Draw the anti-aliasing circle (double for line width)
		pygame.gfxdraw.aacircle(screen, x, y, size/2, color)
		pygame.gfxdraw.aacircle(screen, x, y, size/2-1, color)
		#Render the text very big
		txt = font.render(str(text), True, color)
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

class Edge:
	'''A class to represent an edge in a graph'''
	def __init__(self, node1, node2, weight=-1):
		'''node1, node2:	the starting and arriving nodes (Node objects)
			weight:					the weight of the edge (in case of weighted graph'''
		if not isinstance(node1, Node) or not isinstance(node2, Node):
			raise TypeError, "required Node"
		if not isinstance(weight, int):
			raise TypeError, "required int"

		self.nodeFrom = node1
		self.nodeTo = node2
		self.weight = weight

	def draw(self, surf, color, directed=False, weighted=False):
		'''Draws the Edge on the Surface with the specified color'''
		#The slope of the line
		tan = float(self.nodeTo.y-self.nodeFrom.y)/float(self.nodeTo.x-self.nodeFrom.x)

		#Angle of the line with y=0
		angle = math.atan(tan) + (math.pi if self.nodeTo.x < self.nodeFrom.x else 0)
		
		print "angle {1} tan {0} cos {2} sin {3}".format(tan, math.degrees(angle), math.cos(angle), math.sin(angle))

		#Starting point
		startx = int(self.nodeFrom.x+math.cos(angle)*float(self.nodeFrom.size/2))
		starty = int(self.nodeFrom.y+math.sin(angle)*float(self.nodeFrom.size/2))

		#Ending point
		endx = int(self.nodeTo.x-math.cos(angle)*(self.nodeTo.size/2))
		endy = int(self.nodeTo.y-math.sin(angle)*(self.nodeTo.size/2))

		#Draw the line
		pygame.draw.line(surf, color, (startx, starty), (endx, endy), 3)


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

	def draw(self, surf, color, highlight=[], hlcolors=[]):
		'''Draws every Node and Edge in the Graph.
		   You can specify in the list highlight the nodes you want to highlight with a different color.
		   You can specify colors in hlcolors.
		   highlight[i] willbe drawed with color hlcolor[i]
		   If len(highlight) > len(hlcolors) the overflow nodes will be drawed with the last color (hlcolors[-1]).'''
		if not isinstance(highlight, (list, tuple)) or not isinstance(hlcolors, (list, tuple)):
			raise TypeError, "required a list or tuple"
		elif len(highlight) != len(hlcolors):
			raise ValueError, "highlight and hlcolors arguments must have the same dimension"
		for i in range(len(highlight)):
			highlight[i] = str(highlight[i])
		for e in self.edges:
			e.draw(surf, color)
		for n in self.nodes:
			if n.name in highlight:
				n.draw(surf, hlcolors[highlight.index(n.name)])
			else:
				n.draw(surf, color)


def _swap(surf, rect1, rect2, color1, color2, time, fps=25):
	'''This is an internal function to swap two rects'''
	surfTemp = surf.copy()
	rect1Temp = rect1.copy()
	rect2Temp = rect2.copy()

	totFrames = int(fps*time)+1
	offsetX = rect1.left-rect2.left
	stepX = float(offsetX)/totFrames
	offsetY = rect1.bottom-rect2.bottom
	stepY = float(offsetY)/totFrames

	clock = pygame.time.Clock()
	for i in range(totFrames+1):
		clock.tick(fps)
		surf.blit(surfTemp, (0,0))
		rect1 = rect1Temp.copy()
		rect2 = rect2Temp.copy()
		rect1.left -= int(stepX*i)
		rect1.bottom -= int(stepY*i)
		rect2.left += int(stepX*i)
		rect2.bottom += int(stepY*i)
		pygame.draw.rect(surf, color1, rect1)
		pygame.draw.rect(surf, color2, rect2)
		pygame.display.flip()


def drawArray(screen, array, color=(0,0,0), horizontal=False, highlight=[], hlcolors=[], swap=[], swap_time=500):
	'''This function draws on a Surface the content of a list of integers as rectangles.
	   You can specify in the list highlight the elements you want to highlight with a different color.
	   You can specify colors in hlcolors.
	   highlight[i] willbe drawed with color hlcolor[i]
	   If len(highlight) > len(hlcolors) the overflow nodes will be drawed with the last color (hlcolors[-1]).
	   horizontal is a bool to spacify if you want horizontal rectangle instead of vertical.
	   swap is a list; it can contain 2 elements to swap. You can specify the swap time with the swap_time argument (in ms).'''
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
	#if len(highlight) != len(hlcolors):
	#	raise ValueError, "'highlight' and 'hlcolors' must have the same number of elements"
	if not isinstance(swap_time, int):
		raise TypeError, "swaptime must be an integer (milliseconds)"

	#Surface dimensions
	if not horizontal:
		surfH = screen.get_height()
		surfW = screen.get_width()
	else:
		surfW = screen.get_height()
		surfH = screen.get_width()

	#Calculate maximum and minimum value in list
	maxVal = max(array)

	#Max height of the rectangle (15px blank on top)
	#The height of every rect is calculated using -> maxVal : maxHeight = actualVal : x -> x = (maxHeigh * actualVal)/maxVal
	maxHeight = (surfH - 15)

	#Width of every rectangle
	rectWidth = surfW/len(array)
	#Space between two rectangles
	spaceWidth = rectWidth/10

	toSwap = []

	for i in range(len(array)):
		actualHeight = (maxHeight*array[i])/maxVal
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
		if i not in swap:
			if i in highlight:
				temp_index = highlight.index(i) if highlight.index(i) < len(hlcolors) else len(hlcolors)-1
				pygame.draw.rect(screen, hlcolors[temp_index], rect)
			else:
				pygame.draw.rect(screen, color, rect)
		else:
			toSwap.append(rect)
	if(len(toSwap) == 2):
		c1 = (hlcolors[highlight.index(swap[0])] if swap[0] in highlight else color)
		c2 = (hlcolors[highlight.index(swap[1])] if swap[1] in highlight else color)
		_swap(screen, toSwap[0], toSwap[1], c1, c2, swap_time/1000.0)


