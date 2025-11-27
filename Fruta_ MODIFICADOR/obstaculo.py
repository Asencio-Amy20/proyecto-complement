import pygame, random, math

class Obstaculo:
    def __init__(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)
        self.velocidad = 2  # velocidad del obstáculo

        try:
            imagen_original = pygame.image.load("assets/obstaculos/obstaculo.png")
            self.imagen = pygame.transform.scale(imagen_original, (70, 70))
        except:
            # Si no hay imagen, crea un cuadrado gris
            self.imagen = pygame.Surface((70, 70))
            self.imagen.fill((100, 100, 100))

    def seguir_jugador(self, jugador_x, jugador_y):
        """Hace que el obstáculo se mueva hacia la posición del jugador."""
        dx = jugador_x - self.x
        dy = jugador_y - self.y
        distancia = math.hypot(dx, dy)

        if distancia != 0:  # evitar división por cero
            dx /= distancia
            dy /= distancia

        self.x += dx * self.velocidad
        self.y += dy * self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
