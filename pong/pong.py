import pygame
import random
from pygame.locals import QUIT
VENTANA_HORIZONTAL=800
VENTANA_VERTICAL=600
FPS=60
BLANCO=(255,255,255)
class RaquetaPong:
    def __init__(self):
        self.imagen = pygame.image.load("./assets/raqueta.png").convert_alpha()
        self.ancho,self.alto=self.imagen.get_size()
        self.x=0
        self.y=VENTANA_VERTICAL/2-self.alto/2
        self.dir_y=0
    def mover(self):
        self.y+=self.dir_y
        if self.y<=0:
            self.y=0
        if self.y>=VENTANA_VERTICAL-self.alto:
            self.y=VENTANA_VERTICAL-self.alto
    def golpear(self,pelota):
        if(
                pelota.x>self.x and
                pelota.x<self.x+self.ancho and
                pelota.y>self.y and
                pelota.y < self.y+self.alto):
            pelota.dir_x=-pelota.dir_x
            pelota.x=self.x+self.ancho


class PelotaPong:
    def __init__(self,asset_pelota):
        self.imagen=pygame.image.load(asset_pelota).convert_alpha()
        self.ancho,self.alto=self.imagen.get_size()
        self.x=VENTANA_HORIZONTAL/2-self.ancho/2
        self.y=VENTANA_VERTICAL/2-self.alto/2

        self.dir_x=random.choice([-5,5 ])
        self.dir_y=random.choice([-5,5 ])
    def mover(self):
        self.x+=self.dir_x
        self.y+=self.dir_y
    def rebotar(self):
        if self.x<=0:
            #self.dir_x=-self.dir_x
            self.reiniciar()
        if self.y<=0:
            self.dir_y=-self.dir_y
        if self.x+self.ancho>=VENTANA_HORIZONTAL:
            self.dir_x=-self.dir_x
        if self.y + self.alto >= VENTANA_VERTICAL:
            self.dir_y = -self.dir_y
    def reiniciar(self):
        self.ancho, self.alto = self.imagen.get_size()
        self.x = VENTANA_HORIZONTAL / 2 - self.ancho / 2
        self.y = VENTANA_VERTICAL / 2 - self.alto / 2

def main():
    # Inicialización de Pygame
    pygame.init()

    # Inicialización de la superficie de dibujo (display surface)
    ventana = pygame.display.set_mode((VENTANA_HORIZONTAL, VENTANA_VERTICAL))
    pygame.display.set_caption("Pong 1")

    pelota=PelotaPong("./assets/bola_azul.png")

    raquetaJugador=RaquetaPong()
    raquetaJugador.x=60

    raquetaIA=RaquetaPong()
    raquetaIA.x=VENTANA_HORIZONTAL-60-raquetaIA.ancho
    # Bucle principal
    jugando = True
    while jugando:
        pelota.mover()
        pelota.rebotar()
        raquetaJugador.mover()
        raquetaJugador.golpear(pelota=pelota)
        ventana.fill(BLANCO)
        ventana.blit(pelota.imagen,(pelota.x,pelota.y))
        ventana.blit(raquetaJugador.imagen,(raquetaJugador.x,raquetaJugador.y))
        ventana.blit(raquetaIA.imagen,(raquetaIA.x,raquetaIA.y))

        for event in pygame.event.get():
            if event.type == QUIT:
                jugando = False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w:
                    raquetaJugador.dir_y=-5
                if event.key==pygame.K_s:
                    raquetaJugador.dir_y=5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    raquetaJugador.dir_y = 0
                if event.key == pygame.K_s:
                    raquetaJugador.dir_y = 0

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()