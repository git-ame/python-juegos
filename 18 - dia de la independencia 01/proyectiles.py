class Bala_Laser():

  x = 0
  y = 0
  image = None
  pygame = None
  superficieDeDibujo = None
  ancho = 0
  alto = 0
  velocidad = 0.0

  def cargarImagenes(self):
    self.image = self.pygame.image.load(self.image)

  def dibujar(self):
    self.superficieDeDibujo.blit(self.image, (self.x, self.y))

  def mover(self):
    self.y += self.velocidad

  def __init__(self, x, y, pygame, superficieDeDibujo, velocidad, image):
    self.x = x
    self.y = y
    self.pygame = pygame
    self.superficieDeDibujo = superficieDeDibujo
    self.image = image
    self.cargarImagenes()
    self.velocidad = velocidad

    dimensiones = self.image.get_rect().size
    self.ancho = dimensiones[0]
    self.alto = dimensiones[1]

    self.x -= self.ancho / 2