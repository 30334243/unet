# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1067, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ListSrcImg = QtWidgets.QListWidget(self.centralwidget)
        self.ListSrcImg.setGeometry(QtCore.QRect(10, 10, 256, 531))
        self.ListSrcImg.setObjectName("ListSrcImg")
        self.LstDstImg = QtWidgets.QListWidget(self.centralwidget)
        self.LstDstImg.setGeometry(QtCore.QRect(800, 10, 256, 531))
        self.LstDstImg.setObjectName("LstDstImg")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(280, 10, 511, 271))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.LblSrcImg = QtWidgets.QLabel(self.splitter)
        self.LblSrcImg.setText("")
        self.LblSrcImg.setObjectName("LblSrcImg")
        self.LblDstImg = QtWidgets.QLabel(self.splitter)
        self.LblDstImg.setText("")
        self.LblDstImg.setObjectName("LblDstImg")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1067, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.ActImgs = QtWidgets.QAction(MainWindow)
        self.ActImgs.setObjectName("ActImgs")
        self.ActImg = QtWidgets.QAction(MainWindow)
        self.ActImg.setObjectName("ActImg")
        self.ActiGaussian = QtWidgets.QAction(MainWindow)
        self.ActiGaussian.setObjectName("ActiGaussian")
        self.ActOtsu = QtWidgets.QAction(MainWindow)
        self.ActOtsu.setObjectName("ActOtsu")
        self.ActMean = QtWidgets.QAction(MainWindow)
        self.ActMean.setObjectName("ActMean")
        self.ActGlobal = QtWidgets.QAction(MainWindow)
        self.ActGlobal.setObjectName("ActGlobal")
        self.ActThreshGlobal = QtWidgets.QAction(MainWindow)
        self.ActThreshGlobal.setObjectName("ActThreshGlobal")
        self.menu.addAction(self.ActImgs)
        self.menu.addAction(self.ActImg)
        self.menu_2.addAction(self.ActThreshGlobal)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.toolBar.addAction(self.ActiGaussian)
        self.toolBar.addAction(self.ActOtsu)
        self.toolBar.addAction(self.ActMean)
        self.toolBar.addAction(self.ActGlobal)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Операции"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.ActImgs.setText(_translate("MainWindow", "Директория изображений"))
        self.ActImg.setText(_translate("MainWindow", "Изображение"))
        self.ActiGaussian.setText(_translate("MainWindow", "gaussian"))
        self.ActOtsu.setText(_translate("MainWindow", "otsu"))
        self.ActMean.setText(_translate("MainWindow", "mean"))
        self.ActGlobal.setText(_translate("MainWindow", "global"))
        self.ActThreshGlobal.setText(_translate("MainWindow", "Thresh Global"))
