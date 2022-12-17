import pygame, sys, random, math
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO
import pygame.time as TIEMPO_DEL_JUEGO
import naves

import nivelesDelJuego

anchoVentana = 1024
altoVentana = 614
tiempoTranscurrido = 0

pygame.init()
pygame.font.init()
reloj = pygame.time.Clock()
superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)

pygame.display.set_caption('Es el Dia de Independencia y los aliens nos invaden!')
tipoDeLetra = pygame.font.SysFont("monospace", 50)

juegoIniciado = False
tiempoDeJuegoIniciado = 0
tiempoDeJuegoTerminado = 0
juegoTerminado = False
juegoGanado = False

nivelActual = 0
invasionActual = 0
ultimaGeneracion = 0
sgteNivel = 0

# Variables para el raton
posicionDelRaton = (0,0)
estadosDelRaton = None
botonDeRatonPresionado = False

# Variables para las imagenes
pantallaInicio = pygame.image.load("graficos/inicio.png")
fondo = pygame.image.load("graficos/fondo.png")
pantallaDePerdedor = pygame.image.load("graficos/pantalla_perdedor.png")
pantallaDeGanador = pygame.image.load("graficos/pantalla_ganador.png")
siguienteInvasion = pygame.image.load("graficos/sgte_nivel.png")
ultimaInvasion = pygame.image.load("graficos/ultimo_nivel.png")

# Naves
nave = naves.Jugador(anchoVentana / 2, altoVentana, pygame, superficieDeDibujo)
navesEnemigas = []

balasSobrantes = []

# Configuracion de sonido
pygame.mixer.init()

def lanzamientoDeInvacion():

  global ultimaGeneracion, invasionActual, nivelActual, juegoTerminado, juegoGanado, sgteNivel

  esteNivel = nivelesDelJuego.nivel[nivelActual]["estructura"]

  if invasionActual < len(esteNivel):

    estaInvacion = esteNivel[invasionActual]

    for indice, enemigoEnEstaPosicion in enumerate(estaInvacion):
      if enemigoEnEstaPosicion is 1:
        navesEnemigas.append(naves.Enemigo(((anchoVentana / len(estaInvacion)) * indice), -60, pygame, superficieDeDibujo, 1))

  elif nivelActual + 1 < len(nivelesDelJuego.nivel) :
    nivelActual += 1
    invasionActual = 0
    nave.escudos = nave.escudosMaximo
    sgteNivel = tiempoTranscurrido + 5000
  else:
    juegoGanado = True

  ultimaGeneracion = tiempoTranscurrido
  invasionActual += 1

def actualizarJuego():

  global botonDeRatonPresionado, juegoTerminado, juegoGanado, balasSobrantes

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
        juegoGanado = False
        return

    else:
      enemigosParaRemover.append(indice)

  oC = 0

  for indice in enemigosParaRemover:
    for balasRestantes in navesEnemigas[indice - oC].balas:
      balasSobrantes.append(balasRestantes)

    del navesEnemigas[indice - oC]
    oC += 1

  oC = 0

  for indice, unaBala in enumerate(balasSobrantes):
      unaBala.mover()
      impactaNave = unaBala.verificarImpacto(nave)

      if impactaNave is True or unaBala.y > altoVentana:
        del balasSobrantes[indice - oC]
        oC += 1

def dibujarJuego():

    global balasSobrantes, sgteNivel, tiempoTranscurrido, juegoGanado

    superficieDeDibujo.blit(fondo, (0, 0))
    nave.dibujar()
    nave.dibujarBalas()

    for unaBala in balasSobrantes:
      unaBala.dibujar()

    colorDeSalud = [(62, 180, 76), (180, 62, 62)]
    cualColor = 0

    if(nave.salud <= 1):
      cualColor = 1

    for enemigo in navesEnemigas:
      enemigo.dibujar()
      enemigo.dibujarBalas()

    pygame.draw.rect(superficieDeDibujo, colorDeSalud[cualColor], (0, altoVentana - 5, (anchoVentana / nave.saludMaxima) * nave.salud, 5))
    pygame.draw.rect(superficieDeDibujo, (62, 145, 180), (0, altoVentana - 10, (anchoVentana / nave.escudosMaximo) * nave.escudos, 5))

    if tiempoTranscurrido < sgteNivel:
      if juegoGanado is True:
        superficieDeDibujo.blit(ultimaInvasion, (250, 150))
      else:
        superficieDeDibujo.blit(siguienteInvasion, (250, 150))

def reiniciarJuego():
  global juegoTerminado, nivelActual, invasionActual, ultimaGeneracion, sgteNivel, balasSobrantes, juegoGanado, navesEnemigas, nave

  juegoTerminado = False
  juegoGanado = False
  nivelActual = 0 
  invasionActual = 0
  ultimaGeneracion = 0
  sgteNivel = 0
  balasSobrantes = []
  navesEnemigas = []
  nave.salud = nave.saludMaxima
  nave.escudos = nave.escudosMaximo
  nave.balas = []

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
        pygame.mouse.set_visible(False)
        juegoIniciado = True

    elif estadosDelRaton[0] is 0 and botonDeRatonPresionado is True:
      botonDeRatonPresionado = False

  elif juegoIniciado is True and juegoTerminado is True and juegoGanado is False:
    superficieDeDibujo.blit(pantallaDePerdedor, (0, 0))
    tiempoQueAguanto = (tiempoDeJuegoTerminado - tiempoDeJuegoIniciado) / 1000
  
  if juegoIniciado is True and juegoGanado is True and len(navesEnemigas) is 0:
    superficieDeDibujo.blit(pantallaDeGanador, (0, 0))

  # Eventos generados por el usuario y el sistema 
  for evento in EVENTOS_DEL_JUEGO.get():

    if evento.type == pygame.KEYDOWN:

      if evento.key == pygame.K_ESCAPE:
        salirDelJuego()

      if evento.key == pygame.K_SPACE:
        if juegoIniciado is True and juegoTerminado is True or juegoIniciado is True and juegoGanado is True:
          reiniciarJuego()

  if tiempoTranscurrido - ultimaGeneracion > nivelesDelJuego.nivel[nivelActual]["intervalo"] * 1000 and juegoIniciado is True and juegoTerminado is False:
    lanzamientoDeInvacion()

  if evento.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
    salirDelJuego()
  
  reloj.tick(60)
  pygame.display.update()
