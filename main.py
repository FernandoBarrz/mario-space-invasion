# Mario Space Invasion
# Por: Fernando Barrios


import sys
from pygame import *
from random import choice
from datos import RUTA_IMAGENES, RUTA_MUSICA, NOMBRE_IMAGENES, MOVER_ABAJO_ENEMIGO,POSICION_ENEMIGO_DEFECTO, BLANCO, VERDE, NEGRO, AZUL, MORADO, ROJO, FUENTE


# Variables globales
SCREEN = display.set_mode((800, 600))
# Se vuelve un diccionario con el nombre del archivo y su ruta como valor.
IMAGES = {name: image.load(RUTA_IMAGENES + '{}.png'.format(name)).convert_alpha() for name in NOMBRE_IMAGENES}

class MarioSpaceInvasion(object):
    def __init__(self):
        mixer.pre_init(44100, -16, 1, 4096)
        init()
        self.reloj = time.Clock()
        self.caption = display.set_caption('Mario Space Invasion')
        # Aqui
        self.pantalla = SCREEN
        self.fondo = image.load(RUTA_IMAGENES + 'mario-bg.png').convert()
        self.iniciarJuego = False
        self.pantallaPrincipal = True
        self.finDelJuego = False
        
        self.posicionEnemigo = POSICION_ENEMIGO_DEFECTO
        self.tituloTexto = Text(FUENTE, 50, 'Mario Space Invasion', NEGRO, 130, 55)
        self.tituloTexto2 = Text(FUENTE, 25, 'Presiona cualquier tecla para continuar', MORADO,
                               140, 150)
        self.finDelJuegoTexto = Text(FUENTE, 50, 'Fin del juego', NEGRO, 250, 270)
        self.siguienteRondaTexto = Text(FUENTE, 50, 'Siguiente ronda...', NEGRO, 240, 270)

        self.enemigoUnoTexto = Text(FUENTE, 25, '10 puntos', AZUL, 80, 320)
        self.enemigoDosTexto = Text(FUENTE, 25, '20 puntos', AZUL, 260, 320)
        self.enemigoTresTexto = Text(FUENTE, 25, '30 puntos', AZUL, 480, 320)
        self.enemigoCuatroTexto = Text(FUENTE, 25, '???', ROJO, 660, 320)

        self.puntuacionTexto = Text(FUENTE, 20, 'Puntos ', NEGRO, 8, 495)
        self.vidasTexto = Text(FUENTE, 20, 'Vidas ', NEGRO, 8, 535)

        self.vidaUno = Life(64, 535)
        self.vidaDos = Life(94, 535)
        self.vidaTres = Life(114, 535)
        self.grupo_de_vidas = sprite.Group(self.vidaUno, self.vidaDos, self.vidaTres)


    def main(self):
        while True:
            if self.pantallaPrincipal:
                self.pantalla.blit(self.fondo, (0, 0))
                self.tituloTexto.draw(self.pantalla)
                self.tituloTexto2.draw(self.pantalla)
                self.enemigoUnoTexto.draw(self.pantalla)
                self.enemigoDosTexto.draw(self.pantalla)
                self.enemigoTresTexto.draw(self.pantalla)
                self.enemigoCuatroTexto.draw(self.pantalla)
                self.crear_menu_principal()
                for e in event.get():
                    if self.should_exit(e):       
                        sys.exit()
                    if e.type == KEYUP:
                        self.grupo_de_vidas.add(self.vidaUno, self.vidaDos, self.vidaTres)
                        self.reset(0)
                        self.iniciarJuego = True
                        self.pantallaPrincipal = False

            elif self.iniciarJuego:
                if not self.enemigos and not self.grupo_explosiones:
                    tiempo_actual = time.get_ticks()
                    if tiempo_actual - self.tiempo_de_juego < 3000:
                        self.pantalla.blit(self.fondo, (0, 0))
                        self.puntuacionTexto2 = Text(FUENTE, 20, str(self.puntuacion),
                                               BLANCO, 85, 492)
                        self.puntuacionTexto.draw(self.pantalla)
                        self.puntuacionTexto2.draw(self.pantalla)
                        self.siguienteRondaTexto.draw(self.pantalla)
                        self.vidasTexto.draw(self.pantalla)
                        self.grupo_de_vidas.update()
                        self.check_input()
                    if tiempo_actual - self.tiempo_de_juego > 3000:
                        # hace que los enemigos bajen
                        self.posicionEnemigo += MOVER_ABAJO_ENEMIGO
                        self.reset(self.puntuacion)
                        self.tiempo_de_juego += 3000
                else:
                    tiempo_actual = time.get_ticks()
                    self.tocar_musica_principal(tiempo_actual)
                    self.pantalla.blit(self.fondo, (0, 0))
                    
                    self.puntuacionTexto2 = Text(FUENTE, 20, str(self.puntuacion), BLANCO,
                                           85, 492)
                    self.puntuacionTexto.draw(self.pantalla)
                    self.puntuacionTexto2.draw(self.pantalla)
                    self.vidasTexto.draw(self.pantalla)
                    self.check_input()
                    self.enemigos.update(tiempo_actual)
                    self.allSprites.update(self.keys, tiempo_actual)
                    self.grupo_explosiones.update(tiempo_actual)
                    self.calcular_colisiones()
                    self.crear_nuevo_mario(self.makeNewShip, tiempo_actual)
                    self.make_enemies_shoot()

            elif self.finDelJuego:
                tiempo_actual = time.get_ticks()
                
                self.posicionEnemigo = POSICION_ENEMIGO_DEFECTO
                self.crear_fin_juego(tiempo_actual)

            display.update()
            self.reloj.tick(60)

    def reset(self, puntuacion):
        self.jugador = Mario()
        self.playerGroup = sprite.Group(self.jugador)
        self.grupo_explosiones = sprite.Group()
        self.bullets = sprite.Group()
        self.mysteryShip = Mystery()
        self.mysteryGroup = sprite.Group(self.mysteryShip)
        self.enemyBullets = sprite.Group()
        self.make_enemies()
        self.allSprites = sprite.Group(self.jugador, self.enemigos,
                                       self.grupo_de_vidas, self.mysteryShip)
        self.keys = key.get_pressed()

        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.shipTimer = time.get_ticks()
        self.puntuacion = puntuacion
        self.crear_audio()
        self.makeNewShip = False
        self.shipAlive = True



    def crear_audio(self):
        self.sounds = {}
        for sound_name in ['shoot', 'shoot2', 'invaderkilled', 'mysterykilled',
                           'shipexplosion']:
            self.sounds[sound_name] = mixer.Sound(
                RUTA_MUSICA + '{}.mp3'.format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.musicNotes = [mixer.Sound(RUTA_MUSICA + '{}.mp3'.format(i)) for i
                           in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.5)

        self.noteIndex = 0

    def tocar_musica_principal(self, tiempo_actual):
        if tiempo_actual - self.noteTimer > self.enemigos.moveTime:
            self.note = self.musicNotes[self.noteIndex]
            if self.noteIndex < 3:
                self.noteIndex += 1
            else:
                self.noteIndex = 0

            self.note.play()
            self.noteTimer += self.enemigos.moveTime

    @staticmethod
    def should_exit(evt):
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)

    def check_input(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.bullets) == 0 and self.shipAlive:
                        if self.puntuacion < 1000:
                            bullet = Bullet(self.jugador.rect.x + 23,
                                            self.jugador.rect.y + 5, -1,
                                            15, 'laser', 'center')
                            self.bullets.add(bullet)
                            self.allSprites.add(self.bullets)
                            self.sounds['shoot'].play()
                        else:
                            leftbullet = Bullet(self.jugador.rect.x + 8,
                                                self.jugador.rect.y + 5, -1,
                                                15, 'laser', 'left')
                            rightbullet = Bullet(self.jugador.rect.x + 38,
                                                 self.jugador.rect.y + 5, -1,
                                                 15, 'laser', 'right')
                            self.bullets.add(leftbullet)
                            self.bullets.add(rightbullet)
                            self.allSprites.add(self.bullets)
                            self.sounds['shoot2'].play()

    def make_enemies(self):
        enemigos = EnemiesGroup(10, 5)
        for row in range(5):
            for column in range(10):
                enemy = Enemy(row, column)
                enemy.rect.x = 157 + (column * 50)
                enemy.rect.y = self.posicionEnemigo + (row * 45)
                enemigos.add(enemy)

        self.enemigos = enemigos

    def make_enemies_shoot(self):
        if (time.get_ticks() - self.timer) > 700 and self.enemigos:
            enemy = self.enemigos.random_bottom()
            self.enemyBullets.add(
                Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5,
                       'enemylaser', 'center'))
            self.allSprites.add(self.enemyBullets)
            self.timer = time.get_ticks()

    def calcular_puntaje(self, row):
        scores = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                  }

        puntuacion = scores[row]
        self.puntuacion += puntuacion
        return puntuacion

    def crear_menu_principal(self):
        self.enemy1 = IMAGES['enemigo_3_1']
        self.enemy1 = transform.scale(self.enemy1, (40, 40))
        self.enemy2 = IMAGES['enemigo_2_2']
        self.enemy2 = transform.scale(self.enemy2, (40, 40))
        self.enemy3 = IMAGES['enemigo_1_2']
        self.enemy3 = transform.scale(self.enemy3, (40, 40))
        self.enemy4 = IMAGES['bowser']
        self.enemy4 = transform.scale(self.enemy4, (80, 40))
        self.pantalla.blit(self.enemy1, (130, 280))
        self.pantalla.blit(self.enemy2, (310, 280))
        self.pantalla.blit(self.enemy3, (520, 280))
        self.pantalla.blit(self.enemy4, (640, 280))



    def calcular_colisiones(self):
        sprite.groupcollide(self.bullets, self.enemyBullets, True, True)

        for enemy in sprite.groupcollide(self.enemigos, self.bullets,
                                         True, True).keys():
            self.sounds['invaderkilled'].play()
            self.calcular_puntaje(enemy.row)
            EnemyExplosion(enemy, self.grupo_explosiones)
            self.tiempo_de_juego = time.get_ticks()

        for mystery in sprite.groupcollide(self.mysteryGroup, self.bullets,
                                           True, True).keys():
            mystery.mysteryEntered.stop()
            self.sounds['mysterykilled'].play()
            puntuacion = self.calcular_puntaje(mystery.row)
            MysteryExplosion(mystery, puntuacion, self.grupo_explosiones)
            newShip = Mystery()
            self.allSprites.add(newShip)
            self.mysteryGroup.add(newShip)

        for jugador in sprite.groupcollide(self.playerGroup, self.enemyBullets,
                                          True, True).keys():
            if self.vidaTres.alive():
                self.vidaTres.kill()
            elif self.vidaDos.alive():
                self.vidaDos.kill()
            elif self.vidaUno.alive():
                self.vidaUno.kill()
            else:
                self.finDelJuego = True
                self.iniciarJuego = False
            self.sounds['shipexplosion'].play()
            MarioExplosion(jugador, self.grupo_explosiones)
            self.makeNewShip = True
            self.shipTimer = time.get_ticks()
            self.shipAlive = False

        if self.enemigos.bottom >= 540:
            sprite.groupcollide(self.enemigos, self.playerGroup, True, True)
            if not self.jugador.alive() or self.enemigos.bottom >= 600:
                self.finDelJuego = True
                self.iniciarJuego = False


    def crear_nuevo_mario(self, createShip, tiempo_actual):
        if createShip and (tiempo_actual - self.shipTimer > 900):
            self.jugador = Mario()
            self.allSprites.add(self.jugador)
            self.playerGroup.add(self.jugador)
            self.makeNewShip = False
            self.shipAlive = True

    def crear_fin_juego(self, tiempo_actual):
        self.pantalla.blit(self.fondo, (0, 0))
        passed = tiempo_actual - self.timer
        if passed < 750:
            self.finDelJuegoTexto.draw(self.pantalla)
        elif 750 < passed < 1500:
            self.pantalla.blit(self.fondo, (0, 0))
        elif 1500 < passed < 2250:
            self.finDelJuegoTexto.draw(self.pantalla)
        elif 2250 < passed < 2750:
            self.pantalla.blit(self.fondo, (0, 0))
        elif passed > 3000:
            self.pantallaPrincipal = True

        for e in event.get():
            if self.should_exit(e):
                sys.exit()



class Mario(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['mario']
        self.rect = self.image.get_rect(topleft=(375, 540))
        self.speed = 5

    def update(self, keys, *args):
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 740:
            self.rect.x += self.speed
        game.pantalla.blit(self.image, self.rect)


class Bullet(sprite.Sprite):
    def __init__(self, xpos, ypos, direction, speed, filename, side):
        sprite.Sprite.__init__(self)
        self.image = IMAGES[filename]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.speed = speed
        self.direction = direction
        self.side = side
        self.filename = filename

    def update(self, keys, *args):
        game.pantalla.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()


class Enemy(sprite.Sprite):
    def __init__(self, row, column):
        sprite.Sprite.__init__(self)
        self.row = row
        self.column = column
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def update(self, *args):
        game.pantalla.blit(self.image, self.rect)

    def load_images(self):
        images = {0: ['1_2', '1_1'],
                  1: ['2_2', '2_1'],
                  2: ['2_2', '2_1'],
                  3: ['3_1', '3_2'],
                  4: ['3_1', '3_2'],
                  }
        img1, img2 = (IMAGES['enemigo_{}'.format(img_num)] for img_num in
                      images[self.row])
        self.images.append(transform.scale(img1, (40, 35)))
        self.images.append(transform.scale(img2, (40, 35)))


class EnemiesGroup(sprite.Group):
    def __init__(self, columns, rows):
        sprite.Group.__init__(self)
        self.enemigos = [[None] * columns for _ in range(rows)]
        self.columns = columns
        self.rows = rows
        self.leftAddMove = 0
        self.rightAddMove = 0
        self.moveTime = 600
        self.direction = 1
        self.rightMoves = 30
        self.leftMoves = 30
        self.moveNumber = 15
        self.timer = time.get_ticks()
        self.bottom = game.posicionEnemigo + ((rows - 1) * 45) + 35
        self._aliveColumns = list(range(columns))
        self._leftAliveColumn = 0
        self._rightAliveColumn = columns - 1

    def update(self, current_time):
        if current_time - self.timer > self.moveTime:
            if self.direction == 1:
                max_move = self.rightMoves + self.rightAddMove
            else:
                max_move = self.leftMoves + self.leftAddMove

            if self.moveNumber >= max_move:
                self.leftMoves = 30 + self.rightAddMove
                self.rightMoves = 30 + self.leftAddMove
                self.direction *= -1
                self.moveNumber = 0
                self.bottom = 0
                for enemy in self:
                    enemy.rect.y += MOVER_ABAJO_ENEMIGO
                    enemy.toggle_image()
                    if self.bottom < enemy.rect.y + 35:
                        self.bottom = enemy.rect.y + 35
            else:
                velocity = 10 if self.direction == 1 else -10
                for enemy in self:
                    enemy.rect.x += velocity
                    enemy.toggle_image()
                self.moveNumber += 1

            self.timer += self.moveTime

    def add_internal(self, *sprites):
        super(EnemiesGroup, self).add_internal(*sprites)
        for s in sprites:
            self.enemigos[s.row][s.column] = s

    def remove_internal(self, *sprites):
        super(EnemiesGroup, self).remove_internal(*sprites)
        for s in sprites:
            self.kill(s)
        self.update_speed()

    def is_column_dead(self, column):
        return not any(self.enemigos[row][column]
                       for row in range(self.rows))

    def random_bottom(self):
        col = choice(self._aliveColumns)
        col_enemies = (self.enemigos[row - 1][col]
                       for row in range(self.rows, 0, -1))
        return next((en for en in col_enemies if en is not None), None)

    def update_speed(self):
        if len(self) == 1:
            self.moveTime = 200
        elif len(self) <= 10:
            self.moveTime = 400

    def kill(self, enemy):
        self.enemigos[enemy.row][enemy.column] = None
        is_column_dead = self.is_column_dead(enemy.column)
        if is_column_dead:
            self._aliveColumns.remove(enemy.column)

        if enemy.column == self._rightAliveColumn:
            while self._rightAliveColumn > 0 and is_column_dead:
                self._rightAliveColumn -= 1
                self.rightAddMove += 5
                is_column_dead = self.is_column_dead(self._rightAliveColumn)

        elif enemy.column == self._leftAliveColumn:
            while self._leftAliveColumn < self.columns and is_column_dead:
                self._leftAliveColumn += 1
                self.leftAddMove += 5
                is_column_dead = self.is_column_dead(self._leftAliveColumn)


class Blocker(sprite.Sprite):
    def __init__(self, size, color, row, column):
        sprite.Sprite.__init__(self)
        self.height = size
        self.width = size
        self.color = color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column

    def update(self, keys, *args):
        game.pantalla.blit(self.image, self.rect)


class Mystery(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['bowser']
        self.image = transform.scale(self.image, (75, 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.row = 5
        self.moveTime = 25000
        self.direction = 1
        self.timer = time.get_ticks()
        self.mysteryEntered = mixer.Sound(RUTA_MUSICA + 'bowser.mp3')
        self.mysteryEntered.set_volume(0.3)
        self.playSound = True

    def update(self, keys, tiempo_actual, *args):
        resetTimer = False
        passed = tiempo_actual - self.timer
        if passed > self.moveTime:
            if (self.rect.x < 0 or self.rect.x > 800) and self.playSound:
                self.mysteryEntered.play()
                self.playSound = False
            if self.rect.x < 840 and self.direction == 1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x += 2
                game.pantalla.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x -= 2
                game.pantalla.blit(self.image, self.rect)

        if self.rect.x > 830:
            self.playSound = True
            self.direction = -1
            resetTimer = True
        if self.rect.x < -90:
            self.playSound = True
            self.direction = 1
            resetTimer = True
        if passed > self.moveTime and resetTimer:
            self.timer = tiempo_actual


class EnemyExplosion(sprite.Sprite):
    def __init__(self, enemy, *groups):
        super(EnemyExplosion, self).__init__(*groups)
        self.image = transform.scale(self.get_image(enemy.row), (40, 35))
        self.image2 = transform.scale(self.get_image(enemy.row), (50, 45))
        self.rect = self.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        self.timer = time.get_ticks()

    @staticmethod
    def get_image(row):
        img_colors = ['moneda', 'moneda', 'moneda', 'moneda', 'moneda']
        return IMAGES['img_{}'.format(img_colors[row])]

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 100:
            game.pantalla.blit(self.image, self.rect)
        elif passed <= 200:
            game.pantalla.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
        elif 400 < passed:
            self.kill()


class MysteryExplosion(sprite.Sprite):
    def __init__(self, mystery, puntuacion, *groups):
        super(MysteryExplosion, self).__init__(*groups)
        self.text = Text(FUENTE, 20, str(puntuacion), BLANCO,
                         mystery.rect.x + 20, mystery.rect.y + 6)
        self.timer = time.get_ticks()

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 200 or 400 < passed <= 600:
            self.text.draw(game.pantalla)
        elif 600 < passed:
            self.kill()


class MarioExplosion(sprite.Sprite):
    def __init__(self, mario, *groups):
        super(MarioExplosion, self).__init__(*groups)
        self.image = IMAGES['mario']
        self.rect = self.image.get_rect(topleft=(mario.rect.x, mario.rect.y))
        self.timer = time.get_ticks()

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if 300 < passed <= 600:
            game.pantalla.blit(self.image, self.rect)
        elif 900 < passed:
            self.kill()


class Life(sprite.Sprite):
    def __init__(self, xpos, ypos):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['mario']
        self.image = transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(topleft=(xpos, ypos))

    def update(self, *args):
        game.pantalla.blit(self.image, self.rect)


class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)



if __name__ == '__main__':
    game = MarioSpaceInvasion()
    game.main()
