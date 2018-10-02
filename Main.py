#spacehship game

import sys,pygame,random, operator, pickle
from sprites import *
from constants import *
from my_functions import *
pygame.mixer.init()
pygame.init()

# About game
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Invaders")

# Load font
myFont = pygame.font.SysFont("monospace", 30)
alertFont = pygame.font.SysFont("mistral", 50)

# Setting the background image
background = pygame.image.load("img/space.jpg")
backgroundRect = background.get_rect()

# A list that contains all the sprites
all_sprites_list = pygame.sprite.Group()
# Add lists for the lazers and enemies for colissions
lazerList = pygame.sprite.Group()
enemyList = pygame.sprite.Group()
enemy_hit_list = pygame.sprite.Group()

# Load the ship
playerShip = Ship()
playerShip.rect.x = 205 #x coordinate
playerShip.rect.y = 810 #y coordinate

# Add the ship to the list
all_sprites_list.add(playerShip)

# Game features
gameLoop = True
startLoop = True
endLoop = True
clock=pygame.time.Clock()
start_ticks=pygame.time.get_ticks() #starter tick - for time counter
highscoredict = {}
username = myinput("str","Enter your username: ")

# Load enemies prerequisite
gameRound = 1
wave = 0
xpos = 0
ypos = 70
speed = 1
clr = "pink"

# Splash screen for start
def startScreen(scrn):
    titleFont = pygame.font.SysFont("mistral", 50)
    instructFont = pygame.font.SysFont("calibri", 25)
    scrn.fill(deep_blue)
    titleText = titleFont.render("Welcome to Invaders", 1, white)
    scrn.blit(titleText, ((80, 50)))
    inst1 = instructFont.render("Instructions:", 1, white)
    inst2 = instructFont.render("For left/right movement:", 1, white)
    inst3 = instructFont.render("To shoot:", 1, white)
    inst4 = instructFont.render("Every 25 points:          for a special lazer", 1, white)
    inst5 = instructFont.render("PRESS ANY KEY TO CONTINUE", 1, white)
    leftArrow = pygame.image.load("img/Key_Arrow_Left.png").convert_alpha()
    rightArrow = pygame.image.load("img/Key_Arrow_Right.png").convert_alpha()
    upArrow = pygame.image.load("img/Key_Arrow_Up.png").convert_alpha()
    spaceKey = pygame.image.load("img/Key_Space_bar.png").convert_alpha()
    shipStart = pygame.image.load("img/ship.png").convert_alpha()
    scrn.blit(leftArrow, ((285, 190)))
    scrn.blit(rightArrow, ((345, 190)))
    scrn.blit(spaceKey, ((130, 245)))
    scrn.blit(upArrow, ((195, 290)))
    scrn.blit(inst1, ((30, 150)))
    scrn.blit(inst2, ((30, 200)))
    scrn.blit(inst3, ((30, 250)))
    scrn.blit(inst4, ((30, 300)))
    scrn.blit(inst5, ((95, 500)))
    scrn.blit(shipStart, ((205, 750)))
    pygame.display.flip()

def endScreen(scrn, hsList):
    titleFont = pygame.font.SysFont("mistral", 70)
    leaderboardFont = pygame.font.SysFont("calibri", 30)
    scrn.fill(grey)
    titleText = titleFont.render("Game Over!", 1, white)
    scrn.blit(titleText, ((100, 50)))
    ldrboard = titleFont.render("Leaderboard:", 1, white)
    scrn.blit(ldrboard, ((30, 130)))
    instr = leaderboardFont.render("Press the R key to restart.", 1, white)
    instr2 = leaderboardFont.render("OR press any other key to quit.", 1, white)
    tombstone = pygame.image.load("img/tombstone.png").convert_alpha()
    scrn.blit(tombstone, ((150, 657)))
    scrn.blit(instr, ((30, 350)))
    scrn.blit(instr2, ((30, 380)))
    pos = 165
    x = list(reversed(hsList))
    for i in range(5):
        pos+=30
        txt = leaderboardFont.render(str(i+1)+". "+str(x[i]), 1, white)
        scrn.blit(txt, ((30, pos)))
    pygame.display.flip()

# Start loop
while startLoop:
    startScreen(screen)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit(), sys.exit()
            startLoop=False
        if event.type == pygame.KEYDOWN:
            startLoop = False

# Music and sounds
pygame.mixer.music.load("snd/Shooting Stars.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
ow = pygame.mixer.Sound('snd/Ow.wav')
ow.set_volume(0.5)
pew = pygame.mixer.Sound('snd/Pew.wav')
pew.set_volume(0.5)
fail = pygame.mixer.Sound('snd/Fail.wav')
fail.set_volume(0.5)

# Main game loop
while gameLoop:
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    if gameRound > wave: #loading of a wave
        wave+=1
        num = wave*10
        if num > 50: #makes sure there isn't too many
            num = 50
        xpos = 0
        ypos = 70
        clrRand = random.randrange(1,4)
        print("colour =",clrRand)
        if clrRand == 1:
            clr = "blue"
        elif clrRand == 2:
            clr = "green"
        else:
            clr = "pink"
        for i in range(num):
            enemy = Enemy(speed, clr)
            enemy.rect.x = xpos
            enemy.rect.y = ypos
            enemyList.add(enemy)
            all_sprites_list.add(enemy)
            xpos+=50
            if xpos == 500:
                xpos = 0
                ypos += 80
        #enemy.update.speed(+1)
    for event in pygame.event.get():
        # Exit game sequence
        if event.type==pygame.QUIT:
            pygame.quit(), sys.exit()
            gameLoop=False

        # Spawns the lazer from the ship gun
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                pew.play()
                lazer = Shoot()
                lazer.rect.x = (playerShip.rect.x +42) #spawns from centre of sprite
                lazer.rect.y = (playerShip.rect.y -4)
                all_sprites_list.add(lazer)
                lazerList.add(lazer)

    # Movement of the ship (animations)
    pressed=pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        playerShip.moveLeft(5)
    if pressed[pygame.K_RIGHT]:
        playerShip.moveRight(5)
        if not pressed[pygame.K_RIGHT]:
            playerShip.default()

    # Manages the separate lazer beam
    if score%25 == 0 and score!= 0:
        pressUp = alertFont.render("PRESS UP ARROW NOW!!!", 1, blue)
        screen.blit(pressUp, ((10, 50)))
        pygame.display.flip()
        if pressed[pygame.K_UP]:
            beam = Special_Shoot()
            beam.rect.x = playerShip.rect.x +42 #spawns from centre of sprite
            beam.rect.y = playerShip.rect.y -4
            all_sprites_list.add(beam)
            lazerList.add(beam)

    # Reseting the animation when not moving
    if not pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT]:
        playerShip.default()

    # Wrap around screen
    if playerShip.rect.x < -45:
        playerShip.rect.x = width-45
    if playerShip.rect.x > width-45:
        playerShip.rect.x = -45

    for enemy in enemyList:
        if enemy.rect.y > 760: #if the enemies get too low on the screen
            fail.play()
            print("Out of bounds!")
            f = open("highscore.dat", "rb")
            currentTable = pickle.load(f)
            print(currentTable)
            tempTuple=(score, username)
            currentTable.append(tempTuple)
            currentTable.sort()
            print(currentTable)
            f.close()
            f = open("highscore.dat", "wb")
            pickle.dump(currentTable, f)
            f.close()
            while endLoop:
                endScreen(screen, currentTable)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        endLoop = False
                        if event.key==pygame.K_r:
                            for enemy in enemyList:
                                enemyList.remove(enemy)
                                all_sprites_list.remove(enemy)
                            gameRound = 1
                            wave = 0
                            speed = 1
                            score = 0
                        elif event.key!=pygame.K_r:
                            pygame.quit(), sys.exit()
                            endLoop = False
                            gameLoop = False
                            pygame.quit(), sys.exit()
                            gameLoop=False
                    if event.type==pygame.QUIT:
                        pygame.quit(), sys.exit()
                        endLoop = False
                        gameLoop = False
                        pygame.quit(), sys.exit()
                        gameLoop=False


    # Game Logic
    for lazer in lazerList:
        enemy_hit_list = pygame.sprite.spritecollide(lazer, enemyList, True) #manages colissions
        for enemy in enemy_hit_list:
            ow.play()
            score+=1 #increases score by 1 when enemy is hit
            lazerList.remove(lazer) #so the lazer can't penetrate multiple enemies
            all_sprites_list.remove(lazer)
            #enemy_hit_list.remove(enemy)
            if len(enemyList) == 0: #moves on to next round
                gameRound+=1
                print("Round =",gameRound)
        #removes lazer if misses enemy and goes off screen
        if lazer.rect.y < -10:
            lazerList.remove(lazer)
            all_sprites_list.remove(lazer)

    #THE COLLISION IS CAUSING THE GAME END ERROR
    all_sprites_list.update()


    if gameRound%5 == 0 and len(enemyList) == 0: #to increase the speed every 5 rounds
        speed+=1


    # Drawing on screen
    screen.blit(background, backgroundRect)
    screenStatus = myFont.render("Wave:"+str(gameRound)+" Score:"+str(score)+" Time:"+str(seconds)[:3], 1, white)
    screen.blit(screenStatus, ((20, 20)))

    # Drawing the sprites
    all_sprites_list.draw(screen)

    # Refresh screen
    pygame.display.flip()

    # Number of frames per second
    clock.tick(60)
