import pygame
from pygame.locals import *

background = [1, 1, 2, 2, 2, 1]
screen = [0]*6
for i in range(6):
    screen[i] = background[i]
print(screen)
playerpos = 3
screen[playerpos] = 8
print(screen)

screen[playerpos] = background[playerpos]
playerpos = playerpos + 1
screen[playerpos] = 8
print(screen)

pygame.init()
pygame.display.init()

print(pygame.display.get_init)

background = pygame.image.load('terrain.png').convert()
screen.blit(background, (0, 0))
