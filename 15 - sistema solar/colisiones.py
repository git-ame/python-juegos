import pygame, sys, random, math
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO
import pygame.time as TIEMPO_DEL_JUEGO

anchoVentana = 1024
altoVentana = 768

pygame.init()
reloj = pygame.time.Clock()
superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana))

pygame.display.set_caption('Colisiones')

posicionPreviaDelRaton = [0,0]
posicionDelRaton = None
botonDeRatonPresionado = False

objetosAColisionar = []
objetoActual = None
enExpansion = True

dibujarFuerzaDeAtraccion = False

gravedad = 0.06

def dibujarObjetosAColisionar():

	for unObjeto in objetosAColisionar:
		unObjeto["posicion"][0] += unObjeto["velocidad"][0]
		unObjeto["posicion"][1] += unObjeto["velocidad"][1]

		pygame.draw.circle(superficieDeDibujo, (255,255,255), (int(unObjeto["posicion"][0]), int(unObjeto["posicion"][1])), int(unObjeto["radio"]), 0)

def dibujarObjetoActual():

	global enExpansion, objetoActual

	objetoActual["posicion"][0] = posicionDelRaton[0]
	objetoActual["posicion"][1] = posicionDelRaton[1]

	if enExpansion is True and objetoActual["radio"] < 30:
		objetoActual["radio"] += 0.2

		if objetoActual["radio"] >= 30:
			enExpansion = False
			objetoActual["radio"] = 9.9

	elif enExpansion is False and objetoActual["radio"] > 1:
		objetoActual["radio"] -= 0.2

		if objetoActual["radio"] <= 1:
			enExpansion = True
			objetoActual["radio"] = 1.1

	objetoActual["masa"] = objetoActual["radio"]

	pygame.draw.circle(superficieDeDibujo, (255,0,0), (int(objetoActual["posicion"][0]), int(objetoActual["posicion"][1])), int(objetoActual["radio"]), 0)

def calcularMovimiento():

	for unObjeto in objetosAColisionar:

		for elOtroObjeto in objetosAColisionar:

			if unObjeto is not elOtroObjeto:
				
				direccion = (elOtroObjeto["posicion"][0] - unObjeto["posicion"][0], elOtroObjeto["posicion"][1] - unObjeto["posicion"][1]) 
				magnitud = math.hypot(elOtroObjeto["posicion"][0] - unObjeto["posicion"][0], elOtroObjeto["posicion"][1] - unObjeto["posicion"][1]) 
				direccionNormal = (direccion[0] / magnitud, direccion[1] / magnitud)

				if magnitud < 5:
					magnitud = 5
				elif magnitud > 15:
					magnitud = 15

				fuerza = ((gravedad * unObjeto["masa"] * elOtroObjeto["masa"]) / (magnitud * magnitud))

				fuerzaAplicada = (direccionNormal[0] * fuerza, direccionNormal[1] * fuerza)

				elOtroObjeto["velocidad"][0] -= fuerzaAplicada[0]
				elOtroObjeto["velocidad"][1] -= fuerzaAplicada[1]

				if dibujarFuerzaDeAtraccion is True:
					pygame.draw.line(superficieDeDibujo, (255,255,255), (unObjeto["posicion"][0],unObjeto["posicion"][1]), (elOtroObjeto["posicion"][0],elOtroObjeto["posicion"][1]), 1)

def manejarColisiones():

	h = 0

	while h < len(objetosAColisionar):

		i = 0

		unObjeto = objetosAColisionar[h]

		while i < len(objetosAColisionar):

			otroObjeto = objetosAColisionar[i]

			if unObjeto != otroObjeto:

				distancia = math.hypot(otroObjeto["posicion"][0] - unObjeto["posicion"][0], otroObjeto["posicion"][1] - unObjeto["posicion"][1])

				if distancia < otroObjeto["radio"] + unObjeto["radio"]:

					# Primero se obtiene el angulo de la colision entre dos objetos
					anguloDeColision = math.atan2(unObjeto["posicion"][1] - otroObjeto["posicion"][1], unObjeto["posicion"][0] - otroObjeto["posicion"][0])

					# Luego se calcula la velocidad de cada objeto
					velocidadDeUnObjeto = math.sqrt(unObjeto["velocidad"][0] * unObjeto["velocidad"][0] + unObjeto["velocidad"][1] * unObjeto["velocidad"][1])
					velocidadDelOtroObjeto = math.sqrt(otroObjeto["velocidad"][0] * otroObjeto["velocidad"][0] + otroObjeto["velocidad"][1] * otroObjeto["velocidad"][1])

					# Se trabaja en la direccion de los objetos en radianes
					direccionDeUnObjeto = math.atan2(unObjeto["velocidad"][1], unObjeto["velocidad"][0])
					direccionDelOtroObjeto = math.atan2(otroObjeto["velocidad"][1], otroObjeto["velocidad"][0])

					# Se calcula los nuevos valores X/Y de cada objeto para la colision
					nuevaVelocidadX_deUnObjeto = velocidadDeUnObjeto * math.cos(direccionDeUnObjeto - anguloDeColision)
					nuevaVelocidadY_deUnObjeto = velocidadDeUnObjeto * math.sin(direccionDeUnObjeto - anguloDeColision)

					nuevaVelocidadX_delOtroObjeto = velocidadDelOtroObjeto * math.cos(direccionDelOtroObjeto - anguloDeColision)
					nuevaVelocidadY_delOtroObjeto = velocidadDelOtroObjeto * math.sin(direccionDelOtroObjeto - anguloDeColision)
					
					# Se ajusta la velocidad basada en la masa de los objetos
					velocidadFinalX_deUnObjeto = ((unObjeto["masa"] - otroObjeto["masa"]) * nuevaVelocidadX_deUnObjeto + (otroObjeto["masa"] + otroObjeto["masa"]) * nuevaVelocidadX_delOtroObjeto)/(unObjeto["masa"] + otroObjeto["masa"])
					velocidadFinalX_delOtroObjeto = ((unObjeto["masa"] + unObjeto["masa"]) * nuevaVelocidadX_deUnObjeto + (otroObjeto["masa"] - unObjeto["masa"]) * nuevaVelocidadX_delOtroObjeto)/(unObjeto["masa"] + otroObjeto["masa"])

					# Se establecen los valores
					unObjeto["velocidad"][0] = velocidadFinalX_deUnObjeto
					otroObjeto["velocidad"][0] = velocidadFinalX_delOtroObjeto


			i += 1

		h += 1

def manejarClic():
	global objetoActual

	objetoActual = {
		"radio" : 3,
		"masa" : 3,
		"velocidad" : [0,0],
		"posicion" : [0,0]
	}

def salirDelJuego():
	pygame.quit()
	sys.exit()

# Bucle principal
while True:

	superficieDeDibujo.fill((0,0,0))
	posicionDelRaton = pygame.mouse.get_pos()

	# Eventos generados por el usuario y el sistema 
	for event in EVENTOS_DEL_JUEGO.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:
				salirDelJuego()

		if event.type == pygame.KEYUP:

			if event.key == pygame.K_r:
				objetosAColisionar = []
			if event.key == pygame.K_f:
				if dibujarFuerzaDeAtraccion is True:
					dibujarFuerzaDeAtraccion = False
				elif dibujarFuerzaDeAtraccion is False:
					dibujarFuerzaDeAtraccion = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			botonDeRatonPresionado = True
			manejarClic()

		if event.type == pygame.MOUSEBUTTONUP:
			botonDeRatonPresionado = False

		if event.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
			salirDelJuego()

	calcularMovimiento()
	manejarColisiones()
	dibujarObjetosAColisionar()

	if objetoActual is not None:
		dibujarObjetoActual()

		# Si el usuario ha dejado de presionar el raton, agregar el nuevo objeto en la lista objetosAColisionar
		if botonDeRatonPresionado is False:
			objetoActual["velocidad"][0] = (posicionDelRaton[0] - posicionPreviaDelRaton[0]) / 4
			objetoActual["velocidad"][1] = (posicionDelRaton[1] - posicionPreviaDelRaton[1]) / 4
			objetosAColisionar.append(objetoActual)
			objetoActual = None

	# Almacena las coord previas del raton para crear un vector en el momento de soltar un nuevo objeto
	posicionPreviaDelRaton = posicionDelRaton

	reloj.tick(60)
	pygame.display.update()