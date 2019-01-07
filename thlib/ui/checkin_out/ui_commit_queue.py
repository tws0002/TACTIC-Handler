# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checkin_out/ui_commit_queue.ui'
#
# Created: Thu May 10 14:59:18 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from thlib.side.Qt import QtWidgets as QtGui
from thlib.side.Qt import QtCore

class Ui_commitQueue(object):
    def setupUi(self, commitQueue):
        commitQueue.setObjectName("commitQueue")
        commitQueue.resize(800, 640)
        self.centralwidget = QtGui.QWidget(commitQueue)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(9, 9, 9, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.filesCountLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.filesCountLabel.setObjectName("filesCountLabel")
        self.horizontalLayout_2.addWidget(self.filesCountLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.clearQueuePushButton = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.clearQueuePushButton.setMinimumSize(QtCore.QSize(120, 0))
        self.clearQueuePushButton.setObjectName("clearQueuePushButton")
        self.horizontalLayout_2.addWidget(self.clearQueuePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.filesQueueTreeWidget = QtGui.QTreeWidget(self.verticalLayoutWidget_2)
        self.filesQueueTreeWidget.setMinimumSize(QtCore.QSize(300, 0))
        self.filesQueueTreeWidget.setRootIsDecorated(False)
        self.filesQueueTreeWidget.setHeaderHidden(True)
        self.filesQueueTreeWidget.setObjectName("filesQueueTreeWidget")
        self.verticalLayout.addWidget(self.filesQueueTreeWidget)
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.commitEditorLayout = QtGui.QVBoxLayout()
        self.commitEditorLayout.setObjectName("commitEditorLayout")
        self.verticalLayout_2.addLayout(self.commitEditorLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.commitAllPushButton = QtGui.QPushButton(self.verticalLayoutWidget_3)
        self.commitAllPushButton.setMinimumSize(QtCore.QSize(120, 0))
        self.commitAllPushButton.setObjectName("commitAllPushButton")
        self.horizontalLayout.addWidget(self.commitAllPushButton)
        self.closePushButton = QtGui.QPushButton(self.verticalLayoutWidget_3)
        self.closePushButton.setMinimumSize(QtCore.QSize(120, 0))
        self.closePushButton.setObjectName("closePushButton")
        self.horizontalLayout.addWidget(self.closePushButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(0, 1)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        commitQueue.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(commitQueue)
        self.statusbar.setObjectName("statusbar")
        commitQueue.setStatusBar(self.statusbar)

        self.retranslateUi(commitQueue)
        QtCore.QMetaObject.connectSlotsByName(commitQueue)

    def retranslateUi(self, commitQueue):
        commitQueue.setWindowTitle(QtGui.QApplication.translate("commitQueue", "MainWindow", None))
        self.label.setText(QtGui.QApplication.translate("commitQueue", "Commits in Queue:", None))
        self.filesCountLabel.setText(QtGui.QApplication.translate("commitQueue", "0", None))
        self.clearQueuePushButton.setText(QtGui.QApplication.translate("commitQueue", "Clear Queue", None))
        self.filesQueueTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("commitQueue", "1", None))
        self.commitAllPushButton.setText(QtGui.QApplication.translate("commitQueue", "Commit All", None))
        self.closePushButton.setText(QtGui.QApplication.translate("commitQueue", "Close", None))

