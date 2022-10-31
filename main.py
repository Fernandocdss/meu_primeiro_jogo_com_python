import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

# importando e iniciando a funcao pygame
import pygame
from asteroid import Asteroid
from player import Player
from shot import Shot

import random


pygame.init()

# criando e atribuindo uma tela a variavel display
display = pygame.display.set_mode([840, 480])
pygame.display.set_caption("Meu Jogo 01")

# Groups
objectGroup = pygame.sprite.Group()
asteroidGroup = pygame.sprite.Group()
shotGroup = pygame.sprite.Group()

# Backgrounds
bg = pygame.sprite.Sprite(objectGroup)
bg.image = pygame.image.load("data/desert-mirage.png")
bg.image = pygame.transform.scale(bg.image, [840, 480])
bg.rect = bg.image.get_rect()

player = Player(objectGroup)


# Music
pygame.mixer.music.load("data/music.flac")
pygame.mixer.music.play(-1)

# Sound
shoot = pygame.mixer.Sound("data/alienshoot2.wav")

gameLoop = True
gameOver = False
timer = 20
clock = pygame.time.Clock()

if __name__ == "__main__":
    while gameLoop:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not gameOver:
                    shoot.play()
                    newShot = Shot(objectGroup, shotGroup)
                    newShot.rect.center = player.rect.center

        # Update logic
        if not gameOver:
            objectGroup.update()
            timer += 1
            if timer > 30:
                timer = 0
                if random.random() < 0.3:
                    newAsteroid = Asteroid(objectGroup, asteroidGroup)
                    print("New asteroid!")

            collisions = pygame.sprite.spritecollide(player, asteroidGroup, False, pygame.sprite.collide_mask)

            if collisions:
                print("Game Over!")
                gameOver = True

            hits = pygame.sprite.groupcollide(shotGroup, asteroidGroup, True, True, pygame.sprite.collide_mask)

        # Draw
        display.fill([48, 104, 194])
        objectGroup.draw(display)
        pygame.display.update()

