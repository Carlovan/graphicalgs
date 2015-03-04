#!/usr/bin/python

import drawing
import pygame
import random
import sys

pygame.init()

def simpleDraw(l, ll):
	global a
	global screen
	drawing.drawArray(screen, a, color=blu, highlight=l, hlcolors=ll)
	pygame.display.flip()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Selection sort")
screen.fill((255,255,255))
pygame.display.flip()

maxN = 10

a = range(1,maxN)
random.shuffle(a)

bianco = (255,255,255)
nero = (0,0,0)
rosso = (255,0,0)
verde = (0,255,0)
blu = (0,0,255)
giallo = (255,255,0)

time = 500

for i in range(len(a)-1):
	minVal = maxN
	minInd = 0
	for j in range(i, len(a)):
		if pygame.event.Event(pygame.QUIT) in pygame.event.get():
			pygame.quit()
			sys.exit()

		if a[j] < minVal:
			minVal = a[j]
			minInd = j
		screen.fill(pygame.Color("#dddddd"))
		simpleDraw([minInd, j, i], [rosso, verde, giallo])
		pygame.time.delay(time)
	temp = a[i]
	a[i] = a[minInd]
	a[minInd] = temp


screen.fill((255,255,255))
drawing.drawArray(screen, a, color=(255,0,0), swap=[0, 5])
pygame.display.flip()

while 1:
	if pygame.event.Event(pygame.QUIT) in pygame.event.get():
		pygame.quit()
		sys.exit()
	pygame.time.delay(50)
