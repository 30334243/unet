from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
from ui_main import Ui_MainWindow
import sys
import shutil
import cv2 as cv

from model import *
from Data.data import *

from pathlib import Path

from Filters import black_and_white as bw
from Convert import jpg_to_png as to_png

import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

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
    png = ""
    save = ""

    train = ""
    masks = ""
    src = ""
    aug = ""

    test = ""
    res_test = ""
    weights_train = ""
    weights_test = ""

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # tools
        self.ui.ActImgs.triggered.connect(self.clickDirImages)
        self.ui.ActJPG_PNG.triggered.connect(self.convert_jpg_to_png)
        # buttons
        self.ui.BtnSrcImg.clicked.connect(self.clickDirImages)
        self.ui.BtnJpgToPng.clicked.connect(self.clickJpgToPng)
        self.ui.BtnConvertJpgToPng.clicked.connect(self.convert_jpg_to_png2)
        self.ui.BtnApplyFilter.clicked.connect(self.clickApplyFilterImg)
        self.ui.BtnApplyFilterAll.clicked.connect(self.filter_global)
        self.ui.BtnSaveFilterImg.clicked.connect(self.clickFilterSaveImg)

        # filters
        self.ui.ActThreshGlobal.triggered.connect(self.filter_global)
        self.ui.ActThreshOtsu.triggered.connect(self.filter_otsu)
        self.ui.ActThreshMean.triggered.connect(self.filter_mean)
        self.ui.ActThreshGaussian.triggered.connect(self.filter_gaussian)
        self.ui.ActThreshGaussianAndOtsu.triggered.connect(self.filter_gaussian_and_otsu)

        # lists
        self.ui.LstSrcImg.itemClicked.connect(self.showImg)
        self.ui.LstNNImg.itemClicked.connect(self.showNNImg)

        # train NN
        self.ui.ActTrainData.triggered.connect(self.clickTrainData)
        self.ui.ActSaveTrainData.triggered.connect(self.clickDbSaveWeight)
        self.ui.ActRunTrainNN.triggered.connect(self.neuron_net_train)
        # buttons
        self.ui.BtnTrainData.clicked.connect(self.clickTrainData)
        self.ui.BtnDbSaveWeight.clicked.connect(self.clickDbSaveWeight)
        self.ui.BtnTrainNN.clicked.connect(self.neuron_net_train)

        # test NN
        self.ui.ActTestData.triggered.connect(self.clickTestData)
        self.ui.ActSaveTrainData.triggered.connect(self.clickTrainResult)
        self.ui.ActDbWeights.triggered.connect(self.clickDbOpenWeights)
        # buttons
        self.ui.BtnTestData.clicked.connect(self.clickTestData)
        self.ui.BtnTestResult.clicked.connect(self.clickTrainResult)
        self.ui.BtnDbOpenWeights.clicked.connect(self.clickDbOpenWeights)
        self.ui.BtnTestNN.clicked.connect(self.neuron_net_test)

        # filter global tools
        self.ui.SliderGlobal.valueChanged.connect(self.changeSliderGlobal)
        self.ui.SliderGlobal.valueChanged.connect(self.ui.SpinGlobal.setValue)
        self.ui.SpinGlobal.valueChanged.connect(self.ui.SliderGlobal.setValue)

        self.statusBar()

        menubar = self.menuBar()

        self.show()

    def clearProcess(self):
        for path, dirs, files in os.walk(os.path.join(os.getcwd(), PROCESS)):
            for file in files:
                os.remove(os.path.join(path, file))

    # tools
    def clickDirImages(self):
        if self.ui.LstSrcImg.count() != 0:
            self.ui.LstSrcImg.clear()

        self.current_dir = QFileDialog.getExistingDirectory(self, "Выбрать директорию с изображениями",
                                                            self.current_dir,
                                                            QFileDialog.ShowDirsOnly
                                                            | QFileDialog.DontResolveSymlinks)
        self.ui.LineSrcImg.setText(self.current_dir)

        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for file in files:
                self.ui.LstSrcImg.addItem(QtWidgets.QListWidgetItem(file))

    def convert_jpg_to_png(self):
        if not os.path.isdir(self.current_dir):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                full = os.path.join(path, img)
                if full.endswith(".jpg"):
                    to_png.jpg_to_png(full, path)
                    os.remove(full)

    def clickJpgToPng(self):
        self.png = QFileDialog.getExistingDirectory(self, "Выбрать директорию сохранения *.png файлов", "",
                                                    QFileDialog.ShowDirsOnly
                                                    | QFileDialog.DontResolveSymlinks)
        self.ui.LineJpgToPng.setText(self.png)

    def convert_jpg_to_png2(self):
        if ((not os.path.isdir(self.current_dir)) and
                (not os.path.isdir(self.ui.LineJpgToPng.text()))):
            return

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                full = os.path.join(path, img)
                if full.endswith(".jpg"):
                    to_png.jpg_to_png(full, self.ui.LineJpgToPng.text())

    def clickFilterSaveImg(self):
        self.save = QFileDialog.getExistingDirectory(self,
                                                     "Выбрать директорию сохранения изображений применения фильта",
                                                     self.save,
                                                     QFileDialog.ShowDirsOnly
                                                     | QFileDialog.DontResolveSymlinks)
        self.ui.LineSaveFilterImg.setText(self.save)

    def clickApplyFilterImg(self):
        shutil.copy(os.path.join(os.getcwd(), os.path.join(PROCESS, self.ui.LstSrcImg.currentItem().text())),
                    self.ui.LineSaveFilterImg.text())

    # filters
    def filter_global(self):
        if not os.path.isdir(self.current_dir):
            return
        self.clearProcess()
        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), self.ui.LineSaveFilterImg.text())
                bw.global_bin(os.path.join(self.current_dir, img), self.ui.SliderGlobal.value(),
                              os.path.join(out, img))

    def filter_global_one(self):
        if not os.path.isdir(self.current_dir):
            return
        bw.global_bin(os.path.join(os.getcwd(), self.ui.LstSrcImg.currentItem().text()), self.ui.SliderGlobal.value(),
                      self.ui.LineSaveFilterImg.text())

    def filter_otsu(self):
        if not os.path.isdir(self.current_dir):
            return
        self.clearProcess()

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.otsu(os.path.join(self.current_dir, img), os.path.join(out, img))

    def filter_gaussian_and_otsu(self):
        if not os.path.isdir(self.current_dir):
            return
        self.clearProcess()

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.gaussian_and_otsu(os.path.join(self.current_dir, img), os.path.join(out, img))

    def filter_gaussian(self):
        if not os.path.isdir(self.current_dir):
            return
        self.clearProcess()

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.gaussian(os.path.join(self.current_dir, img), os.path.join(out, img))

    def filter_mean(self):
        if not os.path.isdir(self.current_dir):
            return
        self.clearProcess()

        for path, dirs, files in os.walk(self.current_dir):
            for img in files:
                out = os.path.join(os.getcwd(), PROCESS)
                bw.mean(os.path.join(self.current_dir, img), os.path.join(out, img))

    # test
    def clickTestData(self):
        self.test = QFileDialog.getExistingDirectory(self, "Выбрать директории тестируемых данных", self.test,
                                                     QFileDialog.ShowDirsOnly
                                                     | QFileDialog.DontResolveSymlinks)
        self.ui.LineTestData.setText(self.test)
    def clickDbOpenWeights(self):
        self.weights_test = QFileDialog.getOpenFileName(self, "Выбрать базу данных нейронной сети", "", "*.hdf5")
        self.ui.LineDbOpenWeights.setText(self.weights_test[0])
    def clickTrainResult(self):
        self.res_test = QFileDialog.getExistingDirectory(self,
                                                         "Выбрать директорию сохранения результата тестируемых данных",
                                                         self.res_test)
        self.ui.LineTestResult.setText(self.res_test)

    # train
    def clickTrainData(self):
        self.train = QFileDialog.getExistingDirectory(self, "Выбрать директорию тренировочных данных", self.train)
        self.ui.LineTrainData.setText(self.train)

    def clickDbSaveWeight(self):
        self.weights_train = QFileDialog.getSaveFileName(self, "Сохранить базу данных с весами нейронной сети",
                                                         self.weights_train, "*.hdf5")
        self.ui.LineDbSaveWeight.setText(self.weights_train[0])

    def clearGrafFilter(self):
        if self.ui.VBoxSrcFilter.count():
            self.ui.VBoxSrcFilter.removeWidget(self.ui.VBoxSrcFilter.itemAt(0).widget())
        if self.ui.VBoxDstFilter.count():
            self.ui.VBoxDstFilter.removeWidget(self.ui.VBoxDstFilter.itemAt(0).widget())

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
        self.ui.VBoxSrcFilter.addWidget(sc)

        out = os.path.join(os.getcwd(), PROCESS)
        r2 = cv.imread(os.path.join(out, item.text()))
        unique2, counts2 = np.unique(r2, return_counts=True)
        sc2 = MplCanvas(self, width=5, height=4, dpi=50)
        sc2.axes.scatter(unique2, np.log(counts2))
        self.ui.VBoxDstFilter.addWidget(sc2)

    def showNNImg(self, item: QtWidgets.QListWidgetItem):
        if self.ui.VBoxTestNN.count():
            self.ui.VBoxTestNN.removeWidget(self.ui.VBoxTestNN.itemAt(0).widget())

        pixmap = QPixmap(os.path.join(self.res_test, item.text()))
        self.ui.LblNN.setPixmap(
            pixmap.scaled(self.ui.LblSrcImg.width(), self.ui.LblSrcImg.height(), QtCore.Qt.KeepAspectRatio))

        r = cv.imread(os.path.join(self.res_test, item.text()))
        unique, counts = np.unique(r, return_counts=True)
        sc = MplCanvas(self, width=5, height=4, dpi=50)
        sc.axes.scatter(unique, np.log(counts))
        self.ui.VBoxTestNN.addWidget(sc)

    def addInList(self):
        process = os.path.join(os.getcwd(), PROCESS)
        for path, dirs, files in os.walk(os.path.join(process)):
            for file in files:
                item = QtWidgets.QListWidgetItem(file)
                self.ui.LstSrcImg.addItem(item)

    def neuron_net_test(self):
        if self.ui.LstNNImg.count() != 0:
            self.ui.LstNNImg.clear()

        if not os.path.isdir(self.test):
            return

        model = unet(Path(self.ui.LineDbOpenWeights.text()).name)

        testGene = testGenerator(self.test)

        results = model.predict_generator(testGene, len(os.walk(self.test).__next__()[2]), verbose=1)
        saveResult(self.res_test, results)

        path = os.path.join(os.getcwd(), self.test)
        for path, dirs, files in os.walk(self.res_test):
            for img in files:
                self.ui.LstNNImg.addItem(QtWidgets.QListWidgetItem(img))

    def neuron_net_train(self):
        data_gen_args = dict(rotation_range=0.2,
                             width_shift_range=0.05,
                             height_shift_range=0.05,
                             shear_range=0.05,
                             zoom_range=0.05,
                             horizontal_flip=True,
                             fill_mode='nearest')
        train = self.ui.LineTrainData.text()
        myGene = trainGenerator(2, train, self.ui.LineSrcData.text(),
                                self.ui.LineMasksData.text(), data_gen_args,
                                save_to_dir=os.path.join(train, self.ui.LineAugData.text()))

        model = unet()

        path = Path(self.weights_train[0]).name
        model_checkpoint = ModelCheckpoint(path, monitor='loss', verbose=1, save_best_only=True)
        model.fit_generator(myGene, steps_per_epoch=self.ui.SpinStepEpochs.value(), epochs=self.ui.SpinEpochs.value(),
                            callbacks=[model_checkpoint])


app = QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
