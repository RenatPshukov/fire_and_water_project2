# TODO Импортируем нужные библиотеки
import os
import pygame
from random import randint, choice

# устанавливаем название окну
pygame.display.set_caption('Insanity balls')  # название

# импортируем картинку логотипа из папки data
ICON = pygame.image.load('data\\logo_1.png')
# устанавливаем иконку (логотип)
pygame.display.set_icon(ICON)

# задаём ширину и высоту
SIZE = WIDTH, HEIGHT = 1400, 900
# устанавливаем размер окна
screen = pygame.display.set_mode(SIZE)

# Используется для управления fps
clock = pygame.time.Clock()


# TODO функция загрузки спрайтов
def load_image(name, color_key=None):
    # достаём картинку из папки data
    fullname = os.path.join('data', name)
    try:
        # создаём спрайт убирая задний фон
        image = pygame.image.load(fullname).convert_alpha()
    # в случае отсутствия картинки в папке data выводим ошибку
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    # если есть цветовой ключ то устанавливаем его
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    # иначе убираем задний фон спрайта
    else:
        image = image.convert_alpha()
    # возвращаем спрайт
    return image


# TODO функция секундомера
def display_time(time_s):
    # временная строка с десятыми долями секунды
    # устанавливаем шрифт
    font = pygame.font.Font(None, 30)
    time_str = str(int(time_s * 10) / 10)
    # строка секундомера
    label = font.render(f"Time : {time_str}", True, 'red')
    # отрисовываем на экране секундомер в координатах (20, 20)
    screen.blit(label, (20, 20))


# TODO класс шарика
class Ball(pygame.sprite.Sprite):
    # инициализация класса
    def __init__(self, group, radius, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        # импортируем спрайты шаров из папки data, устанавливая им размер radius
        red_ball = pygame.transform.scale(load_image("red_ball.png"), (radius, radius))
        blue_ball = pygame.transform.scale(load_image("blue_ball.png"), (radius, radius))
        darkblue_ball = pygame.transform.scale(load_image("darkblue_ball.png"), (radius, radius))
        green_ball = pygame.transform.scale(load_image("green_ball.png"), (radius, radius))
        orange_ball = pygame.transform.scale(load_image("orange_ball.png"), (radius, radius))
        pink_ball = pygame.transform.scale(load_image("pink_ball.png"), (radius, radius))
        purple_ball = pygame.transform.scale(load_image("purple_ball.png"), (radius, radius))
        white_ball = pygame.transform.scale(load_image("white_ball.png"), (radius, radius))
        yellow_ball = pygame.transform.scale(load_image("yellow_ball.png"), (radius, radius))
        s = [red_ball, blue_ball, darkblue_ball, green_ball, orange_ball, pink_ball, purple_ball, white_ball,
             yellow_ball]
        super().__init__(group)
        ds = choice(s)
        self.image = ds
        self.rect = pygame.Rect(x, y, radius, radius)
        self.vx = randint(-13, 13)
        self.vy = randint(-13, 13)
        while self.vx == 0:
            self.vx = randint(-13, 13)
        while self.vy == 0:
            self.vy = randint(-13, 13)

    # функция взаимодествия (столкновение и рикошет) шаров и границ
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


# TODO класс игрока(курсора)
class Cursor(pygame.sprite.Sprite):
    # инициализация класса
    def __init__(self, group):
        super().__init__(group)
        # импортируем спрайт курсора из папки data
        self.image = load_image("arrow.png")  # это будет будущий спрайт
        self.rect = self.image.get_rect()
        # скрываем системный курсор
        pygame.mouse.set_visible(False)


# TODO класс границ
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    # инициализация класса
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        # вертикальная стенка
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        # горизонтальная стенка
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def check_collision(alli):
    for ball in alli:
        if cursor.rect.collidepoint(ball.rect.center):
            return True


def game_over():
    print('-')
    termination = True
    while termination:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        print('-')
        return True
    if keys[pygame.K_ESCAPE]:
        print('+')
        return False

    pygame.display.update()
    clock.tick(15)


# группы спрайтов, содержащие горизонтальные и вертикальные границы
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()

# создаём границы
Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

# создаём шары
for i in range(30):
    Ball(all_sprites, randint(30, 80), randint(100, 1300), randint(100, 800))

# группа, содержащая спрайт игрока(курсора)
trigger = pygame.sprite.Group()
# создаём игрока(курсор)
cursor = Cursor(trigger)


# TODO основной цикл
def main_runner():
    # переменная времени (секунды)
    time_seconds = 0
    # флаг цикла игры
    running = True
    # пока running == True
    while running:
        # инициализация Pygame:
        pygame.init()

        # флаг для установки конца игры
        stop = False

        # ожидание закрытия окна:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # проверка события передвижения мыши
            if event.type == pygame.MOUSEMOTION:
                # изменяем положение спрайта-стрелки
                cursor.rect.topleft = event.pos

        # задаём задний фон
        bg = pygame.image.load('data\\bg3.png')
        screen.blit(bg, (0, 0))

        # отрисовываем секундомер
        display_time(time_seconds)

        # Обновляем спрайты
        all_sprites.update()
        trigger.update()

        # Рисуем объекты на окне
        all_sprites.draw(screen)
        trigger.draw(screen)
        # Проверка на столкновение курсора с шарами
        if check_collision(all_sprites):
            running = False
        # FPS
        fps = clock.tick(30)
        # конвертируем время (время идёт пока игрок не коснулся шара)
        if not stop:
            time_seconds += fps / 1000
        # Обновляем экран после рисования объектов
        pygame.display.flip()
    return game_over()


while main_runner():
    pass
pygame.quit()
quit()