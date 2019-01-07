# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_main.ui'
#
# Created: Fri Jan 04 15:31:54 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from thlib.side.Qt import QtWidgets as QtGui
from thlib.side.Qt import QtCore

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.setStyleSheet("QTreeView {\n"
"    show-decoration-selected: 1;\n"
"}\n"
"QTreeView::item {\n"
"    border-style: outset;\n"
"    border-width: 1px;\n"
"    border-color:  rgba(75, 75, 75, 75);\n"
"    border-radius: 1px;\n"
"    padding: 0px;\n"
"    background: rgba(175, 175, 175, 25);\n"
"}\n"
"\n"
"QTreeView::item:hover {\n"
"    background: rgba(175, 175, 175, 50);\n"
"    border: 1px solid rgba(128, 128, 128, 75);\n"
"}\n"
"QTreeView::item:selected {\n"
"    border: 1px solid transparent;\n"
"}\n"
"QTreeView::item:selected:active{\n"
"    background: rgba(82, 133, 166, 255);\n"
"    border: 1px solid transparent;\n"
"}\n"
"QTreeView::item:selected:!active {\n"
"    background: rgba(82, 133, 166, 255);\n"
"    border: 1px solid transparent;\n"
"}\n"
"QTreeView::item:selected{\n"
"    selection-background-color: transparent;\n"
"    border: 1px solid transparent;\n"
"}\n"
"QDockWidget::title{\n"
"    padding: 4px;\n"
"    border-radius: 3px;\n"
"    padding-left: 10px;\n"
"    background-color: rgba(0,0,0,64);\n"
"}\n"
"QDockWidget::close-button, QDockWidget::float-button {\n"
"    padding: 0px;\n"
"}\n"
"\n"
"QDockWidget {\n"
"    border: 0px ;\n"
"    border-radius: 0px;\n"
"}\n"
"QDockWidget::close-button {\n"
"    border: none;\n"
"}\n"
"QTabWidget::pane {\n"
"    border: 0px;\n"
"}\n"
"QTabBar::tab {\n"
"    background: transparent;\n"
"    border: 2px solid transparent;\n"
"    border-top-right-radius: 0px;\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-right-radius: 3px;\n"
"    border-bottom-left-radius: 3px;\n"
"    padding: 4px;\n"
"}\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(255, 255, 255, 32), stop: 1 rgba(255, 255, 255, 48));\n"
"}\n"
"QTabBar::tab:selected {\n"
"    border-color: transparent;\n"
"}\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 0px;\n"
"}\n"
"QGroupBox {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(175, 175, 175, 16), stop: 1 rgba(0, 0, 0, 0));\n"
"    border: 0px;\n"
"    border-radius: 4px;\n"
"    padding: 0px 8px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: left top; \n"
"    padding: 2 6px;\n"
"    background-color: transparent;\n"
"    border-bottom: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(128, 128, 128, 64), stop:1 rgba(128, 128,128, 0));\n"
"}\n"
"")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow.setWindowFilePath("")
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowNestedDocks|QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        self.mainwidget = QtGui.QWidget(MainWindow)
        self.mainwidget.setObjectName("mainwidget")
        MainWindow.setCentralWidget(self.mainwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 96, 21))
        self.menubar.setObjectName("menubar")
        self.menuConfig = QtGui.QMenu(self.menubar)
        self.menuConfig.setObjectName("menuConfig")
        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setTearOffEnabled(True)
        self.menuProject.setObjectName("menuProject")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.actionConfiguration = QtGui.QAction(MainWindow)
        self.actionConfiguration.setObjectName("actionConfiguration")
        self.actionUpdate = QtGui.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionApply_to_all_Tabs = QtGui.QAction(MainWindow)
        self.actionApply_to_all_Tabs.setObjectName("actionApply_to_all_Tabs")
        self.actionServerside_Script = QtGui.QAction(MainWindow)
        self.actionServerside_Script.setObjectName("actionServerside_Script")
        self.actionDock_undock = QtGui.QAction(MainWindow)
        self.actionDock_undock.setObjectName("actionDock_undock")
        self.actionDebug_Log = QtGui.QAction(MainWindow)
        self.actionDebug_Log.setObjectName("actionDebug_Log")
        self.actionCheckin_Checkout = QtGui.QAction(MainWindow)
        self.actionCheckin_Checkout.setCheckable(True)
        self.actionCheckin_Checkout.setChecked(True)
        self.actionCheckin_Checkout.setObjectName("actionCheckin_Checkout")
        self.actionMy_Tactic = QtGui.QAction(MainWindow)
        self.actionMy_Tactic.setCheckable(True)
        self.actionMy_Tactic.setObjectName("actionMy_Tactic")
        self.actionAssets_browser = QtGui.QAction(MainWindow)
        self.actionAssets_browser.setObjectName("actionAssets_browser")
        self.menuConfig.addAction(self.actionConfiguration)
        self.menuConfig.addAction(self.actionApply_to_all_Tabs)
        self.menuConfig.addAction(self.actionDock_undock)
        self.menuConfig.addSeparator()
        self.menuConfig.addAction(self.actionServerside_Script)
        self.menuConfig.addAction(self.actionDebug_Log)
        self.menuConfig.addSeparator()
        self.menuConfig.addAction(self.actionUpdate)
        self.menuConfig.addSeparator()
        self.menuConfig.addSeparator()
        self.menuConfig.addAction(self.actionExit)
        self.menuView.addAction(self.actionCheckin_Checkout)
        self.menuView.addAction(self.actionMy_Tactic)
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(u"TACTIC handler")
        self.menuConfig.setTitle(u"Menu")
        self.menuProject.setTitle(u"Project")
        self.menuView.setTitle(u"View")
        self.actionConfiguration.setText(u"Configuration")
        self.actionUpdate.setText(u"Update")
        self.actionExit.setText(u"Exit")
        self.actionApply_to_all_Tabs.setText(u"Current view to All Tabs")
        self.actionServerside_Script.setText(u"Serverside Script")
        self.actionDock_undock.setText(u"Dock/undock")
        self.actionDebug_Log.setText(u"Debug Log")
        self.actionCheckin_Checkout.setText(u"Checkin / Checkout")
        self.actionMy_Tactic.setText(u"My Tactic")
        self.actionAssets_browser.setText(u"Assets browser")

