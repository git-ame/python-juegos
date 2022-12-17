import pygame
# Inicializacion de la libreria grafica importada
# Estamos listos para usar Pygame
pygame.init()

superficieDeDibujo = pygame.display.set_mode((500, 400))

while True:
	# pygame.draw.rect(superficieDeDibujo, (255, 255, 0), (0, 0, 50, 130))
	# pygame.draw.circle(superficieDeDibujo,(255,0,100), (100, 200), 70, 20)
	pygame.draw.ellipse(superficieDeDibujo, (255,255,0), (150, 100, 200, 50))
	# pygame.draw.lines(superficieDeDibujo, (255, 255, 0),True, ((50, 50),(75, 75),(63, 100),(38, 100)), 2)
	pygame.display.update()