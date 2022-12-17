class Anasto():

  # Especificaiones (propiedades o variables) que describen a Anasto
  x = 0
  y = 625

  golpeRecibido = False
  momentoDelGolpe = 0
  salud = 100

  perfilIzquierdo = None
  perfilDerecho = None
  golpeadoEnLaIzquierda = None
  golpeadoEnLaDerecha = None

  direccion = 1
  velocidad = 8
  pygame = None

  # Las capacidades operacionales y regulaciones (metodos o funciones) de Anasto

  def reiniciar(self, x):
    # Codigo para tener listo a Anasto para otro gran dia
    self.x = x
    self.y = 625

    self.golpeRecibido = False
    self.momentoDelGolpe = 0
    self.salud = 100

    self.direccion = 1
    self.velocidad = 8
    self.pygame = None

  def moverALaIzquierda(self, limiteIzquierdo):
    # Mover a Anasto a la izquierda
    if self.direccion is not 0:
      self.direccion = 0

    if((self.x - self.velocidad) > limiteIzquierdo):
      self.x -= self.velocidad  

  def moverALaDerecha(self, limiteDerecho):
    # Mover a Anasto a la Derecha
    if self.direccion is not 1:
      self.direccion = 1

    if((self.x + self.velocidad) + 58 < limiteDerecho):
      self.x += self.velocidad      

  def cargarImagenes(self, pygame):
    # Obtener las imagenes que necesitamos para dibujar a Anasto
    self.perfilIzquierdo = pygame.image.load("recursos/Anasto-Izq.png")
    self.perfilDerecho = pygame.image.load("recursos/Anasto-Der.png")
    self.golpeadoEnLaIzquierda = pygame.image.load("recursos/Anasto-Izq-Golpe.png")
    self.golpeadoEnLaDerecha = pygame.image.load("recursos/Anasto-Der-Golpe.png")

  def dibujar(self, superficieDeDibujo, momento):
    # Dibujar a Anasto
    if momento - self.momentoDelGolpe > 800:
      self.momentoDelGolpe = 0
      self.golpeRecibido = False

    if self.direccion is 1:
      if self.golpeRecibido is False:
        superficieDeDibujo.blit(self.perfilDerecho, (self.x, self.y))
      else :
        superficieDeDibujo.blit(self.golpeadoEnLaDerecha, (self.x, self.y))
    else :
      if self.golpeRecibido is False:
        superficieDeDibujo.blit(self.perfilIzquierdo, (self.x, self.y))
      else :
        superficieDeDibujo.blit(self.golpeadoEnLaIzquierda, (self.x, self.y))

  def __init__(self, x):
    # Crear a Anasto
    self.x = x

class Barril():

  vacantes = [(4, 103), (82, 27), (157, 104), (234, 27), (310, 104), (388, 27), (463, 104), (539, 27), (615, 104), (691, 27), (768, 104), (845, 27), (920, 104)]
  vacante = 0
  x = 0
  y = 0

  imagen = None
  barrilRoto = None

  estaRoto = False
  seRompioEn = 0
  debeRemoverse = False

  tamanio = [33,22]
  proporcion = 0.66

  velocidadEnY = 1.5
  gravedad = 1.05
  maximaVelocidadEnY = 20

  def partido(self, momento):
    self.estaRoto = True
    self.seRompioEn = momento
    self.velocidadEnY = 5
    self.x -= 10

  def buscarColision(self, anasto):

    golpeEnX = False
    golpeEnY = False

    if anasto.x > self.x and anasto.x < self.x + 75:
      golpeEnX = True
    elif anasto.x + 57 > self.x and anasto.x + 57 < self.x + 75:
      golpeEnX = True
    if anasto.y + 120 > self.y and anasto.y < self.y:
      golpeEnY = True
    elif anasto.y < self.y + 48:
      golpeEnY = True
    if golpeEnX is True and golpeEnY is True:
      return True

  def cargarImagenes(self, pygame):
    self.imagen = pygame.image.load("recursos/Barril.png")
    self.barrilRoto = pygame.image.load("recursos/Barril_roto.png")

  def mover(self, altoVentana):

    if self.velocidadEnY < self.maximaVelocidadEnY:
      self.velocidadEnY = self.velocidadEnY * self.gravedad
    self.y += self.velocidadEnY

    if self.y > altoVentana:
      self.debeRemoverse = True

  def dibujar(self, superficieDeDibujo, pygame):
    if self.estaRoto is True:
      superficieDeDibujo.blit(self.barrilRoto, (self.x, self.y))
    else :
      superficieDeDibujo.blit(self.imagen, (self.x, self.y))

  def __init__(self, vacante):
    self.vacante = vacante
    self.x = self.vacantes[vacante][0]
    self.y = self.vacantes[vacante][1] + 24
