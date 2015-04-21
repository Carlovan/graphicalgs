#!/usr/bin/python2

import graphicalgs
import pygame
import random
import sys

pygame.init()

def simpleDraw(l, ll, s=[]):
	global a
	global screen
	global time
	graphicalgs.drawArray(screen, a, color=blu, highlight=l, hlcolors=ll, swap=s)
	pygame.display.flip()
	pygame.time.delay(time)

win_w = 1000
win_h = 500

screen = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("Insertion sort")
screen.fill((255,255,255))
pygame.display.flip()

maxN = 30

a = range(1,maxN)
random.shuffle(a)

bianco = (255,255,255)
nero = (0,0,0)
rosso = (255,0,0)
verde = (0,255,0)
blu = (0,0,255)
giallo = (255,255,0)
grigio = pygame.Color("#dddddd")

time = 10

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
smile = pygame.image.load("smile.png")
screen.blit(smile, ((win_w-smile.get_width())/2,(win_h-smile.get_height())/2))
pygame.display.flip()

#Clear event queue
pygame.event.get()

while 1:
	if pygame.event.Event(pygame.QUIT) in pygame.event.get():
		pygame.quit()
		sys.exit()
	pygame.time.delay(50)
