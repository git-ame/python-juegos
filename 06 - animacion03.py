import pygame, sys, random
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO

pygame.init()

# Designar el tamaño de la ventana o superficio de dibujo en la que aparecera toda la animacion
anchoVentana = 640
altoVentana = 480
superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana))

# El titulo de la ventana
pygame.display.set_caption('Figuras en PyGame')

# Pertenece a la segunda modificacion del cuerpo
cuadradoAzulX = 0.0
cuadradoAzulY = 0.0
# cuadradoAzulVX = 1
cuadradoAzulVX = 8
cuadradoAzulVY = 1

while True:
	# Llena toda la pantalla con color negro
	superficieDeDibujo.fill((0,0,0))
	# Dibuja rectagulos del mismo tamaño en lugares diferentes por cada iteración
	pygame.draw.rect(superficieDeDibujo, (0,0,255), (cuadradoAzulX, cuadradoAzulY, 10, 10 ))

	# Trabajando con numeros de valor flotante
	cuadradoAzulX += cuadradoAzulVX
	cuadradoAzulY += cuadradoAzulVY
	# cuadradoAzulVX += 0.001
	cuadradoAzulVX -= 0.2
	# cuadradoAzulVY += 0.1

	# Monitorea todos los eventos del sistema
	for evento in EVENTOS_DEL_JUEGO.get():
		# Si el jugador ha hecho click en el icono cerrar [ X ] de la ventana
		if evento.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()
