import pygame
import os
import random
from copy import deepcopy


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def rotate(image, rect, angle):
    new_image = pygame.transform.rotate(image, angle)
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect


pygame.init()
screen = pygame.display.set_mode((500, 500), pygame.SRCALPHA)
system = pygame.sprite.Group()


class Star(pygame.sprite.Sprite):
    image = load_image("star.png", (0, 0, 0))
    image = pygame.transform.smoothscale(image, (5, 5))

    def __init__(self, group):
        super().__init__(group)
        self.image = Star.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(600)
        self.rect.y = random.randrange(600)

    def update(self):
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   random.randrange(3) - 1)


class Background:
    def __init__(self):
        self.image = load_image('background.png')
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.y = -50
        self.size_d = -1
        self.count = 0
        self.stars = pygame.sprite.Group()
        for _ in range(400):
            Star(self.stars)

    def update(self):
        self.rect.x += self.size_d
        self.rect.y += self.size_d
        self.count += self.size_d
        if self.count == -20:
            self.size_d = 1
        elif self.count == 20:
            self.size_d = -1
        for i in self.stars:
            i.update()

    def draw(self, screen, draw_stars=True):
        screen.blit(self.image, self.rect)
        if draw_stars:
            self.stars.draw(screen)


class Letter(pygame.sprite.Sprite):
    def __init__(self, group, sym):
        super().__init__(group)
        self.image = load_image(sym + '.png', (0, 0, 0))
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.size_d = -1

    def update(self):
        self.rect.x += self.size_d
        self.rect.y += self.size_d
        self.size_d = -self.size_d


class Word(pygame.sprite.Group):
    def __init__(self, word, pos, letter_size=None):
        super().__init__()
        dif = 0
        self.pos = pos
        self.y = pos[1]
        for i in range(len(word)):
            if word[i] == ' ':
                continue
            if word[i] == '/' and letter_size is not None:
                pos = (pos[0], pos[1] + letter_size[1])
                dif = letter_size[0] * (i + 1)
                continue
            temp = Letter(self, word[i])
            if letter_size is None:
                letter_size = (temp.rect.width, temp.rect.height)
            temp.rect.x = pos[0] + i * letter_size[0] - dif
            temp.rect.y = pos[1]
            temp.rect.width = letter_size[0]
            temp.rect.height = letter_size[1]
            temp.image = pygame.transform.smoothscale(temp.image, (letter_size[0], letter_size[1]))
            temp.size_d = -1

    def update(self, run_out, update=1):
        if run_out:
            for i in self:
                i.rect.y -= 10
            self.y -= 10
            return
        if update:
            for i in self:
                i.update()

    def move(self, x, y):
        for i in self:
            i.rect.x += x - self.pos[0]
            i.rect.y += y - self.pos[1]
        self.pos = (x, y)


class Tooltip:
    def __init__(self, need_rect, mouse_pos, text, screen, reverse=0):
        self.text = Word(text, mouse_pos, (15, 15))
        self.need_rect = need_rect
        self.screen = screen
        self.reverse = reverse
        self.mouse_pos = mouse_pos
        temp = text.split('/')
        max_len = 0
        for i in temp:
            if len(i) > max_len:
                max_len = len(i)
        self.max_len = max_len
        if reverse == 0:
            self.rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 15 * max_len, 15 * (text.count('/') + 1))
        else:
            self.text = Word(text, (mouse_pos[0] - max_len * 15, mouse_pos[1]), (15, 15))
            self.rect = pygame.Rect(mouse_pos[0] - max_len * 15, mouse_pos[1], 15 * max_len, 15 * (text.count('/') + 1))
        if self.need_rect.collidepoint(mouse_pos):
            self.text.draw(self.screen)
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

    def update_popul(self, new_info):
        self.__init__(self.need_rect, self.mouse_pos, new_info, screen, self.reverse)

    def update(self, mouse_pos):
        if self.need_rect.collidepoint(mouse_pos):
            if self.reverse == 0:
                self.text.move(mouse_pos[0], mouse_pos[1])
                self.rect.x = mouse_pos[0]
                self.rect.y = mouse_pos[1]
            else:
                self.text.move(mouse_pos[0] - 15 * self.max_len, mouse_pos[1])
                self.rect.x = mouse_pos[0] - 15 * self.max_len
                self.rect.y = mouse_pos[1]
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
            self.text.draw(self.screen)


class Planet(pygame.sprite.Sprite):
    def __init__(self, group, planet_name, x, y):
        super().__init__(group)
        self.image = load_image(planet_name + '.png', (0, 0, 0))
        self.planet_name = planet_name
        desize = (25, 25)
        if planet_name == 'saturn':
            desize = (100, 50)
        elif planet_name in ['uran', 'neptune']:
            desize = (50, 50)
        elif planet_name == 'jupiter':
            desize = (100, 100)
        self.image = pygame.transform.smoothscale(self.image, desize)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + (100 - desize[1]) // 2

    def get_clicked(self):
        return Life(300, 300)


class Board:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 10

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.left, self.top, self.width * self.cell_size + 1,
                                                   self.height * self.cell_size + 1))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (0, 0, 0),
                                 (self.left + j * self.cell_size + 1,
                                  self.top + i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), (self.left + j * self.cell_size + 1,
                                                           self.top + i * self.cell_size + 1,
                                                           self.cell_size - 2, self.cell_size - 2))
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (self.left + j * self.cell_size + 1,
                                                         self.top + i * self.cell_size + 1,
                                                         self.cell_size - 2, self.cell_size - 2))

    def get_cell(self, mouse_pos):
        temp_x = (mouse_pos[0] - self.left) // self.cell_size
        temp_y = (mouse_pos[1] - self.top) // self.cell_size
        if (temp_x < 0 or temp_x >= self.width) or (temp_y < 0 or temp_y >= self.height):
            return None
        else:
            return temp_y, temp_x

    def on_click(self, cell_cords):
        if cell_cords is None:
            return 0
        self.board[cell_cords[0]][cell_cords[1]] = 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return self.on_click(cell)


class Life(Board):
    def alive_neighbours(self, x, y):
        count = 0
        if x > 0:
            if y > 0:
                count += self.board[x - 1][y - 1]
            if y < self.height - 1:
                count += self.board[x - 1][y + 1]
            count += self.board[x - 1][y]
        if x < self.width - 1:
            if y > 0:
                count += self.board[x + 1][y - 1]
            if y < self.height - 1:
                count += self.board[x + 1][y + 1]
            count += self.board[x + 1][y]
        if y > 0:
            count += self.board[x][y - 1]
        if y < self.height - 1:
            count += self.board[x][y + 1]
        return count

    def next_move(self):
        copy_field = [[0] * self.width for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0 and self.alive_neighbours(i, j) == 3:
                    copy_field[i][j] = 1
                if self.board[i][j] == 1 and (self.alive_neighbours(i, j) < 2 or self.alive_neighbours(i, j) > 3):
                    copy_field[i][j] = 0
                    continue
                elif self.board[i][j] == 1:
                    copy_field[i][j] = 1
        self.board = deepcopy(copy_field)

    def alive_count(self):
        count = 0
        for i in self.board:
            for j in i:
                if j == 1:
                    count += 1
        return count
