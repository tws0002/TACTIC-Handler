# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conf\ui_conf.ui'
#
# Created: Tue Jan 23 23:02:26 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from thlib.side.Qt import QtWidgets as QtGui
from thlib.side.Qt import QtGui as Qt4Gui
from thlib.side.Qt import QtCore

class Ui_configuration_dialog(object):
    def setupUi(self, configuration_dialog):
        configuration_dialog.setObjectName("configuration_dialog")
        configuration_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        configuration_dialog.resize(750, 700)
        configuration_dialog.setSizeGripEnabled(True)
        configuration_dialog.setModal(True)
        self.confDialogLayout = QtGui.QVBoxLayout(configuration_dialog)
        self.confDialogLayout.setObjectName("confDialogLayout")
        self.uiConfMainWidget = QtGui.QWidget(configuration_dialog)
        self.uiConfMainWidget.setObjectName("uiConfMainWidget")
        self.uiConfLayout = QtGui.QVBoxLayout(self.uiConfMainWidget)
        self.uiConfLayout.setContentsMargins(0, 0, 0, 0)
        self.uiConfLayout.setContentsMargins(0, 0, 0, 0)
        self.uiConfLayout.setObjectName("uiConfLayout")
        self.configToolBox = QtGui.QToolBox(self.uiConfMainWidget)
        palette = Qt4Gui.QPalette()
        self.configToolBox.setPalette(palette)
        self.configToolBox.setStyleSheet("QToolBox > *,\n"
"QToolBox > QScrollArea > #qt_scrollarea_viewport > QWidget {\n"
"    background-color: rgba(128, 128, 128, 48);\n"
"}\n"
"\n"
"QToolBox::tab {\n"
"    border-style: outset;\n"
"    border-width: 1px;\n"
"    border-color:  rgba(75, 75, 75, 75);\n"
"    border-radius: 3px;\n"
"    padding: 1px;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(175, 175, 175, 25), stop: 1 rgba(175, 175, 175, 0));\n"
"}\n"
"/*\n"
"QToolBox::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(175, 175, 175, 50), stop: 1 rgba(175, 175, 175, 0));\n"
"    border: 1px solid rgba(128, 128, 128, 75);\n"
"}\n"
"*/\n"
"QToolBox::tab:selected {\n"
"    font: italic;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(175, 175, 175, 50), stop: 1 rgba(175, 175, 175, 0));\n"
"    border-style: outset;\n"
"    border-width: 1px;\n"
"    border-color:  rgba(128, 128, 128, 75);\n"
"    border-radius: 3px;\n"
"}")
        self.configToolBox.setObjectName("configToolBox")
        self.serverPage = QtGui.QWidget()
        self.serverPage.setGeometry(QtCore.QRect(0, 0, 732, 515))
        self.serverPage.setObjectName("serverPage")
        self.serverPageLayout = QtGui.QVBoxLayout(self.serverPage)
        self.serverPageLayout.setContentsMargins(6, 6, 6, 6)
        self.serverPageLayout.setObjectName("serverPageLayout")
        self.configToolBox.addItem(self.serverPage, "")
        self.projectPage = QtGui.QWidget()
        self.projectPage.setGeometry(QtCore.QRect(0, 0, 732, 515))
        self.projectPage.setObjectName("projectPage")
        self.projectPageLayout = QtGui.QVBoxLayout(self.projectPage)
        self.projectPageLayout.setContentsMargins(6, 6, 6, 6)
        self.projectPageLayout.setObjectName("projectPageLayout")
        self.configToolBox.addItem(self.projectPage, "")
        self.checkinOutOptionsPage = QtGui.QWidget()
        self.checkinOutOptionsPage.setGeometry(QtCore.QRect(0, 0, 732, 515))
        self.checkinOutOptionsPage.setObjectName("checkinOutOptionsPage")
        self.checkinPageLayout = QtGui.QVBoxLayout(self.checkinOutOptionsPage)
        self.checkinPageLayout.setContentsMargins(6, 6, 6, 6)
        self.checkinPageLayout.setObjectName("checkinPageLayout")
        self.configToolBox.addItem(self.checkinOutOptionsPage, "")
        self.checkinOutAppPage = QtGui.QWidget()
        self.checkinOutAppPage.setGeometry(QtCore.QRect(0, 0, 732, 515))
        self.checkinOutAppPage.setObjectName("checkinOutAppPage")
        self.checkinOutPageLayout = QtGui.QVBoxLayout(self.checkinOutAppPage)
        self.checkinOutPageLayout.setContentsMargins(6, 6, 6, 6)
        self.checkinOutPageLayout.setObjectName("checkinOutPageLayout")
        self.configToolBox.addItem(self.checkinOutAppPage, "")
        self.globalCofigPage = QtGui.QWidget()
        self.globalCofigPage.setGeometry(QtCore.QRect(0, 0, 732, 515))
        self.globalCofigPage.setObjectName("globalCofigPage")
        self.globalCofigPageLayout = QtGui.QVBoxLayout(self.globalCofigPage)
        self.globalCofigPageLayout.setContentsMargins(6, 6, 6, 6)
        self.globalCofigPageLayout.setObjectName("globalCofigPageLayout")
        self.configToolBox.addItem(self.globalCofigPage, "")
        self.currentEnvironmentPage = QtGui.QWidget()
        self.currentEnvironmentPage.setGeometry(QtCore.QRect(0, 0, 732, 515))
        self.currentEnvironmentPage.setObjectName("currentEnvironmentPage")
        self.currentEnvironmentPageLayout = QtGui.QVBoxLayout(self.currentEnvironmentPage)
        self.currentEnvironmentPageLayout.setContentsMargins(6, 6, 6, 6)
        self.currentEnvironmentPageLayout.setObjectName("currentEnvironmentPageLayout")
        self.configToolBox.addItem(self.currentEnvironmentPage, "")
        self.uiConfLayout.addWidget(self.configToolBox)
        self.buttonBox = QtGui.QDialogButtonBox(self.uiConfMainWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.uiConfLayout.addWidget(self.buttonBox)
        self.confDialogLayout.addWidget(self.uiConfMainWidget)

        self.retranslateUi(configuration_dialog)
        self.configToolBox.setCurrentIndex(0)
        self.configToolBox.layout().setSpacing(2)
        QtCore.QMetaObject.connectSlotsByName(configuration_dialog)

    def retranslateUi(self, configuration_dialog):
        configuration_dialog.setWindowTitle(QtGui.QApplication.translate("configuration_dialog", "TACTIC Handler configuration", None))
        self.configToolBox.setItemText(self.configToolBox.indexOf(self.serverPage), QtGui.QApplication.translate("configuration_dialog", "TACTIC Server", None))
        self.configToolBox.setItemText(self.configToolBox.indexOf(self.projectPage), QtGui.QApplication.translate("configuration_dialog", "Project", None))
        self.configToolBox.setItemText(self.configToolBox.indexOf(self.checkinOutOptionsPage), QtGui.QApplication.translate("configuration_dialog", "Checkin/Checkout Options", None))
        self.configToolBox.setItemText(self.configToolBox.indexOf(self.checkinOutAppPage), QtGui.QApplication.translate("configuration_dialog", "Checkin/Checkout Appearance", None))
        self.configToolBox.setItemText(self.configToolBox.indexOf(self.globalCofigPage), QtGui.QApplication.translate("configuration_dialog", "Global Config", None))
        self.configToolBox.setItemText(self.configToolBox.indexOf(self.currentEnvironmentPage), QtGui.QApplication.translate("configuration_dialog", "Current Environment Options", None))

