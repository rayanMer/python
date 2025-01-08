import random
import pygame
from pygame.locals import QUIT

VENTANA_HORI = 800
VENTANA_VERT = 600
FPS = 60
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)


class PelotaPong:
    def __init__(self, fichero_imagen):
        self.imagen = pygame.image.load(fichero_imagen).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = VENTANA_HORI / 2 - self.ancho / 2
        self.y = VENTANA_VERT / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.puntuacion = 0
        self.puntuacion_ia = 0

    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self):
        if self.x <= -self.ancho:
            self.reiniciar()
            self.puntuacion_ia += 1
        if self.x >= VENTANA_HORI:
            self.reiniciar()
            self.puntuacion += 1
        if self.y <= 0:
            self.dir_y = -self.dir_y
        if self.y + self.alto >= VENTANA_VERT:
            self.dir_y = -self.dir_y

    def reiniciar(self):
        self.x = VENTANA_HORI / 2 - self.ancho / 2
        self.y = VENTANA_VERT / 2 - self.alto / 2
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-5, 5])


class RaquetaPong:
    def __init__(self):
        self.imagen = pygame.image.load("./assets/raqueta.png").convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = 0
        self.y = VENTANA_VERT / 2 - self.alto / 2
        self.dir_y = 0

    def mover(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= VENTANA_VERT:
            self.y = VENTANA_VERT - self.alto

    def mover_ia(self, pelota):
        if self.y > pelota.y:
            self.dir_y = -3
        elif self.y < pelota.y:
            self.dir_y = 3
        else:
            self.dir_y = 0

        self.y += self.dir_y

    def golpear(self, pelota):
        if (
            pelota.x < self.x + self.ancho
            and pelota.x > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho

    def golpear_ia(self, pelota):
        if (
            pelota.x + pelota.ancho > self.x
            and pelota.x < self.x + self.ancho
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - pelota.ancho


def main():
    pygame.init()
    ventana = pygame.display.set_mode((VENTANA_HORI, VENTANA_VERT))
    pygame.display.set_caption("Pong 9")
    fuente = pygame.font.Font(None, 60)
    pelota = PelotaPong("./assets/bola_roja.png")
    raqueta_1 = RaquetaPong()
    raqueta_1.x = 60
    raqueta_2 = RaquetaPong()
    raqueta_2.x = VENTANA_HORI - 60 - raqueta_2.ancho
    jugando = True
    while jugando:
        pelota.mover()
        pelota.rebotar()
        raqueta_1.mover()
        raqueta_2.mover_ia(pelota)
        raqueta_1.golpear(pelota)
        raqueta_2.golpear_ia(pelota)

        ventana.fill(BLANCO)
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(raqueta_1.imagen, (raqueta_1.x, raqueta_1.y))
        ventana.blit(raqueta_2.imagen, (raqueta_2.x, raqueta_2.y))

        texto = f"{pelota.puntuacion} : {pelota.puntuacion_ia}"
        letrero = fuente.render(texto, False, NEGRO)
        ventana.blit(letrero, (VENTANA_HORI / 2 - fuente.size(texto)[0] / 2, 50))

        for event in pygame.event.get():
            if event.type == QUIT:
                jugando = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = -5
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = 0
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 0

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()