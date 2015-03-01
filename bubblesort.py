#!/usr/bin/python

import drawing
import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1000, 500))
#pygame.display.set_caption("Bubble sort")
screen.fill((255,255,255))
pygame.display.flip()

a = range(1,50)
random.shuffle(a)

for i in range(len(a)-1, 1, -1):
	j = 0
	scambiato = False
	while j < i:
		screen.fill((255,255,255))
		drawing.drawArray(screen, a, color=(255,0,0), highlight=[j], hlcolors=[(0,255,0)])
		pygame.display.flip()
		pygame.time.delay(10)
		if a[j] > a[j+1]:
			scambiato = True
			temp = a[j]
			a[j] = a[j+1]
			a[j+1] = temp
		j += 1
	if scambiato == False:
		break


screen.fill((255,255,255))
drawing.drawArray(screen, a, color=(255,0,0))
pygame.display.flip()

pygame.time.delay(1000)

pygame.quit()