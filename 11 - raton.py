import pygame, sys
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO

# Variables de Pygame
pygame.init()
reloj = pygame.time.Clock()
# Variables del programador
anchoVentana = 800
altoVentana = 600

superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana))

pygame.display.set_caption('El raton en PyGame')

# Variables de raton
posicionDelRaton = None
botonDeRatonPresionado = False

# Variables para el jugador o cuadrado
tamanioDelJugador = 40
colorDelJugador = (255, 0, 0)
espacioEnX = anchoVentana / 2
espacioEnY = altoVentana - tamanioDelJugador
arrastrarAJugador = False
fuerzaDeGravedad = 5.0

def verificarLimite():

	global colorDelJugador, espacioEnX, espacioEnY, arrastrarAJugador

	if botonDeRatonPresionado == True:
		# Esta el cursor sobre el cuadrado?
		if posicionDelRaton[0] > espacioEnX and posicionDelRaton[0] < espacioEnX + tamanioDelJugador:

			if posicionDelRaton[1] > espacioEnY and posicionDelRaton[1] < espacioEnY + tamanioDelJugador:

				arrastrarAJugador = True
				pygame.mouse.set_visible(0)

	else :
		colorDelJugador = (255,0,0)
		pygame.mouse.set_visible(1)
		arrastrarAJugador = False

def verificarGravedad():

	global fuerzaDeGravedad, espacioEnY, tamanioDelJugador, altoVentana

	# Esta el cuadrado en el aire y debemos soltarlo?
	if espacioEnY < altoVentana - tamanioDelJugador and botonDeRatonPresionado == False:
		espacioEnY += fuerzaDeGravedad
		fuerzaDeGravedad = fuerzaDeGravedad * 1.1
	else :
		espacioEnY = altoVentana - tamanioDelJugador
		fuerzaDeGravedad = 5.0

def dibujarCuadrado():

	global colorDelJugador, espacioEnX, espacioEnY, arrastrarAJugador

	if arrastrarAJugador == True:

		colorDelJugador = (0, 255, 0)
		espacioEnX = posicionDelRaton[0] - tamanioDelJugador / 2
		espacioEnY = posicionDelRaton[1] - tamanioDelJugador / 2

	pygame.draw.rect(superficieDeDibujo, colorDelJugador, (espacioEnX, espacioEnY, tamanioDelJugador, tamanioDelJugador))

# Para salir del juego
def salirDelJuego():
	pygame.quit()
	sys.exit()

while True:

	posicionDelRaton = pygame.mouse.get_pos()

	superficieDeDibujo.fill((0,0,0))

	# Verifica si se ha presionado el boton del raton
	if pygame.mouse.get_pressed()[0] == True:
		botonDeRatonPresionado = True
	else :
		botonDeRatonPresionado = False

	verificarLimite()
	verificarGravedad()
	dibujarCuadrado()

	reloj.tick(60)
	pygame.display.update()

	for event in EVENTOS_DEL_JUEGO.get():

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				salirDelJuego()

		if event.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
			salirDelJuego()
