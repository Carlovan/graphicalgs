#!/usr/bin/python2

import graphicalgs
import pygame
import random
import sys


time = input("Durata di un frame: ")
font = pygame.font.SysFont("arial", 60)


pygame.init()

def simpleDraw(l, ll, s=[]):
	global a
	global screen
	rrr = graphicalgs.drawArray(screen, a, color=blu, highlight=l, hlcolors=ll, swap=s, swap_time=time)
	#pygame.display.update(rrr)
	pygame.display.flip()

winW = 1000
winH = 500

bianco = (255,255,255)
nero = (0,0,0)
rosso = pygame.Color("#c0392b")
verde = pygame.Color("#27ae60")
blu = pygame.Color("#2980b9")
giallo = pygame.Color("#f1c40f")
viola = pygame.Color("#8e44ad")

backg = pygame.Color("#dddddd")
elemC = blu
minC = verde
selC = rosso
currC = giallo
okC = viola

screen = pygame.display.set_mode((winW, winH))
pygame.display.set_caption("Selection sort")
screen.fill(backg)
pygame.display.flip()


#Legenda
screen.blit(font.render("Elemento da sostituire", True, currC), (50,10))
screen.blit(font.render("Elemento considerato", True, selC), (50,50))
screen.blit(font.render("Elemento minimo", True, minC), (50,90))
screen.blit(font.render("Elemento gia' posizionato correttamente", True, okC), (50,130))
pygame.display.flip()
while not pygame.event.peek(pygame.MOUSEBUTTONDOWN):
	pygame.time.delay(100)


maxN = 15

a = range(1,maxN)
random.shuffle(a)

for i in range(len(a)-1):
	minVal = maxN
	minInd = 0
	for j in range(i, len(a)):
		if pygame.event.Event(pygame.QUIT) in pygame.event.get():
			pygame.quit()
			sys.exit()

		if a[j] < minVal:
			minVal = a[j]
			minInd = j
		screen.fill(backg)
		simpleDraw([minInd, j, i]+range(i), [minC, currC, selC, okC])
		pygame.time.delay(time)
	screen.fill(backg)
	simpleDraw([minInd, j, i]+range(i), [minC, currC, selC, okC], s=[i, minInd])
	pygame.time.delay(time)
	a[i], a[minInd] = a[minInd], a[i]


screen.fill(backg)
graphicalgs.drawArray(screen, a, color=okC)
smile = pygame.image.load("smile.png")
screen.blit(smile, ((winW-smile.get_width())/2, (winH-smile.get_height())/2))
pygame.display.flip()

while 1:
	if pygame.event.Event(pygame.QUIT) in pygame.event.get():
		pygame.quit()
		sys.exit()
	pygame.time.delay(50)
