class Imperial_1965():

  color = ['blanco','rojo','negro','beige']
  convertible = False

  def controlarMotor(self, acelerador, freno, embriague, caja):
    self.acelerador = True
    self.freno = False
    self.embriague = False
    self.caja = [0, 1, 2, 3, 4, 5]

    if self.convertible is not True:
      self.caja = [0, 1, 2, 3, 4, 5]
    else:
      self.caja = [0, 1, 2, 3, 4]

  def controlarPuerta(self, seguro, manubrio, vidrios):
    self.seguro = False
    self.manubrio = True
    self.vidrios = 9

    if self.convertible is not True:
      self.vidrios = 9 

  def __init__(self, x):
    self.x = x