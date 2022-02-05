#! /usr/bin/env python3

import pygame
from pygame.locals import *
import random
import time
import sys
# COLOR DEFINITIONS
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
#CLEARS  THE BOARD BY WRITING TRUE TO EVERY CELL IN THE GRID
def clear_board(board):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            board[row][col] = False

#SEED THE BOARD, PERCENTAGE IS THE % CHANCE A CELL IS ALIVE AT THE START
def seed_board(board, percentage):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if random.randint(0,100) < percentage:
                board[row][col] = True
            else:
                board[row][col] = False

#ITERATE THROUGH THE GRID AND DRAW A RECTANGLE FOR EACH LIVE CELL
def draw_board(board, screen):
    screen.fill( (0,0,0) )
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == True:
                left = col*CELL_SIZE
                top = row*CELL_SIZE
                pygame.draw.rect( screen, (255,64,255), ( left,top,CELL_SIZE,CELL_SIZE ), 0)

#CALCULATE THE NUMBER OF LIVE NEIGHBORS A CELL IN THE INSIDE OF THE GRID HAS
def calc_num_neighbors_inside(board, row, col):

    num_neighbors = 0
    if board [row-1][ col-1] == True:
        num_neighbors += 1
    if board [ row-1][ col] == True:
        num_neighbors += 1
    if board [ row-1][ col+1] == True:
        num_neighbors += 1
    if board [ row ][ col-1] == True:
        num_neighbors += 1
    if board [ row ][ col+1] == True:
        num_neighbors += 1
    if board [ row+1][ col-1] == True:
        num_neighbors += 1
    if board [ row+1][ col] == True:
        num_neighbors += 1
    if board [ row+1][ col+1] == True:
        num_neighbors += 1
        
    return num_neighbors

#CALCULATE THE NUMBER OF LIVE CELLS A CELL ON THE TWO OUTSIDE ROWS (0 AND NUM_ROWS) AND TWO OUSIDE COLUMNS HAS
#THE FUNCTION WILL WRAP AROUND TO THE OTHER EDGES
def calc_num_neighbors_outside(board, row, col):
    num_neighbors = 0
    
    if board [ (row-1+NUM_ROWS) & ROW_AND][ (col-1+NUM_COLS) & COL_AND] == True:
        num_neighbors += 1
    if board [ (row-1+NUM_ROWS) & ROW_AND][ col] == True:
        num_neighbors += 1
    if board [ (row-1+NUM_ROWS) & ROW_AND][ (col+1) & COL_AND] == True:
        num_neighbors += 1
    if board [ row ][ (col-1+NUM_COLS) & COL_AND] == True:
        num_neighbors += 1
    if board [ row ][ (col+1) & COL_AND] == True:
        num_neighbors += 1
    if board [ (row+1) & ROW_AND][ (col-1+NUM_COLS) & COL_AND] == True:
        num_neighbors += 1
    if board [ (row+1) & ROW_AND][ col] == True:
        num_neighbors += 1
    if board [ (row+1) & ROW_AND][ (col+1) & COL_AND] == True:
        num_neighbors += 1
        
    return num_neighbors

def calc_dead_or_alive(row, col, num_neighbors):
    global board, back_board

    current_cell = board[row][col]
    if current_cell == True and num_neighbors < 2:
        back_board[row][col] = False #this cell dies of lonelyness
    elif current_cell == True and (num_neighbors == 2 or num_neighbors == 3):
        back_board[row][col] = True #this cell lives 
    elif current_cell == True and num_neighbors > 3:
        back_board[row][col] = False #dies from overpopulations
    elif current_cell == False and num_neighbors == 3:
        back_board[row][col] = True #A new cell is born!
    else:
        back_board[row][col] = current_cell
    
#FIGURE OUT THE NEXT GENERATION AND THEN SWAP THE BACK_BOARD AND THE BOARD   
def compute_next_gen():
    global board, back_board
    num_neighbors = 0

    #First do the inside cells        
    for row in range(1,NUM_ROWS-1):
        for col in range(1,NUM_COLS-1):
            num_neighbors = calc_num_neighbors_inside(board, row, col)
            calc_dead_or_alive(row, col, num_neighbors)


    #Now do the two outside rows
    for row in OUTSIDE_ROWS:
        for col in range(NUM_COLS):
            num_neighbors = calc_num_neighbors_outside(board, row, col)
            calc_dead_or_alive(row, col, num_neighbors)
                
    #Now do the two outside columns
    for row in range(NUM_ROWS):
        for col in OUTSIDE_COLS:
            num_neighbors = calc_num_neighbors_outside(board, row, col)
            calc_dead_or_alive(row, col, num_neighbors)

    board, back_board = back_board, board

def print_instructions():

    print("""
                       Conway's Game of Life
This is Conway's Game of Life, a cellular automata simulation.  At the start of
the game a grid is randomly populated with live and dead cells.  In each
generation, each cell either remains populated, dies or comes to life based on
simple rules.

    * Each cell with one or no neighbors dies of lonliness. 
    * Each cell with four or more neighbors dies of over population.
    * Each cell with two or three neighbors survives.
    * Each cell with three neighbors becomes populated.

In this simulation you have a few controls:

    * Press the SPACE key at anytime to pause or unpause the simulation.
    * Press the 's' key at anytime to randomly reseed the board.
    * Press the 'c' key at anytime to clear the board.
    * Press the left mouse button to set a cell (best done while paused)
    * Press the right mouse button to unset a cell (best done while paused)


""")

################################################################################
#                           MAIN PROGRAM AREA                                  #
################################################################################

#MAKE OUR BOARD AND BACK_BOARD, FILL WITH ZEROS

CELL_SIZE = int (input ("What cell size do you want to use: " ))
BOARD_SIZE = int(input ( "Number of cells across: ") )

#CONSTANTS FOR SCREEN, GRID AND CELL SIZES
#SCREEN SIZE AND CELL SIZE MUST BE A POWER OF TWO
#CELL_SIZE = 8
SCREEN_WIDTH = BOARD_SIZE * CELL_SIZE
SCREEN_HEIGHT = BOARD_SIZE * CELL_SIZE

NUM_COLS = BOARD_SIZE
NUM_ROWS = BOARD_SIZE


#PRECOMPUTE A FEW CONSTANTS IN ORDER TO SPEED THINGS UPO
ROW_AND = (NUM_ROWS)-1
COL_AND = (NUM_COLS)-1

OUTSIDE_ROWS = 0, NUM_ROWS-1
OUTSIDE_COLS = 0, NUM_COLS-1

board = [[False for cols in range(NUM_COLS)] for rows in range(NUM_ROWS)]
back_board = [[False for cols in range(NUM_COLS)] for rows in range(NUM_ROWS)]

life_paused = True #TRACKS IF THE GAME IS PAUSED OR NOT, START PAUSED
life_percent = 10 #DEFAULT % CHANCE THAT A CELL IS ALIVE AT THE START
frame_delay = .001
frame_rate = 30

print_instructions()
choice = input("Do you want a random board to start? ")
if choice.upper() == "Y" or choice.upper() == "YES":
    life_percent = int(input("What percentage chance should a cell have to be alive? "))
    seed_board(board, life_percent)



#INIT PYGAME AND START THE DISPLAY
pygame.init()
screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE )
pygame.display.set_caption("Conway's Game of Life")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
    
print ("Press SPACE to begin")
frames = 0 #track the number of frames
print_info = False
start = time.time()

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            print (frames)
            print ( (frames/(time.time()-start)),"generations per second")
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            life_paused = not life_paused
        elif event.key == pygame.K_s:
            seed_board(board, life_percent)
        elif event.key == pygame.K_c:
            clear_board(board)
        elif event.key == pygame.K_p:
            print_info = not print_info
        elif event.key == pygame.K_DOWN:
            frame_rate-=1
            if frame_rate <=0:
                frame_rate = 1
        elif event.key == pygame.K_UP:
            frame_rate += 1
    elif pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        board[pos[1]//CELL_SIZE][pos[0]//CELL_SIZE] = True
    elif pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        board[pos[1]//CELL_SIZE][pos[0]//CELL_SIZE] = False
            
    draw_board(board, screen)
    if print_info == True:
        gen_text = font.render("GEN:"+str(frames), 1, (0, 255, 64))
        delay_text = font.render("TARGET FPS:"+"{:.2f}".format(frame_rate), 1, (0, 255, 64))
        actual_fps = font.render("          ACTUAL FPS:"+"{:.2f}".format(clock.get_fps()), 1, (0, 255, 64))
        screen.blit(gen_text,(SCREEN_WIDTH - gen_text.get_width(), SCREEN_HEIGHT - gen_text.get_height() ))
        screen.blit( actual_fps, (delay_text.get_width() + 10, SCREEN_HEIGHT - delay_text.get_height() ))
        screen.blit(delay_text,(0, SCREEN_HEIGHT - delay_text.get_height() ))

    pygame.display.flip()
    if life_paused == False:
        compute_next_gen()
        frames+=1
    clock.tick(frame_rate)
    #time.sleep(frame_delay)
