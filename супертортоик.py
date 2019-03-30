import pygame
import os
import random
global schot
global text
import easygui
from easygui import *
global var1
name = ''
names = ''
schot = 0
text = ''
def vvod():
    global var1
    global name
    msg = "Введите имя"
    title = "Вход"
    fieldValues2 = enterbox(msg, title)
    var1 = fieldValues2
    if len(var1) > 8:
        var1 = var1[:8]
    name = var1


def saveGameState():
    global schot
    global text
    f = open("savedata.txt", "a")
    line1 = " ".join([str(schot)])
    f.write(line1 + "\n")
    f.close()
    f = open("savedata.txt", "r")
    text = f.read()
    text = text.split()
    for i in range(len(text)):
        text[i] = int(text[i])
    f.close()
    #screen.fill((0, 0, 0))
    #font = pygame.font.Font(None, 50)
    
    #s = font.render(text, 1, pygame.Color('red'))
    #screen.blit(s , (10, 10))
def NaMeS():
    global schot
    global names
    f = open("names.txt", "a")
    line1 = name
    f.write('\n' + line1)
    f.close()
    f = open("names.txt", "r")
    names = f.read()
    names = names.split()
    f.close()    



def generate_tortik(n):
    # я решила не заморачиваться поэтому тортики это одноцветные прямоугольники
    colors = [(255, 0, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255), (0, 255, 0)]
    k = pygame.Surface([n, ht])
    random.shuffle(colors)
    k.fill(colors[0])
    return k, colors[0]


def loose():
    global text
    global names
    global schot
    global running
    # это вызывается когда человек проиграл
    saveGameState()
    NaMeS()
    screen.fill((0, 0, 0))
    sm = [[text[i], names[i]] for i in range(len(names))]
    sm.sort(reverse=True)
    font = pygame.font.Font(None, 50)
    for i in range(10):
        s1 = font.render(str(sm[i][1]), 1, pygame.Color('red'))
        s2 = font.render(str(sm[i][0]), 1, pygame.Color('red'))
        screen.blit(s1 , (10, 150 + i*30))
        screen.blit(s2 , (200, 150 + i*30)) 
    font = pygame.font.Font(None, 50)
    my_text = 'Твой счет: ' + str(schot)
    s = font.render(my_text, 1, (255, 0, 102))
    a = font.render('Ты проиграл', 1, (128, 128, 255))
    screen.blit(s , (10, 10))
    screen.blit(a , (10, 70))
    
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def load_image(name, color_key=None):
    fullname = name
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image


class Tortik(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.h = ht
        self.x = 0
        self.y = 100
        self.rect = pygame.Rect(self.x, self.y, n, self.h)
        a = generate_tortik(n)
        self.image, self.col = a[0], a[1]
        self.dir = 1

    def reinit(self):
        # это обновление текущего тортика(не обычный init чтобы страрый нигде не хранился)
        self.h = ht
        self.x = 0
        self.y = 100
        self.rect = pygame.Rect(self.x, self.y, n, self.h)
        a = generate_tortik(n)
        self.image, self.col = a[0], a[1]
        self.dir = 1

    def tuda_suda(self):
        # передвигание влево-вправо
        if self.x <= 0:
            self.dir = 1
        if self.x >= w - n:
            self.dir = -1
        self.x += self.dir
        self.update()

    def fall(self):
        global running
        global nx
        global schot
        
        # чтобы не ломалось если нажать на крестик пока падает
        while self.y < h - (k+1)*self.h:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            self.y += 1
            screen.fill((0, 0, 0))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 50)
            s= font.render("Score: " + str(schot), 1, pygame.Color('red'))
            screen.blit(s , (10, 10))
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
            clock.tick(300)
        if k > 0:
            self.obrez(oldy[-1].x)
        else:
            nx = self.x

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, n, ht)
        
    def obrez(self, mx):
        global schot
        global n
        global nx
        # проверять касание не нужно т к оно вызывается когда гарантированно касание есть
        if abs(mx - self.x) <= 2:
            n += 5
            schot += 5
            self.rect = pygame.Rect(self.x, self.y, n, ht)
        else:
            if mx > self.x:
                nx = mx
                n = n - (mx-self.x)
                self.rect = pygame.Rect(self.x, self.y, n, ht)
                schot += 1
            elif mx < self.x:
                nx = self.x
                n = n - (self.x-mx)
                self.rect = pygame.Rect(self.x, self.y, n, ht)
                schot += 1
        if n < 0:
            f = False
            loose()


class Static(pygame.sprite.Sprite):
    def __init__(self, x, y, col):
        super().__init__(all_sprites)
        super().__init__(old_sprites)
        self.x = x
        self.y = y
        self.n = n
        self.col = col
        self.rect = pygame.Rect(x, y, n, ht)
        self.image = pygame.Surface([n, ht])
        self.image.fill(col)

    def reinit(self, x, y, col, n):
        self.x = x
        self.y = y
        self.n = n
        self.col = col
        self.rect = pygame.Rect(x, y, n, ht)
        self.image = pygame.Surface([n, ht])
        self.image.fill(col)


if __name__ == '__main__':
    pygame.init()
    vvod()
    msg = "                      Добро пожаловать в игру, " + str(var1) # Str + Int = Error
    msgbox(msg, "Приветствие", "Let's go")
    w = 300
    h = 600
    ht = 50
    f = True
    K = 5 #сколько тортиков будет показываться
    k = 0 #ckoлько тортиков сейчас
    screen = pygame.display.set_mode([w, h])
    screen.fill((0, 0, 0))
    fon = pygame.image.load('tecna.png').convert_alpha()
    screen.blit(fon, (0, 0))
    oldy = [] # массив с тортиками которые внизу
    old_sprites = pygame.sprite.Group() # это вроде не пригодилось
    all_sprites = pygame.sprite.Group()
    all_sprites.draw(screen)
    all_sprites.update()
    running = True
    fps = 100
    clock = pygame.time.Clock()
    t = True
    n = 250
    nx = 0
    Tortic = Tortik() #активный тортик
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    Tortic.fall()
                    k += 1
                    if f:
                        if k > K:
                            for i, a in enumerate(oldy[:-1]):
                                a.reinit(oldy[i+1].x,  oldy[i+1].y + ht, oldy[i+1].col, oldy[i+1].n)
                            oldy[-1].reinit(nx, Tortic.y + ht, Tortic.col, n)
                            k -= 1
                        else:
                            oldy.append(Static(nx, Tortic.y, Tortic.col))
                        Tortic.reinit()
        if f:
            Tortic.tuda_suda()
            screen.fill((0, 0, 0))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 50)
            s= font.render("Score: " + str(schot), 1, pygame.Color('red'))
            screen.blit(s , (10, 10))
            all_sprites.draw(screen)
            all_sprites.update()
            
            pygame.display.flip()
            clock.tick(fps)
    pygame.display.flip()
pygame.quit()