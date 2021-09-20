# Battleship Game -- Player Vs AI
# Author: Jack Song

# Ships:
# Length | Count
# 4 | 1
# 3 | 3
# 2 | 3
# 1 | 3

import pygame
import sys
import webbrowser
import numpy as np
from random import *
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LGREY = (222, 222, 222)
BLUE = 0, 145, 255
RED = (255, 0, 0)
GREEN = (16, 224, 26)
WIN_WIDTH = 1350
WIN_HEIGHT = 700

ships = [4, 3, 3, 3, 2, 2, 2, 1, 1, 1]


def main():
    global screen, axisFont, buttonFont, messageFont, playerGrid, enemyGrid
    global gameStarted, turn, mouse, buttonDown, gameEnded

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Battleship - Player VS AI - Jack Song")
    screen.fill(WHITE)

    axisFont = pygame.font.SysFont('Arial', 20)
    buttonFont = pygame.font.SysFont('Helvetica', 28)
    messageFont = pygame.font.SysFont('Helvetica', 50)

    playerGrid = randomiseShips()
    enemyGrid = randomiseShips()

    gameStarted = False
    gameEnded = False
    turn = 0
    drawButtons()

    while True:

        mouse = pygame.mouse.get_pos()
        buttonDown = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not gameEnded:
                buttonDown = True
                mouseClick()

        if turn == 1 and not gameEnded:
            aiTurn()

        if gameEnded:
            displayEndMessage()

        markSunkenShip()
        drawGrid()
        checkGameEnd()
        pygame.display.update()


def drawGrid():

    markEmptyCells()

    blockSize = 40
    for x in range(10):
        for y in range(10):
            rect1 = pygame.Rect(140+blockSize*y, 140 +
                                blockSize*x, blockSize, blockSize)
            rect2 = pygame.Rect(810+blockSize*y, 140 +
                                blockSize*x, blockSize, blockSize)
            if playerGrid[x][y] == 1:
                pygame.draw.rect(screen, BLUE, rect1)
            elif playerGrid[x][y] == 2:
                pygame.draw.rect(screen, WHITE, rect1)
                pygame.draw.circle(
                    screen, BLACK, (160+blockSize*y, 160+blockSize*x), 3)
            elif playerGrid[x][y] == 3:
                pygame.draw.rect(screen, BLUE, rect1)
                pygame.draw.line(screen, RED, (140+blockSize*y, 140+blockSize*x),
                                 (180+blockSize*y, 180+blockSize*x), width=3)
                pygame.draw.line(screen, RED, (180+blockSize*y, 140+blockSize*x),
                                 (140+blockSize*y, 180+blockSize*x), width=3)
            elif playerGrid[x][y] == 4:
                pygame.draw.rect(screen, BLUE, rect1)
                pygame.draw.rect(screen, RED, rect1, width=3)
                pygame.draw.line(screen, RED, (140+blockSize*y, 140+blockSize*x),
                                 (180+blockSize*y, 180+blockSize*x), width=3)
                pygame.draw.line(screen, RED, (180+blockSize*y, 140+blockSize*x),
                                 (140+blockSize*y, 180+blockSize*x), width=3)
            else:
                pygame.draw.rect(screen, WHITE, rect1)

            if enemyGrid[x][y] == 2:
                pygame.draw.rect(screen, WHITE, rect2)
                pygame.draw.circle(
                    screen, BLACK, (830+blockSize*y, 160+blockSize*x), 3)
            elif enemyGrid[x][y] == 3:
                pygame.draw.rect(screen, WHITE, rect2)
                pygame.draw.line(screen, RED, (810+blockSize*y, 140+blockSize*x),
                                 (850+blockSize*y, 180+blockSize*x), width=3)
                pygame.draw.line(screen, RED, (850+blockSize*y, 140+blockSize*x),
                                 (810+blockSize*y, 180+blockSize*x), width=3)
            elif enemyGrid[x][y] == 4:
                pygame.draw.rect(screen, WHITE, rect2)
                pygame.draw.rect(screen, RED, rect2, width=3)
                pygame.draw.line(screen, RED, (810+blockSize*y, 140+blockSize*x),
                                 (850+blockSize*y, 180+blockSize*x), width=3)
                pygame.draw.line(screen, RED, (850+blockSize*y, 140+blockSize*x),
                                 (810+blockSize*y, 180+blockSize*x), width=3)
            else:
                pygame.draw.rect(screen, WHITE, rect2)

            xAxis = axisFont.render(str(x+1), False, BLACK)
            yAxis = axisFont.render(chr(65+y), False, BLACK)

            screen.blit(xAxis, (155+blockSize*x, 115))
            screen.blit(xAxis, (825+blockSize*x, 115))

            screen.blit(yAxis, (110, 145+blockSize*y))
            screen.blit(yAxis, (780, 145+blockSize*y))

    if mouse[0] > 810 and mouse[0] < 1210 and mouse[1] > 140 and mouse[1] < 540:
        gridx = int((mouse[0]-810)/40)
        gridy = int((mouse[1]-140)/40)
        rect = pygame.Rect(810+blockSize*gridx, 140 +
                           blockSize*gridy, blockSize, blockSize)
        pygame.draw.rect(screen, GREEN, rect)

        if enemyGrid[gridy][gridx] == 2:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.circle(
                screen, BLACK, (830+blockSize*gridx, 160+blockSize*gridy), 3)
        elif enemyGrid[gridy][gridx] == 3:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.line(screen, RED, (810+blockSize*gridx, 140+blockSize*gridy),
                             (850+blockSize*gridx, 180+blockSize*gridy), width=3)
            pygame.draw.line(screen, RED, (850+blockSize*gridx, 140+blockSize*gridy),
                             (810+blockSize*gridx, 180+blockSize*gridy), width=3)
        elif enemyGrid[gridy][gridx] == 4:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, RED, rect, width=3)
            pygame.draw.line(screen, RED, (810+blockSize*gridx, 140+blockSize*gridy),
                             (850+blockSize*gridx, 180+blockSize*gridy), width=3)
            pygame.draw.line(screen, RED, (850+blockSize*gridx, 140+blockSize*gridy),
                             (810+blockSize*gridx, 180+blockSize*gridy), width=3)

    for i in range(11):
        pygame.draw.line(screen, BLACK, (140, 140+i*blockSize),
                         (540, 140+i*blockSize))
        pygame.draw.line(screen, BLACK, (140+i*blockSize, 140),
                         (140+i*blockSize, 540))
        pygame.draw.line(screen, BLACK, (810, 140+i*blockSize),
                         (1210, 140+i*blockSize))
        pygame.draw.line(screen, BLACK, (810+i*blockSize, 140),
                         (810+i*blockSize, 540))


def mouseClick():
    global gameStarted, playerGrid, turn

    if mouse[0] > 260 and mouse[0] < 420 and mouse[1] > 570 and mouse[1] < 620 and buttonDown and not gameStarted:
        playerGrid = randomiseShips()

    if mouse[0] > 810 and mouse[0] < 1210 and mouse[1] > 140 and mouse[1] < 540 and buttonDown and turn == 0:
        gameStarted = True
        hitx = int((mouse[0]-810)/40)
        hity = int((mouse[1]-140)/40)
        if enemyGrid[hity][hitx] == 0:
            enemyGrid[hity][hitx] = 2
            turn = 1
        elif enemyGrid[hity][hitx] == 1:
            enemyGrid[hity][hitx] = 3
            turn = 0

    if mouse[0] > 1230 and mouse[0] < 1330 and mouse[1] > 640 and mouse[1] < 690 and buttonDown:
        webbrowser.open("https://en.wikipedia.org/wiki/Battleship_(game)")


def aiTurn():
    global turn
    hitx = randint(0, 9)
    hity = randint(0, 9)

    while playerGrid[hitx][hity] == 2 or playerGrid[hitx][hity] == 3 or playerGrid[hitx][hity] == 4:
        hitx = randint(0, 9)
        hity = randint(0, 9)

    if playerGrid[hitx][hity] == 0:
        playerGrid[hitx][hity] = 2
        turn = 0
    elif playerGrid[hitx][hity] == 1:
        playerGrid[hitx][hity] = 3
        turn = 1


def drawButtons():
    buttonRect = pygame.Rect(260, 570, 160, 50)
    pygame.draw.rect(screen, LGREY, buttonRect)
    pygame.draw.rect(screen, BLACK, buttonRect, width=1)
    randText = buttonFont.render("Randomise", False, BLACK)
    screen.blit(randText, (282, 577))

    buttonRect = pygame.Rect(1230, 640, 100, 50)
    pygame.draw.rect(screen, LGREY, buttonRect)
    pygame.draw.rect(screen, BLACK, buttonRect, width=1)
    randText = buttonFont.render("Rules", False, BLACK)
    screen.blit(randText, (1250, 648))


def randomiseShips():
    global grid
    grid = np.zeros((10, 10), dtype=np.int8)

    for i in range(10):
        randomPlacement(ships[i])

    for x in range(10):
        for y in range(10):
            if grid[x][y] == 2:
                grid[x][y] = 0

    return grid


def randomPlacement(size):
    global locx, locy, ori
    size -= 1
    locx = randint(0, 9)
    locy = randint(0, 9)
    ori = randint(0, 3)

    while True:
        flag = False
        if grid[locx][locy] == 1 or grid[locx][locy] == 2:
            newLoc()

        if ori == 0 and locx - size >= 0:
            for x in range(locx - size, locx+1):
                if grid[x][locy] == 1 or grid[x][locy] == 2:
                    flag = True
                    break

            if flag:
                newLoc()
                continue

            for x in range(locx - size, locx+1):
                grid[x][locy] = 1
            break

        elif ori == 1 and locy + size <= 9:

            for y in range(locy, locy + size+1):
                if grid[locx][y] == 1 or grid[locx][y] == 2:
                    flag = True
                    break

            if flag:
                newLoc()
                continue

            for y in range(locy, locy + size+1):
                grid[locx][y] = 1
            break

        elif ori == 2 and locx + size <= 9:

            for x in range(locx, locx + size+1):
                if grid[x][locy] == 1 or grid[x][locy] == 2:
                    flag = True
                    break

            if flag:
                newLoc()
                continue

            for x in range(locx, locx + size+1):
                grid[x][locy] = 1

            break

        elif ori == 3 and locy - size >= 0:

            for y in range(locy - size, locy+1):
                if grid[locx][y] == 1 or grid[locx][y] == 2:
                    flag = True
                    break

            if flag:
                newLoc()
                continue

            for y in range(locy - size, locy+1):
                grid[locx][y] = 1
            break

        else:
            newLoc()

    fillAdj()


def newLoc():
    global locx, locy, ori
    locx = randint(0, 9)
    locy = randint(0, 9)
    ori = randint(0, 3)  # 0-up 1-right 2-down 3-left


def fillAdj():
    dir = [[1, 0], [-1, 0], [0, 1], [0, -1],
           [1, 1], [1, -1], [-1, 1], [-1, -1]]

    for x in range(10):
        for y in range(10):
            if grid[x][y] == 1:
                for i in range(8):
                    nx = x+dir[i][0]
                    ny = y+dir[i][1]

                    if nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9 and grid[nx][ny] == 0:
                        grid[nx][ny] = 2


def markSunkenShip():
    dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for x in range(10):
        for y in range(10):
            if enemyGrid[x][y] == 3:
                flag = False
                q = []
                rep = []
                vis = np.zeros((10, 10), dtype=np.int8)

                q.append((x, y))
                rep.append((x, y))
                vis[x][y] = 1
                while q:
                    curx = q[0][0]
                    cury = q[0][1]
                    q.pop(0)
                    for i in range(4):
                        nx = curx+dir[i][0]
                        ny = cury+dir[i][1]

                        if nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9 and vis[nx][ny] == 0:

                            if enemyGrid[nx][ny] == 1:
                                flag = True
                                break

                            elif enemyGrid[nx][ny] == 3:
                                q.append((nx, ny))
                                rep.append((nx, ny))
                                vis[nx][ny] = 1

                    if flag:
                        break

                if not flag:
                    for i in range(len(rep)):
                        enemyGrid[rep[i][0]][rep[i][1]] = 4

    for x in range(10):
        for y in range(10):
            if playerGrid[x][y] == 3:
                flag = False
                q = []
                rep = []
                vis = np.zeros((10, 10), dtype=np.int8)

                q.append((x, y))
                rep.append((x, y))
                vis[x][y] = 1
                while q:
                    curx = q[0][0]
                    cury = q[0][1]
                    q.pop(0)
                    for i in range(4):
                        nx = curx+dir[i][0]
                        ny = cury+dir[i][1]

                        if nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9 and vis[nx][ny] == 0:

                            if playerGrid[nx][ny] == 1:
                                flag = True
                                break

                            elif playerGrid[nx][ny] == 3:
                                q.append((nx, ny))
                                rep.append((nx, ny))
                                vis[nx][ny] = 1

                    if flag:
                        break

                if not flag:
                    for i in range(len(rep)):
                        playerGrid[rep[i][0]][rep[i][1]] = 4


def markEmptyCells():
    dir = [[1, 1], [1, -1], [-1, 1], [-1, -1],
           [1, 0], [-1, 0], [0, 1], [0, -1]]

    for x in range(10):
        for y in range(10):
            if enemyGrid[x][y] == 3:
                for i in range(4):
                    nx = x+dir[i][0]
                    ny = y+dir[i][1]

                    if nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9 and enemyGrid[nx][ny] == 0:
                        enemyGrid[nx][ny] = 2

            elif enemyGrid[x][y] == 4:
                for i in range(8):
                    nx = x+dir[i][0]
                    ny = y+dir[i][1]

                    if nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9 and enemyGrid[nx][ny] == 0:
                        enemyGrid[nx][ny] = 2

            if playerGrid[x][y] == 3:
                for i in range(4):
                    nx = x+dir[i][0]
                    ny = y+dir[i][1]

                    if nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9 and playerGrid[nx][ny] == 0:
                        playerGrid[nx][ny] = 2

            elif playerGrid[x][y] == 4:
                for i in range(8):
                    nx = x+dir[i][0]
                    ny = y+dir[i][1]

                    if nx >= 0 and nx <= 9 and ny >= 0 and ny <= 9 and playerGrid[nx][ny] == 0:
                        playerGrid[nx][ny] = 2


def checkGameEnd():
    global winID, gameEnded
    if not 1 in enemyGrid:
        winID = 5
        gameEnded = True
        return
    elif not 1 in playerGrid:
        winID = 10
        gameEnded = True
        return


def displayEndMessage():
    if winID == 5:
        endMessage = messageFont.render("You Win!", False, BLACK)
    elif winID == 10:
        endMessage = messageFont.render("You Lose", False, BLACK)

    screen.blit(endMessage, (580, 40))


main()
