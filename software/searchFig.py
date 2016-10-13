#!/usr/bin/python
# -*- coding: utf-8 -*-

#--------Librerías--------
import cv2
import numpy as np
#from ToolVisual import *

class findInstruction():

	def __init__(self, img):
	#self.posx = posx - 205
	#self.posy = posy
		self.img = img

	#def findZone(self):
		#cutImg = self.img[self.posy-100:self.posy+100,self.posx-150:self.posx+150]
		#return cutImg

	def segFig(self):

		areaMin = 400 
		areaMax = 800
		hMin = 15
		hMax = 70
		wMin = 15
		wMax = 70

		value = []
		flag = 0

		img = self.img
		results = [[0]]
		#Tratamiento de la imagen
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray,(5,5),0)
		imgFile = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2) #2

		#Contornos distintos
		contours = cv2.findContours(imgFile,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[1]
		areas = [cv2.contourArea(c) for c in contours]
		
		k = 0	
		for data in areas:
			if data < areaMax and data > areaMin:
				contourN = contours[k]
				[x,y,w,h] = cv2.boundingRect(contourN)
				if (h > hMin and w > wMin) and (h < hMax and w < wMax):

					#print w,h,data

					cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
					regNumber = imgFile[y:y+h,x:x+w]
					#Segmento de la imagen new Corner para algoritmo 
					regNumAjuste = cv2.resize(regNumber,(20,20))
					regNumAjuste = regNumAjuste.reshape((1,400))
					regNumAjuste = np.float32(regNumAjuste)
					model = self.trainKNN()
					retval, results, neigh_resp, dists = model.findNearest(regNumAjuste, k = 1)
					
					aux = int((results[0][0]))

					if aux == 1:
						instruction = 'd'
					elif aux == 2:
						instruction = 'i'
					elif aux == 3:
						instruction = 'a'
					elif aux == 4:
						instruction = 'f'
					else:
						instruction = 'u'
						x = 0
						y = 0

					#if aux == 4:
					#	flag = flag + 1
					#	if flag < 2:
					#		yAnt = y 
					#elif aux != 0:
					#	flag = 0

					#if flag == 2:
					#	print "Hola"
					#	if yAnt - 15 < y:
					#		print 'Aqui: ' + str(yAnt) + ',' + str(y)
					#		flag = 0
					#	else:
					#		value.append([x,y,instruction])
					#		flag = 1
					#else:
					#	value.append([x,y,instruction])

					value.append([x,y,instruction])
			k = k + 1
		return value

	def trainKNN(self):
		#samples = np.loadtxt('Muestras.txt',np.float32)
		#path = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
		samples = np.loadtxt('Aldea\MuestrasFig.txt',np.float32)
		responses = np.loadtxt('Aldea\ValoresFig.txt',np.float32)
		responses = responses.reshape((responses.size,1))

		model = cv2.ml.KNearest_create()
		model.train(samples,cv2.ml.ROW_SAMPLE,responses)
		return model

	def fig(self):
		nI = self.segFig(self.img)
		return nI	

#if __name__ == "__main__":

#cam = cv2.VideoCapture(1)
#img = Foto().TomarFoto(cam = cam)

#nTn = findInstruction(img)	
#nI = nTn.segFig()
#print "El número es: " + str(nI)
