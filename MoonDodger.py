import random
import pygame
from math import sqrt
pygame.init()

win = pygame.display.set_mode((600,500))
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("First Game")
font = pygame.font.SysFont("comicsans", DISPLAYSURF.get_height()//40)

background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (DISPLAYSURF.get_width(), DISPLAYSURF.get_height()))

class Entity:
    def __init__(self, x, y, radius, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel
        
    def draw(self):
        pygame.draw.circle(win, (230, 230, 230), (self.x, self.y), self.radius)
        

    def moveLeft(self):
        self.x -= self.vel
        if self.x < 0-self.radius:
            self.x = DISPLAYSURF.get_width() 


class Player(Entity):
    def __init__(self, x, y, radius, vel):
        super().__init__(x, y, radius, vel)

    
    def draw(self):
        pygame.draw.circle(win, (0, 255, 255), (self.x, self.y), self.radius)

    def drawHit(self):
        pygame.draw.circle(win, (255, 255, 0), (self.x, self.y), self.radius * 2)

    def moveUp(self):
        self.y -= self.vel
        if self.y < self.radius + DISPLAYSURF.get_height()/20:
            self.y = self.radius + DISPLAYSURF.get_height()/20

    def moveDown(self):
        self.y += self.vel
        if self.y > DISPLAYSURF.get_height()-self.radius:
            self.y = DISPLAYSURF.get_height()-self.radius

moonList = []
spiller = Player(100, DISPLAYSURF.get_height()/2, DISPLAYSURF.get_height()/60, DISPLAYSURF.get_width()/1000)

def more():
    posx = random.randint(DISPLAYSURF.get_width(), DISPLAYSURF.get_width()*2)
    posy = random.randint(int(DISPLAYSURF.get_height()/20), DISPLAYSURF.get_height())
    size = random.random()*DISPLAYSURF.get_height()/40 + 5
    speed = random.random()*DISPLAYSURF.get_width()/500
    moonList.append(Entity(posx, posy, size, speed))


def startGame():
    global moonList, framecounter, totalframes, level, liv
    moonList = []
    framecounter = 100
    totalframes = 0
    level = 1
    liv = 5
    for i in range(100):
        more()


framecounter = 100
highscore = 0
totalframes = 0
level = 1
liv = 1
run = True

startGame()
while run:
    pygame.time.delay(8)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if liv > 0:  
        win.fill((0,0,0))  # Fills the screen with black
        win.blit(background, (0, 0))
        pygame.draw.rect(win, (30, 30, 30), (0, 0, DISPLAYSURF.get_width(), DISPLAYSURF.get_height()/20))

        

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            spiller.moveUp()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            spiller.moveDown()
        spiller.draw()

        x = spiller.x
        y = spiller.y
        r = spiller.radius
        for i in range(len(moonList)):
            moonList[i].moveLeft()
            moonList[i].draw()
            if framecounter < 100:
                spiller.drawHit()
            elif spiller.radius + moonList[i].radius > sqrt((-spiller.x + moonList[i].x)**2 + (spiller.y - moonList[i].y)**2):
                liv -= 1
                framecounter = 0
        framecounter += 1
        totalframes += 1
        if totalframes > highscore:
            highscore = totalframes
        
        if totalframes % 1000 == 0:
            for i in range(10):
                more()
            level += 1

        tekst = f"Liv: {str(liv)}     Level: {str(level)}         Poengsum: {str(totalframes)}                                                                                                                          Highscore: {str(highscore)}"
        tekstBilde = font.render(tekst, True, (255, 255, 255))
        win.blit(tekstBilde, (DISPLAYSURF.get_width()/100, DISPLAYSURF.get_height()/100))

    else:
        pygame.draw.rect(win, (30, 30, 30), (DISPLAYSURF.get_width()//3, DISPLAYSURF.get_height()//5*2, DISPLAYSURF.get_width()//3, DISPLAYSURF.get_height()//5))
        tekst = f"Level: {str(level)}         Poengsum: {str(totalframes)}"
        tekstBilde = font.render(tekst, True, (255, 255, 255))
        win.blit(tekstBilde, (DISPLAYSURF.get_width()//100*44, DISPLAYSURF.get_height()//100*49))
        

        tekst = f"Press Enter to restart"
        tekstBilde = font.render(tekst, True, (255, 255, 255))
        win.blit(tekstBilde, (DISPLAYSURF.get_width()//100*46, DISPLAYSURF.get_height()//100*52))

        if keys[pygame.K_RETURN]:
            startGame()

    pygame.display.update() 
print(f"Du overlevde i {totalframes} frames og kom til level {level}")
pygame.quit()