from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from ui_main import Ui_MainWindow
from PIL import Image
import sys
import os
import cv2 as cv

from Filters import black_and_white as bw
from Convert import jpg_to_png as to_png

import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from model import *
from data import *

PROCESS = "process"
IMAGES = "images"
AUG = "aug"
MASKS = "masks"


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class mywindow(QMainWindow):
    current_dir = ""
    train = ""
    source = ""
    aug = ""
    test = ""
    db_nn = ""

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.ActImgs.triggered.connect(self.clickDirImages)
        self.ui.ActThreshGlobal.triggered.connect(self.filter_global)
        self.ui.actionThresh_Otsu.triggered.connect(self.filter_otsu)
        self.ui.actionThresh_Mean.triggered.connect(self.filter_mean)
        self.ui.actionThresh_Gaussian.triggered.connect(self.filter_gaussian)
        self.ui.actionThresh_Gaussian_and_Otsu.triggered.connect(self.filter_gaussian_and_otsu)
        self.ui.action_JPG_PNG.triggered.connect(self.convert_jpg_to_png)

        self.ui.LstSrcImg.itemClicked.connect(self.showImg)
        self.ui.LstNNImg.itemClicked.connect(self.showNNImg)

        self.ui.ActRunNN.triggered.connect(self.neuron_net_test)

        self.ui.ActSrcImg.triggered.connect(self.clickSrcDir)
        self.ui.ActTrainImg.triggered.connect(self.clickTrainDir)
        self.ui.ActAugImg.triggered.connect(self.clickAugDir)
        self.ui.ActTestImg.triggered.connect(self.clickTestDir)
        self.ui.ActDbNN.triggered.connect(self.clickDbNNDir)

        self.ui.SliderGlobal.valueChanged.connect(self.changeSliderGlobal)
        self.ui.SliderGlobal.valueChanged.connect(self.ui.SpinGlobal.setValue)
        self.ui.SpinGlobal.valueChanged.connect(self.ui.SliderGlobal.setValue)

        self.statusBar()

        menubar = self.menuBar()

        self.show()

    def clickDirImages(self):
        if self.ui.LstSrcImg.count() != 0:
            self.ui.LstSrcImg.clear()

        self.current_dir = QFileDialog.getExistingDirectory(self, "Выбрать директорию", "",
                                                            QFileDialog.ShowDirsOnly
                                                            | QFileDialog.DontResolveSymlinks)

        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for file in files:
                self.ui.LstSrcImg.addItem(QtWidgets.QListWidgetItem(file))

        self.ui.LblDirSrcImg.setText(self.current_dir)

    def clickSrcDir(self):
        self.source = QFileDialog.getExistingDirectory(self, "Выбрать директории исходных данных", "",
                                                       QFileDialog.ShowDirsOnly
                                                       | QFileDialog.DontResolveSymlinks)

    def clickTrainDir(self):
        self.train = QFileDialog.getExistingDirectory(self, "Выбрать директории тренировочных данных", "",
                                                      QFileDialog.ShowDirsOnly
                                                      | QFileDialog.DontResolveSymlinks)

    def clickAugDir(self):
        self.aug = QFileDialog.getExistingDirectory(self, "Выбрать директории генерации тренировочных данных", "",
                                                    QFileDialog.ShowDirsOnly
                                                    | QFileDialog.DontResolveSymlinks)

    def clickTestDir(self):
        self.test = QFileDialog.getExistingDirectory(self, "Выбрать директории тестируемых данных", "",
                                                     QFileDialog.ShowDirsOnly
                                                     | QFileDialog.DontResolveSymlinks)
        self.ui.LblDirResNN.setText(self.test)

    def clickDbNNDir(self):
        self.db_nn = QFileDialog.getOpenFileName(self, "Выбрать базы данных нейронной сети", "", "*.hdf5")
        self.ui.LblDbNN.setText(self.db_nn[0])

    def clearGrafFilter(self):
        if self.ui.VBoxSrc.count():
            self.ui.VBoxSrc.removeWidget(self.ui.VBoxSrc.itemAt(0).widget())
            self.ui.VBoxDst.removeWidget(self.ui.VBoxDst.itemAt(0).widget())

    def changeSliderGlobal(self):
        self.clearGrafFilter()

        item = self.ui.LstSrcImg.currentItem()
        if item != None:
            out = os.path.join(os.getcwd(), PROCESS)
            bw.global_bin(os.path.join(self.current_dir, item.text()), self.ui.SliderGlobal.value(),
                          os.path.join(out, item.text()))
            self.showImgAndGraf(item)

    def showImg(self, item: QtWidgets.QListWidgetItem):
        self.clearGrafFilter()

        self.showImgAndGraf(item)

    def showImgAndGraf(self, item):
        pixmap_src = QPixmap(os.path.join(self.current_dir, item.text()))
        pixmap_dst = QPixmap(os.path.join(PROCESS, item.text()))
        self.ui.LblSrcImg.setPixmap(
            pixmap_src.scaled(self.ui.LblSrcImg.width(), self.ui.LblSrcImg.height(), QtCore.Qt.KeepAspectRatio))
        self.ui.LblDstImg.setPixmap(
            pixmap_dst.scaled(self.ui.LblDstImg.width(), self.ui.LblDstImg.height(), QtCore.Qt.KeepAspectRatio))

        r = cv.imread(os.path.join(self.current_dir, item.text()))
        unique, counts = np.unique(r, return_counts=True)
        sc = MplCanvas(self, width=5, height=4, dpi=50)
        sc.axes.scatter(unique, np.log(counts))
        self.ui.VBoxSrc.addWidget(sc)

        r2 = cv.imread(os.path.join(PROCESS, item.text()))
        unique2, counts2 = np.unique(r2, return_counts=True)
        sc2 = MplCanvas(self, width=5, height=4, dpi=50)
        sc2.axes.scatter(unique2, np.log(counts2))
        self.ui.VBoxDst.addWidget(sc2)

    def showNNImg(self, item: QtWidgets.QListWidgetItem):
        if self.ui.VBoxNN.count():
            self.ui.VBoxNN.removeWidget(self.ui.VBoxNN.itemAt(0).widget())

        pixmap = QPixmap(os.path.join(self.test, item.text()))
        self.ui.LblNN.setPixmap(
            pixmap.scaled(self.ui.LblSrcImg.width(), self.ui.LblSrcImg.height(), QtCore.Qt.KeepAspectRatio))

        r = cv.imread(os.path.join(self.test, item.text()))
        unique, counts = np.unique(r, return_counts=True)
        sc = MplCanvas(self, width=5, height=4, dpi=500)
        sc.axes.scatter(unique, np.log(counts))
        self.ui.VBoxNN.addWidget(sc)

    def addInList(self):
        process = os.path.join(os.getcwd(), PROCESS)
        for path, dirs, files in os.walk(os.path.join(process)):
            for file in files:
                item = QtWidgets.QListWidgetItem(file)
                self.ui.LstSrcImg.addItem(item)

    def filter_global(self):
        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.global_bin(os.path.join(self.current_dir, img), self.ui.SliderGlobal.value(),
                              os.path.join(out, img))

    def filter_otsu(self):
        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.otsu(os.path.join(self.current_dir, img), os.path.join(out, img))

    def filter_gaussian_and_otsu(self):
        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.gaussian_and_otsu(os.path.join(self.current_dir, img), os.path.join(out, img))

    def filter_gaussian(self):
        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.gaussian(os.path.join(self.current_dir, img), os.path.join(out, img))

    def filter_mean(self):
        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.mean(os.path.join(self.current_dir, img), os.path.join(out, img))

    def convert_jpg_to_png(self):
        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in self.current_dir:
            for img in files:
                full = os.path.join(path, img)
                to_png(full, os.path.join(full, ".png"))

    def neuron_net_test(self):
        if self.ui.LstNNImg.count() != 0:
            self.ui.LstNNImg.clear()

        if not os.path.isdir(self.test):
            return

        model = unet(self.db_nn[0])

        testGene = testGenerator(self.test)

        count = 0
        for i, i2, i3 in os.walk(self.test):
            if 'predict' in i3:
                count += 1

        results = model.predict_generator(testGene, 11, verbose=1)
        saveResult(self.test, results)

        path = os.path.join(os.getcwd(), self.test)
        for path, dirs, files in os.walk(path):
            for img in files:
                if 'predict' in img:
                    self.ui.LstNNImg.addItem(QtWidgets.QListWidgetItem(img))

    def neuron_net_train(self):
        data_gen_args = dict(rotation_range=0.2,
                             width_shift_range=0.05,
                             height_shift_range=0.05,
                             shear_range=0.05,
                             zoom_range=0.05,
                             horizontal_flip=True,
                             fill_mode='nearest')
        myGene = trainGenerator(2, self.train, IMAGES, MASKS, data_gen_args,
                                save_to_dir=os.path.join(os.getcwd(), AUG))

        model = unet()
        model_checkpoint = ModelCheckpoint(self.db_nn, monitor='loss', verbose=1, save_best_only=True)
        model.fit_generator(myGene, steps_per_epoch=300, epochs=1, callbacks=[model_checkpoint])

        testGene = testGenerator(self.test)

        results = model.predict_generator(testGene, 11, verbose=1)
        saveResult(self.test, results)


app = QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
