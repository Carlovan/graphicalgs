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

backg = pygame.Color("#dddddd")
elemC = blu		#Colore degli elementi considerati
nonConsC = grigio_scuro	#Colore degli elementi non considerati
currC = verde	#Colore dell'elemento corrente
prevC = giallo	#Colore dell'elemento precedente (che e' da scambiare)
okC = verde	#Colore per gli elementi correttamente posizionati


winH = 500
winW = 1000

pygame.init()

def simpleDraw(l, ll, s=[]):
	global a
	global screen
	rrr = graphicalgs.drawArray(screen, a, color=nonConsC, highlight=l, hlcolors=ll, swap=s, swap_time=time)
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


MAXN = 10

a = range(1,MAXN)
random.shuffle(a)




# ------ Algoritmo -------

passo = MAXN/2
esci = False
while not esci:
	if passo == 1:
		esci = True

	for i in range(passo):
		#Elementi attivi
		evidenziati = list(range(i, len(a), passo))
		#Reset screen
		screen.fill(backg)
		#Draws the array
		simpleDraw(evidenziati, [elemC])
		#Refresh screen
		pygame.display.flip()
		#Wait
		pygame.time.delay(time)
		#For every considered element
		for j in range(i+passo, len(a), passo):
			#Reset screen
			screen.fill(backg)
			#Draw
			simpleDraw([j]+range(i, len(a), passo), [currC, elemC])
			#Refresh screen
			pygame.display.flip()
			#Wait
			pygame.time.delay(time)
			#Move the element
			while j > i and a[j] < a[j-passo]:
				#Check quit button
				if pygame.event.peek(pygame.QUIT):
					pygame.quit()
					sys.exit()
				#Reset screen
				screen.fill(backg)
				#Draw
				simpleDraw([j, j-passo]+range(i, len(a), passo), [currC, prevC, elemC])
				#Refresh
				pygame.display.flip()
				#Wait
				pygame.time.delay(time)
				#Reset screen
				screen.fill(backg)
				#Draw
				simpleDraw([j, j-passo]+range(i, len(a), passo), [prevC, currC, elemC], [j, j-passo])
				#Refresh
				pygame.display.flip()
				#Wait
				pygame.time.delay(time)
				#Swap values
				tmp = a[j]
				a[j] = a[j-passo]
				a[j-passo] = tmp
				j-= passo
	#New step
	passo = max(1,passo/2)

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
