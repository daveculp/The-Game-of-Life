#! /usr/bin/env python3

import pygame
import random
import time
import sys
import threading

pygame.init()
infoObject = pygame.display.Info()
SCREEN_HEIGHT = infoObject.current_h
SCREEN_WIDTH = infoObject.current_w
CELL_SIZE = 8
NUM_COLS = SCREEN_WIDTH//CELL_SIZE
NUM_ROWS = SCREEN_HEIGHT//CELL_SIZE
    

def seed_board(board, percentage):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if random.randint(1,100) < percentage:
                board[row][col] = True
            else:
                board[row][col] = False
    
def draw_board(board, screen):
    screen.fill( (0,0,0) )
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == True:
                left = col*CELL_SIZE
                top = row*CELL_SIZE
                pygame.draw.rect( screen, (255,64,255), ( left,top,CELL_SIZE,CELL_SIZE ), 0)

def calc_num_neighbors(board, row, col):
    num_neighbors = 0
    if board [ (row-1+NUM_ROWS)%NUM_ROWS][ (col-1+NUM_COLS)%NUM_COLS] == True:
        num_neighbors += 1
    if board [ (row-1+NUM_ROWS)%NUM_ROWS][ col] == True:
        num_neighbors += 1
    if board [ (row-1+NUM_ROWS)%NUM_ROWS][ (col+1)%NUM_COLS] == True:
        num_neighbors += 1
    if board [ row ][ (col-1+NUM_COLS)%NUM_COLS] == True:
        num_neighbors += 1
    if board [ row ][ (col+1)%NUM_COLS] == True:
        num_neighbors += 1
    if board [ (row+1)%NUM_ROWS][ (col-1+NUM_COLS)%NUM_COLS] == True:
        num_neighbors += 1
    if board [ (row+1)%NUM_ROWS][ col] == True:
        num_neighbors += 1
    if board [ (row+1)%NUM_ROWS][ (col+1)%NUM_COLS] == True:
        num_neighbors += 1
        
    return num_neighbors
        
def compute_next_gen():
    global board, back_board
    num_neighbors = 0
                
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            num_neighbors = calc_num_neighbors(board, row, col)
            current_cell = board[row][col]
            if current_cell == True and num_neighbors < 2:
                back_board[row][col] = False
            elif current_cell == True and (num_neighbors == 2 or num_neighbors == 3):
                back_board[row][col] = True
            elif current_cell == True and num_neighbors > 3:
                back_board[row][col] = False
            elif current_cell == False and num_neighbors == 3:
                back_board[row][col] = True
            else:
                back_board[row][col] = current_cell
    
    board, back_board = back_board, board

 
board = [[False for cols in range(NUM_COLS)] for rows in range(NUM_ROWS)]
back_board = [[False for cols in range(NUM_COLS)] for rows in range(NUM_ROWS)]

life_pause = 1
life_percent = 10

choice = input("Do you want a random board to start? ")
if choice.upper() == "Y" or choice.upper() == "YES":
    life_percent = int(input("What percentage chance should a cell have to be alive? "))
    seed_board(board, life_percent)


#pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

#screen = pygame.display.set_mode( (infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN |pygame.DOUBLEBUF | pygame.HWSURFACE )

screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE )


print ("Press SPACE to begin")
frames = 0
start = time.time()
while True:
    
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            print (frames/(time.time()-start))
            pygame.quit()
            sys.exit()
        if event.key == pygame.K_SPACE:
            life_pause = not life_pause
        if event.key == pygame.K_s:
            seed_board(board, life_percent)
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        board[pos[1]//CELL_SIZE][pos[0]//CELL_SIZE] = True
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        board[pos[1]//CELL_SIZE][pos[0]//CELL_SIZE] = False
    
            
    draw_board(board, screen)
    pygame.display.flip()
    if life_pause == 0:
        compute_next_gen()
        frames+=1
