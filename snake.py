"""A naive attempt to automate the game of snake (selfmade obv), to reach the highest possible score, by using a simple math concept known as the Hamiltonian Path.
Not knowing that this will become the reason of my sleeplessness, frustration and FUN for the next few weeks. Anyhow really enjoyed doing this mini project hope you
like it. I learnt a lot in the process (Hope my maths teacher is proud of me 🥲).
Open for any suggestions, tips and etc.
You can try Manipulating some values ( marked with 💀 ) or absolutely everything and see the snake go crazy.
Thamk you for reading and going through this shit, hope you have a good day"""

"""BUGS: 1. Game crashes as soon as it eats the last food.
         2. Grids are not visible. """

"""NOTE: Hamiltonian Path: A path in a graph that visits every vertex exactly once."""


import pyglet as py
import random
from pyglet.window import Window
from pyglet.window import key
from pyglet import graphics
from pyglet import image
from pyglet import shapes
from pyglet import text
from pyglet.shapes import Line
from random import randint

window=py.window.Window(800,800,"SNAKE GAME") # 💀 #This decides the width and height of the window i.e, (width,height)
"""You can change the size of snake,if you want to see how it looks, but remember the height and the width of the Window should be perfectly divisible by this cell_size"""
cell_size = 100 #Size of snake 💀

# Store grid lines in a batch to draw only once
batch=graphics.Batch()

def draw_grid(): #This function doesn't work, it is supposed to show a grid pattern in the window 
    for x in range(0,window.width+cell_size,cell_size):
        Line(x, 0, x, window.height, batch=batch, color=(255,255,255)) 
    for y in range(0,window.height+cell_size,cell_size):
        Line(0, y, window.width, y, batch=batch, color=(255, 255, 255))


@window.event
def on_draw():
    window.clear()
    #draw_grid()
    #batch.draw()
    draw_square(snk_x,snk_y,cell_size)  # Draws the snake's head
    draw_square(fd_x, fd_y, cell_size, colour=(255, 0, 0, 0))  # Draws food #Changes colour 💀
    for coors in tail:
        draw_square(coors[0], coors[1], cell_size, colour=(0, 127, 0, 0))  # Draws the snake's tail
    draw_square(snk_x,snk_y,cell_size)
    display_score() #Displays Score
    if game_over:
        draw_game_over() #Shows game over Screen

def display_score(): #Displays Score
    score = text.Label(f'Score: {len(tail)}', font_name='Times New Roman',
                       font_size=16, x=10, y=window.height - 20,
                       anchor_x='left', anchor_y='top')
    score.draw()

def new_game(): #Starts new game
    global snk_x, snk_y, game_over, tail, hamiltonian_cycle_path
    if cell_size < 1 or window.width % cell_size != 0 or window.height % cell_size != 0:
        #print(window.width, window.height)
        print("Invalid cell size")
        exit()

    snk_x = 0 # X-axis value of snake starting position
    snk_y = 0 # Y-axis value of snake starting position
    tail = []

    # Generate the Hamiltonian cycle before placing food
    #Case 1:
    if window.height/cell_size % 2==0:
        generate_hamiltonian_cycle_even()
    #Case 2:
    elif window.width/cell_size %2==0 and window.height/cell_size %2!=0:
        #print("hi") #Debug print 😅
        generate_hamiltonian_cycle_odd()

    #Case 3:
    elif window.width/cell_size %2!=0 and window.height/cell_size %2!=0:
        generate_hamiltonian_cycle_both_odd_1()
        generate_hamiltonian_cycle_both_odd_2()
    
    
    place_food()  # Now we can safely place food
    
    
    game_over = False

def draw_square(x, y, size, colour=(0, 255, 0, 0)): #💀
    img = image.create(size, size, image.SolidColorImagePattern(colour))
    img.blit(x, y)



def place_food():
    global fd_x, fd_y
    # Place food randomly, avoiding the snake's body
    while True:
        fd_x, fd_y = randint(0, (window.width // cell_size) - 1) * cell_size, randint(0, (window.height // cell_size) - 1) * cell_size
        if (fd_x, fd_y) not in tail and (fd_x, fd_y) != (snk_x, snk_y): # Checks so that the food is not placed on the body of the snake
            break  # Exit the loop when food is placed in an empty spot


def draw_game_over():
    game_screen = text.Label(f'Score: {len(tail)}\n (Press space to restart)', font_size=24,
                             x=window.width // 2, y=window.height // 2, width=window.width,
                             align='center', anchor_x='center', anchor_y='center', multiline=True)
    game_screen.draw()

@window.event
def on_key_press(symbol,modifiers): # If SPACEBAR is pressed it restarts the game
    if symbol==key.SPACE:
            new_game()

hamiltonian_cycle_path = [] #Stores Hamiltonian path coordinates
hamiltonian_cycle_path_1=[]
current_path=hamiltonian_cycle_path #Shows which path the snake currently is following 


def come_down(fll=0,width=window.width,height=window.height): #Appends the coordinates for the snake to come down from top to botton height
    global hamiltonian_cycle_path, tail, snk_x, snk_y
    if fll==1:
        for y in range(height-cell_size,-cell_size,-cell_size):
            hamiltonian_cycle_path_1.append((width-cell_size,y))
    else:
        for y in range(height-cell_size,-cell_size,-cell_size):
            hamiltonian_cycle_path.append((width-cell_size,y))


"""Case 1: When (height/cell_size)i.e, the number of rows is even ."""

def generate_hamiltonian_cycle_even(): 
    global hamiltonian_cycle_path,current_path
    hamiltonian_cycle_path = []

    for y in range(0, window.height, cell_size):
        if y // cell_size % 2 == 0: # Traverse left to right on even rows
            for x in range(window.width - (2*cell_size), -1, -cell_size):
                hamiltonian_cycle_path.append((x, y))
            
        else: # Traverse right to left on odd rows
            for x in range(0, window.width-cell_size, cell_size):
                hamiltonian_cycle_path.append((x, y))
    come_down()
    current_path=hamiltonian_cycle_path #Sets current path to the Hamiltonian path created


"""Case 2: When (width/cell_size) and (height/cell_size) i.e, the number of column is even and number of rows is odd"""

def generate_hamiltonian_cycle_odd(): 
    global hamiltonian_cycle_path,snk_x,snk_y,current_path
    hamiltonian_cycle_path=[]
    for y in range(0, window.height-(2*cell_size), cell_size):
        if y // cell_size % 2 == 0: # Traverse left to right on even rows
            for x in range(window.width - (2*cell_size), -1, -cell_size):
                hamiltonian_cycle_path.append((x, y))
            
        else:
            # Traverse right to left on odd rows
            for x in range(0, window.width-cell_size, cell_size):
                hamiltonian_cycle_path.append((x, y))

    hamiltonian_cycle_path.append((0,window.height-(2*cell_size))) #It appends the coordinates of the last two rows as to make the Hamiltonian path. Refer the diagram for the Hamiltonian Path representation. 
    hamiltonian_cycle_path.append((0,window.height-(cell_size)))
    x,y=hamiltonian_cycle_path[-1]
    #print(x,y)  #Debug Print statement 😅
    fl1=True #Flags to alternate between moves
    fl2=False
    fl3=False
    fl4=False
    while(fl1 or fl2 or fl3 or fl4):
        if (fl1==True): # Moves Right
            x=x+cell_size
            #print(x,y)
            hamiltonian_cycle_path.append((x,y))
            fl1=False
            fl2=True
        elif (fl2==True): # Moves Down
            y=y-cell_size
            #print(x,y)
            hamiltonian_cycle_path.append((x,y))
            fl2=False
            fl3=True
        elif(fl3==True): # Moves Right
            x=x+cell_size 
            #print(x,y)
            hamiltonian_cycle_path.append((x,y))
            fl3=False
            fl4=True
        elif(fl4==True): # Moves Up
            y=y+cell_size
            #print(x,y)
            hamiltonian_cycle_path.append((x,y))
            fl4=False
            fl1=True
        if x==window.width-(2*cell_size) and y==window.height-cell_size: #Condition to check if it has reached last point or not
            fl1=False
            fl2=False
            fl3=False
            fl4=False
    come_down()
    current_path=hamiltonian_cycle_path


"""Case 3:  When (width/cell_size) and (height/cell_size) i.e, the number of column and number of rows both are odd.
There is no Hamiltonian path for this condition hence we use two differnt path sto obtain the highese points. 
Please refer to the example diagram for the path visualization"""

def generate_hamiltonian_cycle_both_odd_1(): #Same as case 2, except the last part where teh snake returns without going to one of the vertex
    global hamiltonian_cycle_path,snk_x,snk_y
    hamiltonian_cycle_path=[]
    #print("hi")
    for y in range(0, window.height-(2*cell_size), cell_size):
        if y // cell_size % 2 == 0:
            # Traverse left to right on even rows
            for x in range(window.width - (2*cell_size), -1, -cell_size):
                hamiltonian_cycle_path.append((x, y))
            
        else:
            # Traverse right to left on odd rows
            for x in range(0, window.width-cell_size, cell_size):
                hamiltonian_cycle_path.append((x, y))
    hamiltonian_cycle_path.append((0,window.height-(2*cell_size)))
    hamiltonian_cycle_path.append((0,window.height-(cell_size)))
    x,y=hamiltonian_cycle_path[-1]
    #print(x,y)
    fl1=True
    fl2=False
    fl3=False
    fl4=False
    while(fl1 or fl2 or fl3 or fl4):
        if (fl1==True):
            x=x+cell_size
            #print(x,y)
            hamiltonian_cycle_path.append((x,y))
            fl1=False
            fl2=True
        elif (fl2==True):
            y=y-cell_size
            #print(x,y)
            hamiltonian_cycle_path.append((x,y))
            fl2=False
            fl3=True
        elif(fl3==True):
            x=x+cell_size
            #print(x,y)
            hamiltonian_cycle_path.append((x,y))
            fl3=False
            fl4=True
        elif(fl4==True):
            y=y+cell_size
            #print(x,y)
            hamiltonian_cycle_path.append((x,y))
            fl4=False
            fl1=True
        if x==window.width-(2*cell_size) and y==window.height-(2*cell_size):
            fl1=False
            fl2=False
            fl3=False
            fl4=False
    #print(x,y)
    hamiltonian_cycle_path.append((x+cell_size,y))
    come_down(0,x+(2*cell_size),y)



def generate_hamiltonian_cycle_both_odd_2(): # Second Hamiltonian path creation
    global hamiltonian_cycle_path_1,snk_x,snk_y,current_path
    hamiltonian_cycle_path_1=[]
    #print("hello")
    for y in range(0, window.height-(2*cell_size), cell_size):
        if y // cell_size % 2 == 0:
            # Traverse left to right on even rows
            for x in range(window.width - (2*cell_size), -1, -cell_size):
                hamiltonian_cycle_path_1.append((x, y))
            
        else:
            # Traverse right to left on odd rows
            for x in range(0, window.width-cell_size, cell_size):
                hamiltonian_cycle_path_1.append((x, y))
    hamiltonian_cycle_path_1.append((0,window.height-(2*cell_size)))
    hamiltonian_cycle_path_1.append((0,window.height-(cell_size)))
    x,y=hamiltonian_cycle_path_1[-1]
    #print(x,y)
    fl1=True
    fl2=False
    fl3=False
    fl4=False
    while(fl1 or fl2 or fl3 or fl4):
        if (fl1==True):
            x=x+cell_size
            #print(x,y)
            hamiltonian_cycle_path_1.append((x,y))
            fl1=False
            fl2=True
        elif (fl2==True):
            y=y-cell_size
            #print(x,y)
            hamiltonian_cycle_path_1.append((x,y))
            fl2=False
            fl3=True
        elif(fl3==True):
            x=x+cell_size
            #print(x,y)
            hamiltonian_cycle_path_1.append((x,y))
            fl3=False
            fl4=True
        elif(fl4==True):
            y=y+cell_size
            #print(x,y)
            hamiltonian_cycle_path_1.append((x,y))
            fl4=False
            fl1=True
        if x==window.width-(2*cell_size) and y==window.height-(cell_size):
            fl1=False
            fl2=False
            fl3=False
            fl4=False
    #print(x,y)
    hamiltonian_cycle_path_1.append((x+cell_size,y))
    come_down(1,x+(2*cell_size),y)
    current_path=hamiltonian_cycle_path_1


"""This function runs to continuously update the position of the snaek and also check for other conditions like: if game over or not, if food eaten etc"""

def update(dt):
    global snk_x, snk_y, game_over, hamiltonian_cycle_path_1, hamiltonian_cycle_path, current_path, tail, fd_x, fd_y

    if game_over:
        return  
    
    if game_over_condn():
        game_over = True
        return

    current_pos = (snk_x, snk_y)
    if current_pos not in current_path:
        return

    current_index = current_path.index(current_pos)
    next_pos = current_path[(current_index + 1) % len(current_path)]

    # Update the path cycle
    current_path = complete_cycle(next_pos)

    # Update snake's position
    tail.append((snk_x, snk_y))
    snk_x, snk_y = next_pos

    if snk_x == fd_x and snk_y == fd_y:
        place_food()
    else:
        tail.pop(0)


""" Checks if the snake has completed a full cycle or not, this condition helps to alterenate between the two paths of case 3 """

def complete_cycle(pos): 
    global current_path, hamiltonian_cycle_path, hamiltonian_cycle_path_1

    if pos == current_path[0]:  # Completed one full cycle
        if window.width / cell_size % 2 != 0 and window.height / cell_size % 2 != 0:
            current_path = (
                hamiltonian_cycle_path_1 if current_path == hamiltonian_cycle_path else hamiltonian_cycle_path
            )
    return current_path

    
def game_over_condn(): # Checks for game over condition
    condn1 = snk_x < 0 or snk_x > window.width - cell_size or snk_y < 0 or snk_y > window.height - cell_size
    condn2 = (snk_x, snk_y) in tail
    return condn1 or condn2




fd_x, fd_y = 0, 0 #Initialization of position of food

new_game()

#print(hamiltonian_cycle_path) # Debug statements 🥲🥲
#print(hamiltonian_cycle_path_1)
#print(current_path)

py.clock.schedule_interval(update, 1/100 ) # Schedules the update function to be called repeatedly at a fixed interval of time. Here, it is 1/15, 💀
#if you want to increase the spped of the snake, increase the value of the denominator (Try making it 1/10000000)  
py.app.run() # Runs the app