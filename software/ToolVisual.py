# -*- coding: utf-8 -*-
import cv2
import numpy as np
from time import sleep
from numberRecognition import numberRecog
from searchFig import findInstruction

class Foto(object):
	"""docstring for Foto"""

	iteTime = 25

	def __init__(self):
		super(Foto, self).__init__()

	# TomarFoto Retorna la imagen en un arreglo
	'''
	cd : cam device
	cf : cam frames
	res [width,height] : cam resolution '''
	def TomarFoto(self, cd = 0, cf = 30, res = [1024,768], cam = None):

		if cam == None:
			cam = cv2.VideoCapture(cd)

		#cam.set(3,res[0])
		#cam.set(4,res[1])
		
		#for x in xrange(1,self.iteTime):
		#	cam.read()

		tempo, cam_cap = cam.read()
		#del(cam)
		return cam_cap

	# Cortar Retorna la imagen cortada en un arreglo
	'''
	imagen : objeto imagen
	size : [x,y,w,h] '''
	def Cortar(self, imagen, size = [0,0,1,1]):
		#size[y : y + h, x : x + w]
		return imagen[size[1]:size[1]+size[3], size[0]:size[0]+size[2]]

	def Salvar(self, imagen, archivo = "archivo.png"):
		cv2.imwrite(archivo, imagen)

	def ColocarImagen(self, imgDes, imgSrc, x = 0, y = 0, w = 10, h = 10):
		imgSrc = cv2.resize(imgSrc, (w, h), interpolation = cv2.INTER_CUBIC)
		yDes,xDes,_ = imgDes.shape
		if (x+w) <= xDes and (y+h) <= yDes:
			imgDes[y:y+h, x:x+w ] = imgSrc
		return imgDes

	def Calibrar(self, cd = 1, cf = 30, res = [1024,768]): #cd = 0

		cam = cv2.VideoCapture(cd)

		cam.set(3,res[0])
		cam.set(4,res[1])

		cv2.namedWindow('Calibracion')

		while cv2.waitKey(1) == -1:
			cv2.imshow('Calibracion',cam.read()[1])

		cv2.destroyWindow('Calibracion')

class Recursos(object):

	"""docstring for Recursos"""
	def __init__(self,
		SRC_GO = None,
		SRC_TL = None,
		SRC_TR = None,
		SRC_REP = None, default = True):

		super(Recursos, self).__init__()
	
		if default:
			self.CargarDefault()
		else:
			self.SRC_GO = SRC_GO
			self.SRC_TL = SRC_TL
			self.SRC_TR = SRC_TR
			self.SRC_REP = SRC_REP

	def CargarDefault(self):
		self.SRC_GO = cv2.imread("src/imgGo.png")
		self.SRC_TL = cv2.imread("src/imgTL.png")
		self.SRC_TR = cv2.imread("src/imgTR.png")
		self.SRC_REP = cv2.imread("src/imgRep.png")
		

class Tablero(object):
	"""docstring for Tablero"""
	def __init__(self):
		super(Tablero, self).__init__()

	# DetectarVertices Retorna un arreglo [2][x,y,w,h] con los vertices de cada tablero
	'''
	imagen : objeto imagen '''
	def DetectarVertices(self, imagen, wInf = 300, wSup = 500, hInf = 500, hSup = 700, auto = True):
		
		k = 0
		contours = cv2.findContours(imagen.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)[1]

		# DEBUG START bubbleSort contornos
		if auto:
			w = []
			h = []
			s = len(contours)
			for x in xrange(s):
				w.append(None)
				h.append(None)
			for x in xrange(s):
				_,_,w[x],h[x] = cv2.boundingRect(contours[x])

			for x in xrange(s-1,0,-1):
				for y in xrange(x):
					if w[y] < w[y+1]:
						tw = w[y]
						th = h[y]
						w[y] = w[y+1]
						h[y] = h[y+1]
						w[y+1] = tw
						h[y+1] = th
			corte = []
			for i in xrange(s):
				x,y,wi,hi = cv2.boundingRect(contours[i])
				if (wi == w[1] and hi == h[1]) or (wi == w[2] and hi == h[2]):
					if k:
						if x < corte[0]:
							return [x,y,wi,hi],corte
						return corte,[x,y,wi,hi]
					corte = [x,y,wi,hi]
					k = True

		# DEBUG FIN bubbleSort contornos
		else:
			for i in range(len(contours)):
				x,y,w,h = cv2.boundingRect(contours[i])
				#print w,h
				if (w > wInf and w < wSup) and (h > hInf and h < hSup):
					if k:
						return corte,[x,y,w,h]
					corte = [x,y,w,h]
					k += 1


		return [[0,0,1024,768],[0,0,1024,768]]
		#return None

	# DetectarVertices Retorna un arreglo [2][x,y,w,h] con los vertices de cada tablero
	'''
	imagen : objeto imagen '''
	def DetectarComandos(self, imagen):
		h,w = imagen.shape[:2]
		return [int(w*2/6),0,int(w*2/6),h]

	# DetectarVertices Retorna un arreglo [2][x,y,w,h] con los vertices de cada tablero
	'''
	imagen : objeto imagen '''
	def DetectarColumnas(self, imagen):
		h,w = imagen.shape[:2]
		return [0,0,int(w*2/6),h],[int(w*2/6),0,int(w*2/6),h],[int(w*4/6),0,int(w*2/6),h]

	def DibujarComandos(self, tablero, comRAW, comNRec, comPar,
		xIni = 100, yIni = 10,
		wTar = 60, hTar = 30, xSpc = 3, ySpc = 3):

		for x in xrange(len(comRAW)):

			if comRAW[x] == Color().BIT_GO :
				tablero = Foto().ColocarImagen(tablero, Recursos().SRC_GO, xIni, yIni + (hTar + ySpc) * x, wTar, hTar)
				continue
			if comRAW[x] == Color().BIT_TL :
				tablero = Foto().ColocarImagen(tablero, Recursos().SRC_TL, xIni, yIni + (hTar + ySpc) * x, wTar, hTar)
				continue
			if comRAW[x] == Color().BIT_TR :
				tablero = Foto().ColocarImagen(tablero, Recursos().SRC_TR, xIni, yIni + (hTar + ySpc) * x, wTar, hTar)
				continue
			if comRAW[x] == Color().BIT_REP :
				tablero = Foto().ColocarImagen(tablero, Recursos().SRC_REP, xIni, yIni + (hTar + ySpc) * x, wTar, hTar)
				#cv2.rectangle(tablero, (xIni - wTar - xSpc, yIni + ySpc * x ) ,
				#	(xIni - xSpc,yIni + (hTar + ySpc) * x) , (25,150,50) , -1)
				cv2.putText(tablero,
					comNRec[x],
					(xIni - int(wTar*.6) - xSpc, yIni + (hTar + ySpc) * x + int(hTar*.7) ),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,255,255),2,cv2.LINE_AA)
				if comPar[x] == Color().BIT_GO :
					tablero = Foto().ColocarImagen(tablero, Recursos().SRC_GO, xIni+wTar+xSpc, yIni + (hTar + ySpc) * x, wTar, hTar)
				elif comPar[x] == Color().BIT_TL :
					tablero = Foto().ColocarImagen(tablero, Recursos().SRC_TL, xIni+wTar+xSpc, yIni + (hTar + ySpc) * x, wTar, hTar)
				elif comPar[x] == Color().BIT_TR :
					tablero = Foto().ColocarImagen(tablero, Recursos().SRC_TR, xIni+wTar+xSpc, yIni + (hTar + ySpc) * x, wTar, hTar)
				continue
			#cv2.rectangle(tablero, (xIni, yIni + (hTar + ySpc) * x), (wTar, hTar), (255,0,0), 2)
		return tablero

	def GenerarLienzo(self, width = 600, height = 400):
		return np.zeros((height,width,3), np.uint8)

class Tarjeta(object):
	"""docstring for Tarjeta"""

	def __init__(self):
		super(Tarjeta, self).__init__()

	def Promedio (self, fhsv, cx, cy, w, h, factor = 0.3):
		
		offset = int(h * factor)

		h += (cy-offset)
		cy+= offset
		w += (cx-offset)
		cx+= offset

		promedioh = (int(fhsv[cy,cx,0])+int(fhsv[h,cx,0])+int(fhsv[cy,w,0])+int(fhsv[h,w,0])) /4
		promedios = (int(fhsv[cy,cx,1])+int(fhsv[h,cx,1])+int(fhsv[cy,w,1])+int(fhsv[h,w,1])) /4
		promediov = (int(fhsv[cy,cx,2])+int(fhsv[h,cx,2])+int(fhsv[cy,w,2])+int(fhsv[h,w,2])) /4

		return [promedioh,promedios,promediov]

	def segFig(self,img):
		#Colores
		#Izquierda
		lower_left = np.array([Color().COLOR_AMARILLO[0],Color().COLOR_AMARILLO[2],Color().COLOR_AMARILLO[4]])
		upper_left = np.array([Color().COLOR_AMARILLO[1],Color().COLOR_AMARILLO[3],Color().COLOR_AMARILLO[5]])
		#Adelante
		lower_go = np.array([Color().COLOR_AZUL[0],Color().COLOR_AZUL[2],Color().COLOR_AZUL[4]])
		upper_go = np.array([Color().COLOR_AZUL[1],Color().COLOR_AZUL[3],Color().COLOR_AZUL[5]])
		#Derecha		
		lower_right = np.array([Color().COLOR_NARANJA[0],Color().COLOR_NARANJA[2],Color().COLOR_NARANJA[4]]) 
		upper_right = np.array([Color().COLOR_NARANJA[1],Color().COLOR_NARANJA[3],Color().COLOR_NARANJA[5]]) 
		#Repetir
		lower_repeat = np.array([Color().COLOR_VIOLETA[0],Color().COLOR_VIOLETA[2],Color().COLOR_VIOLETA[4]])
		upper_repeat = np.array([Color().COLOR_VIOLETA[1],Color().COLOR_VIOLETA[3],Color().COLOR_VIOLETA[5]])
		
		#Aplicando la máscara
		mleft = cv2.inRange(img,lower_left,upper_left)	
		mgo = cv2.inRange(img,lower_go,upper_go)
		mright = cv2.inRange(img,lower_right,upper_right)
		mrepeat = cv2.inRange(img,lower_repeat,upper_repeat)

		return mleft,mgo,mright,mrepeat

	def Filtrar(self, fCom, fNum, fArg,
		wInfF, wSupF, hInfF, hSupF,
		wTar = 80, hTar = 40, xSpc = 100, ySpc = 10):

		hFcom,wFcom = fCom.shape[:2]
		cv2.rectangle(fCom, (0, 0), (wFcom, hFcom), (0,0,0), 10)

		wInf=int(wInfF*wFcom)
		wSup=int(wSupF*wFcom)
		hInf=int(hInfF*hFcom/8)
		hSup=int(hSupF*hFcom/8)

		#Buscando instrucción por forma
		self.nTn = findInstruction(fCom)	
		nT = self.nTn.segFig()
		#print nT

		#HSVcom = cv2.cvtColor(fCom, cv2.COLOR_BGR2HSV)
		#HSVarg = cv2.cvtColor(fArg, cv2.COLOR_BGR2HSV)

		#Segmentación de la figura
		#[mleft,mgo,mright,mrepeat] = self.segFig(HSVcom)

		#Se agrega filtro Close/Open
		#[mleft,mgo,mright,mrepeat] = self.COFilter(mleft,mgo,mright,mrepeat,wM,hM)    

		#-----Imagen con las instrucciones detectadas-----
		#cv2.imshow("Instrucciones detectadas",mleft+mgo+mright+mrepeat)
		#cv2.waitKey(0)

		#Centroides
		#cleft = self.detectCentroid(mleft,Color().BIT_TL, wInf, wSup, hInf, hSup)
		#cgo = self.detectCentroid(mgo,Color().BIT_GO, wInf, wSup, hInf, hSup)
		#cright = self.detectCentroid(mright,Color().BIT_TR, wInf, wSup, hInf, hSup)
		#crepeat = self.detectCentroid(mrepeat,Color().BIT_REP, wInf, wSup, hInf, hSup)

		#Número de elementos
		#nTotal = len(cleft) + len(cgo) + len(cright) + len(crepeat)
		#squarePos = [cleft,cgo,cright,crepeat]
		#auxVector = [0]*nTotal	
		
		#k = 0
		#for i in range(4):
		#	for j in range(len(squarePos[i])):
		#		auxVector[k] = squarePos[i][j]
		#		k += 1

		#Se ordena el vector
		vectInst = nT[::-1]
		#print "----"
		#print vectInst
		#print "----"
		nTotal = len(vectInst)

		#Tamaño de la ventana
		wy = (hSup + hInf)/2
		comando = ""
		comRAW = ""
		comOrg = Tablero().GenerarLienzo()
		comNRec = ""
		comPar = ""

		wxNum = fNum.shape[1]
		wxArg = fArg.shape[1]
		wxCom = fCom.shape[1]

		for n in range(nTotal):
			#Posiciones
			sy = vectInst[n][1] - wy/2
			#print sy
			if sy < 0:
				sy = 1
			
			if vectInst[n][2] == Color().BIT_REP:
			#Aqui mando a pedir el numero

				self.nRg = numberRecog(Foto().Cortar(fNum,[1,sy,wxNum,int(1.5*wy)]))	
				#cv2.imshow('',Foto().Cortar(fNum,[1,sy,wxArg,2*wy]))
				#cv2.waitKey()
				nI = self.nRg.number()
				#print "El número es: " + str(nI)

				if nI == 0:
					continue
					pass

				comNRec += str(nI)

				self.nValue = findInstruction(Foto().Cortar(fArg,[1,sy,wxArg,int(1.5*wy)]))
				m = self.nValue.segFig()
				#cv2.imshow('',Foto().Cortar(fArg,[1,sy,wxArg,wy]))
				#cv2.waitKey()
				if m == []:
					parametro = 'u'
				else:
					parametro = m[0][2]

				comPar += parametro
				for m in range(nI):
					#cv2.imshow('',Foto().Cortar(fArg,[int(wxArg*0.1),sy,int(wxArg*0.7),wy]))
					#cv2.waitKey()
					comando += parametro.upper()
			else:
				comando += vectInst[n][2]
				comNRec += "1"
				comPar += "u"
				
			comRAW += vectInst[n][2]
			Foto().ColocarImagen(comOrg,cv2.resize(Foto().Cortar(fCom,[1,sy,wxCom,wy]),(wTar,hTar),interpolation = cv2.INTER_CUBIC),xSpc, (hTar + ySpc) * n, wTar, hTar)

		#print comando

		return comando,comRAW,comOrg,comNRec,comPar

	def detectCentroid(self,img,instruction, wInf, wSup, hInf, hSup):
		contours = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[1]
		c = []
		
		for cnt in contours:
			#Areas = cv2.contourArea(cnt)
			#if Areas > 1000 and Areas < 3000:
			#Se encuadra el objeto
			[x,y,w,h] = cv2.boundingRect(cnt)
			if  (h > hInf and w > wInf) and (h <= hSup and w <= wSup):
				#print cv2.contourArea(cnt)
				c.append([x + w/2,y + h/2,instruction])   
		
		return c

	def COFilter(self,left,go,right,repeat,wM,hM):
		
		kernel = np.ones((hM,wM),np.uint8)

		left = cv2.morphologyEx(left,cv2.MORPH_CLOSE,kernel)
		left = cv2.morphologyEx(left,cv2.MORPH_OPEN,kernel)   

		go = cv2.morphologyEx(go,cv2.MORPH_CLOSE,kernel)
		go = cv2.morphologyEx(go,cv2.MORPH_OPEN,kernel)

		right = cv2.morphologyEx(right,cv2.MORPH_CLOSE,kernel)
		right = cv2.morphologyEx(right,cv2.MORPH_OPEN,kernel)

		repeat = cv2.morphologyEx(repeat,cv2.MORPH_CLOSE,kernel)
		repeat = cv2.morphologyEx(repeat,cv2.MORPH_OPEN,kernel)

		return left,go,right,repeat
		
class Color(object):
	"""docstring for Color"""

	gx = 0
	gy = 0
	clicked = False

	# COLOR_NAME = [minH, maxH, minS, maxS, minV, maxV]
	#COLOR_AZUL =     [75, 130, 53, 113, 68, 128],
	#COLOR_AMARILLO = [22, 30, 78, 138, 145, 205],
	#COLOR_NARANJA =  [0, 22, 105, 165, 145, 205],
	#COLOR_VIOLETA =  [131, 160, 47, 107, 75, 135],
	
	def __init__(self,
		COLOR_AZUL =     [50, 130, 30, 150, 68, 128],
		COLOR_AMARILLO = [22, 45, 60, 145, 125, 205],
		COLOR_NARANJA =  [0, 22, 80, 200, 145, 215],
		COLOR_VIOLETA =  [131, 180, 30, 120, 75, 135],
		COLOR_UNKNOWN =  [0,0,0,0,0,0],
		BIT_GO = 'a',
		BIT_TL = 'i',
		BIT_TR = 'd',
		BIT_REP = 'f',
		BIT_UNKNOWN = 'u'):

		super(Color, self).__init__()

		self.COLOR_AZUL = COLOR_AZUL
		self.COLOR_AMARILLO = COLOR_AMARILLO
		self.COLOR_NARANJA = COLOR_NARANJA
		self.COLOR_VIOLETA = COLOR_VIOLETA
		self.BIT_GO = BIT_GO
		self.BIT_TL = BIT_TL
		self.BIT_TR = BIT_TR
		self.BIT_REP = BIT_REP
		self.BIT_UNKNOWN = BIT_UNKNOWN
		
	def IsColor (self, color, (minH, maxH, minS, maxS, minV, maxV)):
		if color[0] > minH and color[0] < maxH:
			if color[1] > minS and color[1] < maxS:
				if color[2] > minV and color[2] < maxV:
					return True
		return False

	def DetectarColor(self,HSV,x,y,w,h):

		color = Tarjeta().Promedio(HSV,x,y,w,h)

		if self.IsColor(color,self.COLOR_AZUL):
			return self.BIT_GO
		if self.IsColor(color,self.COLOR_AMARILLO):
			return self.BIT_TL
		if self.IsColor(color,self.COLOR_NARANJA):
			return self.BIT_TR
		if self.IsColor(color,self.COLOR_VIOLETA):
			return self.BIT_REP
		return self.BIT_UNKNOWN

	def CalibrarColor(self,imagen,color,H,S,V,desfase=1):

		self.gx
		self.gy
		self.clicked

		HSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
		cv2.namedWindow('Calibrar Color')
		cv2.setMouseCallback('Calibrar Color',self.onMouse)

		while (cv2.waitKey(1) == -1 and not self.clicked):
			cv2.imshow('Calibrar Color', imagen)

		cv2.destroyAllWindows()

		#Promedio H
		c = int(HSV[self.gy+desfase,self.gx+desfase,0])+int(HSV[self.gy-desfase,self.gx+desfase,0])+int(HSV[self.gy+desfase,self.gx-desfase,0])+int(HSV[self.gy-desfase,self.gx-desfase,0])
		c /= 4
		color[0] = c - H
		if color[0] < 0:
			color[0] = 0
		color[1] = c + H
		if color[1] > 180:
			color[1] = 180

		#Promedio S
		c = int(HSV[self.gy+desfase,self.gx+desfase,1])+int(HSV[self.gy-desfase,self.gx+desfase,1])+int(HSV[self.gy+desfase,self.gx-desfase,1])+int(HSV[self.gy-desfase,self.gx-desfase,1])
		c /= 4
		color[2] = c - S
		if color[2] < 0:
			color[2] = 0
		color[3] = c + S
		if color[3] > 255:
			color[3] = 255

		#Promedio V
		c = int(HSV[self.gy+desfase,self.gx+desfase,2])+int(HSV[self.gy-desfase,self.gx+desfase,2])+int(HSV[self.gy+desfase,self.gx-desfase,2])+int(HSV[self.gy-desfase,self.gx-desfase,2])
		c /= 4
		color[4] = c - V
		if color[4] < 0:
			color[4] = 0
 		color[5] = c + V
 		if color[5] > 255:
 			color[5] = 255

		print color

	def onMouse(self, event, x, y, flags, param):
		self.clicked
		self.gx
		self.gy

		if event == cv2.EVENT_LBUTTONUP:
			self.clicked = True
			self.gx = x
			self.gy = y

class Debugueando(Exception):
	def __init__(self, valor):
		self.valor = valor
	def __str__(self):
		return repr(self.valor)
		