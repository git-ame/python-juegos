import pygame, sys, random
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO
import pygame.time as TIEMPO_DEL_JUEGO

pygame.init()
reloj = pygame.time.Clock()

tituloDelJuego = pygame.image.load("recursos/titulo.png")
finDeJuego = pygame.image.load("recursos/fin.png")

anchoVentana = 400
altoVentana = 600

superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana))
pygame.display.set_caption('Lánzate!')

botonIzquierdo = False
botonDerecho = False

juegoIniciado = False
juegoTerminado = False
plataformasDeJuego = []
velocidadDePlataforma = 3
retrasoDePlataforma = 2000
ultimaPlataforma = 0
plataformasAtravezadas = -1
saltandoAlVacio = False

juegoIniciadoEn = 0
cronometro = 0

jugador = {
  "x" : anchoVentana / 2,
  "y" : 0,
  "alto" : 25,
  "ancho" : 10,
  "velocidadEnY" : 5
}

def dibujarAJugador():

  pygame.draw.rect(superficieDeDibujo, (255,0,0), (jugador["x"], jugador["y"], jugador["ancho"], jugador["alto"]))

def moverAJugador():
  
  global plataformasAtravezadas, saltandoAlVacio

  colorInferiorIzqDelJugador = True
  colorInferiorDerDelJugador = True

  if superficieDeDibujo.get_at(( int(jugador["x"]), int(jugador["y"]) + int(jugador["alto"]) )) == (0,0,0,255):
    colorInferiorIzqDelJugador = False

  if superficieDeDibujo.get_at(( int(jugador["x"]) + int(jugador["ancho"]), int(jugador["y"]) + int(jugador["alto"]) )) == (0,0,0,255):
    colorInferiorDerDelJugador = False

  if colorInferiorIzqDelJugador is False and colorInferiorDerDelJugador is False and (jugador["y"] + jugador["alto"]) + jugador["velocidadEnY"] < altoVentana:
    jugador["y"] += jugador["velocidadEnY"]

    if saltandoAlVacio is False:
      saltandoAlVacio = True
      plataformasAtravezadas += 1

  else :

    pisoDePlataformaEncontrado = False
    grosorDePlataforma = 0
    saltandoAlVacio = False

    while pisoDePlataformaEncontrado is False:

      if superficieDeDibujo.get_at(( int(jugador["x"]), ( int(jugador["y"]) + int(jugador["alto"]) ) - grosorDePlataforma )) == (0,0,0,255):
        jugador["y"] -= grosorDePlataforma
        pisoDePlataformaEncontrado = True
      elif (jugador["y"] + jugador["alto"]) - grosorDePlataforma > 0:
        grosorDePlataforma += 1
      else :

        finDelJuego()
        break

  if botonIzquierdo is True:
    if jugador["x"] > 0 and jugador["x"] - 5 > 0:
      jugador["x"] -= 5
    elif jugador["x"] > 0 and jugador["x"] - 5 < 0:
      jugador["x"] = 0

  if botonDerecho is True:
    if jugador["x"] + jugador["ancho"] < anchoVentana and (jugador["x"] + jugador["ancho"]) + 5 < anchoVentana:
      jugador["x"] += 5
    elif jugador["x"] + jugador["ancho"] < anchoVentana and (jugador["x"] + jugador["ancho"]) + 5 > anchoVentana:
      jugador["x"] = anchoVentana - jugador["ancho"]

def crearPlataforma():

  global ultimaPlataforma, retrasoDePlataforma

  posicion_Y_DePlataforma = altoVentana
  posicionDelAgujero = random.randint(0, anchoVentana - 40)

  plataformasDeJuego.append({"posicion" : [0, posicion_Y_DePlataforma], "agujero" : posicionDelAgujero})
  ultimaPlataforma = TIEMPO_DEL_JUEGO.get_ticks()

  if retrasoDePlataforma > 800:
    retrasoDePlataforma -= 50

def moverPlataformas():
  # print("Platforms")

  for indice, plataforma in enumerate(plataformasDeJuego):

    plataforma["posicion"][1] -= velocidadDePlataforma

    if plataforma["posicion"][1] < -10:
      plataformasDeJuego.pop(indice)
      

def dibujarPlataformas():

  for plataforma in plataformasDeJuego:

    pygame.draw.rect(superficieDeDibujo, (255,255,255), (plataforma["posicion"][0], plataforma["posicion"][1], anchoVentana, 10))
    pygame.draw.rect(superficieDeDibujo, (0,0,0), (plataforma["agujero"], plataforma["posicion"][1], 40, 10) )


def finDelJuego():
  global juegoIniciado, juegoTerminado

  velocidadDePlataforma = 0
  juegoIniciado = False
  juegoTerminado = True

def reiniciarJuego():

  global plataformasDeJuego, jugador, juegoIniciadoEn, plataformasAtravezadas, retrasoDePlataforma

  plataformasDeJuego = []
  jugador["x"] = anchoVentana / 2
  jugador["y"] = 0
  juegoIniciadoEn = TIEMPO_DEL_JUEGO.get_ticks()
  plataformasAtravezadas = -1
  retrasoDePlataforma = 2000

def salirDelJuego():
  pygame.quit()
  sys.exit()

# Bucle principal
while True:

  superficieDeDibujo.fill((0,0,0))

  for event in EVENTOS_DEL_JUEGO.get():

    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_LEFT:
        botonIzquierdo = True
      if event.key == pygame.K_RIGHT:
        botonDerecho = True
      if event.key == pygame.K_ESCAPE:
        salirDelJuego()

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        botonIzquierdo = False
      if event.key == pygame.K_RIGHT:
        botonDerecho = False

      if event.key == pygame.K_SPACE:
        if juegoIniciado == False:
          reiniciarJuego()
          juegoIniciado = True

    if event.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
      salirDelJuego()

  if juegoIniciado is True:
    # Play game
    cronometro = TIEMPO_DEL_JUEGO.get_ticks() - juegoIniciadoEn

    moverPlataformas()
    dibujarPlataformas()
    moverAJugador()
    dibujarAJugador()

  elif juegoTerminado is True:
    # Dibujar fin de juego en la pantalla
    superficieDeDibujo.blit(finDeJuego, (0, 150))

  else :
    # Pantalla de bienvenida
    superficieDeDibujo.blit(tituloDelJuego, (0, 150))

  if TIEMPO_DEL_JUEGO.get_ticks() - ultimaPlataforma > retrasoDePlataforma:
    crearPlataforma()

  reloj.tick(60)
  pygame.display.update()
