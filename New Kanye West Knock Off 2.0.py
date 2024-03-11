import pygame
import sys


pygame.init()
pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 1200
CAMERA_WIDTH, CAMERA_HEIGHT = 800, 600

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shinki da got")

block = pygame.image.load('block.png')
floor = pygame.image.load('floor.png')
player = pygame.image.load('yosi_gizan_noBG.png')
coin = pygame.image.load('coin.png')
enemy = pygame.image.load('enemy.png')
spike = pygame.image.load('spike.png')

cloud1 = pygame.image.load('cloud1.png')
cloud2 = pygame.image.load('cloud2.png')
cloud3 = pygame.image.load('cloud3.png')
cloud4 = pygame.image.load('cloud4.png')
cloud5 = pygame.image.load('cloud5.png')
cloud6 = pygame.image.load('cloud6.png')

blocks_x = [251]
start_y = [840]
blocks_y = [795]

coin_x = []
coin_y = []


clock = pygame.time.Clock()
running = True


class Movement:
    def __init__(self, xPos, yPos,enemy_xPos):
        self.xPos = xPos
        self.yPos = yPos
        self.velocityY = 0
        self.camera_x = 0
        self.facingLeft = True
        self.coinCounter = 0
        self.collected_coins = [False] * len(coin_x)
        self.enemy_xPos = [400, 1200]
        self.goLeft = False
        self.allow_movement = True

    def move(self):
        normalYpos = [807]

        keys = pygame.key.get_pressed()
        if self.allow_movement == True:
            for i in range(len(blocks_x)):
                if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.yPos == normalYpos[0] or (
                        (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and
                        self.yPos == normalYpos[1] or (
                        keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.yPos == normalYpos[
                            2]) and (
                        blocks_x[i] >= self.xPos >= blocks_x[i] - 48):
                    if (blocks_x[0] - 48 <= self.xPos <= blocks_x[i]) and (self.yPos == normalYpos[0]):
                        if (blocks_x[2] - 48 <= self.xPos <= blocks_x[3]):
                            self.velocityY = -16.5
                        else:
                            self.velocityY = -13
                    else:
                        self.velocityY = -22

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.facingLeft = True
                self.xPos -= 7
                if keys[pygame.K_PAUSE]:
                    self.xPos -= 1000


            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.facingLeft = False
                self.xPos += 7
                if keys[pygame.K_PAUSE]:
                    self.xPos += 1000






        self.velocityY += 1
        self.yPos += self.velocityY

        if self.yPos > 807:
            self.yPos = 807
            self.velocityY = 0

        if self.xPos < 0:
            self.xPos = 0

        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(str(self.coinCounter)+" Coins", False, (255, 255, 255))
        surface.blit(text_surface, (1100, 0))

        self.camera_x = max(0, min(self.xPos - CAMERA_WIDTH, 16000))

    def draw_player_cube(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.facingLeft:
                flipped_player = pygame.transform.flip(player, True, False)
                surface.blit(flipped_player, (self.xPos - self.camera_x, self.yPos))
            else:
                surface.blit(player, (self.xPos - self.camera_x, self.yPos))
        elif not self.facingLeft:
            surface.blit(player, (self.xPos - self.camera_x, self.yPos))
        else:
            flipped_player = pygame.transform.flip(player, True, False)
            surface.blit(flipped_player, (self.xPos - self.camera_x, self.yPos))




    @staticmethod
    def Grass(x, y):
        surface.blit(floor, (x, y))

    @staticmethod
    def blocks():
        for i in range(len(blocks_x)):
            surface.blit(block, (blocks_x[i], start_y[i]))


    @staticmethod
    def spike(x,y):
        surface.blit(spike,(x,y))

    def clouds(self, x, y, surface):
        space_between_clouds = 200
        cloud_images = [cloud1, cloud2, cloud3, cloud4, cloud5, cloud6]
        cloud_width = cloud1.get_width()

        index = 0
        while x < 16000:
            surface.blit(cloud_images[index], (x, y))
            x += cloud_width + space_between_clouds
            index = (index + 1) % len(cloud_images)

    def coins(self):
        for i in range(len(coin_x)):
            if not self.collected_coins[i] and coin_x[i] - 96 <= self.xPos <= coin_x[i] and coin_y[i] + 96 >= self.yPos >= coin_y[i]:
                self.coinCounter += 1
                self.collected_coins[i] = True

    def lose(self):
        if self.allow_movement == False:

            surface.fill((255, 255, 255))
            pygame.display.flip()
            pygame.time.delay(1000)
            self.enemy_xPos = self.enemy_xPos
            return



    def collision(self):
        for i in range(len(blocks_x)):
            if blocks_x[i] - 48 <= self.xPos <= blocks_x[i] and blocks_y[i] -48 <= self.yPos <= start_y[i]:
                self.yPos = blocks_y[i]
                self.velocityY = 0

        for enemy_x in self.enemy_xPos:
            if abs(enemy_x - self.xPos) < 10 and 759 < self.yPos <= 807 and self.yPos != 759:
                self.allow_movement = False
                my_game.lose()


        for enemy_x in self.enemy_xPos:
            if (enemy_x - 48 <= self.xPos <= enemy_x + 48) and (self.yPos + 96 >= 759) and (enemy_x - 48 <= self.xPos <= enemy_x + 48) and (self.yPos + 96 <= 807):
                self.enemy_xPos.remove(enemy_x)

    def enemies(self):
        startEnemy_xPos = [400, 1200]
        for i in range(len(self.enemy_xPos)):
            if self.enemy_xPos[i] == startEnemy_xPos[i]:
                self.goLeft = False
            elif self.enemy_xPos[i] == startEnemy_xPos[i]+200:
                self.goLeft = True

            if self.goLeft:
                self.enemy_xPos[i] -= 1
            else:
                self.enemy_xPos[i] += 1

            if self.goLeft:
                flipped_enemy = pygame.transform.flip(enemy, True, False)
            else:
                flipped_enemy = enemy

            surface.blit(flipped_enemy, (self.enemy_xPos[i] - self.camera_x, 837))




my_game = Movement(0, 807 ,443)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    surface.fill((83, 142, 237))

    my_game.move()
    my_game.collision()
    my_game.Grass(0 - my_game.camera_x, 887)
    my_game.blocks()
    my_game.coins()
    my_game.draw_player_cube()
    my_game.clouds(0-my_game.camera_x, 100, surface)
    my_game.enemies()
    my_game.spike(100,807)



    for i in range(len(coin_x)):
        if not my_game.collected_coins[i]:
            surface.blit(coin, (coin_x[i] - my_game.camera_x, coin_y[i]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

