#!/usr/bin/python

import graphicalgs
import pygame
import random
import sys

pygame.init()

def simpleDraw(l, ll):
	global a
	global screen
	graphicalgs.drawArray(screen, a, color=(255,0,0), highlight=l, hlcolors=ll)
	pygame.display.flip()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Bubble sort")
screen.fill((255,255,255))
pygame.display.flip()

a = range(1,10)
random.shuffle(a)

bianco = (255,255,255)
nero = (0,0,0)
rosso = (255,0,0)
verde = (0,255,0)
blu = (0,0,255)
giallo = (255,255,0)

time = 300

for i in range(len(a)-1, 1, -1):
	j = 0
	scambiato = False
	while j < i:
		if pygame.event.Event(pygame.QUIT) in pygame.event.get():
			pygame.quit()
			sys.exit()
		screen.fill(bianco)
		simpleDraw([j], [giallo])
		pygame.time.delay(time)
		simpleDraw([j, j+1], [giallo,blu])
		pygame.time.delay(time)
		if a[j] > a[j+1]:
			simpleDraw([j, j+1], [giallo,verde])
			pygame.time.delay(time)
			scambiato = True
			temp = a[j]
			a[j] = a[j+1]
			a[j+1] = temp
		j += 1
	if scambiato == False:
		break


screen.fill((255,255,255))
graphicalgs.drawArray(screen, a, color=(255,0,0))
pygame.display.flip()

while 1:
	if pygame.event.Event(pygame.QUIT) in pygame.event.get():
		pygame.quit()
		sys.exit()
	pygame.time.delay(50)
