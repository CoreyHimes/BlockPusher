import pygame
from pygame import *
from queue import *

pygame.init()
display_scale = 1
display_width = 800*display_scale
display_height = 600*display_scale

black = (0, 0, 0)
white = (255, 255, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Title')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, tiles):
        super().__init__()

        self.image = pygame.image.load('images/CharacterSprite.png').convert_alpha()

        self.x_change = 0
        self.y_change = 0
        self.rect = Rect(x, y, 32, 32)
        self.jump_legal = True
        self.tiles = tiles
        self.mask = pygame.mask.from_surface(self.image)
        self.level_complete = False

    def jump(self):

        if self.jump_legal is True:
            self.y_change = -4.5
            self.jump_legal = False

    def collision_detection_x(self, x_change, tiles):
        # Checks for Entitys for the player to collide with

        for t in tiles:
            if pygame.sprite.collide_rect(self,t):
                if pygame.sprite.collide_mask(self, t) is not None:

                    if isinstance(t, Platform):

                        if x_change > 0:
                            while pygame.sprite.collide_mask(self,t) is not None:
                                self.rect.left += -1

                        if x_change < 0:
                            while pygame.sprite.collide_mask(self,t) is not None:
                                self.rect.left += 1

                    if isinstance(t, Box):

                        t.x_change=self.x_change
                        # this function checks if the box collides with another object
                        if self.jump_legal is True:
                            if t.box_collision_x(tiles) is False:
                                print (self.rect.left)

                                if x_change > 0:
                                    while pygame.sprite.collide_mask(self, t) is not None:
                                        self.rect.left += -1

                                if x_change < 0:
                                    while pygame.sprite.collide_mask(self, t) is not None:
                                        self.rect.left += 1

                                t.update()
                        else:
                            t.x_change = 0
                            if x_change > 0:
                                while pygame.sprite.collide_mask(self, t) is not None:
                                    self.rect.left += -1

                            if x_change < 0:
                                while pygame.sprite.collide_mask(self, t) is not None:
                                    self.rect.left += 1


    def collision_detection_y(self, y_change, tiles):
        # collides the player while he is moving in the y direction

        for t in tiles:
            if pygame.sprite.collide_rect(self,t):
                if pygame.sprite.collide_mask(self,t) is not None:
                    if isinstance(t, Platform):
                        if y_change > 0:
                            self.rect.bottom = t.rect.top
                            self.jump_legal = True
                            self.y_change = 0

                        if y_change < 0:
                            while pygame.sprite.collide_mask(self, t) is not None:
                                self.rect.top += 1
                                self.y_change = 0

                    if isinstance(t, Box):
                        if y_change > 0:
                            self.rect.bottom = t.rect.top
                            self.jump_legal = True
                            self.y_change = 0

                        if y_change < 0:
                            self.rect.top = t.rect.bottom
                            self.y_change = 0

                    if isinstance(t, Teleporter):
                        self.level_complete = True

    def go_left(self):
        self.x_change = -2

    def go_right(self):
        self.x_change = 2

    def stop(self):
        self.x_change = 0

    def gravity(self):
        self.y_change += .15

    def update(self):

        self.gravity()
        self.rect.left += self.x_change
        self.collision_detection_x(self.x_change,self.tiles)
        self.rect.top += self.y_change
        self.collision_detection_y(self.y_change,self.tiles)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/PlatformEX.png').convert_alpha()
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/test.png').convert_alpha()
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Teleporter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/Teleporter.png').convert_alpha()
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/Box.png').convert_alpha()
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_change = 0
        self.y_change = 0
        self.tiles = []

    def update(self):
        self.gravity()
        self.rect.left += self.x_change
        self.box_collision_x(self.tiles)
        self.x_change = 0
        self.rect.bottom += self.y_change
        self.box_collision_y(self.tiles)

    def tile_adder(self, tiles):
        self.tiles = tiles

    def gravity(self):
        self.y_change += .15

    def box_collision_x(self, tiles):
        for t in tiles:
            if t is not self:
                if pygame.sprite.collide_rect(self,t):
                    if pygame.sprite.collide_mask(self, t) is not None:
                        if self.x_change > 0:
                            while pygame.sprite.collide_mask(self,t) is not None:
                                self.rect.left += -1

                        if self.x_change < 0:
                            while pygame.sprite.collide_mask(self,t) is not None:
                                self.rect.left += 1

                        return True
        return False

    def box_collision_y(self, tiles):
        for t in tiles:
            if t is not self:
                if pygame.sprite.collide_rect(self, t):
                    if pygame.sprite.collide_mask(self, t) is not None:
                        if self.y_change > 0:
                            self.rect.bottom = t.rect.top
                            self.y_change = 0


# This is a class of constants, namely the array representations of all of the levels
class Levels():
    def __init__(self):
        super().__init__()
        # this level should never actually be called, merely a blank slate to build more levels
        self.level_template =[
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP", ]
        self.test_level_1 = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                    PPPP",
            "P                       P",
            "PP                      P",
            "PPP              B      P",
            "PPPPPPPPPPPPPPPPPPP     P",
            "P                       P",
            "P                       P",
            "P                 PPPPPPP",
            "P                       P",
            "P         PPPPPPP       P",
            "P                      TP",
            "P                     PPP",
            "PP                      P",
            "P              B  B     P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP", ]
        self.test_level_2 = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                    PPPP",
            "P                       P",
            "PP                      P",
            "PPP              B      P",
            "PPPPPPPPPPPPPPPPPPP     P",
            "P                       P",
            "P                       P",
            "P                 PPPPPPP",
            "P                       P",
            "P         PPPPPPP       P",
            "P                      TP",
            "P                     PPP",
            "PP                      P",
            "P BB           B  B     P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP", ]
        self.level_1 =[
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P          B            P",
            "P      PPPPP  PP   PPPPPP",
            "PPPPPP     P  PPPP      P",
            "P          P  P         P",
            "P      PPPPP  PP   PPPPPPP",
            "P          P  PPP       P",
            "PPPPPP     P  PPPP      P",
            "P          P  PPPPP P   P",
            "P      PPPPP  P        PP",
            "P          P  P       PPP",
            "PPPPPP     P  PP     PPPP",
            "P          P  P      P TP",
            "P      PPPPP        PP  P",
            "P          P         P  P",
            "PPPP  P    P  PPPPPPPP  P",
            "P   B P                 P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP", ]
        self.level_2 = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P   PPPPPPPPPPPPPPPPPPP P",
            "P                     p P",
            "P                     P P",
            "P                     P P",
            "P                     P P",
            "P                     P P",
            "P                     P P",
            "P                     P P",
            "P                     P P",
            "P                     P P",
            "P       P             P P",
            "P                     P P",
            "P         B           P P",
            "P    B  B P           P P",
            "P  PPPPPP PPPPPPPPPPPPP P",
            "P B B     PT            P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP", ]

    # this function returns a queue of all game levels
    def level_queue(self):
        level_queue = Queue(maxsize=10)
        #level_queue.put(self.level_1)
        level_queue.put(self.level_2)
        return level_queue


class Level():
    def __init__(self):
        super().__init__()

    def build_level(self, level):
        entities = pygame.sprite.Group()
        tiles = []
        x = y = 0
        current_level = level
        # build the level
        for row in current_level:
            for col in row:
                if col == "P":
                    p = Platform(x, y)
                    tiles.append(p)
                    entities.add(p)
                if col == "S":
                    s = Spike(x, y)
                    tiles.append(s)
                    entities.add(s)
                if col == "T":
                    t = Teleporter(x,y)
                    tiles.append(t)
                    entities.add(t)
                if col == "B":
                    b = Box(x,y)
                    tiles.append(b)
                    entities.add(b)
                x += 32
            y += 32
            x = 0
        # adds reference to the entities for box
        for entity in entities:
            if isinstance(entity, Box):
                entity.tile_adder(entities)
        return entities


def gameloop():
# Initializes game loop with level and player start locations
    end = False
    level_queue = Levels().level_queue()
    current_level = Levels()
    tiles = Level().build_level(level_queue.get())
    x = (display_width*0.12)
    y = (display_height * 0.9)
    player = Player(x, y, tiles)

    while not end:
        # starts a new level if the player has completed the current level
        if player.level_complete is True:
            #todo this try except causes the game to loop for now
            if not level_queue.empty():
                tiles= Level().build_level(level_queue.get())
                player = Player(x, y, tiles)
            else:
                end=True

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
        for tile in tiles:
            tile.update()
            gameDisplay.blit(tile.image, (tile.rect.left,tile.rect.top))

        gameDisplay.blit(player.image,(player.rect.left,player.rect.top))
        pygame.display.flip()
        clock.tick(60)


gameloop()
pygame.quit()
quit()
