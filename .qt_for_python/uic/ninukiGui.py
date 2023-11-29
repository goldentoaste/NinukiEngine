# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ninukiGui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1082, 818)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.graphicsView = QGraphicsView(Form)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout.addWidget(self.graphicsView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.blackScoreLabel = QLabel(Form)
        self.blackScoreLabel.setObjectName(u"blackScoreLabel")
        font = QFont()
        font.setFamilies([u"Courier New"])
        font.setPointSize(12)
        self.blackScoreLabel.setFont(font)

        self.verticalLayout.addWidget(self.blackScoreLabel)

        self.whiteScoreLabel = QLabel(Form)
        self.whiteScoreLabel.setObjectName(u"whiteScoreLabel")
        self.whiteScoreLabel.setFont(font)

        self.verticalLayout.addWidget(self.whiteScoreLabel)

        self.currentPlayerLabel = QLabel(Form)
        self.currentPlayerLabel.setObjectName(u"currentPlayerLabel")
        self.currentPlayerLabel.setFont(font)

        self.verticalLayout.addWidget(self.currentPlayerLabel)

        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Courier New"])
        font1.setPointSize(11)
        self.listWidget.setFont(font1)

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.newGameButton = QPushButton(Form)
        self.newGameButton.setObjectName(u"newGameButton")
        self.newGameButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.newGameButton)

        self.predictButton = QPushButton(Form)
        self.predictButton.setObjectName(u"predictButton")
        self.predictButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.predictButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.blackScoreLabel.setText(QCoreApplication.translate("Form", u"Black Score:", None))
        self.whiteScoreLabel.setText(QCoreApplication.translate("Form", u"White Score", None))
        self.currentPlayerLabel.setText(QCoreApplication.translate("Form", u"Current Player:", None))
        self.newGameButton.setText(QCoreApplication.translate("Form", u"New Game", None))
        self.predictButton.setText(QCoreApplication.translate("Form", u"Predict", None))
    # retranslateUi

