import pygame
pygame.init()
screen=pygame.display.set_mode((1350,750))
background=pygame.image.load("court.jpg")
background=pygame.transform.scale(background,(1350,750))
surface=pygame.Surface((1350,750))
surface.set_alpha(128)
surface.fill((255,255,255))

sprite_sheet1 = pygame.image.load("sprite14_1.png").convert_alpha()
sprite_sheet2 = pygame.image.load("judge.png").convert_alpha()
sprite_sheet3 = pygame.image.load("slawyer_sprite.png").convert_alpha()

run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background,(0,0))
    screen.blit(surface,(0,0))
    pygame.display.update()