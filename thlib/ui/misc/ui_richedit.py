# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'misc/ui_richedit.ui'
#
# Created: Thu Apr 27 14:15:15 2017
#      by: pyside-uic 0.2.13 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from thlib.side.Qt import QtWidgets as QtGui
from thlib.side.Qt import QtGui as Qt4Gui
from thlib.side.Qt import QtCore

class Ui_richedit(object):
    def setupUi(self, richedit):
        richedit.setObjectName("richedit")
        richedit.resize(506, 22)
        self.horizontalLayout = QtGui.QHBoxLayout(richedit)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.boldButton = QtGui.QToolButton(richedit)
        self.boldButton.setToolTip("Set selected Text Bold")
        self.boldButton.setStatusTip("Set selected Text Bold")
        icon = Qt4Gui.QIcon()
        icon.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_bold.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.boldButton.setIcon(icon)
        self.boldButton.setCheckable(True)
        self.boldButton.setAutoRaise(True)
        self.boldButton.setObjectName("boldButton")
        self.horizontalLayout.addWidget(self.boldButton)
        self.italicButton = QtGui.QToolButton(richedit)
        icon1 = Qt4Gui.QIcon()
        icon1.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_italic.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.italicButton.setIcon(icon1)
        self.italicButton.setCheckable(True)
        self.italicButton.setAutoRaise(True)
        self.italicButton.setObjectName("italicButton")
        self.horizontalLayout.addWidget(self.italicButton)
        self.underlinedButton = QtGui.QToolButton(richedit)
        icon2 = Qt4Gui.QIcon()
        icon2.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_underline.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.underlinedButton.setIcon(icon2)
        self.underlinedButton.setCheckable(True)
        self.underlinedButton.setAutoRaise(True)
        self.underlinedButton.setObjectName("underlinedButton")
        self.horizontalLayout.addWidget(self.underlinedButton)
        self.strikedButton = QtGui.QToolButton(richedit)
        self.strikedButton.setText("")
        icon3 = Qt4Gui.QIcon()
        icon3.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_strikethrough.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.strikedButton.setIcon(icon3)
        self.strikedButton.setCheckable(True)
        self.strikedButton.setAutoRaise(True)
        self.strikedButton.setObjectName("strikedButton")
        self.horizontalLayout.addWidget(self.strikedButton)
        self.leftButton = QtGui.QToolButton(richedit)
        self.leftButton.setText("")
        icon4 = Qt4Gui.QIcon()
        icon4.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_align_left.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.leftButton.setIcon(icon4)
        self.leftButton.setCheckable(True)
        self.leftButton.setAutoRaise(True)
        self.leftButton.setObjectName("leftButton")
        self.horizontalLayout.addWidget(self.leftButton)
        self.centerButton = QtGui.QToolButton(richedit)
        self.centerButton.setText("")
        icon5 = Qt4Gui.QIcon()
        icon5.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_align_center.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.centerButton.setIcon(icon5)
        self.centerButton.setCheckable(True)
        self.centerButton.setAutoRaise(True)
        self.centerButton.setObjectName("centerButton")
        self.horizontalLayout.addWidget(self.centerButton)
        self.rightButton = QtGui.QToolButton(richedit)
        self.rightButton.setText("")
        icon6 = Qt4Gui.QIcon()
        icon6.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_align_right.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.rightButton.setIcon(icon6)
        self.rightButton.setCheckable(True)
        self.rightButton.setAutoRaise(True)
        self.rightButton.setObjectName("rightButton")
        self.horizontalLayout.addWidget(self.rightButton)
        self.justButton = QtGui.QToolButton(richedit)
        self.justButton.setText("")
        icon7 = Qt4Gui.QIcon()
        icon7.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_align_justify.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.justButton.setIcon(icon7)
        self.justButton.setCheckable(True)
        self.justButton.setAutoRaise(True)
        self.justButton.setObjectName("justButton")
        self.horizontalLayout.addWidget(self.justButton)
        self.numbersListButton = QtGui.QToolButton(richedit)
        self.numbersListButton.setText("")
        icon8 = Qt4Gui.QIcon()
        icon8.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_list_numbers.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.numbersListButton.setIcon(icon8)
        self.numbersListButton.setAutoRaise(True)
        self.numbersListButton.setObjectName("numbersListButton")
        self.horizontalLayout.addWidget(self.numbersListButton)
        self.bulletsListButton = QtGui.QToolButton(richedit)
        self.bulletsListButton.setText("")
        icon9 = Qt4Gui.QIcon()
        icon9.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_list_bullets.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.bulletsListButton.setIcon(icon9)
        self.bulletsListButton.setAutoRaise(True)
        self.bulletsListButton.setObjectName("bulletsListButton")
        self.horizontalLayout.addWidget(self.bulletsListButton)
        self.downTextButton = QtGui.QToolButton(richedit)
        self.downTextButton.setText("")
        icon10 = Qt4Gui.QIcon()
        icon10.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_subscript.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.downTextButton.setIcon(icon10)
        self.downTextButton.setAutoRaise(True)
        self.downTextButton.setObjectName("downTextButton")
        self.horizontalLayout.addWidget(self.downTextButton)
        self.upTextButton = QtGui.QToolButton(richedit)
        self.upTextButton.setText("")
        icon11 = Qt4Gui.QIcon()
        icon11.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_superscript.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.upTextButton.setIcon(icon11)
        self.upTextButton.setAutoRaise(True)
        self.upTextButton.setObjectName("upTextButton")
        self.horizontalLayout.addWidget(self.upTextButton)
        self.capsButton = QtGui.QToolButton(richedit)
        self.capsButton.setText("")
        icon12 = Qt4Gui.QIcon()
        icon12.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_allcaps.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.capsButton.setIcon(icon12)
        self.capsButton.setAutoRaise(True)
        self.capsButton.setObjectName("capsButton")
        self.horizontalLayout.addWidget(self.capsButton)
        self.smallCapsButton = QtGui.QToolButton(richedit)
        self.smallCapsButton.setText("")
        icon13 = Qt4Gui.QIcon()
        icon13.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/text_smallcaps.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.smallCapsButton.setIcon(icon13)
        self.smallCapsButton.setAutoRaise(True)
        self.smallCapsButton.setObjectName("smallCapsButton")
        self.horizontalLayout.addWidget(self.smallCapsButton)
        self.fontcolorButton = QtGui.QToolButton(richedit)
        self.fontcolorButton.setText("")
        icon14 = Qt4Gui.QIcon()
        icon14.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/color_wheel.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.fontcolorButton.setIcon(icon14)
        self.fontcolorButton.setAutoRaise(True)
        self.fontcolorButton.setObjectName("fontcolorButton")
        self.horizontalLayout.addWidget(self.fontcolorButton)
        self.fontButton = QtGui.QToolButton(richedit)
        self.fontButton.setText("")
        icon15 = Qt4Gui.QIcon()
        icon15.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/font.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.fontButton.setIcon(icon15)
        self.fontButton.setAutoRaise(True)
        self.fontButton.setObjectName("fontButton")
        self.horizontalLayout.addWidget(self.fontButton)
        self.linkButton = QtGui.QToolButton(richedit)
        self.linkButton.setText("")
        icon16 = Qt4Gui.QIcon()
        icon16.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/link_add.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.linkButton.setIcon(icon16)
        self.linkButton.setAutoRaise(True)
        self.linkButton.setObjectName("linkButton")
        self.horizontalLayout.addWidget(self.linkButton)
        self.pictureButton = QtGui.QToolButton(richedit)
        self.pictureButton.setText("")
        icon17 = Qt4Gui.QIcon()
        icon17.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/picture_add.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.pictureButton.setIcon(icon17)
        self.pictureButton.setAutoRaise(True)
        self.pictureButton.setObjectName("pictureButton")
        self.horizontalLayout.addWidget(self.pictureButton)
        self.folderButton = QtGui.QToolButton(richedit)
        self.folderButton.setText("")
        icon18 = Qt4Gui.QIcon()
        icon18.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/folder_add.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.folderButton.setIcon(icon18)
        self.folderButton.setAutoRaise(True)
        self.folderButton.setObjectName("folderButton")
        self.horizontalLayout.addWidget(self.folderButton)
        self.cutButton = QtGui.QToolButton(richedit)
        self.cutButton.setText("")
        icon19 = Qt4Gui.QIcon()
        icon19.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/cut_red.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.cutButton.setIcon(icon19)
        self.cutButton.setAutoRaise(True)
        self.cutButton.setObjectName("cutButton")
        self.horizontalLayout.addWidget(self.cutButton)
        self.copyButton = QtGui.QToolButton(richedit)
        self.copyButton.setText("")
        icon20 = Qt4Gui.QIcon()
        icon20.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/page_white_copy.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.copyButton.setIcon(icon20)
        self.copyButton.setAutoRaise(True)
        self.copyButton.setObjectName("copyButton")
        self.horizontalLayout.addWidget(self.copyButton)
        self.pasteButton = QtGui.QToolButton(richedit)
        self.pasteButton.setText("")
        icon21 = Qt4Gui.QIcon()
        icon21.addPixmap(Qt4Gui.QPixmap(":/ui_richedit/gliph/richedit/page_white_paste.png"), Qt4Gui.QIcon.Normal, Qt4Gui.QIcon.Off)
        self.pasteButton.setIcon(icon21)
        self.pasteButton.setAutoRaise(True)
        self.pasteButton.setObjectName("pasteButton")
        self.horizontalLayout.addWidget(self.pasteButton)
        spacerItem = QtGui.QSpacerItem(0, 8, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(22, 1)

        self.retranslateUi(richedit)
        QtCore.QMetaObject.connectSlotsByName(richedit)
        richedit.setTabOrder(self.boldButton, self.italicButton)
        richedit.setTabOrder(self.italicButton, self.underlinedButton)
        richedit.setTabOrder(self.underlinedButton, self.strikedButton)
        richedit.setTabOrder(self.strikedButton, self.leftButton)
        richedit.setTabOrder(self.leftButton, self.centerButton)
        richedit.setTabOrder(self.centerButton, self.rightButton)
        richedit.setTabOrder(self.rightButton, self.justButton)
        richedit.setTabOrder(self.justButton, self.numbersListButton)
        richedit.setTabOrder(self.numbersListButton, self.fontcolorButton)
        richedit.setTabOrder(self.fontcolorButton, self.pictureButton)
        richedit.setTabOrder(self.pictureButton, self.linkButton)
        richedit.setTabOrder(self.linkButton, self.folderButton)
        richedit.setTabOrder(self.folderButton, self.copyButton)
        richedit.setTabOrder(self.copyButton, self.cutButton)

    def retranslateUi(self, richedit):
        richedit.setWindowTitle(QtGui.QApplication.translate("richedit", "Form", None))

import thlib.ui.resources_rc
