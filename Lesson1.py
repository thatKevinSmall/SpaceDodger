import pygame
import random
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class Stars:
    def __init__(self, screenWidth, screenHeight, numStars, minSpeed, maxSpeed):
        self.screenWidth = screenWidth
        self.screeHeight = screenHeight
        self.numStars = numStars
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.stars = self.generateStars()

    def generateStars(self):
        stars = []
        for _ in range(self.numStars):
            x = random.randint(0, self.screenWidth)
            y = random.randint(0, self.screeHeight)
            speed = random.uniform(self.minSpeed, self.maxSpeed)
            stars.append([x, y, speed])
        return stars
    
    def moveStars(self):
        for star in self.stars:
            star[1] += star[2]
            if star[1] > self.screeHeight:
                star[1] = 0
                star[0] = random.randint(0, self.screenWidth)
                star[2] = random.uniform(self.minSpeed, self.maxSpeed)

    def drawStars(self, screen):
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), 2)

pygame.init()

screenInfo = pygame.display.Info()
displayW = screenInfo.current_w
displayH = screenInfo.current_h

#vars
screenWidth = 600
screenHeight = round(displayH * .80)
baseSize = round(screenHeight * .1111)
new_width = baseSize
new_height = baseSize
screen = pygame.display.set_mode((screenWidth, screenHeight))

starfield = Stars(screenWidth, screenHeight, 100, 1, 4)

#gameLoop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    starfield.moveStars()
    screen.fill((0,0,0))
    starfield.drawStars(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
