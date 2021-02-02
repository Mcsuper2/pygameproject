# main.py
# program code goes here

import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "Coins in the snow"
MAX_SNOW = 100


# Classes


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.image = pygame.image.load("images/sprite.png")
        self.image = pygame.transform.scale(self.image, [80, 104])

        self.rect = self.image.get_rect()

        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.vel_x

        # Move up/down
        self.rect.y += self.vel_y

        # Set boundaries

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.vel_x *= -0.01
        elif self.rect.top < 0:
            self.vel_y *= 0.01

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = HEIGHT - self.rect.height

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.vel_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.vel_x = 6

    def jump(self):
        """ Called when user hits 'jump' button. """
        self.rect.y += 2
        self.rect.y -= 2
        self.vel_y = -10

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.vel_x = 0


class Snow:
    def __init__(self, size=2):

        self.colour = WHITE
        self.size = size

        # randomize location
        self.x = random.randrange(0, WIDTH)
        self.y = random.randrange(0, HEIGHT)

        self.y_vel = random.randrange(1, 3)

    def update(self):
        self.y += self.y_vel

        # if the snow reaches the bottom
        # reset position
        if self.y > HEIGHT:
            self.y = random.randrange(-15, 0)
            self.x = random.randrange(0, WIDTH)

    def draw(self, screen):
        """Draw snow on screen

        Arguments:
            screen = surface to draw on

        Returns:
            none
            """
        pygame.draw.circle(
            screen,
            self.colour,
            (self.x, self.y),
            self.size
        )


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super(Coin, self).__init__()
        self.image = pygame.image.load("./images/Coin.png")
        self.image = pygame.transform.scale(self.image, [16, 16])
        self.rect = self.image.get_rect()


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    score = 0

    # create snow
    snow_list = []
    for i in range(MAX_SNOW):
        snow = Snow(size=random.randrange(3, 6))
        snow_list.append(snow)

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    coin_sprites = pygame.sprite.Group()

    # Populate sprite groups
    player = Player()
    coin = Coin()
    coin.rect.x = 170
    all_sprites.add(coin)
    coin_sprites.add(coin)
    all_sprites.add(player)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vel_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.vel_x > 0:
                    player.stop()

        # ----- LOGIC
        # game terminates when the player collects 15 coins
        if score == 15:
            pygame.quit()
            print("You Win!")
        all_sprites.update()
        coin_sprites.update()
        for snow in snow_list:
            snow.update()

        # collision

        coin_hit_group = pygame.sprite.spritecollide(player, coin_sprites, True)

        # spawn a new coin if a coin is collected by the player
        if len(coin_hit_group):
            score += 1
            coin = Coin()
            all_sprites.add(coin)
            coin_sprites.add(coin)
            coin.rect.x = random.randrange(0, WIDTH)
            coin.rect.y = random.randrange(0, HEIGHT)

        # ----- DRAW
        screen.fill(BLACK)
        all_sprites.draw(screen)
        for snow in snow_list:
            snow.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
