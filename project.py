import pygame
import random
from time import sleep

WHITE = (255, 255, 255)  #배경은 기본적으로 흰색
RED = (255, 0, 0)  #게임오버에 쓰일 빨간색 값
pad_width = 1000
pad_height = 530  #해상도 입력(이왕이면 배경이랑 딱 맞게)
background_width = 1000
enemy_width = 60
aircraft_width = 80
aircraft_height = 36
enemy_width = 60
enemy_height = 50
fires1_width = 100
fires1_height = 50
fires2_width = 120
fires2_height = 40


def Score(count):
    global gamepad

    font = pygame.font.SysFont(None, 25)
    text = font.render('Enemy Passed: ' + str(count), True, WHITE)
    gamepad.blit(text, (0, 0))


def gameOver():
    global gamepad
    dispMessage('Game Over')


def textObj(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()


def dispMessage(text):
    global gamepad

    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width / 2), (pad_height / 2))
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(2)
    runGame()


def crash():
    global gamepad, explosion_sound
    pygame.mixer.Sound.play(explosion_sound)
    dispMessage('Game Over')


def Obj(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))  #물체를 모두 이걸로 묶음 아마도


def runGame():
    global gamepad, aircraft, clock, background1, background2
    global enemy, fires, bullet, boom
    global shot_sound
    isShotEnemy = False
    boom_count = 0

    enemy_passed = 0

    bullet_xy = []

    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0  #y값 변화

    enemy_x = pad_width
    enemy_y = random.randrange(0, pad_height)

    fire_x = pad_width
    fire_y = random.randrange(0, pad_height)
    random.shuffle(fires)
    fire = fires[0]

    background1_x = 0
    background2_x = background_width

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change -= 10  #위로 움직이는 속도
                elif event.key == pygame.K_DOWN:
                    y_change += 10  #아래로 움직임
                elif event.key == pygame.K_x:  #총쏘는 키 설정 현재 x
                    pygame.mixer.Sound.play(shot_sound)
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height / 2
                    bullet_xy.append([bullet_x, bullet_y])

                elif event.key == pygame.K_SPACE:
                    sleep(5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        gamepad.fill(WHITE)  #게임패드 초기화

        #배경
        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width

        Obj(background1, background1_x, 0)
        Obj(background2, background2_x, 0)

        #적 놓치면 게임오버
        Score(enemy_passed)
        if enemy_passed > 1:
            gameOver()

        #플레이어 뱅기
        y += y_change
        if y < 0:
            y = 0
        elif y > pad_height - aircraft_height:
            y = pad_height - aircraft_height

        #적 뱅기
        enemy_x -= 7
        if enemy_x <= 0:
            enemy_passed += 1
            enemy_x = pad_width
            enemy_y = random.randrange(0, pad_height)

        #운석
        if fire[1] == None:
            fire_x -= 45
        else:
            fire_x -= 35

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        #탄막
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 20  #탄막속도
                bullet_xy[i][0] = bxy[0]

                if bxy[0] > enemy_x:
                    if bxy[1] > enemy_y and bxy[1] < enemy_y + enemy_height:
                        bullet_xy.remove(bxy)
                        isShotEnemy = True

                if bxy[0] >= pad_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        #적에 의해서 파괴될때
        if x + aircraft_width > enemy_x:
            if (y > enemy_y and y < enemy_y + enemy_height) or \
            (y + aircraft_height > enemy_y and y + aircraft_height < enemy_y + enemy_height):
                crash()

        #운석에 의해 파괴될때
        if fire[1] != None:
            if fire[0] == 0:
                fires_width = fires1_width
                fires_height = fires1_height

            elif fire[0] == 1:
                fires_width = fires2_width
                fires_height = fires2_height

            if x + aircraft_width > fire_x:
                if (y > fire_y and y < fire_y + fires_height) or \
                (y + aircraft_height > fire_y and y + aircraft_height < fire_y + fires_height):
                    crash()

        Obj(aircraft, x, y)

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                Obj(bullet, bx, by)

        if not isShotEnemy:
            Obj(enemy, enemy_x, enemy_y)
        else:
            Obj(boom, enemy_x, enemy_y)
            boom_count += 1
            if boom_count > 5:
                boom_count = 0
                enemy_x = pad_width
                enemy_y = random.randrange(0, pad_height - enemy_height)
                isShotEnemy = False

        if fire[1] != None:
            Obj(fire[1], fire_x, fire_y)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()


def initGame():
    global gamepad, aircraft, clock, background1, background2
    global enemy, fires, bullet, boom
    global shot_sound, explosion_sound

    fires = []

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('pyGallag')  #게임제목
    aircraft = pygame.image.load('images\\ship.png')  # png 파일 있는곳 위치 적기 (백슬래시는 무조건 두개씩!!)
    background1 = pygame.image.load('images\\iasd.png')  # png 파일 있는곳 위치 적기
    background2 = background1.copy()  #말그대로 카피
    enemy = pygame.image.load('images\\enemy.png')  #적 이미지 위치
    fires.append((0, pygame.image.load('images\\asteroid1.png')))  #운석 이미지 위치
    fires.append((1, pygame.image.load('images\\asteroid3.png')))  #두번째 운석 이미지 위치
    shot_sound = pygame.mixer.Sound('images\\laser beam.wav')
    explosion_sound = pygame.mixer.Sound('images\\boom sound.wav')
    pygame.mixer.music.load('images\\bgm.wav')
    pygame.mixer.music.play(-1)

    boom = pygame.image.load('images\\boom.png')

    for i in range(3):
        fires.append((i + 2, None))

    bullet = pygame.image.load('images\\laser.png')  #총알 이미지 위치 넣기

    clock = pygame.time.Clock()
    runGame()


if __name__ == '__main__':
    initGame()
