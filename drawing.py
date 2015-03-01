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
		if not _is_type(x, int) or not _is_type(y, int):
			raise TypeError, "coordinates must be integers"
		if not _is_type(size, int):
			raise TypeError, "size must be an integer"
		self.name = name
		self.x = x
		self.y = y
		self.size = size

class Edge:
	'''A class to represent an edge in a graph'''
	def __init__(self, node1, node2, weight=-1, directed=False):
		if not _is_type(node1, Node) or not _is_type(node2, Node):
			raise TypeError, "required Node"
		if not _is_type(weight, int):
			raise TypeError, "required int"
		if not _is_type(directed, bool):
			raise TypeError, "required bool"

		self.nodeFrom = node1
		self.nodeTo = node2
		self.weight = weight
		self.directed = directed

def _check_color(a):
	if not _is_type(a, list) and not _is_type(a, tuple):
		raise TypeError, "required a list or tuple object"
	if len(a) != 3:
		raise ValueError, "the color must be (R, G, B)"

def _is_type(a, t):
	if type(t) != type:
		raise TypeError
	return type(a) == t

def _is_color(a):

	return ((_is_type(a, list) or _is_type(a, list)) and len(a) == 3 and (_is_type(a[0], int) and _is_type(a[1], int) and _is_type(a[2], int)))

def drawArray(screen, array, color=(0,0,0), horizontal=False, highlight=[], hlcolors=[]):
	'''This function draws on a Surface the content of a list of integers as rectangles.
	highlight is a list that contains the indices of the elements you want to highlight.
	hlcolors is a list that contains the color to highlighting'''
	#Check arguments type
	if not _is_type(array, list) and not _is_type(array, tuple):
		raise TypeError, "required a list or tuple"
	#if not _is_color(color):
	#	raise ValueError, "invalid color"
	for el in array:
		if not _is_type(el, int):
			raise TypeError, "required an integer"

	if not _is_type(screen, pygame.Surface):
		raise TypeError, "required a pygame.Surface object"

	if not _is_type(horizontal, bool):
		raise TypeError, "required bool"
	if not _is_type(highlight, list) or not _is_type(hlcolors, list):
		raise TypeError, "required a list"
	if len(highlight) != len(hlcolors):
		raise ValueError, "'highlight' and 'hlcolors' must have the same number of elements"

	_check_color(color)

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
		if i in highlight:
			pygame.draw.rect(screen, hlcolors[highlight.index(i)], rect)
		else:
			pygame.draw.rect(screen, color, rect)

def drawNode(screen, obj, color=(0,0,0)):
	'''Draws a Node object on the Surface, as a circle with text inside'''
	if not _is_type(obj, Node):
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
