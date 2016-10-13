#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from ToolVisual import *

class trainCorn(object):

    def __init__(self, img):
        self.img = img

    def writeFile(self,fileName,data):
        file = open(fileName,'ab')
        np.savetxt(file,data)
        file.close()

    def trainC(self,areaMin,areaMax,hMin,hMax,wMin,wMax):
        #Tratamiento de la imágen
        gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),3)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,2) #2

        cv2.imshow('',thresh)
        cv2.waitKey()

        contours = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[1]

        samples =  np.empty((0,400))
        responses = []
        #Se le enseña al algoritmo quién es quién
        keys = [i for i in range(48,50)]	#48 -> 0, 49 -> 1 Este es el comando chido 

        for cnt in contours:
            if cv2.contourArea(cnt) > areaMin and cv2.contourArea(cnt) < areaMax:
        	#Se encuadra el objeto
                [x,y,w,h] = cv2.boundingRect(cnt)

                if  (h > hMin and w > wMin) and (h < hMax and w < wMax): #40
                    #print w,h,cv2.contourArea(cnt)
                    cv2.rectangle(self.img,(x,y),(x+w,y+h),(0,0,255),2)
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(20,20))
        	    #print h,w,cv2.contourArea(cnt)
                    cv2.imshow('Selecciona el logo de CTIN',self.img)
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
        self.writeFile('Aldea\MuestrasCorner.txt',samples)
        self.writeFile('Aldea\ValoresCorner.txt',responses)

        cv2.destroyAllWindows()