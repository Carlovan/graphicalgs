#!/usr/bin/python2

import graphicalgs
import pygame

pygame.init()

s = pygame.display.set_mode((400, 400))

clock = pygame.time.Clock()

rect1 = pygame.Rect(0, 0, 10, 10)
rect2 = pygame.Rect(390, 390, 10, 10)


s.fill((255,255,255))

pygame.draw.rect(s, (0,0,255), (10, 10, 100, 100))


clock.tick()

graphicalgs._swap(s, rect1, rect2, (255,0,0), (0,255,0), .5, 1000)

clock.tick()

print clock.get_time()

pygame.time.delay(1000)

pygame.quit()