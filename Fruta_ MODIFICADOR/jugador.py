import pygame

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5
        try:
            # Carga y escala la imagen del jugador
            imagen_original = pygame.image.load("assets/jugador/jugador.png")
            self.imagen = pygame.transform.scale(imagen_original, (60, 60))
        except:
            # En caso de error, crea un cuadrado azul
            self.imagen = pygame.Surface((60, 60))
            self.imagen.fill((0, 0, 255))

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad

        # Limitar los bordes de la pantalla
        if self.x < 0: self.x = 0
        if self.x > 740: self.x = 740
        if self.y < 0: self.y = 0
        if self.y > 540: self.y = 540

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
