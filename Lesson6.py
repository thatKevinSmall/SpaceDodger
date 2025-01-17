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
            pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), star[2])

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
            random_add = random.choice([self.images["left1"],self.images["left2"]]) 
            self.image = random_add
            
        elif direction == "right" and self.rect.right < self.screen_width:
            self.rect.x += self.speed
            random_add = random.choice([self.images["right1"],self.images["right2"]]) 
            self.image = random_add
            
        elif direction == "up" and self.rect.top > self.screen_height - 350  :
            self.rect.y -= self.speed
            random_add = random.choice([self.images["up1"],self.images["up2"]]) 
            self.image = random_add
            
            
        elif direction == "down" and self.rect.bottom < self.screen_height - 10:
            self.rect.y += self.speed
            self.image = self.images["default"]
        else:
            random_add = random.choice([self.images["up1"],self.images["up2"]]) 
            self.image = random_add

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Obstacle:
    def __init__(self, screen_width, screen_height):
        random_add = random.choice([astronaut, astronaut, satellite, alien, asteroid, asteroid]) 
        self.image = random_add
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.uniform(4, 6)

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)
            self.speed = random.uniform(4, 6)
            return True  # Indicates the asteroid has passed the ship
        return False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def resetLocation(self):
        self.rect.y = 0
        self.rect.x = random.randint(0, screenWidth - self.rect.width)

def display_message(screen, text, font, color, y_offset=0):
    message = font.render(text, True, color)
    screen.blit(message, (screen.get_width() // 2 - message.get_width() // 2, screen.get_height() // 2 - message.get_height() // 2 + y_offset))

def reset_game():
    global game_over, obs, ship, score, level
    game_over = False
    score = 0
    level = 0
    pygame.mixer.music.unpause()
    ship = Ship(screenWidth, screenHeight)
    obs = [Obstacle(screenWidth, screenHeight) for _ in range(3)] 

def add_obsticles():
    obs.append(Obstacle(screenWidth, screenHeight)) 

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

font = pygame.font.Font(None, 36)
game_over = False
score = 0
level = 0
asteroid_added_scores = set()
hiScore = 0
hiLevel = 0

RED = (255, 0, 0)
WHITE = (255, 255, 255)
#images
#ship
ship_forward = pygame.image.load("shipcenter.png").convert_alpha()
ship_left1 = pygame.image.load("shipleft1.png").convert_alpha()
ship_left2 = pygame.image.load("shipleft2.png").convert_alpha()
ship_right1 = pygame.image.load("shipright1.png").convert_alpha()
ship_right2 = pygame.image.load("shipright2.png").convert_alpha()
ship_up1 = pygame.image.load("shipforward1.png").convert_alpha()
ship_up2 = pygame.image.load("shipforward2.png").convert_alpha()

#obstacles
asteroid = pygame.image.load("asteroid.png").convert_alpha()
astronaut = pygame.image.load("astronaut.png").convert_alpha()
satellite = pygame.image.load('sat.png').convert_alpha()
alien = pygame.image.load('alien.png').convert_alpha()

#transform images
ship_forward = pygame.transform.scale(ship_forward, (new_width, new_height))
ship_left1 = pygame.transform.scale(ship_left1, (new_width, new_height))
ship_right1 = pygame.transform.scale(ship_right1, (new_width, new_height))
ship_left2 = pygame.transform.scale(ship_left2, (new_width, new_height))
ship_right2 = pygame.transform.scale(ship_right2, (new_width, new_height))
ship_up1 = pygame.transform.scale(ship_up1, (new_width, new_height))
ship_up2 = pygame.transform.scale(ship_up2, (new_width, new_height))

alien = pygame.transform.scale(alien, (new_width - 10, new_height - 10))
asteroid = pygame.transform.scale(asteroid, (new_width + 50, new_height + 50))
astronaut = pygame.transform.scale(astronaut, (new_width - 50, new_height - 50))
satellite = pygame.transform.scale(satellite, (new_width, new_height - 20))

starfield = Stars(screenWidth, screenHeight, 100, 1, 4)
ship = Ship(screenWidth, screenHeight)
obs = [Obstacle(screenWidth, screenHeight) for _ in range(3)] 

pygame.init()
#add sound
pygame.mixer.init()
#add music
pygame.mixer.music.load('space.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.25)
#add effect
sfxExplode = pygame.mixer.Sound("explosion.mp3")
sfxExplode.set_volume(0.5)
#gameLoop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not game_over:
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

        for ob in obs:
            if ob.move():
                score += 1     
            ob.draw(screen)       

        if level > 0 and level < 6: 
            if score % 10 == 0 and score not in asteroid_added_scores:
                add_obsticles()
                level = level + 1 
                asteroid_added_scores.add(score)
        else:
            if score % 20 == 0 and score not in asteroid_added_scores:
                add_obsticles()
                level = level + 1 
                asteroid_added_scores.add(score)   

        ship.draw(screen)
        if pygame.sprite.spritecollide(ship, obs, False, pygame.sprite.collide_mask):
            sfxExplode.play()
            pygame.mixer.music.pause()
            game_over = True
            
        scoreText = font.render(f"Score: {score}", True, (255, 255, 255))
        if score > hiScore:
            hiScore = score
        hiScoreText = font.render(f"High Score: {hiScore}", True, (255, 255, 255))
        levelText = font.render(f"Level: {level}", True, (255, 255, 255))
        if level > hiLevel:
            hiLevel = level
        hiLevelText = font.render(f"High Level: {hiLevel}", True, (255, 255, 255))
        screen.blit(scoreText, (10,  10))
        screen.blit(hiScoreText, (10, 30))
        screen.blit(levelText, (10, 50))
        screen.blit(hiLevelText, (10, 70))
    else:
        if score > hiScore:
            hiScore = score
        display_message(screen, "Game Over", font, (255, 0, 0), -100)
        display_message(screen, f"Final Score: {score}", font, (255, 255, 255), -50)
        display_message(screen, f"Final Level: {level}", font, (255, 255, 255))
        display_message(screen, f"Hi Score: {hiScore}", font, (255, 255, 255), 50)
        display_message(screen, f"Hi Level: {hiLevel}", font, (255, 255, 255), 100)
        display_message(screen, "Would you like to play again? (Y/N)", font, (255, 255, 255), 150)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            reset_game()
        elif keys[pygame.K_n]:
            running = False
    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
