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
pygame.display.set_caption('El teclado en PyGame')
# Variables para el jugador
tamanioDelJugador = 20
espacioEnX = (anchoVentana/2) - (tamanioDelJugador/2)
espacioEnY = altoVentana - tamanioDelJugador
velocidadEnX = 1.0
velocidadEnY = 0.0
alturaDeSalto = 25.0
velocidadDeMovimiento = 1.0
velocidadMaxima = 10.0
fuerzaDeGravedad = 1.0
# Variables para el teclado 
botonIzquierdo = False
botonDerecho = False
botonSalto = False

# Para mover al jugador (cuadrado)
def mover():
	# Definicion de variables globales
	global espacioEnX, espacioEnY, velocidadEnX, velocidadEnY, botonSalto, fuerzaDeGravedad

	# Mover a la izquierda
	if botonIzquierdo:
		# Si el jugador se mueve a la derecha, inicializar la velocidad e invertir la direccion
		if velocidadEnX > 0.0:
			velocidadEnX = velocidadDeMovimiento
			velocidadEnX = -velocidadEnX
		# Asegurarse que el jugador no deje la superficie de dibujo por la izquierda
		if espacioEnX > 0:
			espacioEnX += velocidadEnX

	# Mover a la derecha
	if botonDerecho:
		# Si el jugador se mueve a la izquierda, inicializar la velocidad e invertir la direccion
		if velocidadEnX < 0.0:
			velocidadEnX = velocidadDeMovimiento
		# Asegurarse que el jugador no deje la superficie de dibujo por la derecha
		if espacioEnX + tamanioDelJugador < anchoVentana:
			espacioEnX += velocidadEnX

	# Saltar
	if velocidadEnY > 1.0:
		velocidadEnY = velocidadEnY * 0.9
	else:
		velocidadEnY = 0.0
		botonSalto = False

	# Si el jugador esta en el aire, agregar la gravedad para que vuelva a tierra
	if espacioEnY < altoVentana - tamanioDelJugador:
		espacioEnY += fuerzaDeGravedad
		fuerzaDeGravedad = fuerzaDeGravedad * 1.1
	else:
		espacioEnY = altoVentana - tamanioDelJugador
		fuerzaDeGravedad = 1.0

	espacioEnY -= velocidadEnY

	if velocidadEnX > 0.0 and velocidadEnX < velocidadMaxima or velocidadEnX < 0.0 and velocidadEnX > -velocidadMaxima:
		if botonSalto == False:
			velocidadEnX = velocidadEnX * 1.1

# Para salir del juego
def salirDelJuego():
	pygame.quit()
	sys.exit()

while True:
	superficieDeDibujo.fill((0,0,0))

	pygame.draw.rect(superficieDeDibujo, (255,0,0), (espacioEnX, espacioEnY, tamanioDelJugador, tamanioDelJugador))

	# Obtener la lista de eventos ocurridos desde el ultimo "dibujado"
	for evento in EVENTOS_DEL_JUEGO.get():

		if evento.type == pygame.KEYDOWN:
			# Eventos ocurridos cuando se presionan las teclas de direccion 
			if evento.key == pygame.K_LEFT:
				botonIzquierdo = True
			if evento.key == pygame.K_RIGHT:
				botonDerecho = True
			if evento.key == pygame.K_UP:
				if not botonSalto:
					botonSalto = True
					velocidadEnY += alturaDeSalto
			if evento.key == pygame.K_ESCAPE:
				salirDelJuego()

		if evento.type == pygame.KEYUP:
			# Eventos ocurridos cuando se dejan de presionar las teclas de direccion 
			if evento.key == pygame.K_LEFT:
				botonIzquierdo = False
				velocidadEnX = velocidadDeMovimiento
			if evento.key == pygame.K_RIGHT:
				botonDerecho = False
				velocidadEnX = velocidadDeMovimiento

		if evento.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
			salirDelJuego()

	mover()

	reloj.tick(60)
	pygame.display.update()