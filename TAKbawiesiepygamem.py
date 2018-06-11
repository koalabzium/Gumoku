import sys, pygame
from pygame.locals import *
from math import pi


#ZMIENNE POCZĄTKOWE:

BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
GREEN = (0, 255, 0)
BLUE = (100,100,200,0.1)
DARK_RED = (133, 42, 44)
RED = (255,0,0)
GREY = (200,200,200,0)

pygame.init()
pygame.font.init()


def getFieldNumber(pos):
    return int(pos[0]/field_size),int(pos[1]/field_size)


myfont = pygame.font.SysFont("monospace", 12)
game_over_font = pygame.font.SysFont("monospace", 50)
infoObject = pygame.display.Info()
size = (infoObject.current_w-100, infoObject.current_h-100)
field_size = 30
screen = pygame.display.set_mode(size)
field_count_x = getFieldNumber((infoObject.current_w-100, infoObject.current_h-100))[0]
field_count_y = getFieldNumber((infoObject.current_w-100, infoObject.current_h-100))[1]

exit = False
clock = pygame.time.Clock()
board = [[0 for i in range(field_count_y)]for j in range (field_count_x)]

o_win = False
x_win = False
x_places = []
o_places = []

available_fields = []
x_move = True
single_player = True

def drawOX(x,y,sign):
    x_pos = x*field_size
    y_pos = y*field_size
    if sign == 'o':
        pygame.draw.circle(screen, RED, [x_pos+int(field_size/2),y_pos+int(field_size/2)], int(field_size/2),4)
    else:
        pygame.draw.line(screen,GREEN,[x_pos+2,y_pos+2],[x_pos+field_size-2,y_pos+field_size-2],5)
        pygame.draw.line(screen,GREEN,[x_pos+field_size-2,y_pos+2],[x_pos+2,y_pos-2+field_size],5)

def drawOnScreen():

    screen.fill(WHITE)
    if o_win:
        pygame.draw.circle(screen, RED, [int(size[0]/2)-50,int(size[1]/2)-80], 40,10)
        message("WYGRYWA", BLACK)
    elif x_win:
        message("WYGRAŁAŚ/EŚ", BLACK)
    else:
        for y in range(int(size[1]/field_size)):
            for x in range(int(size[0]/field_size)):
                pygame.draw.rect(screen, GREY, [x*field_size,y*field_size,field_size,field_size],1)
                # label = myfont.render(str(x), 5, DARK_RED)

                # screen.blit(label, (x*field_size,y*field_size))
                if (x,y) in o_places:
                    drawOX(x,y,'o')
                elif (x,y) in x_places:
                    drawOX(x,y,'x')
                label2 = myfont.render(str(board[x][y]), 5, DARK_RED)
                print(board[0][0])
                screen.blit(label2, (x * field_size + 10, y * field_size + 10))
        drawAvailable()

def message(msg,color):
    label2 = game_over_font.render(msg, 300, BLACK)
    screen.blit(label2, (int(size[0]/2),int(size[1]/2)-100))

def findTmpAvailable():
    tmp = []
    for i in o_places:
        for j in range(i[0] - 1, i[0] + 2):
            for k in range(i[1] - 1, i[1] + 2):
                if isinstance(board[j][k], int):
                    tmp.append((j, k))

    for i in x_places:
        for j in range(i[0] - 1, i[0] + 2):
            for k in range(i[1] - 1, i[1] + 2):
                if isinstance(board[j][k], int):
                    tmp.append((j, k))
    return tmp

def findAvailable():
    for i in o_places:
        for j in range(i[0] - 1, i[0] + 2):
            for k in range(i[1] - 1, i[1] + 2):
                if isinstance(board[j][k], int):
                    available_fields.append((j, k))

    for i in x_places:
        for j in range(i[0] - 1, i[0] + 2):
            for k in range(i[1] - 1, i[1] + 2):
                if isinstance(board[j][k], int):
                    available_fields.append((j, k))

def drawAvailable():
    for i in available_fields:
        pygame.draw.rect(screen,BLUE,[i[0]*field_size,i[1]*field_size,field_size,field_size],1)


def heuristics(fields):
    for i in range(field_count_x):
        for j in range(field_count_y):
            if isinstance(board[i][j], int):
                board[i][j] = 0
    for i in fields:
        board[i[0]][i[1]] = 0
        for j in range(i[0]-1,i[0]+2):
            for k in range(i[1]-1,i[1]+2):
                if board[j][k] == 'X':
                    board[i[0]][i[1]] += 1
                    if board[j-i[0]+j][k-i[1]+k] == 'X':
                        board[i[0]][i[1]] += 2
                        if board[2*(i[0]-j)+j][2*(i[1]-k)+k] == 'X':
                            board[i[0]][i[1]] += 3
                        if board[2*(j-i[0])+j][2*(k-i[1])+k] == 'X':
                            board[i[0]][i[1]] += 4
                            if board[3 * (i[0] - j) + j][3 * (i[1] - k) + k] == 'X':
                                board[i[0]][i[1]] += 3
                            if board[3*(j-i[0])+j][3*(k-i[1])+k] == 'X':
                                board[i[0]][i[1]] += 4
                                if board [4*(j-i[0])+j][4*(k-i[1])+k] == 'X':
                                    global x_win
                                    x_win = True
                elif board[j][k] == 'O':
                    board[i[0]][i[1]] += 1
                    if board[j-i[0]+j][k-i[1]+k] == 'O':
                        board[i[0]][i[1]] += 2
                        if board[2*(i[0]-j)+j][2*(i[1]-k)+k] == 'O':
                            board[i[0]][i[1]] += 1
                        if board[2*(j-i[0])+j][2*(k-i[1])+k] == 'O':
                            board[i[0]][i[1]] += 3
                            if board[3 * (i[0] - j) + j][3 * (i[1] - k) + k] == 'O':
                                board[i[0]][i[1]] += 3
                            if board[3*(j-i[0])+j][3*(k-i[1])+k] == 'O':
                                board[i[0]][i[1]] += 6
                                if board[4*(j-i[0])+j][4*(k-i[1])+k] == 'O':
                                    global o_win
                                    o_win = True

        # print(str(i[0])+','+str(i[1])+":  "+str(counter))

def minMax():
    best_value = 0
    current_value = 0
    best_move = (0,0)
    for i in available_fields: #ruch kółka
        current_value += board[i[0]][i[1]]
        o_places.append(i)
        board[i[0]][i[1]] = 'O'
        tmp = findTmpAvailable()
        heuristics(tmp)
        for j in tmp: #ruch krzyżyka
            current_value -= board[j[0]][j[1]]
            x_places.append(j)
            board[j[0]][j[1]] = 'X'
            tmp2 = findTmpAvailable()
            heuristics(tmp2)
            current_value += findMax(tmp2) #największy możliwy ruch kółka
            if current_value > best_value:
                best_value = current_value
                best_move = i
            x_places.remove(j)
            board[j[0]][j[1]] = 0
        o_places.remove(i)
        board[i[0]][i[1]] = 0
    return best_move




def findMax(fields):
    max = 0
    for i in fields:
        if board[i[0]][i[1]] > max:
            max = board[i[0]][i[1]]
    return max


while not exit:
    clock.tick(100)
    drawOnScreen()
    if not x_move:
        pygame.draw.circle(screen, RED, [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]],10,2)
    else:
        pygame.draw.line(screen,GREEN,[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]],[pygame.mouse.get_pos()[0]-10,pygame.mouse.get_pos()[1]-10],2)
        pygame.draw.line(screen,GREEN,[pygame.mouse.get_pos()[0]-10,pygame.mouse.get_pos()[1]],[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-10],2)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            a = getFieldNumber(pygame.mouse.get_pos())
            if isinstance(board[a[0]][a[1]],int):
                if x_move:
                    board[a[0]][a[1]] = 'X'
                    x_places.append(a)
                    findAvailable()
                    heuristics(available_fields)
                    x_move = False
                else:
                    if single_player:
                        a = minMax()
                    board[a[0]][a[1]] = 'O'
                    o_places.append(a)
                    findAvailable()
                    heuristics(available_fields)
                    x_move = True

        if event.type == pygame.QUIT:
            exit=True

    # pygame.draw.circle(screen, RED, [100,100], 30)
    pygame.display.flip()
pygame.quit()
