#!/usr/bin/python

import graphicalgs
import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))

temp = raw_input("inserisci dei numeri: ").split()

a = []
for i in temp:
	a.append(int(i))
graphicalgs.drawArray(screen, a, color=(255,0,0), horizontal=True)
pygame.display.flip()

pygame.time.delay(3000)

n1 = graphicalgs.Node(1, 100, 100)
n2 = graphicalgs.Node(2, 100, 200, 40)

graphicalgs.drawNode(screen, n1)
graphicalgs.drawNode(screen, n2)
pygame.display.flip()

pygame.time.delay(3000)

pygame.quit()