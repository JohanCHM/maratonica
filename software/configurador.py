import xml.etree.ElementTree as ET
from win32com.shell import shell, shellcon

class Configurador(object):
	"""docstring for Configurador"""

	def __init__(self):
		super(Configurador, self).__init__()
		try:			
			#path = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
			self.archivo = 'data.xml'
			self.LoadXml()
		except:
			print 'Data no encontrada, CERRANDO...'
			import time
			time.sleep(3)
			exit()

	def LoadXml(self):
		self.tree = ET.parse(self.archivo)
		self.root = self.tree.getroot()

	def ReloadXml(self):
		self.root = None
		self.tree = None
		self.LoadXml()

	def GetCarbetos(self):
		#Lista completa de instancias XML : carbeto
		carbetosObj =  self.root.findall('carbeto')
		carbetos = []
		for x in carbetosObj:
			carbetos.append(x.get('name'))
		return carbetos

	def GetCarbeto(self,opcCarbeto):
		#Lista completa de instancias XML : carbeto
		carbetos =  self.root.findall('carbeto')
		for carbeto in carbetos:
			#Instancia XML : carbeto = toolBox :carbeto
			if carbeto.get('name') == opcCarbeto:
				#datos del carro mov : adelante
				adelante = carbeto.find('adelante')
				AmotorA  = adelante.get('motorA')
				AmotorB  = adelante.get('motorB')
				Atime    = adelante.get('time')
				#datos del carro mov : vueltaLeft
				vueltaLeft = carbeto.find('vueltaLeft')
				LmotorA  = vueltaLeft.get('motorA')
				LmotorB  = vueltaLeft.get('motorB')
				Ltime    = vueltaLeft.get('time')
				#datos del carro mov : vueltaRight
				vueltaRight = carbeto.find('vueltaRight')
				RmotorA  = vueltaRight.get('motorA')
				RmotorB  = vueltaRight.get('motorB')
				Rtime    = vueltaRight.get('time')
				return int(carbeto.get('puerto')),int(RmotorA),int(RmotorB),int(Rtime),int(LmotorA),int(LmotorB),int(Ltime),int(AmotorA),int(AmotorB),int(Atime)

	def SetCarbeto(self,opcCarbeto,puerto,
		RmotorA,RmotorB,Rtime,
		LmotorA,LmotorB,Ltime,
		AmotorA,AmotorB,Atime):
		#Lista completa de instancias XML : carbeto
		carbetos =  self.root.findall('carbeto')
		for carbeto in carbetos:
			#Instancia XML : carbeto = toolBox :carbeto
			if carbeto.get('name') == opcCarbeto:
				carbeto.set('puerto',str(puerto))
				#datos del carro mov : adelante
				adelante = carbeto.find('adelante')
				adelante.set('motorA',str(AmotorA))
				adelante.set('motorB',str(AmotorB))
				adelante.set('time',str(Atime))
				#datos del carro mov : vueltaLeft
				vueltaLeft = carbeto.find('vueltaLeft')
				vueltaLeft.set('motorA',str(LmotorA))
				vueltaLeft.set('motorB',str(LmotorB))
				vueltaLeft.set('time',str(Ltime))
				#datos del carro mov : vueltaRight
				vueltaRight = carbeto.find('vueltaRight')
				vueltaRight.set('motorA',str(RmotorA))
				vueltaRight.set('motorB',str(RmotorB))
				vueltaRight.set('time',str(Rtime))
				#ACTUALIZANDO DATOS de opcCarbeto a data.xml
				self.tree.write('data.xml')
				continue

	def GetColor(self):
		#XML : perfil-color
		color =  self.root.find('perfil-color')
		#datos del color : azul
		azul = color.find('azul')
		aH  = azul.get('H')
		aS  = azul.get('S')
		aV  = azul.get('V')
		#datos del color : amarillo
		amarillo = color.find('amarillo')
		yH  = amarillo.get('H')
		yS  = amarillo.get('S')
		yV  = amarillo.get('V')
		#datos del color : naranja
		naranja = color.find('naranja')
		nH  = naranja.get('H')
		nS  = naranja.get('S')
		nV  = naranja.get('V')
		#datos del color : violeta
		violeta = color.find('violeta')
		vH  = violeta.get('H')
		vS  = violeta.get('S')
		vV  = violeta.get('V')
		return int(aH),int(aS),int(aV),int(yH),int(yS),int(yV),int(nH),int(nS),int(nV),int(vH),int(vS),int(vV)

	def GetTablero(self):
		tablero =  self.root.find('tablero')
		#datos del tablero : area
		area = tablero.find('area')
		amax  = area.get('max')
		amin  = area.get('min')
		#datos del tablero : altura
		altura = tablero.find('altura')
		hmax  = altura.get('max')
		hmin  = altura.get('min')
		#datos del tablero : ancho
		ancho = tablero.find('ancho')
		wmax  = ancho.get('max')
		wmin  = ancho.get('min')
		#datos del tablero : filtro
		filtro = tablero.find('filtro')
		val  = filtro.get('val')
		return int(amax),int(amin),int(hmax),int(hmin),int(wmax),int(wmin),int(val)
