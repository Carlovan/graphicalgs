#!/usr/bin/python2

import graphicalgs
import pygame
import random
import sys

time = input("Durata di un frame: ")
font = pygame.font.SysFont("arial", 60)


bianco = (255,255,255)
nero = (0,0,0)
rosso = pygame.Color("#c0392b")
verde = pygame.Color("#27ae60")
blu = pygame.Color("#2980b9")
giallo = pygame.Color("#f1c40f")
viola = pygame.Color("#8e44ad")

backg = pygame.Color("#dddddd")
elemC = blu
chC = verde
selC = rosso
currC = giallo
okC = viola

winH = 500
winW = 1000

pygame.init()

def simpleDraw(l, ll, s=[]):
	global a
	global screen
	rrr = graphicalgs.drawArray(screen, a, color=elemC, highlight=l, hlcolors=ll, swap=s, swap_time=time)
	#pygame.display.update(rrr)
	pygame.display.flip()

screen = pygame.display.set_mode((winW, winH))
pygame.display.set_caption("Bubble sort")
screen.fill(backg)
pygame.display.flip()


#Legenda
screen.blit(font.render("Elemento che sto considerando", True, currC), (50,20))
screen.blit(font.render("Elemento che controllo per lo scambio", True, selC), (50,70))
screen.blit(font.render("Elemento da scambiare", True, chC), (50,120))
screen.blit(font.render("(e' maggiore di quello prima)", True, chC), (50,160))
screen.blit(font.render("Elemento gia' posizionato correttamente", True, okC), (50,210))
pygame.display.flip()
while not pygame.event.peek(pygame.MOUSEBUTTONDOWN):
	pygame.time.delay(100)


MAXN = 10

a = range(1,MAXN)
random.shuffle(a)


for i in range(len(a)-1, 1, -1):
	j = 0
	scambiato = False
	while j < i:
		if pygame.event.peek(pygame.QUIT):
			pygame.quit()
			sys.exit()
		screen.fill(backg)
		simpleDraw([j] + range(i+1, MAXN), [currC, okC])
		pygame.time.delay(time)
		simpleDraw([j, j+1] + range(i+1, MAXN), [currC,selC,okC])
		pygame.time.delay(time)
		if a[j] > a[j+1]:
			screen.fill(backg)
			simpleDraw([j, j+1] + range(i+1, MAXN), [currC,chC,okC], [j, j+1])
			pygame.time.delay(time)
			scambiato = True
			temp = a[j]
			a[j] = a[j+1]
			a[j+1] = temp
		j += 1
	if scambiato == False:
		break


screen.fill(backg)
graphicalgs.drawArray(screen, a, color=okC)
smile = pygame.image.load("smile.png")
screen.blit(smile, ((winW-smile.get_width())/2, (winH-smile.get_height())/2))
pygame.display.flip()

while 1:
	if pygame.event.peek(pygame.QUIT):
		pygame.quit()
		sys.exit()
	pygame.time.delay(50)
