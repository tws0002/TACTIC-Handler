# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conf\ui_checkinPage.ui'
#
# Created: Sat Dec 23 23:51:24 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from lib.side.Qt import QtWidgets as QtGui
from lib.side.Qt import QtCore

class Ui_checkinPageWidget(object):
    def setupUi(self, checkinPageWidget):
        checkinPageWidget.setObjectName("checkinPageWidget")
        self.checkinPageWidgetLayout = QtGui.QVBoxLayout(checkinPageWidget)
        self.checkinPageWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.checkinPageWidgetLayout.setObjectName("checkinPageWidgetLayout")
        self.checkinMiscOptionsGroupBox = QtGui.QGroupBox(checkinPageWidget)
        self.checkinMiscOptionsGroupBox.setFlat(True)
        self.checkinMiscOptionsGroupBox.setObjectName("checkinMiscOptionsGroupBox")
        self.checkinMiscOptionsLayout = QtGui.QGridLayout(self.checkinMiscOptionsGroupBox)
        self.checkinMiscOptionsLayout.setContentsMargins(9, -1, 0, 0)
        self.checkinMiscOptionsLayout.setObjectName("checkinMiscOptionsLayout")
        self.versionsSeparateCheckinCheckBox = QtGui.QCheckBox(self.checkinMiscOptionsGroupBox)
        self.versionsSeparateCheckinCheckBox.setObjectName("versionsSeparateCheckinCheckBox")
        self.checkinMiscOptionsLayout.addWidget(self.versionsSeparateCheckinCheckBox, 2, 0, 1, 1)
        self.snapshotDescriptionLimitCheckBox = QtGui.QCheckBox(self.checkinMiscOptionsGroupBox)
        self.snapshotDescriptionLimitCheckBox.setChecked(True)
        self.snapshotDescriptionLimitCheckBox.setObjectName("snapshotDescriptionLimitCheckBox")
        self.checkinMiscOptionsLayout.addWidget(self.snapshotDescriptionLimitCheckBox, 4, 0, 1, 1)
        self.doubleClickSaveCheckBox = QtGui.QCheckBox(self.checkinMiscOptionsGroupBox)
        self.doubleClickSaveCheckBox.setObjectName("doubleClickSaveCheckBox")
        self.checkinMiscOptionsLayout.addWidget(self.doubleClickSaveCheckBox, 0, 0, 1, 1)
        self.doubleClickOpenCheckBox = QtGui.QCheckBox(self.checkinMiscOptionsGroupBox)
        self.doubleClickOpenCheckBox.setObjectName("doubleClickOpenCheckBox")
        self.checkinMiscOptionsLayout.addWidget(self.doubleClickOpenCheckBox, 1, 0, 1, 1)
        self.snapshotDescriptionLimitSpinBox = QtGui.QSpinBox(self.checkinMiscOptionsGroupBox)
        self.snapshotDescriptionLimitSpinBox.setMinimum(20)
        self.snapshotDescriptionLimitSpinBox.setMaximum(50000)
        self.snapshotDescriptionLimitSpinBox.setSingleStep(5)
        self.snapshotDescriptionLimitSpinBox.setProperty("value", 80)
        self.snapshotDescriptionLimitSpinBox.setObjectName("snapshotDescriptionLimitSpinBox")
        self.checkinMiscOptionsLayout.addWidget(self.snapshotDescriptionLimitSpinBox, 4, 2, 1, 1)
        self.bottomVersionsRadioButton = QtGui.QRadioButton(self.checkinMiscOptionsGroupBox)
        self.bottomVersionsRadioButton.setObjectName("bottomVersionsRadioButton")
        self.checkinMiscOptionsLayout.addWidget(self.bottomVersionsRadioButton, 2, 1, 1, 1)
        self.rightVersionsRadioButton = QtGui.QRadioButton(self.checkinMiscOptionsGroupBox)
        self.rightVersionsRadioButton.setChecked(True)
        self.rightVersionsRadioButton.setObjectName("rightVersionsRadioButton")
        self.checkinMiscOptionsLayout.addWidget(self.rightVersionsRadioButton, 2, 2, 1, 1)
        self.checkinMiscOptionsLayout.setColumnStretch(0, 1)
        self.checkinPageWidgetLayout.addWidget(self.checkinMiscOptionsGroupBox)
        self.snapshotsSavingOptionsGroupBox = QtGui.QGroupBox(checkinPageWidget)
        self.snapshotsSavingOptionsGroupBox.setFlat(True)
        self.snapshotsSavingOptionsGroupBox.setObjectName("snapshotsSavingOptionsGroupBox")
        self.snapshotsSavingOptionsLayout = QtGui.QGridLayout(self.snapshotsSavingOptionsGroupBox)
        self.snapshotsSavingOptionsLayout.setContentsMargins(9, -1, 0, 0)
        self.snapshotsSavingOptionsLayout.setObjectName("snapshotsSavingOptionsLayout")
        self.checkinMethodLabel = QtGui.QLabel(self.snapshotsSavingOptionsGroupBox)
        self.checkinMethodLabel.setObjectName("checkinMethodLabel")
        self.snapshotsSavingOptionsLayout.addWidget(self.checkinMethodLabel, 2, 0, 1, 1)
        self.updateVersionlessCheckBox = QtGui.QCheckBox(self.snapshotsSavingOptionsGroupBox)
        self.updateVersionlessCheckBox.setChecked(True)
        self.updateVersionlessCheckBox.setObjectName("updateVersionlessCheckBox")
        self.snapshotsSavingOptionsLayout.addWidget(self.updateVersionlessCheckBox, 3, 0, 1, 1)
        self.createMayaDirsCheckBox = QtGui.QCheckBox(self.snapshotsSavingOptionsGroupBox)
        self.createMayaDirsCheckBox.setObjectName("createMayaDirsCheckBox")
        self.snapshotsSavingOptionsLayout.addWidget(self.createMayaDirsCheckBox, 5, 0, 1, 1)
        self.generatePreviewsCheckBox = QtGui.QCheckBox(self.snapshotsSavingOptionsGroupBox)
        self.generatePreviewsCheckBox.setChecked(True)
        self.generatePreviewsCheckBox.setObjectName("generatePreviewsCheckBox")
        self.snapshotsSavingOptionsLayout.addWidget(self.generatePreviewsCheckBox, 4, 0, 1, 1)
        self.repositoryLabel = QtGui.QLabel(self.snapshotsSavingOptionsGroupBox)
        self.repositoryLabel.setObjectName("repositoryLabel")
        self.snapshotsSavingOptionsLayout.addWidget(self.repositoryLabel, 1, 0, 1, 1)
        self.sequencePaddingCheckBox = QtGui.QCheckBox(self.snapshotsSavingOptionsGroupBox)
        self.sequencePaddingCheckBox.setObjectName("sequencePaddingCheckBox")
        self.snapshotsSavingOptionsLayout.addWidget(self.sequencePaddingCheckBox, 9, 0, 1, 1)
        self.sequqnceNamingTemplatelabel = QtGui.QLabel(self.snapshotsSavingOptionsGroupBox)
        self.sequqnceNamingTemplatelabel.setObjectName("sequqnceNamingTemplatelabel")
        self.snapshotsSavingOptionsLayout.addWidget(self.sequqnceNamingTemplatelabel, 10, 0, 1, 1)
        self.seuqenceNamingHorizontalLayout = QtGui.QHBoxLayout()
        self.seuqenceNamingHorizontalLayout.setSpacing(4)
        self.seuqenceNamingHorizontalLayout.setObjectName("seuqenceNamingHorizontalLayout")
        self.sequenceNamingTemplateLineEdit = QtGui.QLineEdit(self.snapshotsSavingOptionsGroupBox)
        self.sequenceNamingTemplateLineEdit.setReadOnly(True)
        self.sequenceNamingTemplateLineEdit.setObjectName("sequenceNamingTemplateLineEdit")
        self.seuqenceNamingHorizontalLayout.addWidget(self.sequenceNamingTemplateLineEdit)
        self.editSequenceNamingTemplateToolButton = QtGui.QToolButton(self.snapshotsSavingOptionsGroupBox)
        self.editSequenceNamingTemplateToolButton.setText("")
        self.editSequenceNamingTemplateToolButton.setAutoRaise(True)
        self.editSequenceNamingTemplateToolButton.setObjectName("editSequenceNamingTemplateToolButton")
        self.seuqenceNamingHorizontalLayout.addWidget(self.editSequenceNamingTemplateToolButton)
        self.seuqenceNamingHorizontalLayout.setStretch(0, 1)
        self.snapshotsSavingOptionsLayout.addLayout(self.seuqenceNamingHorizontalLayout, 10, 1, 1, 3)
        self.sequencePaddingHorizontalLayout = QtGui.QHBoxLayout()
        self.sequencePaddingHorizontalLayout.setSpacing(4)
        self.sequencePaddingHorizontalLayout.setObjectName("sequencePaddingHorizontalLayout")
        self.sequencePaddingHorizontalSlider = QtGui.QSlider(self.snapshotsSavingOptionsGroupBox)
        self.sequencePaddingHorizontalSlider.setMinimum(1)
        self.sequencePaddingHorizontalSlider.setMaximum(9)
        self.sequencePaddingHorizontalSlider.setProperty("value", 3)
        self.sequencePaddingHorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sequencePaddingHorizontalSlider.setObjectName("sequencePaddingHorizontalSlider")
        self.sequencePaddingHorizontalLayout.addWidget(self.sequencePaddingHorizontalSlider)
        self.sequencePaddingSpinBox = QtGui.QSpinBox(self.snapshotsSavingOptionsGroupBox)
        self.sequencePaddingSpinBox.setMinimum(1)
        self.sequencePaddingSpinBox.setMaximum(9)
        self.sequencePaddingSpinBox.setProperty("value", 3)
        self.sequencePaddingSpinBox.setObjectName("sequencePaddingSpinBox")
        self.sequencePaddingHorizontalLayout.addWidget(self.sequencePaddingSpinBox)
        self.sequencePaddingHorizontalLayout.setStretch(0, 1)
        self.snapshotsSavingOptionsLayout.addLayout(self.sequencePaddingHorizontalLayout, 9, 1, 1, 3)
        self.checkinMethodComboBox = QtGui.QComboBox(self.snapshotsSavingOptionsGroupBox)
        self.checkinMethodComboBox.setObjectName("checkinMethodComboBox")
        self.checkinMethodComboBox.addItem("")
        self.checkinMethodComboBox.addItem("")
        self.checkinMethodComboBox.addItem("")
        self.checkinMethodComboBox.addItem("")
        self.checkinMethodComboBox.addItem("")
        self.snapshotsSavingOptionsLayout.addWidget(self.checkinMethodComboBox, 2, 1, 1, 3)
        self.confirmsHorizontalLayout = QtGui.QHBoxLayout()
        self.confirmsHorizontalLayout.setSpacing(0)
        self.confirmsHorizontalLayout.setObjectName("confirmsHorizontalLayout")
        self.askBeforeSaveCheckBox = QtGui.QCheckBox(self.snapshotsSavingOptionsGroupBox)
        self.askBeforeSaveCheckBox.setChecked(True)
        self.askBeforeSaveCheckBox.setObjectName("askBeforeSaveCheckBox")
        self.confirmsHorizontalLayout.addWidget(self.askBeforeSaveCheckBox)
        self.askReplaceRevisionCheckBox = QtGui.QCheckBox(self.snapshotsSavingOptionsGroupBox)
        self.askReplaceRevisionCheckBox.setChecked(True)
        self.askReplaceRevisionCheckBox.setObjectName("askReplaceRevisionCheckBox")
        self.confirmsHorizontalLayout.addWidget(self.askReplaceRevisionCheckBox)
        self.snapshotsSavingOptionsLayout.addLayout(self.confirmsHorizontalLayout, 7, 0, 1, 4)
        self.repositoryComboBox = QtGui.QComboBox(self.snapshotsSavingOptionsGroupBox)
        self.repositoryComboBox.setObjectName("repositoryComboBox")
        self.snapshotsSavingOptionsLayout.addWidget(self.repositoryComboBox, 1, 1, 1, 3)
        self.createPlayblastCheckBox = QtGui.QCheckBox(self.snapshotsSavingOptionsGroupBox)
        self.createPlayblastCheckBox.setChecked(True)
        self.createPlayblastCheckBox.setObjectName("createPlayblastCheckBox")
        self.snapshotsSavingOptionsLayout.addWidget(self.createPlayblastCheckBox, 6, 0, 1, 1)
        self.checkinPageWidgetLayout.addWidget(self.snapshotsSavingOptionsGroupBox)
        self.dropPlateOptionsGroupBox = QtGui.QGroupBox(checkinPageWidget)
        self.dropPlateOptionsGroupBox.setFlat(True)
        self.dropPlateOptionsGroupBox.setObjectName("dropPlateOptionsGroupBox")
        self.dropPlateOptionsLayout = QtGui.QGridLayout(self.dropPlateOptionsGroupBox)
        self.dropPlateOptionsLayout.setContentsMargins(-1, -1, 0, 0)
        self.dropPlateOptionsLayout.setObjectName("dropPlateOptionsLayout")
        self.clearDropPlateAfterCheckincheckBox = QtGui.QCheckBox(self.dropPlateOptionsGroupBox)
        self.clearDropPlateAfterCheckincheckBox.setObjectName("clearDropPlateAfterCheckincheckBox")
        self.dropPlateOptionsLayout.addWidget(self.clearDropPlateAfterCheckincheckBox, 1, 0, 1, 1)
        self.uncheckFromDropPlateCheckBox = QtGui.QCheckBox(self.dropPlateOptionsGroupBox)
        self.uncheckFromDropPlateCheckBox.setObjectName("uncheckFromDropPlateCheckBox")
        self.dropPlateOptionsLayout.addWidget(self.uncheckFromDropPlateCheckBox, 0, 0, 1, 1)
        self.checkinPageWidgetLayout.addWidget(self.dropPlateOptionsGroupBox)
        self.defaultRepoPathsGroupBox = QtGui.QGroupBox(checkinPageWidget)
        self.defaultRepoPathsGroupBox.setFlat(True)
        self.defaultRepoPathsGroupBox.setObjectName("defaultRepoPathsGroupBox")
        self.defaultRepoPathsLayout = QtGui.QGridLayout(self.defaultRepoPathsGroupBox)
        self.defaultRepoPathsLayout.setContentsMargins(9, 9, 0, 0)
        self.defaultRepoPathsLayout.setObjectName("defaultRepoPathsLayout")
        self.assetBaseDirPathLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.assetBaseDirPathLineEdit.setObjectName("assetBaseDirPathLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.assetBaseDirPathLineEdit, 0, 3, 1, 1)
        self.handoffDirPathLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.handoffDirPathLineEdit.setObjectName("handoffDirPathLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.handoffDirPathLineEdit, 4, 2, 1, 2)
        self.sandboxDirPathLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.sandboxDirPathLineEdit.setObjectName("sandboxDirPathLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.sandboxDirPathLineEdit, 1, 3, 1, 1)
        self.localRepoDirPathLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.localRepoDirPathLineEdit.setObjectName("localRepoDirPathLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.localRepoDirPathLineEdit, 2, 3, 1, 1)
        self.clientRepoDirPathLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.clientRepoDirPathLineEdit.setObjectName("clientRepoDirPathLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.clientRepoDirPathLineEdit, 3, 3, 1, 1)
        self.assetBaseDirCheckBox = QtGui.QCheckBox(self.defaultRepoPathsGroupBox)
        self.assetBaseDirCheckBox.setChecked(True)
        self.assetBaseDirCheckBox.setObjectName("assetBaseDirCheckBox")
        self.defaultRepoPathsLayout.addWidget(self.assetBaseDirCheckBox, 0, 0, 1, 1)
        self.sandboxCheckBox = QtGui.QCheckBox(self.defaultRepoPathsGroupBox)
        self.sandboxCheckBox.setObjectName("sandboxCheckBox")
        self.defaultRepoPathsLayout.addWidget(self.sandboxCheckBox, 1, 0, 1, 1)
        self.localRepoCheckBox = QtGui.QCheckBox(self.defaultRepoPathsGroupBox)
        self.localRepoCheckBox.setChecked(True)
        self.localRepoCheckBox.setObjectName("localRepoCheckBox")
        self.defaultRepoPathsLayout.addWidget(self.localRepoCheckBox, 2, 0, 1, 1)
        self.clientRepoCheckBox = QtGui.QCheckBox(self.defaultRepoPathsGroupBox)
        self.clientRepoCheckBox.setObjectName("clientRepoCheckBox")
        self.defaultRepoPathsLayout.addWidget(self.clientRepoCheckBox, 3, 0, 1, 1)
        self.handoffCheckBox = QtGui.QCheckBox(self.defaultRepoPathsGroupBox)
        self.handoffCheckBox.setObjectName("handoffCheckBox")
        self.defaultRepoPathsLayout.addWidget(self.handoffCheckBox, 4, 0, 1, 1)
        self.assetBaseDirNameLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.assetBaseDirNameLineEdit.setObjectName("assetBaseDirNameLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.assetBaseDirNameLineEdit, 0, 2, 1, 1)
        self.sandboxDirNameLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.sandboxDirNameLineEdit.setObjectName("sandboxDirNameLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.sandboxDirNameLineEdit, 1, 2, 1, 1)
        self.localRepoDirNameLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.localRepoDirNameLineEdit.setObjectName("localRepoDirNameLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.localRepoDirNameLineEdit, 2, 2, 1, 1)
        self.clientRepoDirNameLineEdit = QtGui.QLineEdit(self.defaultRepoPathsGroupBox)
        self.clientRepoDirNameLineEdit.setObjectName("clientRepoDirNameLineEdit")
        self.defaultRepoPathsLayout.addWidget(self.clientRepoDirNameLineEdit, 3, 2, 1, 1)
        self.assetBaseDirColorToolButton = QtGui.QToolButton(self.defaultRepoPathsGroupBox)
        self.assetBaseDirColorToolButton.setMaximumSize(QtCore.QSize(20, 20))
        self.assetBaseDirColorToolButton.setStyleSheet("QToolButton {\n"
"    border: 1px solid rgb(128, 128, 128);\n"
"    border-radius: 4px;\n"
"    background-color:  rgb(96, 96, 96);\n"
"}\n"
"QToolButton:pressed {\n"
"    background-color: rgb(64, 64, 64);\n"
"}")
        self.assetBaseDirColorToolButton.setChecked(False)
        self.assetBaseDirColorToolButton.setObjectName("assetBaseDirColorToolButton")
        self.defaultRepoPathsLayout.addWidget(self.assetBaseDirColorToolButton, 0, 1, 1, 1)
        self.sandboxDirColorToolButton = QtGui.QToolButton(self.defaultRepoPathsGroupBox)
        self.sandboxDirColorToolButton.setMaximumSize(QtCore.QSize(20, 20))
        self.sandboxDirColorToolButton.setStyleSheet("QToolButton {\n"
"    border: 1px solid rgb(128, 128, 128);\n"
"    border-radius: 4px;\n"
"    background-color:  rgb(128, 64, 64);\n"
"}\n"
"QToolButton:pressed {\n"
"    background-color: rgb(108, 44, 44);\n"
"}")
        self.sandboxDirColorToolButton.setChecked(False)
        self.sandboxDirColorToolButton.setObjectName("sandboxDirColorToolButton")
        self.defaultRepoPathsLayout.addWidget(self.sandboxDirColorToolButton, 1, 1, 1, 1)
        self.clientRepoDirColorToolButton = QtGui.QToolButton(self.defaultRepoPathsGroupBox)
        self.clientRepoDirColorToolButton.setMaximumSize(QtCore.QSize(20, 20))
        self.clientRepoDirColorToolButton.setStyleSheet("QToolButton {\n"
"    border: 1px solid rgb(128, 128, 128);\n"
"    border-radius: 4px;\n"
"    background-color:  rgb(31, 143, 0);\n"
"}\n"
"QToolButton:pressed {\n"
"    background-color: rgb(11, 123, 0);\n"
"}")
        self.clientRepoDirColorToolButton.setChecked(False)
        self.clientRepoDirColorToolButton.setObjectName("clientRepoDirColorToolButton")
        self.defaultRepoPathsLayout.addWidget(self.clientRepoDirColorToolButton, 3, 1, 1, 1)
        self.localRepoDirColorToolButton = QtGui.QToolButton(self.defaultRepoPathsGroupBox)
        self.localRepoDirColorToolButton.setMaximumSize(QtCore.QSize(20, 20))
        self.localRepoDirColorToolButton.setStyleSheet("QToolButton {\n"
"    border: 1px solid rgb(128, 128, 128);\n"
"    border-radius: 4px;\n"
"    background-color:  rgb(255, 140, 40);\n"
"}\n"
"QToolButton:pressed {\n"
"    background-color: rgb(235, 120, 20);\n"
"}")
        self.localRepoDirColorToolButton.setChecked(False)
        self.localRepoDirColorToolButton.setObjectName("localRepoDirColorToolButton")
        self.defaultRepoPathsLayout.addWidget(self.localRepoDirColorToolButton, 2, 1, 1, 1)
        self.defaultRepoPathsLayout.setColumnStretch(3, 1)
        self.checkinPageWidgetLayout.addWidget(self.defaultRepoPathsGroupBox)
        self.customRepoPathsGroupBox = QtGui.QGroupBox(checkinPageWidget)
        self.customRepoPathsGroupBox.setEnabled(True)
        self.customRepoPathsGroupBox.setFlat(True)
        self.customRepoPathsGroupBox.setCheckable(True)
        self.customRepoPathsGroupBox.setChecked(False)
        self.customRepoPathsGroupBox.setObjectName("customRepoPathsGroupBox")
        self.customRepoPathsLayout = QtGui.QGridLayout(self.customRepoPathsGroupBox)
        self.customRepoPathsLayout.setContentsMargins(9, -1, 0, -1)
        self.customRepoPathsLayout.setObjectName("customRepoPathsLayout")
        self.label_7 = QtGui.QLabel(self.customRepoPathsGroupBox)
        self.label_7.setObjectName("label_7")
        self.customRepoPathsLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.customRepoDirColorToolButton = QtGui.QToolButton(self.customRepoPathsGroupBox)
        self.customRepoDirColorToolButton.setMaximumSize(QtCore.QSize(20, 20))
        self.customRepoDirColorToolButton.setStyleSheet("QToolButton {\n"
"    border: 1px solid rgb(128, 128, 128);\n"
"    border-radius: 4px;\n"
"    background-color:  rgb(64, 64, 64);\n"
"}\n"
"QToolButton:pressed {\n"
"    background-color: rgb(44, 44, 44);\n"
"}")
        self.customRepoDirColorToolButton.setChecked(False)
        self.customRepoDirColorToolButton.setObjectName("customRepoDirColorToolButton")
        self.customRepoPathsLayout.addWidget(self.customRepoDirColorToolButton, 0, 1, 1, 1)
        self.customRepoDirNameLineEdit = QtGui.QLineEdit(self.customRepoPathsGroupBox)
        self.customRepoDirNameLineEdit.setObjectName("customRepoDirNameLineEdit")
        self.customRepoPathsLayout.addWidget(self.customRepoDirNameLineEdit, 0, 2, 1, 3)
        self.label_8 = QtGui.QLabel(self.customRepoPathsGroupBox)
        self.label_8.setObjectName("label_8")
        self.customRepoPathsLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.customRepoDirPathLineEdit = QtGui.QLineEdit(self.customRepoPathsGroupBox)
        self.customRepoDirPathLineEdit.setObjectName("customRepoDirPathLineEdit")
        self.customRepoPathsLayout.addWidget(self.customRepoDirPathLineEdit, 1, 1, 1, 4)
        self.customRepoComboBox = QtGui.QComboBox(self.customRepoPathsGroupBox)
        self.customRepoComboBox.setObjectName("customRepoComboBox")
        self.customRepoPathsLayout.addWidget(self.customRepoComboBox, 2, 0, 1, 1)
        self.addCustomRepoToListPushButton = QtGui.QPushButton(self.customRepoPathsGroupBox)
        self.addCustomRepoToListPushButton.setObjectName("addCustomRepoToListPushButton")
        self.customRepoPathsLayout.addWidget(self.addCustomRepoToListPushButton, 2, 1, 1, 2)
        self.editCustomRepoPushButton = QtGui.QPushButton(self.customRepoPathsGroupBox)
        self.editCustomRepoPushButton.setObjectName("editCustomRepoPushButton")
        self.customRepoPathsLayout.addWidget(self.editCustomRepoPushButton, 2, 3, 1, 1)
        self.deleteCustomRepoPushButton = QtGui.QPushButton(self.customRepoPathsGroupBox)
        self.deleteCustomRepoPushButton.setObjectName("deleteCustomRepoPushButton")
        self.customRepoPathsLayout.addWidget(self.deleteCustomRepoPushButton, 2, 4, 1, 1)
        self.customRepoTreeWidget = QtGui.QTreeWidget(self.customRepoPathsGroupBox)
        self.customRepoTreeWidget.setStyleSheet("QTreeView::item {\n"
"    padding: 2px;\n"
"}")
        self.customRepoTreeWidget.setIndentation(0)
        self.customRepoTreeWidget.setRootIsDecorated(False)
        self.customRepoTreeWidget.setObjectName("customRepoTreeWidget")
        self.customRepoPathsLayout.addWidget(self.customRepoTreeWidget, 3, 0, 1, 5)
        self.checkinPageWidgetLayout.addWidget(self.customRepoPathsGroupBox)

        self.retranslateUi(checkinPageWidget)
        QtCore.QObject.connect(self.sequencePaddingHorizontalSlider, QtCore.SIGNAL("valueChanged(int)"), self.sequencePaddingSpinBox.setValue)
        QtCore.QObject.connect(self.sequencePaddingSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.sequencePaddingHorizontalSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(checkinPageWidget)

    def retranslateUi(self, checkinPageWidget):
        self.checkinMiscOptionsGroupBox.setTitle(QtGui.QApplication.translate("checkinPageWidget", "Search Results Options:", None))
        self.versionsSeparateCheckinCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Display Versions separated:", None))
        self.snapshotDescriptionLimitCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Limit snapshot description preview (symbols):", None))
        self.doubleClickSaveCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "DoubleClick for Save", None))
        self.doubleClickOpenCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Shift + DoubleClick for Open", None))
        self.bottomVersionsRadioButton.setText(QtGui.QApplication.translate("checkinPageWidget", "Bottom", None))
        self.rightVersionsRadioButton.setText(QtGui.QApplication.translate("checkinPageWidget", "Right", None))
        self.snapshotsSavingOptionsGroupBox.setTitle(QtGui.QApplication.translate("checkinPageWidget", "Snapshots Saving Options:", None))
        self.checkinMethodLabel.setText(QtGui.QApplication.translate("checkinPageWidget", "Checkin Method:", None))
        self.updateVersionlessCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Update versionless snapshot", None))
        self.createMayaDirsCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Create Maya Dirs (worspace.mel)", None))
        self.generatePreviewsCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Generate Previews", None))
        self.repositoryLabel.setText(QtGui.QApplication.translate("checkinPageWidget", "Current Repository:", None))
        self.sequencePaddingCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Sequence Padding:", None))
        self.sequqnceNamingTemplatelabel.setText(QtGui.QApplication.translate("checkinPageWidget", "Sequence, udim/uv naming Template:", None))
        self.sequenceNamingTemplateLineEdit.setText(QtGui.QApplication.translate("checkinPageWidget", "$FILENAME_$LAYER_$UDIM/UV.$FRAME.$EXT", None))
        self.checkinMethodComboBox.setItemText(0, QtGui.QApplication.translate("checkinPageWidget", "Preallocate", None))
        self.checkinMethodComboBox.setItemText(1, QtGui.QApplication.translate("checkinPageWidget", "In-Place", None))
        self.checkinMethodComboBox.setItemText(2, QtGui.QApplication.translate("checkinPageWidget", "Copy", None))
        self.checkinMethodComboBox.setItemText(3, QtGui.QApplication.translate("checkinPageWidget", "Move", None))
        self.checkinMethodComboBox.setItemText(4, QtGui.QApplication.translate("checkinPageWidget", "Upload", None))
        self.askBeforeSaveCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Confirm Saving", None))
        self.askReplaceRevisionCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Revision Confirm Saving", None))
        self.createPlayblastCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Create screenshot (playblast)", None))
        self.dropPlateOptionsGroupBox.setTitle(QtGui.QApplication.translate("checkinPageWidget", "Drop Plate Options:", None))
        self.clearDropPlateAfterCheckincheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Clear DropPlate after Checkin", None))
        self.uncheckFromDropPlateCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Uncheck \"From DropPlate\" after Checkin", None))
        self.defaultRepoPathsGroupBox.setTitle(QtGui.QApplication.translate("checkinPageWidget", "Repository Paths:", None))
        self.assetBaseDirCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Asset base dir:", None))
        self.sandboxCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Sandbox dir:", None))
        self.localRepoCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Local repo dir:", None))
        self.clientRepoCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Client repo dir:", None))
        self.handoffCheckBox.setText(QtGui.QApplication.translate("checkinPageWidget", "Use handoff dir:", None))
        self.customRepoPathsGroupBox.setTitle(QtGui.QApplication.translate("checkinPageWidget", "Custom Repository Path:", None))
        self.label_7.setText(QtGui.QApplication.translate("checkinPageWidget", "Custom Repo name:", None))
        self.label_8.setText(QtGui.QApplication.translate("checkinPageWidget", "Repo path:", None))
        self.addCustomRepoToListPushButton.setText(QtGui.QApplication.translate("checkinPageWidget", "Add", None))
        self.editCustomRepoPushButton.setText(QtGui.QApplication.translate("checkinPageWidget", "Edit", None))
        self.deleteCustomRepoPushButton.setText(QtGui.QApplication.translate("checkinPageWidget", "Delete", None))
        self.customRepoTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("checkinPageWidget", "Visible", None))
        self.customRepoTreeWidget.headerItem().setText(1, QtGui.QApplication.translate("checkinPageWidget", "Color", None))
        self.customRepoTreeWidget.headerItem().setText(2, QtGui.QApplication.translate("checkinPageWidget", "Name", None))
        self.customRepoTreeWidget.headerItem().setText(3, QtGui.QApplication.translate("checkinPageWidget", "Path", None))

