import pygame
from pygame.locals import *

# Constants
WIDTH, HEIGHT = 800, 200
DIGITS = 5
TIME_STEPS = 10  ** (DIGITS - 1)
BLOCK_SIZE = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Block class
class Block:
    def __init__(self, x, y, m, v, w, screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.m = m
        self.v = v
        self.w = w

    def update(self):
        self.x += self.v

    def show(self):
        pygame.draw.rect(self.screen, BLACK, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def collide(self, other):
        return self.x + BLOCK_SIZE >= other.x and self.x <= other.x + BLOCK_SIZE

    def bounce(self, other):
        sum_m = self.m + other.m
        new_v = (self.m - other.m) / sum_m * self.v
        new_v += (2 * other.m / sum_m) * other.v
        return new_v

    def hit_wall(self):
        return self.x <= 0 or self.x + BLOCK_SIZE >= WIDTH

    def reverse(self):
        self.v *= -1

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pi Day Collisions")

    block1 = Block(100, 100, 1, 0, 0, screen)
    m2 = 100 ** (DIGITS - 1)
    block2 = Block(300, 100, m2, -1 / TIME_STEPS, 20, screen)

    count = 0

    # Font for displaying the count
    font = pygame.font.Font(None, 72)

    clock = pygame.time.Clock()

    clack_sound = pygame.mixer.Sound('data/clack.wav')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        # Update
        clack_sound_played = False
        for i in range(TIME_STEPS):
            if block1.collide(block2):
                v1 = block1.bounce(block2)
                v2 = block2.bounce(block1)
                block1.v = v1
                block2.v = v2
                clack_sound_played = True
                count += 1

            if block1.hit_wall():
                block1.reverse()
                clack_sound_played = True
                count += 1

            block1.update()
            block2.update()

        # Draw
        screen.fill(WHITE)
        block1.show()
        block2.show()

        # Display count
        count_text = font.render(str(count).zfill(DIGITS), True, BLACK)
        screen.blit(count_text, (10, 10))

        pygame.display.flip()

        # Play clack sound
        if clack_sound_played:
            clack_sound.play()

        clock.tick(60)

if __name__ == "__main__":
    main()
