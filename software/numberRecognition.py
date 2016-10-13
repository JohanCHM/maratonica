#!/usr/bin/python
# -*- coding: utf-8 -*-

#--------Librerías--------
import cv2
import numpy as np

class numberRecog():

	def __init__(self, img):
	#self.posx = posx - 205
	#self.posy = posy
		self.img = img

	#def findZone(self):
		#cutImg = self.img[self.posy-100:self.posy+100,self.posx-150:self.posx+150]
		#return cutImg

	def segColor(self,img):

		results = [[0]]
		#Tratamiento de la imagen
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray,(5,5),0)
		myellow = cv2.adaptiveThreshold(blur,255,1,1,11,2)  

		#Contornos distintos
		contours = cv2.findContours(myellow,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[1]
		areas = [cv2.contourArea(c) for c in contours]
		
		k = 0	
		for data in areas:
			if data < 500 and data > 200:
				contourN = contours[k]
				[x,y,w,h] = cv2.boundingRect(contourN)
				if (h > 15 and w > 15) and (h < 40 and w < 40):
					cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
					regNumber = myellow[y:y+h,x:x+w]
					#Segmento de la imagen new Corner para algoritmo 
					regNumAjuste = cv2.resize(regNumber,(20,20))
					regNumAjuste = regNumAjuste.reshape((1,400))
					regNumAjuste = np.float32(regNumAjuste)
					model = self.trainKNN()
					retval, results, neigh_resp, dists = model.findNearest(regNumAjuste, k = 1)
					#cv2.imshow('square',img) 
			k = k + 1
		return int((results[0][0]))

	def trainKNN(self):
		#path = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
		#samples = np.loadtxt('Muestras.txt',np.float32)
		samples = np.loadtxt('Aldea\Muestras.txt',np.float32)
		responses = np.loadtxt('Aldea\Valores.txt',np.float32)
		responses = responses.reshape((responses.size,1))

		model = cv2.ml.KNearest_create()
		model.train(samples,cv2.ml.ROW_SAMPLE,responses)
		return model

	def number(self):
		nI = self.segColor(self.img)
		return nI	

