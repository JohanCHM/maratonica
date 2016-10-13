import sys
import cv2
from PyQt4 import QtCore, QtGui, uic

class MainWindowC(QtGui.QMainWindow):

	res = [1024,768]

	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.winTestCam = uic.loadUi("TestRendimiento/testcam.ui")
		self.winTestCam.show()

		self.cam = cv2.VideoCapture(0)

		self.cam.set(3,self.res[0])
		self.cam.set(4,self.res[1])
 
		self.pixmap = QtGui.QPixmap()
		
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.ShowFrame)
		self.timer.start(40)


	def ShowFrame(self):
		try:
			foto = self.cam.read()[1]
			image = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)
		except Exception, e:
			foto = cv2.imread("src/imgCamara.png")
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(foto,'Camera NOT FOUND',(50,70), font, .8,(255,255,255),2,cv2.LINE_AA)
			image = QtGui.QImage(foto, foto.shape[1],foto.shape[0], foto.shape[1] * 3,QtGui.QImage.Format_RGB888)
		self.pixmap.convertFromImage(image.rgbSwapped())
		#pix1 = self.pixmap.scaled(self.ui.Camara.width(), self.ui.Camara.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		self.winTestCam.visorMain.setPixmap(self.pixmap)
		
#Ejecucion del programa
app = QtGui.QApplication(sys.argv)
MyWindow = MainWindowC()
sys.exit(app.exec_())