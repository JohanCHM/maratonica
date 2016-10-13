#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from ToolVisual import *

class trainNum():

    def __init__(self, img):
        self.img = img

    #Función para almacenar los datos entrenados
    def writeFile(self,fileName,data):
        file = open(fileName,'ab')
        np.savetxt(file,data)
        file.close()

    def trainN(self,areaMin,areaMax,hMin,hMax,wMin,wMax):

        #Tratamiento de la imágen
        gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        thresh = cv2.adaptiveThreshold(blur,255,1,1,11,4) #2
        
        contours = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[1]

        samples =  np.empty((0,400))
        responses = []
        
        #Se le enseña al algoritmo quién es quién
        keys = [i for i in range(48,58)]

        for cnt in contours:
            if cv2.contourArea(cnt) > areaMin and cv2.contourArea(cnt) < areaMax:
            #Se encuadra el objeto
                [x,y,w,h] = cv2.boundingRect(cnt)

                if  (h > hMin and w > wMin) and (h < hMax and w < wMax): #40
                    cv2.rectangle(self.img,(x,y),(x+w,y+h),(0,0,255),2)
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(20,20))
                    cv2.imshow('Elige numero',self.img)
                    key = cv2.waitKey(0)

                    if key == 27:  #ESC para salir
                        sys.exit()
                    elif key in keys:
                        responses.append(int(chr(key)))
                        sample = roismall.reshape((1,400))
                        samples = np.append(samples,sample,0)

        responses = np.array(responses,np.float32)
        responses = responses.reshape((responses.size,1))

        #path = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
        self.writeFile('Aldea\Muestras.txt',samples)
        self.writeFile('Aldea\Valores.txt',responses)

        cv2.destroyAllWindows()