import pygame, sys, random
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO
import pygame.time as TIEMPO_DEL_JUEGO

anchoVentana = 600
altoVentana = 650

pygame.init()
superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana))
pygame.display.set_caption('Sonidos')

botones = []
botonDetener = { "imagen" : pygame.image.load("recursos/iconos/detener.png"), "posicion" : (275, 585)}

posicionDelRaton = None
volumen = 1.0

pygame.mixer.init()
pygame.mixer.music.load('recursos/sonidos/OGG/granja.ogg')
pygame.mixer.music.play(-1)

def dibujarBotones():

  for boton in botones:
    superficieDeDibujo.blit(boton["imagen"], boton["posicion"])

  superficieDeDibujo.blit(botonDetener["imagen"], botonDetener['posicion'])

def dibujarVolumen():

  pygame.draw.rect(superficieDeDibujo, (229, 229, 229), (450, 610, 100, 5))

  posicionDeVolumen = (100 / 100) * (volumen * 100)

  pygame.draw.rect(superficieDeDibujo, (204, 204, 204), (450 + posicionDeVolumen, 600, 10, 25))

def manejarClick():

  global posicionDelRaton, volumen

  for boton in botones:

    tamanioDelBoton = boton['imagen'].get_rect().size
    posicionDelBoton = boton['posicion']

    if posicionDelRaton[0] > posicionDelBoton[0] and posicionDelRaton[0] < posicionDelBoton[0] + tamanioDelBoton[0]:

      if posicionDelRaton[1] > posicionDelBoton[1] and posicionDelRaton[1] < posicionDelBoton[1] + tamanioDelBoton[1]:
        boton['sonido'].set_volume(volumen)
        boton['sonido'].play()

    if posicionDelRaton[0] > botonDetener['posicion'][0] and posicionDelRaton[0] < botonDetener['posicion'][0] + botonDetener['imagen'].get_rect().size[0]:
      if posicionDelRaton[1] > botonDetener['posicion'][1] and posicionDelRaton[1] < botonDetener['posicion'][1] + botonDetener['imagen'].get_rect().size[1]:
        pygame.mixer.stop()

def verificarVolumen():

  global posicionDelRaton, volumen

  if pygame.mouse.get_pressed()[0] == True:
    
    if posicionDelRaton[1] > 600 and posicionDelRaton[1] < 625:
      if posicionDelRaton[0] > 450 and posicionDelRaton[0] < 550:
        volumen = float((posicionDelRaton[0] - 450)) / 100

def salirDelJuego():
  pygame.quit()
  sys.exit()

# Crear botones
botones.append({ "imagen" : pygame.image.load("recursos/iconos/oveja.png"), "posicion" : (25, 25), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/oveja.ogg')})
botones.append({ "imagen" : pygame.image.load("recursos/iconos/gallo.png"), "posicion" : (225, 25), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/gallo.ogg')})
botones.append({ "imagen" : pygame.image.load("recursos/iconos/cerdo.png"), "posicion" : (425, 25), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/cerdo.ogg')})
botones.append({ "imagen" : pygame.image.load("recursos/iconos/raton.png"), "posicion" : (25, 225), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/raton.ogg')})
botones.append({ "imagen" : pygame.image.load("recursos/iconos/caballo.png"), "posicion" : (225, 225), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/caballo.ogg')})
botones.append({ "imagen" : pygame.image.load("recursos/iconos/perro.png"), "posicion" : (425, 225), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/perro.ogg')})
botones.append({ "imagen" : pygame.image.load("recursos/iconos/vaca.png"), "posicion" : (25, 425), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/vaca.ogg')})
botones.append({ "imagen" : pygame.image.load("recursos/iconos/gallina.png"), "posicion" : (225, 425), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/gallina.ogg')})
botones.append({ "imagen" : pygame.image.load("recursos/iconos/gato.png"), "posicion" : (425, 425), "sonido" : pygame.mixer.Sound('recursos/sonidos/OGG/gato.ogg')})

# Bucle Principal
while True:

  superficieDeDibujo.fill((255,255,255))

  posicionDelRaton = pygame.mouse.get_pos()

  for event in EVENTOS_DEL_JUEGO.get():

    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_ESCAPE:
        salirDelJuego()

    if event.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
      salirDelJuego()

    if event.type == pygame.MOUSEBUTTONUP:
      manejarClick()

  dibujarBotones()
  verificarVolumen()
  dibujarVolumen()

  pygame.display.update()
