#!/usr/bin/python

import graphicalgs
import pygame
import random
import sys

def simpleDraw(l, ll, s=[]):
	global a
	global screen
	global frame_time
	graphicalgs.drawArray(screen, a, color=blu, highlight=l, hlcolors=ll, swap=s)
	pygame.display.flip()
	pygame.time.delay(frame_time)


win_h = 500
win_w = 1000
screen = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("Shell sort")
screen.fill((255,255,255))
pygame.display.flip()

maxN = 100

'''	0 random
		1 inverse
		2 sorted
'''
init_state = 1


#Random
if init_state == 0:
	a = range(1,maxN)
	random.shuffle(a)
elif init_state == 1:
	#Inverse
	a = range(maxN-1, 0, -1)
elif init_state == 2:
	#Sorted
	a = range(1, maxN)

bianco = (255,255,255)
nero = (0,0,0)
rosso = (255,0,0)
verde = (0,255,0)
blu = (0,0,255)
giallo = (255,255,0)
grigio = pygame.Color("#dddddd")
grigio_scuro = pygame.Color("#aaaaaa")

frame_time = 0

passo = maxN/2
esci = False
while not esci:
	if passo == 1:
		esci = True
	scambiato = False
	for i in range(passo):
		evidenziati = list(range(i, len(a), passo))
		screen.fill(grigio)
		graphicalgs.drawArray(screen, a, color=grigio_scuro, highlight=evidenziati, hlcolors=[blu])
		pygame.display.flip()
		pygame.time.delay(frame_time)
		for j in range(i+passo, len(a), passo):
			screen.fill(grigio)
			graphicalgs.drawArray(screen, a, color=grigio_scuro, highlight=[j]+range(i, len(a), passo), hlcolors=[verde, blu])
			pygame.display.flip()
			pygame.time.delay(frame_time)
			while j > i and a[j] < a[j-passo]:
				screen.fill(grigio)
				graphicalgs.drawArray(screen, a, color=grigio_scuro, highlight=[j, j-passo]+range(i, len(a), passo), hlcolors=[verde, giallo, blu], swap=[j, j-passo], swap_time=frame_time)
				pygame.display.flip()
				pygame.time.delay(frame_time)
				tmp = a[j]
				a[j] = a[j-passo]
				a[j-passo] = tmp
				j-= passo
				scambiato = True
	if not scambiato:
		esci = True
	passo = max(1,passo/2)



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
