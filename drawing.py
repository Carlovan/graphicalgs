import sys
import pygame
from pygame import gfxdraw

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("arial", 50)

class Node:
	def __init__(self, name, x, y, size=30):
		self.name = name
		self.x = x
		self.y = y
		self.size = size

def _check_color(a):
	if not _is_type(a, list) and not _is_type(a, tuple):
		raise TypeError, "required a list or tuple object"
	if len(a) != 3:
		raise ValueError, "the color must be (R, G, B)"

def _is_type(a, t):
	if type(t) != type:
		raise TypeError
	return type(a) == t

def drawArray(screen, array, color=(0,0,0), horizontal=False, highlight=[], hlcolors=[]):
	'''This function draws on a Surface the content of a list of integers as rectangles.'''
	#Check arguments type
	if not _is_type(array, list) and not _is_type(array, tuple):
		raise TypeError, "required a list or tuple"

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
	x = obj.x
	y = obj.y
	text = obj.name
	size = obj.size
	pygame.gfxdraw.aacircle(screen, x, y, size/2, color)
	pygame.gfxdraw.aacircle(screen, x, y, size/2-1, color)
	txt = font.render(str(text), True, color)
	txtW = txt.get_width()
	txtH = txt.get_height()
	tempTxtSize = size*3/4
	if txtW > txtH:
		txtH = tempTxtSize*txtH/txtW
		txtW = tempTxtSize
	else:
		txtW = tempTxtSize*txtW/txtH
		txtH = tempTxtSize
	txt = pygame.transform.smoothscale(txt, (txtW, txtH))
	screen.blit(txt, (x-txtW/2, y-txtH/2))

def drawLine(screen, vertical, pos, color=(0,0,0)):
	if vertical:
		pygame.gfxdraw.vline(screen, pos, 0, screen.get_height(), color)
	else:
		pygame.gfxdraw.vline(screen, pos, 0, screen.get_width(), color)