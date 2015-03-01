#!/usr/bin/python

import drawing
import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))

temp = raw_input("inserisci dei numeri: ").split()

a = []
for i in temp:
	a.append(int(i))
drawing.drawArray(screen, a, color=(255,0,0), horizontal=True)
pygame.display.flip()

pygame.time.delay(3000)

n1 = drawing.Node(1, 100, 100)
n2 = drawing.Node(2, 100, 200, 40)

drawing.drawNode(screen, n1)
drawing.drawNode(screen, n2)
pygame.display.flip()

pygame.time.delay(3000)

pygame.quit()