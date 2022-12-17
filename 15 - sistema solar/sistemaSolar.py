import pygame, copy

imagenes = {
	"mercurio" : pygame.image.load("recursos/mercurio.png"),
	"venus" : pygame.image.load("recursos/venus.png"),
	"tierra" : pygame.image.load("recursos/tierra.png"),
	"marte" : pygame.image.load("recursos/marte.png"),
	"jupiter" : pygame.image.load("recursos/jupiter.png"),
	"saturno" : pygame.image.load("recursos/saturno.png"),
	"neptuno" : pygame.image.load("recursos/neptuno.png"),
	"urano" : pygame.image.load("recursos/urano.png"),
}

planetas = [{
	"nombre" : "mercurio",
	"radio" : 15.0,
	"masa" : 0.6,
	"velocidad" : [0,0],
	"posicion" : [0,0]
},
{
	"nombre" : "venus",
	"radio" : 23.0,
	"masa" : 0.95,
	"velocidad" : [0,0],
	"posicion" : [0,0]
},
{
	"nombre" : "tierra",
	"radio" : 24.0,
	"masa" : 1.0,
	"velocidad" : [0,0],
	"posicion" : [0,0]
},
{
	"nombre" : "marte",
	"radio" : 15.0,
	"masa" : 0.4,
	"velocidad" : [0,0],
	"posicion" : [0,0]
},
{
	"nombre" : "jupiter",
	"radio" : 37.0,
	"masa" : 15.0,
	"velocidad" : [0,0],
	"posicion" : [0,0]
},
{
	"nombre" : "saturno",
	"radio" : 30.0,
	"masa" : 4,
	"velocidad" : [0,0],
	"posicion" : [0,0]
},
{
	"nombre" : "neptuno",
	"radio" : 30.0,
	"masa" : 4.2,
	"velocidad" : [0,0],
	"posicion" : [0,0]
},
{
	"nombre" : "urano",
	"radio" : 30.0,
	"masa" : 3.8,
	"velocidad" : [0,0],
	"posicion" : [0,0]
}]

def crearNuevoPlaneta(which):

	for masaPlanetaria in planetas:

		if masaPlanetaria["nombre"] == which:
			return copy.deepcopy(masaPlanetaria)

	return False

