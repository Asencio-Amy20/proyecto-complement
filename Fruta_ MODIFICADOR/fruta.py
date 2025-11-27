import pygame, random

class Fruta:
    def __init__(self):
        self.x = random.randint(50, 740)
        self.y = random.randint(50, 540)
        try:
            imagen_original = pygame.image.load("assets/frutas/fruta.png")
            self.imagen = pygame.transform.scale(imagen_original, (40, 40))
        except:
            self.imagen = pygame.Surface((40, 40))
            self.imagen.fill((255, 0, 0))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
