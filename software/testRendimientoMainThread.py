import sys
import cv2
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QThread
from PyQt4.phonon import Phonon

import time

class MainWindowC(QtGui.QMainWindow):

	res = [1024,768]

	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.winTestCam = uic.loadUi("TestRendimiento/testcam.ui")
		self.winTestCam.show()

		self.EncenderCam()

		self.timFlags = QtCore.QTimer(self)
		self.timFlags.timeout.connect(self.UpdateVisores)
		self.timFlags.start(20)

		self.winTestCam.botCam.clicked.connect(self.EncenderCam)
		self.winTestCam.botLab.clicked.connect(self.EncenderLab)
		self.winTestCam.botVid.clicked.connect(self.EncenderVid)


		#TEMPO
		self.winTestCam.videoPlayer.setVisible(False)
		
			#TEMPO
			#t0 = time.time()

			#TEMPO
			#print time.time()-t0

	def EncenderCam(self):
		self.cam = cv2.VideoCapture(0)
		self.cam.set(3,self.res[0])
		self.cam.set(4,self.res[1])
		foto = self.cam.read()[1]
		self.camY = foto.shape[1]
		self.camX = foto.shape[0]
		self.camF = foto.shape[1] * 3
		self.timVisorCam = QtCore.QTimer(self)
		self.timVisorCam.timeout.connect(self.ShowFrame)
		self.timVisorCam.start(40)
		self.pixVisorCam = QtGui.QPixmap()

	def EncenderLab(self):
		self.flagMain = self.FLAG_LAB

	def EncenderVid(self):
		self.winTestCam.videoPlayer.play(Phonon.MediaSource('Videos/N1T04P3RB.mp4'))
		self.flagMain = self.FLAG_VID

	def UpdateVisores(self):
		pass

	def ShowFrame(self):
		try:
			self.pixVisorCam.convertFromImage(QtGui.QImage(self.cam.read()[1], self.camY, self.camX, self.camF, QtGui.QImage.Format_RGB888).rgbSwapped())		
			self.winTestCam.visorMain.setPixmap(self.pixVisorCam)


		except Exception, e:
			foto = cv2.imread("src/imgCamara.png")
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(foto,'Camera NOT FOUND',(50,70), font, .8,(255,255,255),2,cv2.LINE_AA)
			self.imgVisorMain = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)

				
#Ejecucion del programa
app = QtGui.QApplication(sys.argv)
MyWindow = MainWindowC()
sys.exit(app.exec_())