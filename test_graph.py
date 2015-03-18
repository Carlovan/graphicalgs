#!/usr/bin/python

from drawing import *

pygame.init()

screen = pygame.display.set_mode((400, 300))

bianco = (255, 255, 255)
rosso = (255, 0, 0)

n1 = Node(1, 10, 10, 20)
n2 = Node(2, 150, 60, 20)
n3 = Node(3, 100, 100, 20)
e2 = Edge(n1, n2)
e1 = Edge(n3, n1)
g1 = Graph([e1, e2])

screen.fill(bianco)

g1.draw(screen, rosso, highlight=[1], hlcolors=[(0,255,0)])

pygame.display.flip()

pygame.time.delay(3000)
pygame.quit()