import pygame, sys, random, math
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO
import pygame.time as TIEMPO_DEL_JUEGO
import objetos

anchoVentana = 1000
altoVentana = 768

pygame.init()
pygame.font.init()
reloj = pygame.time.Clock()
superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana), pygame.FULLSCREEN)

pygame.display.set_caption('El dia negro de Anastasio')
tipoDeLetra = pygame.font.SysFont("monospace", 50)

juegoIniciado = False
tiempoDeJuegoIniciado = 0
tiempoDeJuegoTerminado = 0
juegoTerminado = False

pantallaInicio = pygame.image.load("recursos/iniciarJuego.png")
pantallaFin = pygame.image.load("recursos/juegoTerminado.png")

fondo = pygame.image.load("recursos/fondo.png")
Anasto = objetos.Anasto(anchoVentana / 2)
Barriles = []
ultimoBarril = 0
ultimoVacanteDeBarril = 0
intervaloEntreBarriles = 1500

irPorLaIzquierda = False
irPorLaDerecha = False

def salirDelJuego():
	pygame.quit()
	sys.exit()

def nuevoBarril():
	global Barriles, ultimoBarril, ultimoVacanteDeBarril

	vacante = random.randint(0, 12)

	while vacante == ultimoVacanteDeBarril:
		vacante = random.randint(0, 12)

	elBarril = objetos.Barril(vacante)
	elBarril.cargarImagenes(pygame)

	Barriles.append(elBarril)
	ultimoBarril = TIEMPO_DEL_JUEGO.get_ticks()
	ultimoVacanteDeBarril = vacante

Anasto.cargarImagenes(pygame)

# Bucle principal
while True:
	
	tiempoTranscurrido = TIEMPO_DEL_JUEGO.get_ticks()

	if juegoIniciado is True and juegoTerminado is False:

		superficieDeDibujo.blit(fondo, (0, 0))

		Anasto.dibujar(superficieDeDibujo, tiempoTranscurrido)

		barrilesParaRemover = []

		for indice, barril in enumerate(Barriles):
			barril.mover(altoVentana)
			barril.dibujar(superficieDeDibujo, pygame)

			if barril.estaRoto is False:

				haColisionado = barril.buscarColision(Anasto);
				
				if haColisionado is True:
					barril.partido(tiempoTranscurrido)
					Anasto.golpeRecibido = True
					Anasto.momentoDelGolpe = tiempoTranscurrido
					if Anasto.salud >= 10:
						Anasto.salud -= 10
					else :
						juegoTerminado = True
						tiempoDeJuegoTerminado = tiempoTranscurrido

			elif tiempoTranscurrido - barril.seRompioEn > 1000:

				barrilesParaRemover.append(indice)
				continue

			if barril.debeRemoverse is True:
				barrilesParaRemover.append(indice)
				continue
		
		pygame.draw.rect(superficieDeDibujo, (175,59,59), (0, altoVentana - 10, (anchoVentana / 100) * Anasto.salud , 10))

		for indice2 in barrilesParaRemover:
			del Barriles[indice2]

		if irPorLaIzquierda is True:
			Anasto.moverALaIzquierda(0)
		
		if irPorLaDerecha is True:
			Anasto.moverALaDerecha(anchoVentana)

	elif juegoIniciado is False and juegoTerminado is False:
		superficieDeDibujo.blit(pantallaInicio, (0, 0))

	elif juegoIniciado is True and juegoTerminado is True:
		superficieDeDibujo.blit(pantallaFin, (0, 0))
		tiempoQueAguanto = (tiempoDeJuegoTerminado - tiempoDeJuegoIniciado) / 1000
	
		if tiempoQueAguanto < 10:
			tiempoQueAguanto = "0" + str(tiempoQueAguanto)
		else :
			tiempoQueAguanto = str(tiempoQueAguanto)

		mensajeDeTexto = tipoDeLetra.render(tiempoQueAguanto, 1, (175,59,59))
		superficieDeDibujo.blit(mensajeDeTexto, (495, 430))

	# Eventos generados por el usuario y el sistema 
	for evento in EVENTOS_DEL_JUEGO.get():

		if evento.type == pygame.KEYDOWN:

			if evento.key == pygame.K_ESCAPE:
				salirDelJuego()
			elif evento.key == pygame.K_LEFT:
				irPorLaIzquierda = True
				irPorLaDerecha = False
			elif evento.key == pygame.K_RIGHT:
				irPorLaIzquierda = False
				irPorLaDerecha = True
			elif evento.key == pygame.K_RETURN:
				if juegoIniciado is False and juegoTerminado is False:
					juegoIniciado = True
					tiempoDeJuegoIniciado = tiempoTranscurrido
				elif juegoIniciado is True and juegoTerminado is True:
					Anasto.reiniciar(anchoVentana / 2)
					
					Barriles = []
					intervaloEntreBarriles = 1500

					juegoTerminado = False

	if evento.type == pygame.KEYUP:

		if evento.key == pygame.K_LEFT:
			irPorLaIzquierda = False
		if evento.key == pygame.K_RIGHT:
			irPorLaDerecha = False

		if evento.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
			salirDelJuego()

	reloj.tick(60)
	pygame.display.update()

	if TIEMPO_DEL_JUEGO.get_ticks() - ultimoBarril > intervaloEntreBarriles and juegoIniciado is True:
		nuevoBarril()
		if intervaloEntreBarriles > 150:
			intervaloEntreBarriles -= 50
