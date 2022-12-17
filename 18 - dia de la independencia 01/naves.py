import proyectiles, random

class Jugador():

  x = 0
  y = 0
  disparando = False
  image = None
  efectoDeSonido = 'sonidos/tu_laser.wav'
  pygame = None
  superficieDeDibujo = None
  ancho = 0
  alto = 0
  balas = []
  imagenDeBala = "graficos/tu_proyectil.png"
  velocidadDeBala = -10
  salud = 5

  def cargarImagenes(self):
    self.image = self.pygame.image.load("graficos/tu_nave.png")

  def dibujar(self):
    self.superficieDeDibujo.blit(self.image, (self.x, self.y))

  def fijarPosicion(self, posicion):
    self.x = posicion[0] - self.ancho / 2

  def fuego(self):
    self.balas.append(proyectiles.Bala_Laser(self.x + self.ancho / 2, self.y, self.pygame, self.superficieDeDibujo, self.velocidadDeBala, self.imagenDeBala))
    a = self.pygame.mixer.Sound(self.efectoDeSonido)
    a.set_volume(0.2)
    a.play()

  def dibujarBalas(self):
    for b in self.balas:
      b.mover()
      b.dibujar()

  def anotarImpacto(self):
    self.salud -= 1

  def verificarImpacto(self, verificarComparandoCon):
    balasParaRemover = []

    for indice, b in enumerate(self.balas):
      if b.x > verificarComparandoCon.x and b.x < verificarComparandoCon.x + verificarComparandoCon.ancho:
        if b.y > verificarComparandoCon.y and b.y < verificarComparandoCon.y + verificarComparandoCon.alto:
          verificarComparandoCon.anotarImpacto()
          balasParaRemover.append(indice)

    for balasUsadas in balasParaRemover:
      del self.balas[balasUsadas]

    if verificarComparandoCon.salud <= 0:
      return True

  def __init__(self, x, y, pygame, superficieDeDibujo):
    self.x = x
    self.y = y
    self.pygame = pygame
    self.superficieDeDibujo = superficieDeDibujo
    self.cargarImagenes()

    dimensiones = self.image.get_rect().size
    self.ancho = dimensiones[0]
    self.alto = dimensiones[1]

    self.x -= self.ancho / 2
    self.y -= self.alto + 10

class Enemigo(Jugador):

  x = 0
  y = 0
  disparando = False
  image = None
  efectoDeSonido = 'sonidos/enemigo_laser.wav'
  imagenDeBala = "graficos/enemigo_proyectil.png"
  velocidadDeBala = 10
  velocidad = 2

  def mover(self):
    self.y += self.velocidad

  def intentarDisparar(self):
    deberiaDisparar = random.random()

    if deberiaDisparar <= 0.01:
      self.fuego()

  def cargarImagenes(self):
    self.image = self.pygame.image.load("graficos/enemigo_nave.png")

  def __init__(self, x, y, pygame, superficieDeDibujo, salud):
    self.x = x
    self.y = y
    self.pygame = pygame
    self.superficieDeDibujo = superficieDeDibujo
    self.cargarImagenes()
    self.balas = []
    self.salud = salud

    dimensiones = self.image.get_rect().size
    self.ancho = dimensiones[0]
    self.alto = dimensiones[1]

    self.x -= self.ancho / 2 