import sys
import pygame
from random import randint


# klasa aplikacji gra
class Agame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('a Game')
        # parametry gry
        self.max_tangos = 2
        self.max_lives = 5
        self.new_tango_interval = 30
        # elementy gry
        self.board = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.score = 0
        self.lives = self.max_lives
        self.state = 'menu'
        self.new_tango = 0

        # strzelec
        self.alfa = Alfa(self)
        # wystrzelone pociski
        self.bullets = pygame.sprite.Group()
        # napierający wrogowie
        self.tangos = pygame.sprite.Group()
        self.tangos.add(Tango(self))


    def run(self):
        while True:
            if self.state == 'menu':
                self.show_menu()
            elif self.state == 'about':
                self.show_about()
            elif self.state == 'score':
                # self.state = 'menu'
                self.show_score()
            elif self.state == 'rules':
                self.show_rules()
            elif self.state == 'game':
                # wyczyszczenie planszy do aktualizacji
                self.board.fill((0, 0, 0))
                # obsługa zdarzeń z klawiatury
                self.handle_events()
                # przesuwanie aktorów dramatu po planszy
                self.handle_alfa()
                self.handle_bullets()
                self.handle_tangos()
                # tabelka z punktami
                self.handle_chart()
                # aktualizacja planszy
                pygame.display.flip()
                # synchronizacja odświeżania planszy
                self.clock.tick(10)
                # new tango
                self.new_tango += self.new_tango_interval
                if self.new_tango > 50 and len(self.tangos) < self.max_tangos:
                    self.tangos.add(Tango(self))
                    self.new_tango = 0

    def show_menu(self):
        while self.state == 'menu':
            self.board.fill((30, 30, 30))
            title = self.font.render('A Game - MENU', True, (255, 255, 255))
            play_btn = self.font.render('1. Start Game', True, (255, 255, 0))
            about_btn = self.font.render('2. Author', True, (255, 255, 0))
            score_btn = self.font.render('3. Score', True, (255, 255, 0))
            rules_btn = self.font.render('4. Rules', True, (255, 255, 0))
            quit_btn = self.font.render('Q. Exit', True, (255, 255, 0))

            self.board.blit(title, (500, 200))
            self.board.blit(play_btn, (500, 300))
            self.board.blit(about_btn, (500, 350))
            self.board.blit(score_btn, (500, 400))
            self.board.blit(rules_btn, (500, 450))
            self.board.blit(quit_btn, (500, 500))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.state = 'game'
                    elif event.key == pygame.K_2:
                        self.state = 'about'
                    elif event.key == pygame.K_3:
                        self.state = 'score'
                    elif event.key == pygame.K_4:
                        self.state = 'rules'
                    elif event.key == pygame.K_q:
                        sys.exit()
            self.clock.tick(60)

    def show_about(self):
        while self.state == 'about':
            self.board.fill((0, 0, 40))
            title = self.font.render('A Game - ABOUT', True, (255, 255, 255))
            self.board.blit(title, (450, 150))
            lines = ["This is a game created by Zuza",
            "in Python using the PyGame library.",
            "Enjoy!",
            "Press ESC to return to the menu."]
            for i, line in enumerate(lines):
                rendered = self.font.render(line, True, (255, 255, 255))
                self.board.blit(rendered, (300, 250 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'

            self.clock.tick(60)

    def show_rules(self):
        while self.state == 'rules':
            self.board.fill((0, 0, 40))
            title = self.font.render('A Game - RULES', True, (255, 255, 255))
            self.board.blit(title, (450, 150))
            rules = ["1. Press spacebar to shoot.",
                     "2. Try to hit enemies falling from above to gain",
                     "points by pressing the spacebar.",
                     "3. Don't let the enemies touch the ground or you.",
                     "Press ESC to return to the menu."]

            for i, line in enumerate(rules):
                rendered = self.font.render(line, True, (255, 255, 255))
                self.board.blit(rendered, (300, 250 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'

            self.clock.tick(60)

    def show_score(self):
        while self.state == 'score':
            self.board.fill((0, 0, 40))
            title = self.font.render('A Game - SCORE', True, (255, 255, 255))
            self.board.blit(title, (450, 150))

            try:
                with open('your_best_score.txt', 'r') as file:
                    high_score = file.read().strip()
            except FileNotFoundError:
                score = "0"

            current_score_record = self.font.render(f"Your current score is: {self.score}", True, (255, 255, 255))
            best_score_record = self.font.render(f"All-time high score: {high_score}", True, (255, 255, 0))

            self.board.blit(current_score_record, (450, 300))
            self.board.blit(best_score_record, (450, 350))

            # text = f"Your best score is {score}."
            # rendered = self.font.render(text, True, (255, 255, 255))
            # self.board.blit(rendered, (450, 400))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'

            self.clock.tick(60)

    def handle_alfa(self):
        self.alfa.move()
        self.alfa.draw()

    def handle_tangos(self):
        for t in self.tangos.sprites(): t.draw()
        # sprawdzenie kolizji ze strzelcem
        if pygame.sprite.spritecollideany(self.alfa, self.tangos):
            self.handle_los()
        # czy wróg osiągnął linię strzelca
        for t in self.tangos:
            if t.rect.bottom == 800: # było <=
                self.handle_los()

    def handle_bullets(self):
        # usunięcie pocisków poza planszą
        for b in self.bullets.copy():
            if b.rect.bottom <= 0:
                self.bullets.remove(b)
        # przemieszczanie i rysowanie pocisków
        for b in self.bullets.sprites():
            b.draw()
        # sprawdzenie trafień
        hits = pygame.sprite.groupcollide(self.bullets, self.tangos, True, True)
        if hits:
            self.score += 1
            if len(self.tangos) == 0:
                self.pause('WIN')

    def handle_chart(self):
        score_text = self.font.render(f'Score: {self.score:}    Lives: {self.lives:}', True, (255, 255, 255))
        self.board.blit(score_text, (950, 10))

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.save_high_score()
                sys.exit()
            # naciśnięty klawisz
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    self.save_high_score()
                    sys.exit()

                elif e.key == pygame.K_ESCAPE:
                    self.pause('ESC')
                elif e.key == pygame.K_SPACE:
                    self.fire()
                elif e.key == pygame.K_RIGHT:
                    self.alfa.moving = 30
                elif e.key == pygame.K_LEFT:
                    self.alfa.moving = -30
            # zwolniiony klawisz
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT or e.key == pygame.K_LEFT:
                    self.alfa.moving = 0

    def save_high_score(self):
        try:
            with open('your_best_score.txt', 'r') as file:
                best_score = int(file.read().strip())
        except (FileNotFoundError, ValueError):
            best_score = 0

        if self.score > best_score:
            with open('your_best_score.txt', 'w') as file:
                file.write(str(self.score))

    def fire(self):
        self.bullets.add(Bullet(self))
        try:
            pygame.mixer.Sound('362482__jalastram__shooting_sounds_020.wav').play()
        except:
            pass

    def handle_los(self):
        self.lives -= 1
        hit_text = self.font.render("-1", True, (255, 0, 0))
        self.board.blit(hit_text, (self.alfa.rect.centerx, self.alfa.rect.top - 30))
        pygame.display.flip()
        pygame.time.delay(500)

        if self.lives <= 0:
            self.pause('LOS')
        else:
            self.bullets.empty()
            self.tangos.empty()
            self.tangos.add(Tango(self))

        # self.lives -= 1
        # if self.lives == 0:
        #     self.pause('LOS')
        # else:
        #     self.pause('HIT')

    def pause(self, case):
        text = ''
        if case in ('WIN', 'LOS'):
            self.save_high_score()
        if case == 'ESC':
            text = self.font.render('Game Paused', True, 'green')
            self.board.blit(text, dest=(0, 0))
            text = self.font.render('  C - Continue', True, 'green')
            self.board.blit(text, dest=(0, 30))
        else:
            if case == 'WIN':
                text = self.font.render('Game Over. You won!', True, 'green')
                self.board.blit(text, dest=(0, 0))
                text = self.font.render('  N  - New Game', True, 'green')
                self.board.blit(text, dest=(0, 30))
            elif case == 'LOS':
                text = self.font.render('Game Over. You lost!', True, 'red')
                self.board.blit(text, (self.board.get_width()//2 - 135, self.board.get_height()//2 - 50))
                text = self.font.render('  N  - New Game', True, 'green')
                self.board.blit(text, (self.board.get_width()//2 - 100, self.board.get_height()//2 + 10))
            elif case == 'HIT':
                text = self.font.render('You lost 1 life...', True, 'red')
                self.board.blit(text, dest=(0, 0))
                text = self.font.render('  R  - Resume', True, 'green')
                self.board.blit(text, dest=(0, 30))
            # self.board.blit(text, dest=(0, 0))
            # text = self.font.render('  N  - New Game', True, 'green')
            # self.board.blit(text, dest=(0, 30))
        text = self.font.render('  Q  - Quit', True, 'green')
        self.board.blit(text, (self.board.get_width()//2 - 100, self.board.get_height()//2 + 40))

        pygame.display.flip()
        # oczekiwanie na decyzję gracza
        wait = True
        while wait:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_n and case != 'ESC':
                        # nowa gra
                        self.bullets.empty()
                        self.tangos.empty()
                        self.tangos.add(Tango(self))
                        self.alfa.rect.midbottom = self.board.get_rect().midbottom
                        self.lives = self.max_lives
                        wait = False
                    elif e.key ==  pygame.K_r:
                        # wznowienie gry
                        self.bullets.empty()
                        self.tangos.empty()
                        self.tangos.add(Tango(self))
                        wait = False
                    elif e.key == pygame.K_c and case == 'ESC':
                        # kontynowanie gry
                        wait = False
                    elif e.key == pygame.K_q:
                        sys.exit()

# obiekt na planszy
class Sprite(pygame.sprite.Sprite):
    def __init__(self, game: Agame, color = (0, 0, 0)):
        super().__init__()
        self.game = game
        self.color  = color
        self.rect = None

    def move(self):
        pass

    def draw(self):
        # obliczenie nowej pozycji
        self.move()
        # rysowanie aktora na planszy
        pygame.draw.rect(self.game.board, self.color, self.rect, 5)

# wojownik
class Soldier(Sprite):
    def __init__(self, game: Agame, color):
        super().__init__(game, color)
        self.rect = pygame.Rect(0, 0, 20, 40)

# strzelec
class Alfa(Soldier):
    def __init__(self, game: Agame):
        super().__init__(game, (0,0,255))
        # początkowo stoi w miejscu
        self.moving = 0

        try:
            import os
            image_path = os.path.join(os.path.dirname(__file__), 'DurrrSpaceShip.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 60))  # Dostosuj rozmiar
            self.rect = self.image.get_rect()
        except Exception as e:
            print(f"Nie można załadować obrazka: {e}")
            self.image = None
            self.rect = pygame.Rect(0, 0, 40, 60)

        self.rect.midbottom = self.game.board.get_rect().midbottom

    def draw(self):
        if self.image:
            # Rysowanie obrazka
            self.game.board.blit(self.image, self.rect)
        else:
            # Rysowanie prostokąta (fallback)
            pygame.draw.rect(self.game.board, self.color, self.rect, 5)

    def move(self):
        self.rect.move_ip(self.moving, 0)
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.game.board.get_width(), self.rect.right)

    # def move(self):
    #     super().move()
    #     # zmiana pozycji wg moving w osi X
    #     self.rect.move_ip(self.moving, 0)

# wróg
class Tango(Soldier):
    def __init__(self, game: Agame):
        super().__init__(game, (255, 0, 0))
        # początkowe ustawienie pośrodku góry planszy
        self.rect.midtop = self.game.board.get_rect().midtop
        #
        # try:
        #     import os
        #     image_path = os.path.join(os.path.dirname(__file__), 'Layered Rock_0.png')
        #     self.image = pygame.image.load(image_path).convert_alpha()
        #     self.image = pygame.transform.scale(self.image, (40, 60))  # Dostosuj rozmiar
        #     self.rect = self.image.get_rect()
        #
        #     self.rect.y = 0
        #     self.rect.x = 50 * randint(2, 23)
        #
        # except:
        #     self.image = None
        #     self.rect = pygame.Rect(0, 0, 20, 40)
        #
        #     self.rect.y = 0
        #     self.rect.x = 50 * randint(2, 23)

    # def draw(self):
    #     if self.image:
    #         # rysowanie obrazka
    #         self.game.board.blit(self.image, self.rect)
    #     else:
    #         # gdyby nie było obrazka
    #         pygame.draw.rect(self.game.board, self.color, self.rect, 5)

    def move(self):
        # self.rect.move_ip(self.moving, 0)
        # losowa zmiana pozycji
        x = 10 * randint(-1, 1)
        self.rect.move_ip(x, 10)
        # y = 10
        # self.rect.move_ip(x, y)

# pocisk
class Bullet(Sprite):
    def __init__(self, game: Agame):
        super().__init__(game, (255, 255, 255))
        self.rect = pygame.Rect(0, 0, 5, 15)
        # początkowe ustawienie ze środka strzelca
        self.rect.midtop = game.alfa.rect.midtop

    def move(self):
        self.rect.move_ip(0, -20)

# główny blok aplikacji
if __name__ == '__main__':
    g = Agame()
    g.run()