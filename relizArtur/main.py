#Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500
window = display.set_mode(
(win_width, win_height)
)
display.set_caption("Shooter Game")
background = transform.scale(
image.load("road.jpg"), 
(win_width, win_height)
)

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        
        self.speed = player_speed
       
        self.player_image=player_image
        self.size_x=size_x
        self.size_y=size_y
        self.image = transform.scale(image.load(self.player_image), (self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного гравця
class Player(GameSprite):
 
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 50, -15)
        bullets.add(bullet)

    def fire1(self):
        raketa = Bullet(raketa_bullet, self.rect.centerx, self.rect.top, 15, 50, -15)
        raketan.add(raketa)


    # клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
            


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

class raketas(GameSprite):
    # рух ракети
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо ракета йде за екран
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()
raketan = sprite.Group()
            
# шрифти і написи
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))



img_enemy = "carwar2.png"  # ворог
score = 0  # збито кораблів
lost = 0  # пропущено кораблів
goal = 20 # стільки кораблів потрібно збити для перемоги
max_lost = 4 # програли, якщо пропустили стільки
life = 3

if life == 3:
            life_color = (0, 150, 0)
if life == 2:
            life_color = (150, 150, 0)
if life == 1:
            life_color = (150, 0, 0)

text_life = font1.render(str(life), 1, life_color)
window.blit(text_life, (650, 10))

img_hero = "car1.png"
img_bullet = "bullet.png" # куля
img_ast = "carwar.png" # астероїд
raketa_bullet = "raketa.png"
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 120, randint(1, 5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 120, randint(1, 7))
    asteroids.add(asteroid)
run = True
mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
finish = False

rel_time = False  # прапор, що відповідає за перезаряджання

num_fire = 0  # змінна для підрахунку пострілів

while run:
   for e in event.get():
       if e.type == QUIT:
           run = False

       elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #if num_fire < 5 and rel_time == False:
                    #num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

            if e.key == K_b:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire1()

                if num_fire >= 5 and rel_time == False : #якщо гравець зробив 5 пострілів
                    last_time = timer() #засікаємо час, коли це сталося
                    rel_time = True #ставимо прапор перезарядки




   if not finish:
    window.blit(background,(0, 0))
    # пишемо текст на екрані
    text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
    window.blit(text, (10, 20))
    text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
    window.blit(text_lose, (10, 50))
    ship.update()
    monsters.update()
    ship.reset()
    monsters.draw(window)
    bullets.update()
    bullets.draw(window)
    raketan.update()
    raketan.draw(window)
    asteroids.update()
    asteroids.draw(window)

# перезарядка
    # if rel_time == True:
    #         now_time = timer() # зчитуємо час
         
    #         if now_time - last_time < 3: #поки не минуло 3 секунди виводимо інформацію про перезарядку
    #             reload = font2.render('Wait, reload...', 1, (150, 0, 0))
    #             window.blit(reload, (260, 460))
    #         else:
    #             num_fire = 0     #обнулюємо лічильник куль
    #             rel_time = False #скидаємо прапор перезарядки

         #перевірка зіткнення кулі та монстрів (і монстр, і куля при дотику зникають)
    collides = sprite.groupcollide(monsters, bullets, True, True)
   
    for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 120, randint(1, 5))
            monsters.add(monster)

    collides = sprite.groupcollide(asteroids, bullets, True, True)
    for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            asteroid = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 120, randint(1, 5))
            asteroids.add(asteroids)
            
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 120, randint(1, 5))
            monsters.add(monster)
    '''        
    # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
    if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True # програли, ставимо тло і більше не керуємо спрайтами.
            window.blit(lose, (200, 200))
    '''
    # якщо спрайт торкнувся ворога зменшує життя
    if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True) 
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

    #програш
    if life == 0 or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))

    # перевірка виграшу: скільки очок набрали?
    if score >= goal:
            finish = True
            window.blit(win, (200, 200))


   display.update()
   time.delay(50)