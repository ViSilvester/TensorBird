import random
import sys

import pygame
from pygame.locals import *

import numpy as np
import matplotlib.pyplot as plt
import cv2

def getRandomPipe():
    rec = pygame.Rect(SCREENWIDTH, 0, pipe_w, pipeHeights[random.randrange(0,5)]-(pipe_gap/2))
    return rec

def colisao (r1, r2):
    if r1.left < r2.left + r2.width and r1.left + r1.width > r2.left and r1.top < r2.top + r2.height and r1.top + r1.height > r2.top:
        return True
    else:
        return False

def game():

album=[]
labels=[]
global SCREEN, FPSCLOCK, pipeHeights 
running = True
FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
cronometro = 0
chao = pygame.Rect(0, SCREENHEIGHT-150, SCREENWIDTH, 150)
areaUtil = SCREENHEIGHT - chao.height
playerRect = pygame.Rect(40,SCREENHEIGHT*0.4, 25, 25)
vely=0
pipeHeights = [areaUtil*0.5, areaUtil*0.6, areaUtil*0.4, areaUtil*0.7, areaUtil*0.3, areaUtil*0.2]
pipeList =[]
pipe_w = 38
pipe_gap = 100

pygame.init()

pygame.display.set_caption('Tensor Bird')
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
bird = pygame.image.load('C:/Users/vineo/DEV/tensor bird/assets/sprites/yellowbird-midflap.png').convert_alpha()

while running:
    cronometro = cronometro+1
    if cronometro == 33:
        pipeList.append(getRandomPipe())
        cronometro = 0


    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
           running = False
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                vely=-9
    
    playerRect.top += vely
    if vely < 15  :
        vely+=1

    SCREEN.fill((200,200,255,0))    
    for i in pipeList:
        i.left -= 4 
        if i.left + i.width <= 0:
            pipeList.pop
        else:
            r = pygame.Rect(i.left, i.top, i.width, i.height)
            r.top = i.height + pipe_gap
            r.height = SCREENHEIGHT - i.height
            pygame.draw.rect(SCREEN, (0,255,0), i)
            pygame.draw.rect(SCREEN, (0,255,0), r)

            if colisao(playerRect, i) or colisao(playerRect, r):
                running = False

    if colisao(playerRect, chao):
        running = False
    pygame.draw.rect(SCREEN,(255,200,100), chao)     
    newbird = pygame.transform.rotate(bird, (-vely/10)*(18))
    SCREEN.blit(newbird, (playerRect.left-7,playerRect.top-4)) 
    #spygame.draw.rect(SCREEN,(255,255,0), playerRect)
    screenshot = pygame.surfarray.array2d(SCREEN)
    screenshot = np.array(screenshot, dtype='uint8')
    screenshot = cv2.resize(screenshot, (int(SCREENHEIGHT/2), int(SCREENWIDTH/2)),interpolation = cv2.INTER_NEAREST)
    album.append(screenshot)
    if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
        labels.append(1)
    else:
        labels.append(0)
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)

pygame.quit()

print("deseja gravar esta sessão como dataset? S/N")
if input() == 's':
    np.save("c:/users/vineo/DEV/tensor bird/album", album)
    np.save("c:/users/vineo/DEV/tensor bird/labels", labels)
    print("dataset gravado com sucesso")
plt.figure()
plt.imshow(album[-1], cmap='gray')
plt.show()

print(len(album),len(labels))