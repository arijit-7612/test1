import pygame
pygame.init()
screen=pygame.display.set_mode((1350,750))
background=pygame.image.load("court.jpg")
background=pygame.transform.scale(background,(1350,750))
surface=pygame.Surface((1350,750))
surface.set_alpha(128)
surface.fill((255,255,255))
run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background,(0,0))
    screen.blit(surface,(0,0))
    pygame.display.update()