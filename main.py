import pygame
from sys import exit
import datetime
import random
import generator

pygame.init()
pygame.display.set_caption("Slide")
FPS = 60
WIDTH = 400
HEIGHT = 500
TILESIZE = 100
BLACK = (23,32,56)
BLUE = (51,175,223)
font = pygame.font.SysFont('Arial', 32)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
tileGroup = pygame.sprite.Group()
wonGame = False
playAgainImg = pygame.image.load("img/p.png").convert_alpha()
tileGrid = []
pMoves = 0
pTime = 0

class ParticlePrinciple:
    def __init__(self):
        self.particles = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.1
                pygame.draw.circle(screen,particle[3], particle[0], int(particle[1]))

    def add_particles(self):
        pos_x = (WIDTH/2)
        pos_y = (HEIGHT/2)
        radius = random.randint(5, 20)
        direction_x = random.randint(-3,3)
        direction_y = random.randint(-3,3)
        cR = random.randint(0, 255)
        cG = random.randint(0, 255)
        cB = random.randint(0, 255)
        particle_circle = [[pos_x,pos_y], radius, [direction_x, direction_y], (cR, cG, cB)]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,50)
particle1 = ParticlePrinciple()

class Button():
    def __init__(self, xButton, yButton, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = xButton
        self.rect.y = yButton
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

playAgainBtn = Button((WIDTH/2)-(TILESIZE/2), (HEIGHT/2)-(TILESIZE/2), playAgainImg)

class Tile(pygame.sprite.Sprite):
    def __init__(self,xTile,yTile,nTile):
        super().__init__()
        self.image = pygame.image.load('img/' + str(nTile) + '.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = xTile * TILESIZE
        self.rect.y = yTile * TILESIZE

def startGame():
    global tileGrid, wonGame, pMoves, pTime
    tileGrid = generator.spitItOut()
    tileGroup.empty()
    configureGrid(tileGrid)
    pMoves = 0
    pTime = 0
    wonGame = False

def configureGrid(tileGrid):
    for r, row in enumerate(tileGrid):
        for e, element in enumerate(row):
            tileGroup.add(Tile(e, r, element))

def updateGrid(pressedKey):
    didMove = False
    x = -1
    for row in tileGrid:
        x += 1
        if (0 in row):
            indexOfZeroRow = x
            indexOfZeroCol = row.index(0)
    if pressedKey == 119: # W - 0 is in in row 0, 1, or 2
        if (indexOfZeroRow < 3):
            didMove = True
            movingTile = tileGrid[indexOfZeroRow+1][indexOfZeroCol]
            tileGrid[indexOfZeroRow][indexOfZeroCol] = movingTile
            tileGrid[indexOfZeroRow+1][indexOfZeroCol] = 0
    if pressedKey == 97: # A - 0 is in column 0, 1, or 2
        if (indexOfZeroCol < 3):
            didMove = True
            movingTile = tileGrid[indexOfZeroRow][indexOfZeroCol+1]
            tileGrid[indexOfZeroRow][indexOfZeroCol] = movingTile
            tileGrid[indexOfZeroRow][indexOfZeroCol+1] = 0
    if pressedKey == 115: # S - 0 is in row 1, 2, or 3
        if (indexOfZeroRow > 0):
            didMove = True
            movingTile = tileGrid[indexOfZeroRow-1][indexOfZeroCol]
            tileGrid[indexOfZeroRow][indexOfZeroCol] = movingTile
            tileGrid[indexOfZeroRow-1][indexOfZeroCol] = 0
    if pressedKey == 100: # D - 0 is in column 1, 2, or 3
        if (indexOfZeroCol > 0):
            didMove = True
            movingTile = tileGrid[indexOfZeroRow][indexOfZeroCol-1]
            tileGrid[indexOfZeroRow][indexOfZeroCol] = movingTile
            tileGrid[indexOfZeroRow][indexOfZeroCol-1] = 0
    if didMove == True:
        global pMoves
        pMoves += 1
    tileGroup.empty()
    configureGrid(tileGrid)
    if tileGrid == [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]:
        global wonGame
        wonGame = True

def drawText(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

startGame()

while True:
    screen.fill(BLACK)
    if wonGame == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d):
                    updateGrid(event.key)
        tileGroup.draw(screen)
        pTime += 1/FPS
        pTimeConverted = datetime.timedelta(seconds=int(pTime))
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_SPACE):
                    startGame()
        if event.type == PARTICLE_EVENT:
            particle1.add_particles()
        particle1.emit()
        if playAgainBtn.draw():
            startGame()
    drawText("Moves: " + str(pMoves),font,BLUE,7,407)
    drawText("Time: " + str(pTimeConverted),font,BLUE,7,447)
    pygame.display.flip()
    clock.tick(FPS)