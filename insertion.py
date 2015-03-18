#!/usr/bin/python

import drawing
import pygame
import random
import sys

pygame.init()

def simpleDraw(l, ll, s=[]):
	global a
	global screen
	global time
	drawing.drawArray(screen, a, color=blu, highlight=l, hlcolors=ll, swap=s)
	pygame.display.flip()
	pygame.time.delay(time)

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Insertion sort")
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
grigio = pygame.Color("#dddddd")

time = 300

for i in range(len(a)):
	screen.fill(grigio)
	simpleDraw([i], [verde])
	if pygame.event.Event(pygame.QUIT) in pygame.event.get():
		pygame.quit()
		sys.exit()
	while i > 0 and a[i] < a[i-1]:
		screen.fill(grigio)
		simpleDraw([i, i-1], [verde, giallo], s=[i,i-1])
		a[i], a[i-1] = a[i-1], a[i]
		i -= 1


screen.fill(grigio)
simpleDraw([], [])
pygame.display.flip()

#Clear event queue
pygame.event.get()

while 1:
	if pygame.event.Event(pygame.QUIT) in pygame.event.get():
		pygame.quit()
		sys.exit()
	pygame.time.delay(50)
