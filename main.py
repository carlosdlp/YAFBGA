import sys, pygame
from pygame.locals import *
from objects import *
import settings
import copy
import csv

# INITIALIZE
pygame.init()
settings.init()


# SET CANVAS AND COLORS
size = settings.width + 100, settings.height + 75
black = 0, 0, 0
white = 255,255,255
red = 209, 20, 0

screen = pygame.display.set_mode(size)
screen.fill(black)



def main():
    # CREATE BIRDS AND PIPES
    birds = []
    for i in range(0,settings.population):
        birds.append(Bird())

    pipes = []
    pipes.append(Pipe())
    backup = []

    clock = pygame.time.Clock()
    counter = 0 
    highS = 0
    onlybest = -1
    generation = 0
    ticker = 50
    generationScores = []
    

    font = pygame.font.Font(None, 26)
    while True:
        counter = counter + 1
        #LOCK FPS TO 60
        clock.tick(ticker)

        #FILL BACKGROUND WITH BLACK
        screen.fill(black)
        
        #BIRDS DINAMYCS
        for i in range(len(birds)-1,-1,-1):
            if onlybest > 0:
                if i == 0:
                    birds[i].show(screen,red)
            else:
                if birds[i].best:
                    birds[i].show(screen,red)
                else:
                    birds[i].show(screen,white)
            birds[i].update()

            if pipes[0].x > birds[i].pos[0]:
                birds[i].calcDist(pipes[0])
                if birds[i].pos[1] < pipes[0].y+80 and birds[i].pos[1] > pipes[0].y:
                    birds[i].score = birds[i].score + 10
            else:
                birds[i].calcDist(pipes[1])
                if birds[i].pos[1] < pipes[1].y+80 and birds[i].pos[1] > pipes[1].y:
                    birds[i].score = birds[i].score + 10

            birds[i].think()

            if birds[i].pos[1] <= 0:
                birds[i].pos[1] = 0
            elif birds[i].pos[1] >= settings.height:
                backup.append(birds.pop(i))


        #PIPES DINAMYCS
        for i in range (len(pipes)-1,-1,-1):
            pipes[i].show(screen,white)
            pipes[i].update()
            if pipes[i].x <= -30:
                pipes.pop(i)

            # CHECK COLLISION WITH BIRDS
            for j in range(len(birds)-1,-1,-1):

                if birds[j].pos[1] < pipes[i].y or birds[j].pos[1] > pipes[i].y+80:
                    if birds[j].pos[0] > pipes[i].x and birds[j].pos[0] < pipes[i].x + 30:
                        backup.append(birds.pop(j))


        # ADD NEW PIPE EVERY 100 FRAMES
        if counter % 100 == 0:
            pipes.append(Pipe())

        # WHEN ALL BIRDS ARE DEAD RESET GAME
        if len(birds) == 0:
            pipes = []
            pipes.append(Pipe())
            counter = 0 
            generation = generation + 1

            maxScore = 0
            scores = []
            for i in range(0, len(backup)):
                scores.append(backup[i].score)
                if backup[i].score > maxScore:
                    maxScore = backup[i].score
                    maxBird = i
                    if backup[i].score > highS:
                        highS = backup[i].score

            generationScores.append(scores)
            with open('scoresData.csv', 'w') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerows(generationScores)

            bestBird = backup[maxBird]
            bestBird.pos = copy.deepcopy(np.array([50,int(settings.height/2)]))
            bestBird.v = 0
            bestBird.score = 0
            bestBird.best = False
            for i in range(0,settings.population):
                birds.append(copy.deepcopy(bestBird))
                if i > 0:
                    birds[i].brain.mutate()
                else:
                    birds[i].best = True

            backup = []


        # EVENTS
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    onlybest = onlybest * -1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    ticker = ticker + 100

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ticker = ticker - 100

        fps = font.render("FPS: {}".format(str(int(clock.get_fps()))), True, (255,0,0))
        score = font.render("SCORE: {}".format(str(int(birds[0].score))), True, (255,0,0))
        highScore = font.render("HIGHSCORE: {}".format(str(int(highS))), True, (255,0,0))
        generationText = font.render("GENERATION: {}".format(str(int(generation))), True, (255,0,0))
        speed = font.render("SPEED: {}".format(str(int(ticker))), True, (255,0,0))
        birdsleft = font.render("BIRDS ALIVE: {}".format(str(int(len(birds)))), True, (255,0,0))

        screen.blit(fps, (0,settings.height + 15))
        screen.blit(generationText, (0,settings.height + 35))
        screen.blit(birdsleft, (0,settings.height + 55))
        screen.blit(highScore, (200,settings.height + 15))
        screen.blit(score, (200,settings.height + 35))
        screen.blit(speed, (200,settings.height + 55))

        pygame.draw.rect(screen, white, pygame.Rect(0, settings.height, settings.width, 10))
        pygame.draw.rect(screen, white, pygame.Rect(settings.width, 0, 10, settings.height+10))
        pygame.display.update()




main()