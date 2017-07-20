import pygame
from pygame import *

pygame.init()
display_scale = 1
display_width =800*display_scale
display_height =600*display_scale


black = (0,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Title')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, tiles):
        super().__init__()

        self.image = pygame.image.load('lib/CharacterSprite.png')

        self.x_change = 0
        self.y_change = 0
        self.rect = Rect(x, y, 32, 32)
        self.jump_legal = True
        self.tiles=tiles

    def jump(self):

        if self.jump_legal == True:
            self.y_change = -6
            self.jump_legal = False

    def collision_detection_x(self, x_change, tiles):
        #Checks for Entitys for the player to collide with

        for t in tiles:
            if pygame.sprite.collide_rect(self, t):
                #if isinstance(t, Spike):

                if isinstance(t, Platform):

                    if x_change > 0:
                        self.rect.right = t.rect.left
                        print(self.rect.bottom)

                    if x_change < 0:
                        self.rect.left = t.rect.right



    def collision_detection_y(self, y_change, tiles):
        # collides the player while he is moving in the y direction

        for t in tiles:
            if pygame.sprite.collide_rect(self, t):
                if isinstance(t, Platform):
                    if y_change > 0:
                        print (t.rect.top)
                        self.rect.bottom = t.rect.top
                        self.jump_legal = True
                        self.y_change = 0


                    if y_change < 0:
                        self.rect.top = t.rect.bottom
                        self.y_change = 0

    def go_left(self):
        self.x_change = -2

    def go_right(self):
        self.x_change = 2

    def stop(self):
        self.x_change = 0

    def gravity(self):
       self.y_change += .1

    def update(self):

        self.gravity()
        self.rect.left += self.x_change
        self.collision_detection_x(self.x_change,self.tiles)
        self.rect.top += self.y_change
        self.collision_detection_y(self.y_change,self.tiles)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('lib/PlatformEX.png')
        #self.image.convert()
       # self.image.f

        self.rect = Rect(x, y, 32, 32)
    def update(self):
        pass

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('lib/test.png')
        #self.image.convert()
       # self.image.f

        self.rect = Rect(x, y, 32, 32)
    def update(self):
        pass
class Level():
    def __init__(self):
        super().__init__()

def gameloop():



    end = False
    entities = pygame.sprite.Group()

    tiles = []
    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                       P",
        "P                       P",
        "P                       P",
        "P                    PPPP",
        "P                       P",
        "P                       P",
        "P                S      P",
        "PPPPPPPPPPPPPPPPPPP     P",
        "P                       P",
        "P                       P",
        "P                 PPPPPPP",
        "P                       P",
        "P         PPPPPPP       P",
        "P                       P",
        "P                     PPP",
        "P                       P",
        "P                       P",
        "PPPPPPPPPPPPPPPPPPPPPPPPP",]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                tiles.append(p)
                entities.add(p)
            if col == "S":
                s = Spike(x,y)
                tiles.append(s)
                entities.add(s)

            x += 32
        y += 32
        x = 0
    x = (display_width*0.45)
    y = (display_height * 0.80)
    player = Player(x,y,tiles)
    while not end:
        gameDisplay.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_z:
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:
                    player.stop()
                elif event.key == pygame.K_RIGHT:
                    player.stop()
        player.update()
        print
        for platform in tiles:
            gameDisplay.blit(platform.image, (platform.rect.left,platform.rect.top))


        gameDisplay.blit(player.image,(player.rect.left,player.rect.top))

        pygame.display.flip()


        clock.tick(60)


gameloop()
pygame.quit()
quit()