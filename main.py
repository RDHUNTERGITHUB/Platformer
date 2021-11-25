#Up to: Tutorial part 5

#-----Issues----
#Animation not smooth
#Map is lack of variation


import pygame

pygame.init()
#init framerate
clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer')


#Load the images
bg_img = pygame.image.load('img/bg.png')


#Variables
tile_size = 40

#Draw grid
def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

#Player class
class Player():
    def __init__(self,x,y):
        #Animation
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0 # used to change speed with "walk cd" at running through the frame for the animation
                         # for a more smooth animation
        for num in range (1,9): #running through the list (7 frames)
            img_right = pygame.image.load(f'img/right/r_{num}.png')
            img_right = pygame.transform.scale(img_right,(40,80))
            img_left = pygame.transform.flip(img_right, True, False) #Flip the right animation on the x-axis
            #Add frames to the list
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect() #Used for collision later
        self.rect.x = x
        self.rect.y = y
        #----Need height and width for the "dummy" rectangle---|
        self.width = self.image.get_width() # Extract the width of the character image
        self.height =self.image.get_height() #Extract the height of the character image
        #----Need height andd width for the "dummy" rectangle---|
        self.vel_y = 0 #Needs this y velocity variable or else the jump won't look smooth
        self.jumped = False #Check if the player has jumped
        self.direction = 0 #Stay in center

    def update(self):
        dx = 0
        dy = 0
        walk_cd = 0 #slow down the iteration of the animation to make it more smooth
                    ###(should be smoother as the number goes up but didn't work)###
        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1 #Counter runs when key pressed
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        #Make sure the character stand still while the key is not pressed by resetting to the first frame
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
        if self.direction == 1:
            self.image = self.images_right[self.index]
        if self.direction == -1:
            self.image = self.images_left[self.index]

        #|--------animation--------|
        if self.counter > walk_cd: #reset counter
            self.counter = 1
            self.index +=1 #going to next frame
            if self.index >= len(self.images_right): #if animation got to the last image go back to the first frame
                self.index = 0

        # add gravity
        if self.vel_y > 15:
            self.vel_y = 15
        self.vel_y += 1
        dy += self.vel_y

        #COLLISION
        # There are pygame build-in functions for collision and using rectangle this time
    #### Can't use if tile[1].colliderect(self.rect)  directly because then character and the dirt tile will overlap####
        # So we need another "dummy" rect before the collision
        for tile in world.tile_list:
            #Check for collision in "X" direction
            if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                 dx = 0 #stops moving
            # check for collision in "Y" direction
            #to create a rect, we need (x,y(location),width,height(dimension))
            if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
                #Check if below the ground aka jumping because y axis is fliped
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top #Recalculate the character's location when it's head hit the tile
                    self.vel_y = 0
                # Check if above the ground aka falling because y axis is fliped
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom  # Recalculate the character's location when it's feet hit the tile
                    self.vel_y = 0
        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255,255,255),self.rect,2) #Draws a rectangle on top of the player object and HAS A
                                                            # BOARDER of 2 so it doesn't cover the entire character



#Creating the world
class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('img/dirt.png')


        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    # noinspection PyTypeChecker
                    enemy = Enemy(col_count * tile_size, row_count *tile_size)
                    enemy_group.add(enemy) #Using .add to add to groups

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,(255,255,255), tile[1],2) #Put a white boarder around the tiles
#Enemy class
class Enemy(pygame.sprite.Sprite):
    def __int__(self,x, y): #paramater that the enemy class takes in the x and y coord
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/enemy/e1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#The numbers represents different tiles for the world that we going to make
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 7, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 4, 0, 0, 1, 1, 3, 0, 0, 3, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100,screen_height-120)
enemy_group = pygame.sprite.Group() #Create an enemy group which's similar to a list
world = World(world_data)


#Game Loop
run = True
while run:
    clock.tick(fps) #make sure the game runs smooth
    screen.blit(bg_img,(0,0)) #Puts the background image in and center it correctly (negative goes UP,positive goes DOWN)

    world.draw()

    enemy_group.draw(screen)

    player.update() #Updates player onto the screen while the game runs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Able to quit the game
            run = False

        pygame.display.update()
pygame.quit()