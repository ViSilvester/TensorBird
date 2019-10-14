import pygame
import random
import numpy as np
import cv2
from pygame.locals import *
import copy
import keras.backend as K

def getRandomPipe():
    rec = pygame.Rect(SCREENWIDTH, 0, pipe_w, pipeHeights[random.randrange(0,5)]-(pipe_gap/2))
    return rec

def colisao (r1, r2):
    if r1.left < r2.left + r2.width and r1.left + r1.width > r2.left and r1.top < r2.top + r2.height and r1.top + r1.height > r2.top:
        return True
    else:
        return False

def game(modelo, deubug, invencivel):
    global SCREEN, FPSCLOCK, pipeHeights, SCREENWIDTH, SCREENHEIGHT,  pipe_w, pipe_gap
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
    b = False

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
        
        if b == True:
            vely=-9
            b = False


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
                    if not invencivel:
                        running = False

        if colisao(playerRect, chao):
            if not invencivel:
                running = False
            else:
                playerRect.top-=vely
        pygame.draw.rect(SCREEN,(255,200,100), chao)     
        newbird = pygame.transform.rotate(bird, (-vely/10)*(18))
        SCREEN.blit(newbird, (playerRect.left-7,playerRect.top-4))        
        pygame.display.update()
        FPSCLOCK.tick(FPS)


        screenshot = copy.copy(pygame.surfarray.array2d(SCREEN))
        screenshot = np.array(screenshot, dtype='uint8')
        screenshot = cv2.resize(screenshot, (int(SCREENHEIGHT/2), int(SCREENWIDTH/2)),interpolation = cv2.INTER_NEAREST)
        screenshot = np.array(screenshot, dtype='float16').reshape(-1,int(SCREENHEIGHT/2),int(SCREENWIDTH/2),1)
        screenshot/=255
        predicao = modelo.predict(screenshot)
        K.clear_session()
        if deubug == True:
            print((predicao[0])[0])
        if (predicao[0])[0] > 0.8:
            b = True


    pygame.quit()