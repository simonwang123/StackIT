import pygame
import time


# Initialize pygame and store colors that will be used into variables.
pygame.init()
white = (255,255,255)
objectColor = (153,217,234)
backgroundColor = (63,72, 204)

# Store images, sound and fonts to be used into variables. Set volume, create Screen object for GUI canvas.
clock = pygame.time.Clock()
pygame.display.set_caption('StackIT')
icon = pygame.image.load('images\\icon.png')
pygame.display.set_icon(icon)
font1 = pygame.font.Font("fonts\\aldhabi.ttf", 50)
font2 = pygame.font.Font("fonts\\aldhabi.ttf", 40)
font3 = pygame.font.Font("fonts\\aldhabi.ttf", 70)
sound = pygame.mixer.Sound('sounds\\stackit.wav')
success = pygame.mixer.Sound('sounds\\success.wav')
fail = pygame.mixer.Sound('sounds\\fail.wav')
sound.set_volume(0.3)
success.set_volume(0.2)
fail.set_volume(0.2)
introbg = pygame.image.load('images\\openbg.png')
Screen = pygame.display.set_mode((400,600))



# Enter the INTRODUCTION LOOP when called. If the player presses the space key, end loop and enter GAME LOOP.         
def gameIntro():
    GameStart = False
    sound.play(loops = -1)
    while GameStart == False:
        for event in pygame.event.get():
            Screen.blit(introbg,(0,0,400,600))    
            text = font1.render("Press Space key to stack", True, white)
            Screen.blit(text, [45,475])
            pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GameStart = True
                    sound.stop()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Enter the GAME LOOP when called.
def gameLoop():

    # Define function for printing points on the screen.
    def score(points):
        text = font2.render("Stacks: "+ str(points), True, white)
        Screen.blit(text, [20,0])


        
    # Initialize the variables as they should be before the game begins.
    GameOver = False
    xLoc = 200
    yLoc = 550
    height = 50
    width = 200
    lastxLoc = xLoc
    lastWidth = width
    speed = 6
    points = 0
    Screen.fill(backgroundColor)
    moveLeft = True
    moveRight = False
    Exit = False
    levelHeight = 250
    leveli = 1
    chopLeft = False
    chopRight = False
    choppedHeight = 0
    levelUps = 0
    
    
    # Begin the GAME LOOP    
    while not Exit:

        # Special case for calculations of lastWidth when points == 0.
        if points == 0:
            lastWidth = 800
            lastxLoc = xLoc
            lastobjectColorxLoc = xLoc
        else:
            lastWidth = width

            
            
        # If player lost, enter the nested GAME OVER LOOP. If player presses R key, reset all variables and re-enter GAME LOOP by ending GAME OVER LOOP. 
        while GameOver == True:
            Screen.fill(backgroundColor)
            text = font1.render('Game Over!', True, objectColor)
            text2 = font2.render('Press R to play again or Q to quit.', True, objectColor)
            text3 = font2.render('Your Score was', True, objectColor)
            text4 = font1.render(str(points - 1), True, objectColor)
            Screen.blit(text, [125,0])
            Screen.blit(text2, [25,90])
            Screen.blit(text3, [120,280])
            Screen.blit(text4, [190, 320])
            pygame.display.update()

            for event in pygame.event.get():                
                if event.type == pygame.QUIT:
                    Exit = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        GameOver = False
                        xLoc = 200
                        yLoc = 550
                        height = 50
                        width = 200
                        lastxLoc = xLoc
                        lastWidth = width
                        speed = 6
                        points = 0
                        Screen.fill(backgroundColor)
                        moveLeft = True
                        moveRight = False
                        Exit = False
                        levelHeight = 250
                        leveli = 1
                        chopLeft = False
                        chopRight = False
                        choppedHeight = 0
                        levelUps = 0
                    if event.key == pygame.K_q:
                            GameOver = False
                            Exit = True



        # Player loses and enters Game Over screen when width has shrunk to nil or negative.              
        if width <= 0:
            GameOver = True
        
        # Close game if ESC key is pressed.           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Exit = True                
                    
                # If space key is pressed:  
                if event.key == pygame.K_SPACE:
                    # 1. Move object up by 50 pixels
                    yLoc = yLoc - height
                    
                    # 2. Leaving a +/- 8 pixel buffer, if the width of the object is the same size as the width of the last object, do not change the width of the next object. If width is less than 20 pixels, player loses the buffer.
                    if xLoc + width <= lastxLoc + lastWidth + 8 and xLoc >= lastxLoc - 8 and width >= 20:
                        lastWidth = width
                        success.play()
                        
                    # 3. Chop the right if object hangs off the right of the last object. Chop the left if object hangs off the left of the last object.
                    elif  (xLoc + width) > (lastxLoc + lastWidth):
                        chopRight = True
                        fail.play()

                    elif xLoc < lastxLoc:
                        chopLeft = True
                        fail.play()
                    
                    # As long as the player has not lost, increase points by 1.                    
                    if GameOver == False:   
                        points = points + 1
                        


        # Collision detection.
        if xLoc <= 0:
            moveLeft = False
            moveRight = True
        if xLoc + width >= 400:
            moveRight = False
            moveLeft = True
        if moveLeft == True:
            xLoc = xLoc - speed
        if moveRight == True:
            xLoc = xLoc + speed

            

        # Every frame, fill the canvas, print the current object and the last object.
        Screen.fill(backgroundColor)
        pygame.draw.rect(Screen, objectColor, (xLoc, yLoc, width, height))
        pygame.draw.rect(Screen, objectColor, (lastxLoc, yLoc + 50, lastWidth, height))
        score(points)

        

        # If chopped, enter a short loop to show the animation of the chop. 
        if chopRight == True:
            
            if xLoc > lastxLoc + lastWidth:
                GameOver = True
                continue
            
            choppedHeight = yLoc
            lastobjectColorxLoc = xLoc
            choppedWidth =  width - ((xLoc + width) - (lastxLoc + lastWidth))
                       
            while choppedHeight < 600:
                Screen.fill(backgroundColor)
                pygame.draw.rect(Screen,objectColor, ((lastxLoc + lastWidth), choppedHeight,(xLoc + width) - (lastxLoc + lastWidth), height))
                pygame.draw.rect(Screen, objectColor, (xLoc, yLoc, choppedWidth, height))
                
                pygame.draw.rect(Screen, objectColor, (lastxLoc, yLoc + 50, lastWidth, height))
                score(points)
                pygame.display.update()
                choppedHeight = choppedHeight + 1
                      
            width = lastxLoc + lastWidth - xLoc
            lastxLoc = xLoc
            chopRight = False

        if chopLeft == True:
            
            if xLoc + width < lastxLoc:
                GameOver = True
                continue
            
            choppedHeight = yLoc
            lastobjectColorxLoc = xLoc
            choppedWidth =  xLoc + width - lastxLoc
                       
            while choppedHeight < 600:
                Screen.fill(backgroundColor)
                pygame.draw.rect(Screen,objectColor, (xLoc, choppedHeight,lastxLoc - xLoc, height))
                pygame.draw.rect(Screen, objectColor, (lastxLoc, yLoc, choppedWidth, height))
                
                pygame.draw.rect(Screen, objectColor, (lastxLoc, yLoc + 50, lastWidth, height))
                score(points)
                pygame.display.update()
                choppedHeight = choppedHeight + 1
                
            width = xLoc + width - lastxLoc
            lastxLoc = lastxLoc
            chopLeft = False



        # Every time stacks reach the top of the screen, speed up until the max speed. Enter a short loop to show the animation of the speed up alert.
        if (points == leveli * 11 + 1):
            
            if levelUps <= 2:
                speed = speed + 1.2
                
            while levelHeight > -100 and levelUps <= 2:
                
                if levelUps < 2:
                    speedUp =  font3.render("Speed Up!", True, white)
                    Screen.fill(backgroundColor)
                    Screen.blit(speedUp, [110,levelHeight])
                    pygame.display.update()
                    levelHeight = levelHeight - 0.2
                    
                elif levelUps == 2:
                    maxSpeed =  font3.render("MAX SPEED!", True, white)
                    Screen.fill(backgroundColor)
                    Screen.blit(maxSpeed, [75,levelHeight])
                    pygame.display.update()
                    levelHeight = levelHeight - 0.2
                
            levelHeight = 250
            leveli = leveli + 1
            yLoc = 500
            levelUps = levelUps + 1

 
        pygame.display.update()
        clock.tick(30) 
    

gameIntro()
gameLoop()
pygame.quit()
quit()
