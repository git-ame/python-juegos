import pygame, sys, random, math
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO
import pygame.time as TIEMPO_DEL_JUEGO
import naves

anchoVentana = 1024
altoVentana = 614

pygame.init()
pygame.font.init()
reloj = pygame.time.Clock()
superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana))

pygame.display.set_caption('Es el Dia de Independencia y los aliens nos invaden!')
tipoDeLetra = pygame.font.SysFont("monospace", 50)

juegoIniciado = False
tiempoDeJuegoIniciado = 0
tiempoDeJuegoTerminado = 0
juegoTerminado = False

# Variables para el raton
posicionDelRaton = (0,0)
estadosDelRaton = None
botonDeRatonPresionado = False

# Variables para las imagenes
pantallaInicio = pygame.image.load("graficos/inicio.png")
fondo = pygame.image.load("graficos/fondo.png")

# Naves
nave = naves.Jugador(anchoVentana / 2, altoVentana, pygame, superficieDeDibujo)
navesEnemigas = []

ultimoEnemigoCreado = 0
intervaloEnemigo = random.randint(1000, 2500)

# Configuracion de sonido
pygame.mixer.init()

def actualizarJuego():

  global botonDeRatonPresionado, juegoTerminado

  if estadosDelRaton[0] is 1 and botonDeRatonPresionado is False:
    nave.fuego()
    botonDeRatonPresionado = True
  elif estadosDelRaton[0] is 0 and botonDeRatonPresionado is True:
    botonDeRatonPresionado = False

  nave.fijarPosicion(posicionDelRaton)

  enemigosParaRemover = []

  for indice, enemigo in enumerate(navesEnemigas):

    if enemigo.y < altoVentana:
      enemigo.mover()
      enemigo.intentarDisparar()
      jugadorEsDestruido = enemigo.verificarImpacto(nave)
      enemigoEsDestruido = nave.verificarImpacto(enemigo)

      if enemigoEsDestruido is True:
        enemigosParaRemover.append(indice)

      if jugadorEsDestruido is True:
        juegoTerminado = True
        print ('\n\n\nJuego Terminado\n\n\n')
        salirDelJuego()

    else:
      enemigosParaRemover.append(indice)

  for indice in enemigosParaRemover:
    del navesEnemigas[indice]

def dibujarJuego():
    superficieDeDibujo.blit(fondo, (0, 0))
    nave.dibujar()
    nave.dibujarBalas()

    for enemigo in navesEnemigas:
      enemigo.dibujar()
      enemigo.dibujarBalas()

def salirDelJuego():
  pygame.quit()
  sys.exit()

# Bucle principal
while True:

  tiempoTranscurrido = TIEMPO_DEL_JUEGO.get_ticks()
  posicionDelRaton = pygame.mouse.get_pos()
  estadosDelRaton = pygame.mouse.get_pressed()

  if juegoIniciado is True and juegoTerminado is False:

    actualizarJuego()
    dibujarJuego()

  elif juegoIniciado is False and juegoTerminado is False:
    superficieDeDibujo.blit(pantallaInicio, (0, 0))

    if estadosDelRaton[0] is 1:

      if posicionDelRaton[0] > 445 and posicionDelRaton[0] < 580 and posicionDelRaton[1] > 450 and posicionDelRaton[1] < 510:

        juegoIniciado = True

    elif estadosDelRaton[0] is 0 and botonDeRatonPresionado is True:
      botonDeRatonPresionado = False

  elif juegoIniciado is True and juegoTerminado is True:
    superficieDeDibujo.blit(pantallaInicio, (0, 0))
    tiempoQueAguanto = (tiempoDeJuegoTerminado - tiempoDeJuegoIniciado) / 1000

  # Eventos generados por el usuario y el sistema 
  for evento in EVENTOS_DEL_JUEGO.get():

    if evento.type == pygame.KEYDOWN:

      if evento.key == pygame.K_ESCAPE:
        salirDelJuego()

  if tiempoTranscurrido - ultimoEnemigoCreado > intervaloEnemigo and juegoIniciado is True:
    navesEnemigas.append(naves.Enemigo(random.randint(0, anchoVentana), -60, pygame, superficieDeDibujo, 1))
    ultimoEnemigoCreado = TIEMPO_DEL_JUEGO.get_ticks()

  if evento.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
    salirDelJuego()
 
  reloj.tick(60)
  pygame.display.update()
