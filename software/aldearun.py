# -*- coding: utf-8 -*-

#Librerias a utilizar
import sys
import cv2
import serial
import os
import random as r
from PyQt4 import QtCore, QtGui, uic
from PyQt4.phonon import Phonon
from ToolVisual import *
from findCorners import *
from train import trainNum 
from trainPatron import trainCorn
from configurador import *

import threading
from PyQt4.QtCore import QThread
import time

#Programa principal
class MainConfig(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # Se monta la interfaz de usuario para la configuracion
        self.conf = uic.loadUi("Pantallas/config_v1.1.ui")

class PantallaVideo(QtGui.QWidget):
    def __init__(self):
         QtGui.QWidget.__init__(self)
         # Se monta la interfaz de usuario para los videos
         self.vidi = uic.loadUi("Pantallas/videon.ui")

class PantallaImagen(QtGui.QWidget):
    def __init__(self):
         QtGui.QWidget.__init__(self)
         # Se monta la interfaz de usuario para las imagenes
         self.imag = uic.loadUi("Pantallas/imagen.ui")

class MainWindowC(QtGui.QMainWindow):
        res = [1024,768]
        screen = []
        panimag = []
        panvidi = []
        con = []
        pantalla = []
        imagen = []
        respuesta = []
        bandera=0
        pathvideos='Videos/'
        pathobst='Obs/'
        pro=[]
        #self.comandos = ""
        def __init__(self):
             QtGui.QMainWindow.__init__(self)
             #self.threads = list()

             self.imagen = 'src/logo_ctin.png'
             screen = QtGui.QDesktopWidget().screenGeometry()
             # Se monta la interfaz de usuario para la pantalla principal
             self.ui = uic.loadUi("Pantallas/aldea_v1.1.ui")
             size = self.ui.geometry()

             self.ui.setWindowFlags(self.ui.windowFlags() | QtCore.Qt.CustomizeWindowHint)
             self.ui.setWindowFlags(QtCore.Qt.FramelessWindowHint)
             self.ui.setWindowFlags(self.ui.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

             self.ui.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)
             self.ui.show()

             #Se crean las pantallas extras(configuracion,imagen,video)
             self.screen = QtGui.QDesktopWidget().screenGeometry()
             self.con=MainConfig()
             self.panimag=PantallaImagen()
             self.panvidi=PantallaVideo()
             
             self.Reset()
             self.panimag.imag.move(self.screen.width(),self.screen.height() - 1)
             self.panvidi.vidi.move(self.screen.width(),self.screen.height() - 1)
             self.Reset()
             # Tomamos el dispositivo de captura a partir de la webcam.
             self.cam = cv2.VideoCapture(1)

             self.cam.set(3,self.res[0])
             self.cam.set(4,self.res[1])
             tempo, cam_cap = self.cam.read()
             # Creamos un temporizador para que cuando se cumpla el tiempo limite tome una captura desde la webcam.
             self.timer = QtCore.QTimer(self.ui)
             # Conectamos la senal timeout() que emite nuestro temporizador con la funcion Show_Frame().
             self.ui.connect(self.timer, QtCore.SIGNAL('timeout()'), self.Show_Frame)
             # Tomamos una captura cada 1 mili-segundo.
             self.timer.start(1);

             #Se conectan las entradas de la interfaz con su respectiva accion
             self.ui.Nivel.currentIndexChanged.connect(self.NivelSelec)
             self.ui.chkTerminal.stateChanged.connect(self.EstadoTerminal)
             #Botón restart puerto 
             self.ui.butPort.stateChanged.connect(self.checkPort)

             self.ui.chkTerminal.stateChanged.connect(self.EstadoTerminal)
             self.ui.chkComandos.stateChanged.connect(self.EstadoComandos)
             self.con.conf.PortCam.currentIndexChanged.connect(self.Camera)
             self.con.conf.camBoton.clicked.connect(self.CameraPortFinder)
             self.con.conf.trainNumber.clicked.connect(self.trainningNumber)
             self.con.conf.trainCorner.clicked.connect(self.trainningCorner)

             # cargando configuracion
             self.flagVisor = False
             self.ui.botVisor.clicked.connect(self.CambiarVisor)


             self.ser = None
             self.CameraPortFinder()
             self.data_config = Configurador()
             #self.LoadColorProfile()
             self.con.conf.Carbeto.clear()
             carbetos = self.data_config.GetCarbetos()
             for elemento in carbetos:
                self.con.conf.Carbeto.addItem(elemento)
             self.LoadCarbeto()
             self.con.conf.Carbeto.currentIndexChanged.connect(self.LoadCarbeto)
             self.con.conf.bluBoton.clicked.connect(self.ReloadCarbeto)
             self.con.conf.botReloadTablero.clicked.connect(self.ReloadTarjeta)
             self.con.conf.botReloadImagen.clicked.connect(self.ReloadImagen)
             self.con.conf.botSaveCarro.clicked.connect(self.SaveCarbeto)
             self.ReloadTarjeta()
             self.ReloadImagen()
             # cargando configuracion END

             self.ui.Refresh.clicked.connect(self.Reset)
             self.ui.botReloadCam.clicked.connect(self.ResetCam)
             self.ui.Ver.clicked.connect(self.Verlo)
             self.ui.Reproducir.clicked.connect(self.Play)
             self.ui.Foto.clicked.connect(self.AnalizarFoto)
             self.ui.Programar.clicked.connect(self.Programar)
             self.ui.Configuracion.clicked.connect(self.AbrirConf)
             self.ui.Evaluar.clicked.connect(self.Evaluar)
             self.ui.botClose.clicked.connect(self.Salir)
             self.ui.botMinimize.clicked.connect(self.Minimizar)

             self.ui.txtComandos.textChanged.connect(self.RefreshComandos)

        def CambiarVisor(self):
            self.flagVisor = not self.flagVisor
            print 'apretado'

        def LoadCarbeto(self):
            p,rma,rmb,rt,lma,lmb,lt,ama,amb,at = self.data_config.GetCarbeto(self.con.conf.Carbeto.currentText())
            self.con.conf.bluePort.setValue(p)
            self.con.conf.aMotorRight.setValue(rma)
            self.con.conf.bMotorRight.setValue(rmb)
            self.con.conf.aMotorLeft.setValue(lma)
            self.con.conf.bMotorLeft.setValue(lmb)
            self.con.conf.aMotorGo.setValue(ama)
            self.con.conf.bMotorGo.setValue(amb)
            self.con.conf.timeRight.setValue(rt)
            self.con.conf.timeLeft.setValue(lt)
            self.con.conf.timeGo.setValue(at)
            self.ui.labPuerto.setText('COM' + str(p))
            self.ui.labDevice.setText(self.con.conf.Carbeto.currentText())

        def ReloadCarbeto(self):
            self.data_config.ReloadXml()
            self.con.conf.Carbeto.currentIndexChanged.emit(0)

        def SaveCarbeto(self):
            #Lectura de los parámetros
            self.data_config.SetCarbeto(self.con.conf.Carbeto.currentText(),
                self.con.conf.bluePort.value(),
                self.con.conf.aMotorRight.value(),
                self.con.conf.bMotorRight.value(),
                self.con.conf.timeRight.value(),
                self.con.conf.aMotorLeft.value(),
                self.con.conf.bMotorLeft.value(),
                self.con.conf.timeLeft.value(),
                self.con.conf.aMotorGo.value(),
                self.con.conf.bMotorGo.value(),
                self.con.conf.timeGo.value())

        def LoadColorProfile(self):
            aH,aS,aV,yH,yS,yV,nH,nS,nV,vH,vS,vV = self.data_config.GetColor()
            Color().CalibrarColor(foto,Color().COLOR_AZUL,H=aH,S=aS,V=aV)
            Color().CalibrarColor(foto,Color().COLOR_AMARILLO,H=yH,S=yS,V=yV)
            Color().CalibrarColor(foto,Color().COLOR_NARANJA,H=nH,S=nS,V=nV)
            Color().CalibrarColor(foto,Color().COLOR_VIOLETA,H=vH,S=vS,V=vV)

        def Minimizar(self):
            self.ui.showMinimized()

        def Salir(self):
            app.quit()

        def Programar(self):

            self.ui.Programar.setEnabled(False)

            try:
                #x = 80
                #y = 300
                #font = cv2.FONT_HERSHEY_SIMPLEX
                #foto = self.comandosParaEnviar
                #cv2.putText(foto,'Enviando...',(x,y), font, .8,(255,255,255),2,cv2.LINE_AA)
                #image = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)
                #pixmap = QtGui.QPixmap()
                #pixmap.convertFromImage(image.rgbSwapped())
                #pix1= pixmap.scaled(self.ui.Camara.width(), self.ui.Camara.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                #self.ui.Camara.setPixmap(pix1)

      
                self.ser.write(str(self.ui.txtCmd.toPlainText()))
                print str(self.ui.txtCmd.toPlainText())
                #self.ser.close()

                #foto = self.comandosParaEnviar
                #cv2.putText(foto,'Enviado...EXITOSO',(x,y), font, .8,(255,255,255),2,cv2.LINE_AA)
                #image = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)
                #pixmap = QtGui.QPixmap()
                #pixmap.convertFromImage(image.rgbSwapped())
                #pix1= pixmap.scaled(self.ui.Camara.width(), self.ui.Camara.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                #self.ui.Camara.setPixmap(pix1)
                '''
                if puerto != "":
                    if self.ser.isOpen:
                        self.ser.close()
                    print 'hola'
                    self.ser = serial.Serial(puerto,9600)
                    print 'adios'
                    #Derecha/izquierda/adelante/m1/m2/time
                    trama = "s80,80,81,80,80,80,1000,1110,1050dididiF"
                    print trama
                    self.ser.write(trama)
                    #self.ser.write(str(self.ui.txtCmd.toPlainText()))
                    self.ser.close()
                '''
            except Exception, e:
                    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', u"""Imposible enviar instrucciones al carro.""",QtGui.QMessageBox.Ok)
                    msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                    msgBox.exec_()

            self.ui.Programar.setEnabled(True)

        def EstadoTerminal(self):
            if self.ui.chkTerminal.isChecked():
                self.ui.txtCmd.setEnabled(True)
            else:
                self.ui.txtCmd.setEnabled(False)

        def EstadoComandos(self):
            if self.ui.chkComandos.isChecked():
                self.ui.txtComandos.setEnabled(True)
            else:
                self.ui.txtComandos.setEnabled(False)

        def updateColorH(self):
            self.con.conf.Hvalue.setText(str(self.con.conf.H.value()))

        def updateColorS(self):
            self.con.conf.Svalue.setText(str(self.con.conf.S.value()))

        def updateColorV(self):
            self.con.conf.Vvalue.setText(str(self.con.conf.V.value()))

        def trainningNumber(self):
            #Parámetros de corte
            areaMin = self.con.conf.areaMinNum.value()
            areaMax = self.con.conf.areaMaxNum.value()
            hMin = self.con.conf.hMinNum.value()
            hMax = self.con.conf.hMaxNum.value()
            wMin = self.con.conf.wMinNum.value()
            wMax = self.con.conf.wMaxNum.value()
             
            img = Foto().TomarFoto(cam = self.cam)
            #img = cv2.imread("test.png")
            
            if img is not None:
                trainningNum = trainNum(img)
                trainningNum.trainN(areaMin,areaMax,hMin,hMax,wMin,wMax)

                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Information, 'Listo', u"""Entrenamiento finalizado.""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()

            else:
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', u"""Imagen no válida.\nCámara no localizada.""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()               

        def trainningCorner(self):
            #Parámetros de corte
            areaMin = self.con.conf.areaMinTab.value()
            areaMax = self.con.conf.areaMaxTab.value()
            hMin = self.con.conf.hMinTab.value()
            hMax = self.con.conf.hMaxTab.value()
            wMin = self.con.conf.wMinTab.value()
            wMax = self.con.conf.wMaxTab.value()

            #img = cv2.imread("test.png")
            img = Foto().TomarFoto(cam = self.cam)
            
            if img is not None:
                trainningNum = trainCorn(img)
                trainningNum.trainC(areaMin,areaMax,hMin,hMax,wMin,wMax) 
                
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Information, 'Listo', u"""Entrenamiento finalizado.""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()

            else:
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', u"""Imagen no válida.\nCámara no localizada.""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()

        def checkPort(self):
            try:
                puerto = 'COM' + str(self.con.conf.bluePort.value())

                if self.ui.butPort.isChecked():
                    if self.ser == None or not self.ser.isOpen():
                        self.ser = serial.Serial(puerto,9600)
                        self.ui.Foto.setEnabled(True)
                        self.ui.Programar.setEnabled(True)
                else:
                    if self.ser.isOpen():
                        self.ser.close()
                        self.ui.Foto.setEnabled(False)
                        self.ui.Programar.setEnabled(False)
            except Exception, e:
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', u"""Error configurando puerto.\nEs culpa de Marcial. No de Ulises""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()

        def ColorSelect(self):

            foto = self.cam.read()[1]
            #foto = cv2.imread("test.png")

            if foto is not None:

                color = self.con.conf.Color.currentIndex()
                if color == 0:
                    Color().CalibrarColor(foto,Color().COLOR_AZUL,
                        H=self.con.conf.H.value(),
                        S=self.con.conf.S.value(),
                        V=self.con.conf.V.value())
                elif color == 1:
                    Color().CalibrarColor(foto,Color().COLOR_AMARILLO,
                        H=self.con.conf.H.value(),
                        S=self.con.conf.S.value(),
                        V=self.con.conf.V.value())
                elif color == 2:
                    Color().CalibrarColor(foto,Color().COLOR_NARANJA,
                        H=self.con.conf.H.value(),
                        S=self.con.conf.S.value(),
                        V=self.con.conf.V.value())
                else:
                    Color().CalibrarColor(foto,Color().COLOR_VIOLETA,
                        H=self.con.conf.H.value(),
                        S=self.con.conf.S.value(),
                        V=self.con.conf.V.value())
                
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Information, 'Listo', u"""Color actualizado.""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()
            
            else:
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', u"""Imagen no válida.\nCámara no localizada.""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()

        def Camera(self):
            del(self.cam)
            self.bandera = 0
            index=self.con.conf.PortCam.currentIndex()
            self.cam = cv2.VideoCapture(index)
            self.cam.set(3,self.res[0])
            self.cam.set(4,self.res[1])

        def ReloadTarjeta(self):
            #Parámetros de corte
            self.areaMin = self.con.conf.areaMin.value()
            self.areaMax = self.con.conf.areaMax.value()
            self.hMin = self.con.conf.hMin.value()
            self.hMax = self.con.conf.hMax.value()
            self.wMin = self.con.conf.wMin.value()
            self.wMax = self.con.conf.wMax.value()
            self.tresh = self.con.conf.threshDetect.value()

        def ReloadImagen(self):
            #Parámetros de corte
            self.wInfF = self.con.conf.wInf.value()
            self.wSupF = self.con.conf.wSup.value()
            self.hInfF = self.con.conf.hInf.value()
            self.hSupF = self.con.conf.hSup.value()

        def AnalizarFoto(self):
            self.ConfigurarAnalizador()
            time.sleep(1)
            self.Fotografia()
            #t = threading.Thread(target=self.Fotografia)
            #self.threads.append(t)
            #t.start()

        def ConfigurarAnalizador(self):
            self.bandera = 1
            pixmap = QtGui.QPixmap('src/imgAnalizandoFoto.png')
            self.ui.Camara.setPixmap(pixmap)

        def Fotografia(self):

            try:

                #self.ser.write('g')
                foto = Foto().TomarFoto(cam = self.cam)
                image = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(image.rgbSwapped())
                pix1= pixmap.scaled(self.ui.Camara.width(), self.ui.Camara.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                
                self.panimag.imag.pantalla1.setPixmap(pix1)
                
                vertices = findCorners(foto).findIt(self.tresh,self.areaMin,self.areaMax,self.hMin,self.hMax,self.wMin,self.wMax)
                vertices = findCorners(foto).cutTable(vertices[0],vertices[1],vertices[2],vertices[3])    


                if vertices != [[0, 0, 0, 0], [0, 0, 0, 0]]:

                    tablero =  Foto().Cortar(foto,vertices[0])
                    vNum,vCom,vArg = Tablero().DetectarColumnas(tablero)

                    tCom = Foto().Cortar(tablero,vCom)
                    tNum = Foto().Cortar(tablero,vNum)
                    tArg = Foto().Cortar(tablero,vArg)

                    comandos,comRAW,comOrg,comNRec,comPar = Tarjeta().Filtrar(tCom,tNum,tArg,
                        self.wInfF,
                        self.wSupF,
                        self.hInfF,
                        self.hSupF)

                    tablero =  Foto().Cortar(foto,vertices[1])
                    vNum,vCom,vArg = Tablero().DetectarColumnas(tablero)

                    tCom = Foto().Cortar(tablero,vCom)
                    tNum = Foto().Cortar(tablero,vNum)
                    tArg = Foto().Cortar(tablero,vArg)

                    com,comR,comO,comNR,comP = Tarjeta().Filtrar(tCom,tNum,tArg,
                        self.wInfF,
                        self.wSupF,
                        self.hInfF,
                        self.hSupF)

                    comandos += com

                    lienzo = Tablero().GenerarLienzo()
                    #print "Comandos: " + comandos
                    Tablero().DibujarComandos(lienzo,comRAW,comNRec,comPar,xIni = 100)
                    Tablero().DibujarComandos(lienzo,comR,comNR,comP,xIni = 400)

                    self.comandos = comandos

                    foto = lienzo
                    self.comandosParaEnviar = foto
                    image = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap()
                    pixmap.convertFromImage(image.rgbSwapped())
                    pix1= pixmap.scaled(self.ui.Camara.width(), self.ui.Camara.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    self.bandera = 1
                    self.ui.Camara.setPixmap(pix1)
                    self.panimag.imag.pantalla1.setPixmap(pix1)

                    self.ui.txtComandos.setText(self.comandos)
                    
                else:
                    self.ResetCam()
                    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', u"""No se localizaron los puntos de referencia del tablero.""",QtGui.QMessageBox.Ok)
                    msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                    msgBox.exec_()


            except Exception as e:
                self.ResetCam()
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', str(e),QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()



            '''
            if foto is not None:



        
            else:
                self.ResetCam()
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', u"""Imagen no válida.\nCámara no localizada.""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()
            
            '''
            #self.ui.imgAnalizando.setVisible(False)
            #self.ui.Foto.setEnabled(True)

        def RefreshComandos(self):
            # TRAMA
            self.trama = "s" + str(self.con.conf.aMotorRight.value()) + ',' + str(self.con.conf.aMotorLeft.value()) + ',' + str(self.con.conf.aMotorGo.value()) + ',' + str(self.con.conf.bMotorRight.value()) + ',' + str(self.con.conf.bMotorLeft.value()) + ',' + str(self.con.conf.bMotorGo.value()) + ',' + str(self.con.conf.timeGo.value()) + ',' + str(self.con.conf.timeLeft.value()) + ',' + str(self.con.conf.timeRight.value()) + ',2000' + self.ui.txtComandos.toPlainText() + "F"
            self.ui.txtCmd.setText(self.trama)
                

        def ResetCam(self):
            self.bandera = 0

        def Reset(self):

            self.flagVisor = False
            self.bandera = 0
            self.panimag.imag.close()
            self.panvidi.vidi.close()
            self.ui.Nivel.setCurrentIndex(0)
            pixmap = QtGui.QPixmap('src/logo_ctin.png')
            self.panimag.imag.pantalla1.setPixmap(pixmap)
            self.panimag.imag.showFullScreen()
            self.ui.Obstaculos.setPixmap(pixmap)
            #self.ui.show()

        def Play(self):
            try:
                self.bandera = 0
                self.ui.videoPlayer.play(Phonon.MediaSource(self.pantalla))
                self.panimag.imag.close()
                self.panvidi.vidi.pantalla2.play(Phonon.MediaSource(self.pantalla))
                self.panvidi.vidi.showFullScreen()
            except Exception,e:                
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, 'Error', u"""No puede reproducirse el video.\nSeleccione un nivel.""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()

        def Verlo(self):
            try:
                self.bandera = 0
                self.panvidi.vidi.close()
                pixmap = QtGui.QPixmap(self.imagen)
                if self.imagen != 'src/logo_ctin.png':
                    pixmap = pixmap.scaledToHeight(self.panimag.imag.pantalla1.height())
                self.panimag.imag.pantalla1.setPixmap(pixmap)
                self.panimag.imag.showFullScreen()
            except Exception,e:
                msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Information, ' ', """Completed""",QtGui.QMessageBox.Ok)
                msgBox.setWindowIcon(QtGui.QIcon('Pantallas/mensajeIcon.png'))   
                msgBox.exec_()               

        def CameraPortFinder(self):
            self.con.conf.PortCam.clear()
            self.con.conf.PortCam.setEnabled(True)
            for x in xrange(0,5):
                try:
                    if len(cv2.VideoCapture(x).read()[1]):
                        self.con.conf.PortCam.addItem(str(x))
                except:
                    pass
            if self.con.conf.PortCam.count():
                return
            self.con.conf.PortCam.setEnabled(False)

        def AbrirConf(self):
            screen = QtGui.QDesktopWidget().screenGeometry()
            self.con.conf.show()
            size = self.con.conf.geometry()
            self.con.conf.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

        def Show_Frame(self):

            if self.bandera==0:
                # Tomamos una captura desde la webcam.
                try:
                    foto = self.cam.read()[1]
                    image = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)
                    #del(self.cam)
                except Exception, e:
                    foto = cv2.imread("src/imgCamara.png")
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(foto,'Camera NOT FOUND',(50,70), font, .8,(255,255,255),2,cv2.LINE_AA)
                    image = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)
                # Creamos un pixmap a partir de la imagen.
                # OpenCV entraga los pixeles de la imagen en formato BGR en lugar del tradicional RGB,
                # por lo tanto tenemos que usar el metodo rgbSwapped() para que nos entregue una imagen con
                # los bytes Rojo y Azul intercambiados, y asi poder mostrar la imagen de forma correcta.
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(image.rgbSwapped())
                #Escalamos el tamano de los pixmap para que se ajusten a la pantalla
                pix1= pixmap.scaled(self.ui.Camara.width(), self.ui.Camara.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                # Mostramos el QPixmap en la QLabel.
                self.ui.Camara.setPixmap(pix1)
                if self.flagVisor == True:
                    self.panimag.imag.pantalla1.setPixmap(self.ui.Camara.pixmap())

            else:
                pass

        def Ninos(self):
            nin=['N1T06P1RB','N1T06P2RA','N1T12P1RA','N1T12P2RB']
            ind=r.randrange(0,len(nin)-1,1)
            elemento=nin[ind]
            resp=elemento[8]
            vid= self.pathvideos+elemento+".mp4"
            obsta= self.pathobst+elemento+".png"
            data=[obsta, vid, resp]
            return data
        
        def Normal(self):
            nor=['N2T01P1RC', 'N2T01P2RB', 'N2T01P3RA','N2T02P1RA', 'N2T02P2RB', 'N2T02P3RA','N2T03P1RB', 'N2T03P2RC', 'N2T05P1RA', 'N2T05P2RC','N2T06P2RB','N2T07P2RA','N2T08P1RB','N2T08P2RC','N2T08P3RB','N2T09P1RB','N2T09P2RC','N2T10P1RA','N2T10P2RB','N2T11P1RA','N2T11P2RB','N2T13P1RB','N2T13P2RA','N2T14P1RC']
            ind=r.randrange(0,len(nor)-1,1)
            elemento=nor[ind]
            resp=elemento[8]
            vid= self.pathvideos+elemento+".mp4"
            obsta= self.pathobst+elemento+".png"
            data=[obsta, vid, resp]
            return data

        def Pros(self):
            nor=['N3T07P1RB','N3T13P3RA']
            ind=r.randrange(0,len(nor)-1,1)
            elemento=nor[ind]
            resp=elemento[8]
            vid= self.pathvideos+elemento+".mp4"
            obsta= self.pathobst+elemento+".png"
            data=[obsta, vid, resp]
            return data

        def Evaluar(self):
            pantallavideo= self.pantalla
            if self.ui.Respuesta.currentText() == self.respuesta :
                self.pantalla = self.pathvideos + self.respuesta + '.mp4'
            else:
                self.pantalla = self.pathvideos + '0.mp4'
            self.Play();
            self.pantalla = pantallavideo

        def Execute(self, a, b, c):
            #a=Imagen del tablero
            #b=Video pregunta
            #c=Respuesta a la pregunta
            pixmap = QtGui.QPixmap(a)
            if a != 'src/logo_ctin.png':
                pixmap = pixmap.scaledToWidth(self.ui.Obstaculos.width())
            self.ui.Obstaculos.setPixmap(pixmap)
            self.imagen = a
            self.pantalla = b
            self.respuesta = c

        def NivelSelec(self): 
            nivel = self.ui.Nivel.currentIndex()
            if nivel == 1:
                datos = self.Ninos()
                ob = datos[0]
                vi = datos[1]
                re = datos[2]
            elif nivel == 2:
                datosn = self.Normal()
                ob = datosn[0]
                vi = datosn[1]
                re = datosn[2]
            elif nivel == 3:
                datosn = self.Pros()
                ob = datosn[0]
                vi = datosn[1]
                re = datosn[2]
            else:
                ob= 'src/logo_ctin.png'
                vi='a.mp4'
                re='0'
            self.Execute(ob,vi,re)

#Ejecucion del programa
app = QtGui.QApplication(sys.argv)
MyWindow = MainWindowC()
sys.exit(app.exec_())

