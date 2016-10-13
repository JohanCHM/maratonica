#!/usr/bin/python
# -*- coding: utf-8 -*-

#--------Librerías--------
import cv2
import numpy as np

class findCorners():

	def __init__(self,img):
		self.img = img		

	def findIt(self,tresh,areaMin,areaMax,hMin,hMax,wMin,wMax):
		img = self.img

		cx,cy = [],[]
		wS,hS = [],[]

		if img is not None:
			#Tratamiento de la imagen
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(gray,(5,5),3)
			msquare = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,2)

			#cv2.imshow('',msquare)
			#cv2.waitKey()

			#Contornos distintos
			contours = cv2.findContours(msquare,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[1]
			areas = [cv2.contourArea(c) for c in contours]

			k,ci = 0,0
			for data in areas:
				if data < areaMax and data > areaMin:
					contourN = contours[k]
					[x,y,w,h] = cv2.boundingRect(contourN)

					if (h > hMin and w > wMin) and (h < hMax and w < wMax):
						#Ajuste de la imagen para aplicar algoritmo
						regNumber = msquare[y:y+h,x:x+w] 
						regNumAjuste = cv2.resize(regNumber,(20,20))
						regNumAjuste = regNumAjuste.reshape((1,400))
						regNumAjuste = np.float32(regNumAjuste)
						model = self.trainKNN()
						retval, results, neigh_resp, dists = model.findNearest(regNumAjuste, k = 1)

						if int(results[0][0]) == 1: #Es 1 en lugar de 2
							#Cálculo de los centroides
							cx.append(x)
							cy.append(y)
							wS.append(w)
							hS.append(h)		
							#print h,w,data
				k = k + 1
		return cx,cy,wS,hS

	def trainKNN(self):
		#path = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
		samples = np.loadtxt('Aldea\MuestrasCorner.txt',np.float32)
		responses = np.loadtxt('Aldea\ValoresCorner.txt',np.float32)
		responses = responses.reshape((responses.size,1))

		model = cv2.ml.KNearest_create()
		model.train(samples,cv2.ml.ROW_SAMPLE,responses)
		return model

	def drawSquare(self):
		img = self.img
		cx,cy = self.findIt(img)
		for i in range(len(cx)):	
			cv2.circle(img,(cx[i],cy[i]), 5, (0,0,255), -1)
		cv2.imshow("Imagen",img)

	def cutTable(self,cx,cy,wS,hS):
		img = self.img
		#NOTA: wS y hS cambiarán según la posición final de los recuadros
		x,y = 0,0
		x1,y1 = 0,0
		w1 = 0
		h1 = 0
		newImg = 0
		if len(cx) < 3 and len(cx) > 1:
			x1,y1 = cx[1] + wS[1],cy[1]
			#A partir de aquí es nuevo
			fx,fy = cx[0],cy[0] + hS[0]
			w1 = (fx - x1)
			h1 = (fy - y1)
			#newImg = img[1 + cy[1]-wS[1]:cy[0]+wS[0],1 + cx[1]+hS[1]:cx[0]-hS[0]]
		#return newImg
		#return [[int(x1+w1/40),y1,int(20*w1/42),h1],[int(x1+22*w1/42),y1,int(20*w1/42),h1]]
		return [[int(x1),y1,int(w1/2),h1],[int(x1+w1/2),y1,int(w1/2),h1]]