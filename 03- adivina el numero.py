#JUEGO de adivina el numero
import random

intentosRealizados = 0

print ('Hola! Como te llamas')
miNomnbre=input()

numero=random.randint(1, 20)
print('Bueno ' + miNomnbre +', estoy pensando en numero del 1 al 20.')

while intentosRealizados < 6:
	print('Intenta adivinar')
	estimacion = input()
	estimacion = int(estimacion)

	intentosRealizados = intentosRealizados + 1

	if estimacion < numero:
		print('tu estimacion es muy baja')

	if estimacion > numero:
		print('tu estimacion es muy alta')

	if estimacion == numero:
		break

if estimacion == numero:
	intentosRealizados = str(intentosRealizados)
	print('Buen trabajo ' + miNomnbre +' !Has adivinado, el numero ' + intentosRealizados + 'intentos')

if estimacion != numero:
	numero = str(numero)
	print('Pues no. El numero que estaba pensando era '+ numero)