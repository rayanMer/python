import pygame
import random

pygame.init()

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

FPS = 60
ANCHO = 800
ALTO = 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Arkanoid")

# variables para la paleta
paleta_ancho = 100
paleta_alto = 10
paleta_x = ANCHO // 2 - paleta_ancho // 2
paleta_y = ALTO - 30
paleta_vel = 10

# variables para la pelota
pelota_radio = 10
pelota_x = ANCHO // 2
pelota_y = ALTO // 2
pelota_vel_x = 5
pelota_vel_y = -5

# variables para bloques
bloques = []
bloque_ancho = 60
bloque_alto = 20
num_filas = 1
num_columnas = 1
bloques_destruidos = 0

# crear bloques
for i in range(num_filas):
    fila_bloques = []
    # pygame.Rect(x, y, ancho, alto) Rect se usa para usar rectángulos
    for j in range(num_columnas):
        fila_bloques.append(pygame.Rect(j * (bloque_ancho + 10) + 10, i * (bloque_alto + 10) + 10, bloque_ancho, bloque_alto))
    bloques.append(fila_bloques)

# funcion para dibujar los bloques
def dibujar_bloques():
    for fila in bloques:
        for bloque in fila:
            pygame.draw.rect(screen, AZUL, bloque)

# funcion principal del juego
def juego():
    global paleta_x, pelota_x, pelota_y, pelota_vel_x, pelota_vel_y, bloques_destruidos

    # mensaje al ganar
    fuente = pygame.font.Font(None, 50)
    mensaje_ganador = fuente.render("¡HAS GANADO!", True, BLANCO)

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # movimiento de la paleta
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and paleta_x > 0:
            paleta_x -= paleta_vel
        if teclas[pygame.K_RIGHT] and paleta_x < ANCHO - paleta_ancho:
            paleta_x += paleta_vel

        # movimiento de la pelota
        pelota_x += pelota_vel_x
        pelota_y += pelota_vel_y

        # verificar si la pelota ha llegado al borde inferior
        if pelota_y >= ALTO:
            # restablecer la pelota a su posición inicial
            pelota_x = ANCHO // 2
            pelota_y = ALTO // 2
            pelota_vel_x = 5 * random.choice([1, -1])  # Velocidad aleatoria en X
            pelota_vel_y = -5  # Velocidad inicial en Y


        # colision con los bordes ventana
        if pelota_x <= 0 or pelota_x >= ANCHO - pelota_radio:
            pelota_vel_x = -pelota_vel_x
        if pelota_y <= 0:
            pelota_vel_y = -pelota_vel_y

        # colision con la paleta
        if (paleta_x < pelota_x < paleta_x + paleta_ancho) and (paleta_y < pelota_y + pelota_radio < paleta_y + paleta_alto):
            pelota_vel_y = -pelota_vel_y

        # chocar con los bloques
        for fila in bloques:
            for bloque in fila:
                if bloque.colliderect(pygame.Rect(pelota_x - pelota_radio, pelota_y - pelota_radio, pelota_radio * 2, pelota_radio * 2)):
                    fila.remove(bloque)
                    pelota_vel_y = -pelota_vel_y
                    bloques_destruidos += 1
                    break

        # verificar si el jugador ha ganado
        if bloques_destruidos == num_filas * num_columnas:
            screen.fill(NEGRO)  # rellenar el fondo con negro
            screen.blit(mensaje_ganador, (ANCHO // 2 - mensaje_ganador.get_width() // 2, ALTO // 2 - mensaje_ganador.get_height() // 2))
            pygame.display.flip()  # mostrar el mensaje de victoria
            pygame.time.delay(2000)  # mostrar el mensaje por 2 segundos
            corriendo = False

        # rellenar  fondo
        screen.fill(NEGRO)

        # dibujar los bloques, la paleta y la pelota
        dibujar_bloques()
        pygame.draw.rect(screen, ROJO, (paleta_x, paleta_y, paleta_ancho, paleta_alto))
        pygame.draw.circle(screen, BLANCO, (pelota_x, pelota_y), pelota_radio)

        # actualizar la pantalla
        pygame.display.flip()

        pygame.time.Clock().tick(FPS)

    pygame.quit()

def main():
    juego()

if __name__ == "__main__":
    main()
