from graphics import *
import time
import pygame
from random import randint
pygame.mixer.init()


def game():
    win = GraphWin("Minesweeper!", 630,630, autoflush = False)

    #Stores Grid Template:
    
    undertiles = [[1,9,1,0,0,0,0,0,0], #STORES THE GAME GRID TEMPLATE
                  [1,1,1,0,0,0,1,1,1],
                  [0,0,0,0,0,0,2,9,3],
                  [0,1,1,1,0,0,2,9,9],
                  [0,1,9,1,0,0,1,3,2],
                  [0,1,1,2,1,1,0,1,9],
                  [0,1,1,2,9,2,1,1,1],
                  [0,1,9,2,2,9,1,1,1],
                  [0,1,1,1,1,1,1,1,9]]

    rememberFlags = [[0,0,0,0,0,0,0,0,0], #THIS LIST REMEMBERS WHEN A FLAG IS PLACED
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0]]

    adjacentTracker = [[1,1,1,1,1,1,1,1,1], #THIS LIST COUNTS WHEN A TILE IS UNDRAWN 
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1]]

    #COVERING TILES:
    tilesLocation = [[Point(35,35), Point(105,35), Point(175,35), Point(245,35), Point(315,35), Point(385,35), Point(455,35), Point(525,35), Point(595,35)],
            [Point(35,105), Point(105,105), Point(175,105), Point(245,105), Point(315,105), Point(385,105), Point(455,105), Point(525,105), Point(595,105)],
            [Point(35,175), Point(105,175), Point(175,175), Point(245,175), Point(315,175), Point(385,175), Point(455,175), Point(525,175), Point(595,175)],
            [Point(35,245), Point(105,245), Point(175,245), Point(245,245), Point(315,245), Point(385,245), Point(455,245), Point(525,245), Point(595,245)],
            [Point(35,315), Point(105,315), Point(175,315), Point(245,315), Point(315,315), Point(385,315), Point(455,315), Point(525,315), Point(595,315)],
            [Point(35,385), Point(105,385), Point(175,385), Point(245,385), Point(315,385), Point(385,385), Point(455,385), Point(525,385), Point(595,385)],
            [Point(35,455), Point(105,455), Point(175,455), Point(245,455), Point(315,455), Point(385,455), Point(455,455), Point(525,455), Point(595,455)],
            [Point(35,525), Point(105,525), Point(175,525), Point(245,525), Point(315,525), Point(385,525), Point(455,525), Point(525,525), Point(595,525)],
            [Point(35,595), Point(105,595), Point(175,595), Point(245,595), Point(315,595), Point(385,595), Point(455,595), Point(525,595), Point(595,595)]]

    #PRINT THE GRID TEMPLATE:
    #BOMBS = 9 EMPTY TILE = 0 NUMBERED TILE = 1-8
    for row in range (9):
        for col in range (9):
            if undertiles[row][col] == 9:
                undertile = Image(tilesLocation[row][col], "Images/bomb.gif")
                undertile.draw(win)
            elif undertiles[row][col] == 0:
                undertile = Image(tilesLocation[row][col], "Images/0.gif")
                undertile.draw(win)
            elif undertiles[row][col] == 1:
                undertile = Image(tilesLocation[row][col], "Images/1.gif")
                undertile.draw(win)
            elif undertiles[row][col] == 2:
                undertile = Image(tilesLocation[row][col], "Images/2.gif")
                undertile.draw(win)
            elif undertiles[row][col] == 3:
                undertile = Image(tilesLocation[row][col], "Images/3.gif")
                undertile.draw(win)
        #print()

    #PRINT THE TILES THAT COVER THE GRID TEMPLATE:
    tiles = []
    for row in range (9):
        rowsTemp = []
        for col in range (9):
            rowsTemp.append(Image(tilesLocation[row][col], "Images/tile.gif"))
            rowsTemp[col].draw(win)
        tiles.append (rowsTemp)

        
    #PROGRAM Z AND X CLICK:
    #Z + Click will dig
    #X + Click will flag
    #C + Click will reset click
    tilesdug = 0
    tilesFlagged = 0
    while True:
        if tilesdug == 71 and tilesFlagged == 10: #IF THE GAME IS WON (ALL SAFE TILES ARE DUG)...
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Sounds/win.wav"),-1)
            winscreen = GraphWin("Winner!", 300,330, autoflush = False)
            winscreen.setBackground(color_rgb(195,195,195))
            button = Image(Point(150,230), "Images/smiley.gif")
            button.draw(winscreen)
            gamewon = Text(Point(150, 50), "YOU WON! :-)")
            playagain = Text(Point(150, 100), "Play Again? :")
            gamewon.setSize(26)
            gamewon.draw(winscreen)
            playagain.setSize(26)
            playagain.draw(winscreen)

            while True: 
                winPos = winscreen.getMouse()
                xwin = winPos.getX ()
                ywin = winPos.getY ()

                if xwin <= 225 and xwin >= 75 and ywin <= 305 and ywin >= 155: #PLAY AGAIN BUTTON:
                    pygame.mixer.Channel(1).stop()
                    winscreen.close()
                    win.close()
                    game()
                
        clickedPos = win.getMouse () #GETS MOUSE INPUT FOR GAME
        x = clickedPos.getX ()
        y = clickedPos.getY ()
        key = win.getKey() #GETS KEYBOARD INPUT FOR GAME
        
        if (key == "z") or (key == "Z"): #DIG (CODE FOR FLAGGING IS AT LINE 179)
            if  rememberFlags[int(y//70)][int(x//70)] == 1: #This ensures that all flagged tiles can not be dug!
                continue
            elif adjacentTracker[int(y//70)][int(x//70)] == 1:
                pygame.mixer.music.load("Sounds/dignoise.wav") #digging noise is played
                pygame.mixer.music.play()
                
                
                tilesdug = tilesdug + 1 #number of tiles dug are counted (later used to determine when game is won)
                adjacentTracker[int(y//70)][int(x//70)] = 0 #Ensures that the tile is registered as undrawn on the adjacent tile list. 
                tiles[int(y//70)][int(x//70)].undraw() #Undraws tile. 
                
                if undertiles[int(y//70)][int(x//70)] == 9: #IF THE GAME IS LOST (MINE IS DUG)...
                    #Reveals all bomb locations:
                    for row in range (9):
                        for col in range (9):
                            if undertiles[row][col] == 9:
                                tiles[row][col].undraw()
                                
                    #EXPOSES THE CLICKED MINE (red):
                    clickedBomb = Image(tilesLocation[int(y//70)][int(x//70)], "Images/clickbomb.gif")
                    clickedBomb.draw(win)
                    
                    #Shows wrong flags: (IF THERE ARE INCORRECT FLAGS)
                    for row in range (9):
                        for col in range (9):
                            if rememberFlags[row][col] == 1 and undertiles[row][col] != 9:
                                incorrectFlag = Image(tilesLocation[row][col], "Images/wrongflag.gif")
                                incorrectFlag.draw(win)

                    #Explosion sound:
                    pygame.mixer.music.load("Sounds/explosion.wav") #plays explosion sound 
                    pygame.mixer.music.play()
                    time.sleep(1)
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("Sounds/loss.wav"),-1)
                    #End game screen:
                    losescreen = GraphWin("GAME OVER", 300,330, autoflush = False)
                    losescreen.setBackground(color_rgb(195,195,195))
                    button = Image(Point(150,230), "Images/smiley.gif")
                    button.draw(losescreen)
                    gameover = Text(Point(150, 50), "GAME OVER! :-(")
                    playagain = Text(Point(150, 100), "Play Again? :")
                    gameover.setSize(26)
                    gameover.draw(losescreen)
                    playagain.setSize(26)
                    playagain.draw(losescreen)

                    while True:
                        losePos = losescreen.getMouse()
                        xlose = losePos.getX ()
                        ylose = losePos.getY ()

                        if xlose <= 225 and xlose >= 75 and ylose <= 305 and ylose >= 155:
                            pygame.mixer.Channel(0).stop()
                            losescreen.close()
                            win.close()
                            game()
                        
                elif undertiles[int(y//70)][int(x//70)] == 0: #IF A BLANK TILE IS DUG, ALL ADJACENT TILES NOT TOUCHING A MINE MUST BE EXPOSED
                    #If a tile is a blank tile, the following code checks all the surrounding tiles to determine if there are any more blank tiles. 
                    if int(y//70)-1 >= 0 and int(x//70)-1 >= 0 and undertiles[int(y//70)-1][int(x//70)-1] == 0:
                        if rememberFlags[int(y//70)-1][int(x//70)-1] == 1: #If a blank tile is flagged, the program must move on (you can't undraw a flagged tile!)
                            continue
                        else:
                            if adjacentTracker[int(y//70)-1][int(x//70)-1] == 1:
                                tiles[int(y//70)-1][int(x//70)-1].undraw()
                                tilesdug = tilesdug + 1 #Later used to determine when the game is won
                                adjacentTracker[int(y//70)-1][int(x//70)-1] = 0 #Used to tell the program if a tile is dug or not.
                        
                    if int(y//70)-1 >= 0 and undertiles[int(y//70)-1][int(x//70)] == 0:
                        if rememberFlags[int(y//70)-1][int(x//70)] == 1:
                            continue
                        else:
                            if adjacentTracker[int(y//70)-1][int(x//70)] == 1:
                                tiles[int(y//70)-1][int(x//70)].undraw()
                                tilesdug = tilesdug + 1
                                adjacentTracker[int(y//70)-1][int(x//70)] = 0
                    
                    if int(y//70)-1 >= 0 and int(x//70)+1 <= 8 and undertiles[int(y//70)-1][int(x//70)+1] == 0:
                        if rememberFlags[int(y//70)-1][int(x//70)+1] == 1:
                            continue
                        else:
                            if adjacentTracker[int(y//70)-1][int(x//70)+1] == 1:
                                tiles[int(y//70)-1][int(x//70)+1].undraw()
                                tilesdug = tilesdug + 1
                                adjacentTracker[int(y//70)-1][int(x//70)+1] = 0
                
                    if int(x//70)-1 >= 0 and undertiles[int(y//70)][int(x//70)-1] == 0:
                        if rememberFlags[int(y//70)][int(x//70)-1] == 1:
                            continue
                        else:
                            if adjacentTracker[int(y//70)][int(x//70)-1] == 1:
                                tiles[int(y//70)][int(x//70)-1].undraw()
                                tilesdug = tilesdug + 1
                                adjacentTracker[int(y//70)][int(x//70)-1] = 0
            
                    if int(x//70)+1 <= 8 and undertiles[int(y//70)][int(x//70)+1] == 0:
                        if rememberFlags[int(y//70)][int(x//70)+1] == 1:
                            continue
                        else:
                            if adjacentTracker[int(y//70)][int(x//70)+1] == 1:
                                tiles[int(y//70)][int(x//70)+1].undraw()
                                tilesdug = tilesdug + 1
                                adjacentTracker[int(y//70)][int(x//70)+1] = 0

                    if int(y//70)+1 <= 8 and int(x//70)-1 >= 0 and undertiles[int(y//70)+1][int(x//70)-1] == 0:
                        if rememberFlags[int(y//70)+1][int(x//70)-1] == 1:
                            continue
                        else:
                            if adjacentTracker[int(y//70)+1][int(x//70)-1] == 1:
                                tiles[int(y//70)+1][int(x//70)-1].undraw()
                                tilesdug = tilesdug + 1
                                adjacentTracker[int(y//70)+1][int(x//70)-1] = 0

                    if (y//70)+1 <= 8 and undertiles[int(y//70)+1][int(x//70)] == 0:
                        if rememberFlags[int(y//70)+1][int(x//70)] == 1:
                            continue
                        else:
                            if adjacentTracker[int(y//70)+1][int(x//70)] == 1:
                                tiles[int(y//70)+1][int(x//70)].undraw()
                                tilesdug = tilesdug + 1
                                adjacentTracker[int(y//70)+1][int(x//70)] = 0

                    if int(y//70)+1 <= 8 and int(x//70)+1 <= 0 and undertiles[int(y//70)+1][int(x//70)+1] == 0:
                        if rememberFlags[int(y//70)+1][int(x//70)+1] == 1:
                            continue
                        else:
                            if adjacentTracker[int(y//70)+1][int(x//70)+1] == 1:
                                tiles[int(y//70)+1][int(x//70)+1].undraw()
                                tilesdug = tilesdug + 1
                                adjacentTracker[int(y//70)+1][int(x//70)+1] = 0
                                        
        elif (key == "x") or (key == "X"): #FLAG (CODE FOR DIGGING IS AT LINE 87)
            pygame.mixer.music.load("Sounds/flag.wav")
            pygame.mixer.music.play()
            tiles[int(y//70)][int(x//70)].undraw()
            if rememberFlags[int(y//70)][int(x//70)] == 0:
                tiles[int(y//70)][int(x//70)] = Image(tilesLocation[int(y//70)][int(x//70)], "Images/flag.gif")
                tiles[int(y//70)][int(x//70)].draw(win)
                tilesFlagged = tilesFlagged + 1
                rememberFlags[int(y//70)][int(x//70)] = 1
                
            else:
                tiles[int(y//70)][int(x//70)].undraw()
                tiles[int(y//70)][int(x//70)] = Image(tilesLocation[int(y//70)][int(x//70)], "Images/tile.gif")
                tiles[int(y//70)][int(x//70)].draw(win)
                tilesFlagged = tilesFlagged - 1
                rememberFlags[int(y//70)][int(x//70)] = 0
                
        elif (key == "c") or (key == "C"): #NOTHING (FOR IF USER MISCLICKS AND WANTS TO CLICK A NEW TILE)
            continue 


aboutLocation = [[Point(75,75),Point(225,75),Point(375,75)],[Point(75,225),Point(225,225),Point(375,225)],[Point(75,375),Point(225,375),Point(375,375)]]

win = GraphWin("Minesweeper!", 450,450, autoflush = False)
one = Image(Point(75,75), "Images/1opening.gif")
one.draw(win)
smile = Image(Point(225,75), "Images/smiley.gif")
smile.draw(win)
start = Image(Point(375,75), "Images/0opening.gif")
start.draw(win)
mine = Image(Point(75,225), "Images/mineopening.gif")
mine.draw(win)
two = Image(Point(225,225), "Images/2opening.gif")
two.draw(win)
blank = Image(Point(375,225), "Images/0opening.gif")
blank.draw(win)
blank = Image(Point(75,375), "Images/0opening.gif")
blank.draw(win)
three = Image(Point(225,375), "Images/3opening.gif")
three.draw(win)
flag = Image(Point(375,375), "Images/flagopening.gif")
flag.draw(win)
start = Text(Point(375,75), "START")
start.setSize(28)
start.draw(win)
about = Text(Point(75,375), "ABOUT")
about.setSize(28)
about.draw(win)



while True:
    startClick = win.getMouse ()
    startx = startClick.getX ()
    starty = startClick.getY ()
    if starty <= 450 and starty >= 300 and startx <= 150: #START BUTTON
        aboutCover = [[1,1,0],[1,1,1],[1,1,1]] #Covers the opening screen's pictures when ABOUT text needs to be showed. 
        for row in range (3):
            for col in range (3):
                if aboutCover[row][col] == 1:
                    coverAbout = Image(aboutLocation[row][col], "Images/0opening.gif")
                    coverAbout.draw(win)
                    by = Text(Point(75,55), "NOAH KIM 2021")
                    forr = Text(Point(75,95), "FOR ICS201")
                    date = Text(Point(225,225), "June 20, 2021")
                    instructions1 = Text(Point(225,325), "INSTRUCTIONS & RULES:")
                    instructions2 = Text(Point(225,350), "CLICK A TILE TO SELECT IT.")
                    instructions3 = Text(Point(225,375), "PRESS Z TO DIG, X TO FLAG, AND C IF YOU WISH TO SELECT A NEW TILE")
                    instructions4 = Text(Point(225,400), "DIG ALL SAFE SPOTS AND YOU WIN ")
                    instructions5 = Text(Point(225,425), "DIG A MINE AND YOU LOSE")
                    trout = Image(Point(225, 75), "Images/trout.gif")
                    by.setSize(15)
                    forr.setSize(15)
                    date.setSize(15)
                    instructions1.setSize(15)
                    instructions1.setFill("red")
                    instructions2.setSize(15)
                    instructions3.setSize(12)
                    instructions4.setSize(15)
                    instructions5.setSize(15)
                    by.draw(win)
                    forr.draw(win)
                    date.draw(win)
                    instructions1.draw(win)
                    instructions2.draw(win)
                    instructions3.draw(win)
                    instructions4.draw(win)
                    instructions5.draw(win)
                    trout.draw(win)
                     
    elif startx <= 450 and startx >= 300 and starty <= 150:
        pygame.mixer.music.load("Sounds/start.wav") #starting noise is played
        pygame.mixer.music.play()
        win.close()
        game() #Game is started!
        
            
