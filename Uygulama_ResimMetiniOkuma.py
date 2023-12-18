import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QComboBox, QLineEdit, QTextEdit, QScrollArea, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import cv2
import numpy as np
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

kaynak_yolu=""
def metin_oku(img_yolu,dil=None):
    img=cv2.imread(img_yolu)

    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    kernel=np.ones((1,1),np.uint8)
    img=cv2.erode(img,kernel,iterations=1)
    img = cv2.dilate( img, kernel, iterations=1)

    img=cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,2)
    cv2.imwrite(kaynak_yolu+'gurultusuz.png',img)

    sonuc=pytesseract.image_to_string(Image.open(kaynak_yolu+'gurultusuz.png'),lang='{}'.format(dil))
    return sonuc

class ResimGoruntulemeUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Çok Dilli Renkli Resim Görüntüleyici')
        self.setStyleSheet('background-color: #333333;')

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 700, 400)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('border: 2px solid #000000; background-color: #F0F0F0;')

        self.btn_ac = QPushButton('Resim Aç', self)
        self.btn_ac.setGeometry(350, 480, 100, 40)
        self.btn_ac.setStyleSheet('background-color: #4CAF50; color: white; font-weight: bold;')

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(50, 480, 150, 40)
        self.comboBox.addItems(['Türkçe', 'Kürtçe', 'Arapça', 'İngilizce'])
        self.comboBox.setStyleSheet('background-color: #4CAF50; color: white; font-weight: bold;')

        self.textBox = QLineEdit(self)
        self.textBox.setGeometry(600, 480, 150, 40)
        self.textBox.setStyleSheet('background-color: #FFFFFF; border: 2px solid #000000; color: black;')

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(50, 530, 700, 50)
        self.scrollArea.setStyleSheet('background-color: #FFFFFF; border: 2px solid #000000;')

        self.scrollContent = QTextEdit(self)
        self.scrollContent.setFixedHeight(50)
        self.scrollContent.setStyleSheet('background-color: #FFFFFF; border: none; color: black;')
        self.scrollArea.setWidget(self.scrollContent)

        self.btn_temizle = QPushButton('Temizle', self)
        self.btn_temizle.setGeometry(50, 590, 100, 40)
        self.btn_temizle.setStyleSheet('background-color: #FFD700; color: black; font-weight: bold;')

        self.btn_kopyala = QPushButton('Kopyala', self)
        self.btn_kopyala.setGeometry(200, 590, 100, 40)
        self.btn_kopyala.setStyleSheet('background-color: #0000FF; color: white; font-weight: bold;')

        self.btn_ac.clicked.connect(self.resimAc)
        self.btn_temizle.clicked.connect(self.temizle)
        self.btn_kopyala.clicked.connect(self.kopyala)

    def resimAc(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, 'Resim Aç', '', 'Resim Dosyaları (*.png *.jpg *.bmp);;Tüm Dosyalar (*)')
        liste=dosya_yolu.split("/")
        veri=liste[-1]
        if dosya_yolu:
            pixmap = QPixmap(dosya_yolu)
            self.label.setPixmap(pixmap)
            self.label.setAlignment(Qt.AlignCenter)
            self.textBox.setText(f'{pixmap.width()}x{pixmap.height()}')
            self.secilen_dil = self.comboBox.currentText()

            if (self.secilen_dil=="İngilizce"):
                x = metin_oku(veri)
                self.scrollContent.append(x)

            elif (self.secilen_dil=="Kürtçe"):
                x = metin_oku(veri,"kmr")
                self.scrollContent.append(x)

            elif(self.secilen_dil=="Türkçe"):
                x = metin_oku(veri,"tur")
                self.scrollContent.append(x)

            elif(self.secilen_dil=="Arapça"):
                x = metin_oku(veri,"ara")
                self.scrollContent.append(x)

    def temizle(self):
        self.scrollContent.clear()

    def kopyala(self):
        icerik = self.scrollContent.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(icerik)
        QMessageBox.information(self, 'Kopyalandı', 'Metin Panoya Kopyalandı', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ResimGoruntulemeUygulamasi()
    ex.show()
    sys.exit(app.exec_())