import sys
import sys
import pandas as pd
import os
import matplotlib.pyplot as plt

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.QtGui import QPixmap

class Drowka():
    def drow1(self):
        plot_data = Data.File[Data.File['Kadr'] == Data.kadr]
        x = range(0,1024)
        for i in range(plot_data.shape[0]):
            y = plot_data.iloc[i][3:]
            plt.plot(x, y)
        plt.savefig('0.png', bbox_inches='tight')
        plt.clf()
        print(Data.kanal)
        print(Data.kadr)
        self.load_image('0.png')
        
        
    def drow2(self):
        plot_data = Data.File[Data.File['Kanal'] == Data.kanal]
        x = range(0,1024)
        for i in Data.File['Kadr'].unique():
            y = plot_data[plot_data['Kadr'] == i].iloc[0][3:]
            plt.plot(x, y)
        plt.savefig('0.png', bbox_inches='tight')
        plt.clf()
        self.load_image('0.png')
        
    def drow3(self):
        plot_data = Data.File[(Data.File['Kanal'] == Data.kanal)&(Data.File['Kadr'] == Data.kadr)]
        y = plot_data.iloc[0][3:].tolist()
        x = range(0,1024)
        plt.plot(x, y)
        plt.savefig('0.png', bbox_inches='tight')
        plt.clf()
        self.load_image('0.png')

class Data():
    File = pd.DataFrame()
    kadr = ''
    kanal = ''
    
    def __init__(self, filename):
        df = pd.read_csv(filename, sep="\s+", encoding="windows-1251", header=None)
        df.columns = columns = ['Kadr', 'Time', 'Kanal'] + [f'{i}' for i in range(1024)]
        Data.File = df

class MyWidget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('vigual.ui', self)  # Загружаем дизайн
        self.load_file.clicked.connect(self.lf)
        self.postr.clicked.connect(self.drow)
        # Обратите внимание: имя элемента такое же как в QTDesigner

    def lf(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        
        if fname[0] != '':
            Data(fname[0])
        else:
            return None
        self.kanals.clear()
        self.kanals.addItems([str(i) for i in range(0, 32)])
        self.kanals.addItem('all')
        self.kadrs.clear()
        self.kadrs.addItem('all')
        self.kadrs.addItems([str(i) for i in Data.File['Kadr'].unique()])
        
        
    def drow(self):
        if self.kanals.currentText() == 'all' and self.kadrs.currentText() == 'all':
            return None
        if self.kanals.currentText() == 'all':
            Data.kanal = 'all'
            Data.kadr = int(self.kadrs.currentText())
            Drowka.drow1(self)
            return None
        if self.kadrs.currentText() == 'all':
            Data.kanal = int(self.kanals.currentText())
            Data.kadr = 'all'
            Drowka.drow2(self)
            return None
        Data.kanal = int(self.kanals.currentText())
        Data.kadr = int(self.kadrs.currentText())
        Drowka.drow3(self)
        
    def load_image(self, file_name):
        pixmap = QPixmap(file_name)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.label.move(200, 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
