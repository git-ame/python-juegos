import pygame, sys, random, math
import pygame.locals as VARIABLES_GLOBALES_DEL_JUEGO
import pygame.event as EVENTOS_DEL_JUEGO
import pygame.time as TIEMPO_DEL_JUEGO
import sistemaSolar

anchoVentana = 1024
altoVentana = 768

pygame.init()
reloj = pygame.time.Clock()
superficieDeDibujo = pygame.display.set_mode((anchoVentana, altoVentana), pygame.FULLSCREEN)

pygame.display.set_caption('Simulador de Sistema Solar')

posicionPreviaDelRaton = [0,0]
posicionDelRaton = None
botonDeRatonPresionado = False

fondo = pygame.image.load("recursos/fondo.jpg")
logo = pygame.image.load("recursos/logo.png")
pestaniasIU = pygame.image.load("recursos/pestanias.png")
coordenadasIU = [{"nombre" : "mercurio", "coordenadas" : (132,687)}, {"nombre" : "venus", "coordenadas" : (229,687)}, {"nombre" : "tierra", "coordenadas" : (326,687)}, {"nombre" : "marte", "coordenadas" : (423,687)}, {"nombre" : "jupiter", "coordenadas" : (520,687)}, {"nombre" : "saturno", "coordenadas" : (617,687)}, {"nombre" : "neptuno", "coordenadas" : (713,687)}, {"nombre" : "urano", "coordenadas" : (810,687)}]

cuerposCelestes = []
planetaActual = None

dibujarFuerzas = True

gravedad = 6.67

def dibujarInterfaz():
	superficieDeDibujo.blit(pestaniasIU, (131,687))
	superficieDeDibujo.blit(sistemaSolar.imagenes["mercurio"], (158,714))
	superficieDeDibujo.blit(sistemaSolar.imagenes["venus"], (247,706))
	superficieDeDibujo.blit(sistemaSolar.imagenes["tierra"], (344,704))
	superficieDeDibujo.blit(sistemaSolar.imagenes["marte"], (451,714))
	superficieDeDibujo.blit(sistemaSolar.imagenes["jupiter"], (524,692))
	superficieDeDibujo.blit(sistemaSolar.imagenes["saturno"], (620,695))
	superficieDeDibujo.blit(sistemaSolar.imagenes["neptuno"], (724,697))
	superficieDeDibujo.blit(sistemaSolar.imagenes["urano"], (822,697))

def dibujarPlanetas():

	for planeta in cuerposCelestes:
		planeta["posicion"][0] += planeta["velocidad"][0]
		planeta["posicion"][1] += planeta["velocidad"][1]
		superficieDeDibujo.blit(sistemaSolar.imagenes[planeta["nombre"]], (planeta["posicion"][0] - planeta["radio"], planeta["posicion"][1] - planeta["radio"]))

def dibujarPlanetaActual():

	planetaActual["posicion"][0] = posicionDelRaton[0]
	planetaActual["posicion"][1] = posicionDelRaton[1]

	superficieDeDibujo.blit(sistemaSolar.imagenes[planetaActual["nombre"]], (planetaActual["posicion"][0] - planetaActual["radio"], planetaActual["posicion"][1] - planetaActual["radio"]))

def calcularMovimiento():

	for planeta in cuerposCelestes:

		for otroPlaneta in cuerposCelestes:

			if otroPlaneta is not planeta:
				
				direccion = (otroPlaneta["posicion"][0] - planeta["posicion"][0], otroPlaneta["posicion"][1] - planeta["posicion"][1]) # La diferencia en las coord. X, Y de los planetas
				magnitud = math.hypot(otroPlaneta["posicion"][0] - planeta["posicion"][0], otroPlaneta["posicion"][1] - planeta["posicion"][1]) # La distancia entre dos planetas
				direccionNormal = (direccion[0] / magnitud, direccion[1] / magnitud) # Vector normalizado apuntando en la direccion de la fuerza

				# Estableciendo el limite de la fuerza de gravedad
				if magnitud < 5:
					magnitud = 5
				elif magnitud > 30:
					magnitud = 30

				fuerza = ((gravedad * planeta["masa"] * otroPlaneta["masa"]) / (magnitud * magnitud)) # Calculando la fuerza de atraccion

				fuerzaAplicada = (direccionNormal[0] * fuerza, direccionNormal[1] * fuerza)

				otroPlaneta["velocidad"][0] -= fuerzaAplicada[0]
				otroPlaneta["velocidad"][1] -= fuerzaAplicada[1]

				if dibujarFuerzas is True:
					pygame.draw.line(superficieDeDibujo, (255,255,255), (planeta["posicion"][0],planeta["posicion"][1]), (otroPlaneta["posicion"][0],otroPlaneta["posicion"][1]), 1)

def verificarClicEnIU(coordenadas):

	for pestania in coordenadasIU:
		pestaniaX = pestania["coordenadas"][0]

		if coordenadas[0] > pestaniaX and coordenadas[0] < pestaniaX + 82:
			return pestania["nombre"]

	return False

def manejarClic():
	global posicionDelRaton, planetaActual

	if(posicionDelRaton[1] >= 687):
		nuevoPlaneta = verificarClicEnIU(posicionDelRaton)

		if nuevoPlaneta is not False:
			planetaActual = sistemaSolar.crearNuevoPlaneta(nuevoPlaneta)

def salirDelJuego():
	pygame.quit()
	sys.exit()

# Bucle principal
while True:

	posicionDelRaton = pygame.mouse.get_pos()
	superficieDeDibujo.blit(fondo, (0,0))

	# Eventos generados por el usuario y el sistema 
	for event in EVENTOS_DEL_JUEGO.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:
				salirDelJuego()

		if event.type == pygame.KEYUP:

			if event.key == pygame.K_r:
				cuerposCelestes = []
			if event.key == pygame.K_f:
				if dibujarFuerzas is True:
					dibujarFuerzas = False
				elif dibujarFuerzas is False:
					dibujarFuerzas = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			botonDeRatonPresionado = True
			manejarClic()

		if event.type == pygame.MOUSEBUTTONUP:
			botonDeRatonPresionado = False

		if event.type == VARIABLES_GLOBALES_DEL_JUEGO.QUIT:
			salirDelJuego()

	# Dibujar la interfaz: Actualizar el movimiento de los planetas. Dibujar los planetas en sus nuevas posiciones
	dibujarInterfaz()
	calcularMovimiento()
	dibujarPlanetas()

	# Si el usuario ha creado un nuevo planeta, dibujarlo en la ubicacion del raton
	if planetaActual is not None:
		dibujarPlanetaActual()

		# Si el usuario ha dejado de presionar el raton, agregar el nuevo planeta en la lista cuerposCelestes
		if botonDeRatonPresionado is False:
			planetaActual["velocidad"][0] = (posicionDelRaton[0] - posicionPreviaDelRaton[0]) / 4
			planetaActual["velocidad"][1] = (posicionDelRaton[1] - posicionPreviaDelRaton[1]) / 4
			cuerposCelestes.append(planetaActual)
			planetaActual = None

	# Dibuja el logo al principio por 4 segundos
	if TIEMPO_DEL_JUEGO.get_ticks() < 4000:
		superficieDeDibujo.blit(logo, (108,77))

	# Almacena las coord previas del raton para crear un vector en el momento de soltar un nuevo planeta
	posicionPreviaDelRaton = posicionDelRaton

	reloj.tick(60)
	pygame.display.update()