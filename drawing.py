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
		if not isinstance(x, int) or not isinstance(y, int):
			raise TypeError, "coordinates must be integers"
		if not isinstance(size, int):
			raise TypeError, "size must be an integer"
		self.name = str(name)
		self.x = x
		self.y = y
		self.size = size

class Edge:
	'''A class to represent an edge in a graph'''
	def __init__(self, node1, node2, weight=-1):
		if not isinstance(node1, Node) or not isinstance(node2, Node):
			raise TypeError, "required Node"
		if not isinstance(weight, int):
			raise TypeError, "required int"

		self.nodeFrom = node1
		self.nodeTo = node2
		self.weight = weight

class Graph:
	def __init__(self, edges, directed=False, weighted=False):
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
		#Gen an empty list for every node
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


def _swap(surf, rect1, rect2, color1, color2, time, fps=25):
	surfTemp = surf.copy()
	rect1Temp = rect1.copy()
	rect2Temp = rect2.copy()

	totFrames = int(fps*time)
	offsetX = rect1.left-rect2.left
	stepX = float(offsetX)/totFrames
	offsetY = rect1.top-rect2.top
	stepY = float(offsetY)/totFrames
	print offsetX, stepX, offsetY, stepY

	clock = pygame.time.Clock()
	for i in range(totFrames+1):
		clock.tick(fps)
		surf.blit(surfTemp, (0,0))
		rect1 = rect1Temp.copy()
		rect2 = rect2Temp.copy()
		rect1.left -= int(stepX*i)
		rect1.top -= int(stepY*i)
		rect2.left += int(stepX*i)
		rect2.top += int(stepY*i)
		pygame.draw.rect(surf, color1, rect1)
		pygame.draw.rect(surf, color2, rect2)
		pygame.display.flip()
	print rect1, rect2


def drawArray(screen, array, color=(0,0,0), horizontal=False, highlight=[], hlcolors=[], swap=[]):
	'''This function draws on a Surface the content of a list of integers as rectangles.
	highlight is a list that contains the indices of the elements you want to highlight.
	hlcolors is a list that contains the color to highlighting'''
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
	if len(highlight) != len(hlcolors):
		raise ValueError, "'highlight' and 'hlcolors' must have the same number of elements"

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
				pygame.draw.rect(screen, hlcolors[highlight.index(i)], rect)
			else:
				pygame.draw.rect(screen, color, rect)
		else:
			swap[swap.index(i)] = rect
	if(len(swap) == 2):
		_swap(screen, swap[0], swap[1], color, color, 10)

def drawNode(screen, obj, color=(0,0,0)):
	'''Draws a Node object on the Surface, as a circle with text inside'''
	if not isinstance(obj, Node):
		raise TypeError, "you must give a Node object"
	if not _is_color(color):
		raise ValueError, "invalid color"

	#Node coordinates
	x = obj.x
	y = obj.y
	#Text inside the node
	text = obj.name
	#Node size
	size = obj.size
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
