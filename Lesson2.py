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

class Ship:
    def __init__(self, screen_width, screen_height):
        self.images = {
            "default": ship_forward,
            "left1": ship_left1,
            "right1": ship_right1,
            "left2": ship_left2,
            "right2": ship_right2,
            "up1": ship_up1,
            "up2": ship_up2
        }
        self.image = self.images["default"]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5

    def move(self, direction):
        
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
            random_add = random.choice([1,3]) 
            if random_add == 1:
                self.image = self.images["left1"]
            else:
                self.image = self.images["left2"]
            
        elif direction == "right" and self.rect.right < self.screen_width:
            self.rect.x += self.speed
            random_add = random.choice([1,3]) 
            if random_add == 1:
                self.image = self.images["right1"]
            else:
                self.image = self.images["right2"]
            
        elif direction == "up" and self.rect.top > self.screen_height - 350  :
            random_add = random.choice([1,3]) 
            if random_add == 1:
                self.image = self.images["up1"]
            else:
                self.image = self.images["up2"]
            self.rect.y -= self.speed
            
        elif direction == "down" and self.rect.bottom < self.screen_height - 10:
            self.rect.y += self.speed
            self.image = self.images["default"]
        else:
            random_add = random.choice([1,3]) 
            if random_add == 1:
                self.image = self.images["up1"]
            else:
                self.image = self.images["up2"]
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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

#images
ship_forward = pygame.image.load("shipcenter.png").convert_alpha()
ship_left1 = pygame.image.load("shipleft1.png").convert_alpha()
ship_left2 = pygame.image.load("shipleft2.png").convert_alpha()
ship_right1 = pygame.image.load("shipright1.png").convert_alpha()
ship_right2 = pygame.image.load("shipright2.png").convert_alpha()
ship_up1 = pygame.image.load("shipforward1.png").convert_alpha()
ship_up2 = pygame.image.load("shipforward2.png").convert_alpha()

#transform images
ship_forward = pygame.transform.scale(ship_forward, (new_width, new_height))
ship_left1 = pygame.transform.scale(ship_left1, (new_width, new_height))
ship_right1 = pygame.transform.scale(ship_right1, (new_width, new_height))
ship_left2 = pygame.transform.scale(ship_left2, (new_width, new_height))
ship_right2 = pygame.transform.scale(ship_right2, (new_width, new_height))
ship_up1 = pygame.transform.scale(ship_up1, (new_width, new_height))
ship_up2 = pygame.transform.scale(ship_up2, (new_width, new_height))

starfield = Stars(screenWidth, screenHeight, 100, 1, 4)
ship = Ship(screenWidth, screenHeight)
#gameLoop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.move("left")
    elif keys[pygame.K_RIGHT]:
        ship.move("right")
    elif keys[pygame.K_UP]:
        ship.move("up")
    elif keys[pygame.K_DOWN]:
        ship.move("down")
    else:
        ship.move("default")    

    starfield.moveStars()
    screen.fill((0,0,0))
    starfield.drawStars(screen)

    ship.draw(screen)
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
