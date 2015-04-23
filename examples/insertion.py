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
grigio_scuro = pygame.Color("#aaaaaa")

backg = pygame.Color("#dddddd")	#Sfondo
elemC = blu		#Colore base degli elementi
currC = verde	#Colore dell'elemento corrente
prevC = giallo	#Colore dell'elemento precedente (che e' da scambiare)
okC = verde	#Colore per gli elementi correttamente posizionati


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
screen.blit(font.render("Elementi da ordinare", True, elemC), (50,20))
screen.blit(font.render("Elemento considerato", True, currC), (50,70))
screen.blit(font.render("Elemento da scambiare", True, prevC), (50,120))
screen.blit(font.render("(e' maggiore di quello dopo)", True, prevC), (50,160))
pygame.display.flip()
while not pygame.event.peek(pygame.MOUSEBUTTONDOWN):
	pygame.time.delay(100)


MAXN = 100

a = range(1,MAXN)
random.shuffle(a)




# ------ Algoritmo -------

for i in range(len(a)):
	#Reset screen
	screen.fill(backg)
	#Draw
	simpleDraw([i], [currC])
	#Move the element
	while i > 0 and a[i] < a[i-1]:
		#Check quit button
		if pygame.event.Event(pygame.QUIT) in pygame.event.get():
			pygame.quit()
			sys.exit()
		#Reset
		screen.fill(backg)
		#Draw
		simpleDraw([i, i-1], [prevC, currC], s=[i,i-1])
		#Swap
		a[i], a[i-1] = a[i-1], a[i]
		i -= 1

# ------ Fine Algoritmo ------



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
