#!/usr/bin/python

import drawing
import pygame

pygame.init()

screen = pygame.display.set_mode((400, 500))
#pygame.display.set_caption("Bubble sort")
screen.fill((255,255,255))
pygame.display.flip()

a = [1, 5, 3, 8, 6, 2, 9, 4]

for i in range(len(a)-1, 1, -1):
	j = 0
	while j < i:
		screen.fill((255,255,255))
		drawing.drawArray(screen, a, color=(255,0,0), highlight=[j], hlcolors=[(0,255,0)])
		pygame.display.flip()
		pygame.time.delay(1000)
		if a[j] > a[j+1]:
			temp = a[j]
			a[j] = a[j+1]
			a[j+1] = temp
		j += 1


drawing.drawArray(screen, a, color=(255,0,0))
pygame.display.flip()

pygame.time.delay(1000)

pygame.quit()