import pygame


pygame.init()
pygame.font.init()
score = 0

screen = pygame.display.set_mode((800, 600))
myfont = pygame.font.SysFont('Courier', 25)

pygame.display.set_caption("Breakout Game")
icon = pygame.image.load('./img/logo.png')
pygame.display.set_icon(icon)


class Enemy:
    all = []
    x_coord = 5
    y_coord = 5

    def __init__(self):
        if len(Enemy.all) < 9:
            self.img = pygame.image.load('./img/break_red.png')
            self.score = 300
        elif len(Enemy.all) <= 26:
            self.img = pygame.image.load('./img/break_yellow.png')
            self.score = 200
        elif len(Enemy.all) > 26:
            self.img = pygame.image.load('./img/break_green.png')
            self.score = 100
        self.x = self.x_coord
        self.y = self.y_coord
        Enemy.all.append(self)
        Enemy.x_coord += 88
        if len(Enemy.all) % 9 == 0:
            Enemy.x_coord = 5
            Enemy.y_coord += 18




# Player
player_img = pygame.image.load('./img/player.png')
player_x = 370
player_y = 530
player_x_change = 0
player_x_range = [player_x, player_x+60]
player_y_range = [player_y, player_y+15]
player_movement_side = 'None'

def player(x, y):
    screen.blit(player_img, (x, y))

# Ball
ball_img = pygame.image.load('./img/ball.png')
ball_x = 390
ball_y = 290
ball_x_change = 0.03
ball_y_change = 0.05
ball_x_range = [ball_x, ball_x+20]
ball_y_range = [ball_y, ball_y+20]


def ball(x, y):
    screen.blit(ball_img, (x, y))


def ball_check_bounce_platform():
    global ball_y_change, ball_x_change
    if (ball_y+20 > player_y and ball_y+20 < player_y+15) and ((ball_x >= player_x and ball_x <= player_x+60) or (ball_x+20 >= player_x and ball_x <= player_x+60)):
        if player_movement_side == 'Right':
            ball_x_change = abs(ball_x_change)
        if player_movement_side == 'Left':
            ball_x_change = abs(ball_x_change) * -1
        ball_y_change *= -1


def ball_check_bounce_walls():
    global ball_y_change, ball_x_change, running
    if ball_x <= 0 and ball_x_change < 0:
        ball_x_change *= -1
    if ball_y <= 0 and ball_y_change < 0:
        ball_y_change *= -1
    if ball_x+20 >= 800 and ball_x_change > 0:
        ball_x_change *= -1
    if ball_y >= 600:
        running = False


for i in range(54):
    enemy = Enemy()


def ball_check_bounce_bricks():
    global ball_y_change, ball_x_change, score
    for enemy in Enemy.all:

        if (ball_y > enemy.y and ball_y+20 <= enemy.y) and ((ball_x >= enemy.x and ball_x <= enemy.x+83) or (ball_x+20 >= enemy.x and ball_x+20 <= enemy.x+83)):
            score += enemy.score
            del Enemy.all[Enemy.all.index(enemy)]
            ball_y_change *= -1.03
            ball_x_change *= 1.03
            break

        elif (ball_x < enemy.x and ball_x+20 >= enemy.x) and ((ball_y >= enemy.y and ball_y <= enemy.y+13) or (ball_y+20 >= enemy.y and ball_y+20 <= enemy.y+13) or (ball_y+10 >= enemy.y and ball_y + 10 <= enemy.y+13)):
            score += enemy.score
            del Enemy.all[Enemy.all.index(enemy)]
            ball_y_change *= 1.03
            ball_x_change *= -1.03
            break

        elif (ball_x <= enemy.x+83 and ball_x+20 > enemy.x+83) and ((ball_y >= enemy.y and ball_y <= enemy.y+13) or (ball_y+20 >= enemy.y and ball_y+20 <= enemy.y+13) or (ball_y+10 >= enemy.y and ball_y + 10 <= enemy.y+13)):
            score += enemy.score
            del Enemy.all[Enemy.all.index(enemy)]
            ball_y_change *= 1.03
            ball_x_change *= -1.03
            break

        elif ball_y < enemy.y+13 and ((ball_x >= enemy.x and ball_x <= enemy.x+83) or (ball_x+20 >= enemy.x and ball_x+20 <= enemy.x+83)):
            score += enemy.score
            del Enemy.all[Enemy.all.index(enemy)]
            ball_y_change *= -1.03
            ball_x_change *= 1.03
            break


def enemy_display():
    for enemy in Enemy.all:
        screen.blit(enemy.img, (enemy.x, enemy.y))


def score_display():
    global score
    textsurface = myfont.render(f'Score: {score}', False, (255, 255, 255))
    screen.blit(textsurface, (0, 570))


running = True
while running:

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_x > 0:
                player_x_change = -0.2
                player_movement_side = 'Left'
            if event.key == pygame.K_RIGHT and player_x < 740:
                player_x_change = 0.2
                player_movement_side = 'Right'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
                player_movement_side = 'None'
    if player_x > 0 and player_x_change < 0 or player_x < 740 and player_x_change > 0:
        player_x += player_x_change

    ball_check_bounce_bricks()
    ball_check_bounce_walls()
    ball_check_bounce_platform()
    ball_x += ball_x_change
    ball_y += ball_y_change
    ball(ball_x, ball_y)
    player(player_x, player_y)
    enemy_display()
    score_display()
    pygame.display.update()
