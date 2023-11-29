import random
import sys
import math
import numpy as np
from PyQt6.QtCore import QPoint, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen, QMouseEvent
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QWidget

from alphaBetaPlayer import BLACK, WHITE, AlphaBetaPlayer
from board import Board, WALL, EMPTY
from ninukiGui import Ui_Form

linePen = QPen(QColor("#000000"), 2)
backgroundColor = QColor("#fcecbb")

blackColor = QBrush(QColor("#2b2820"))
whiteColor = QBrush(QColor("#dedede"))


class NinukiWindow(QWidget):
    def __init__(
        self,
    ):

        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # arr = np.zeros((7, 7))
        # for i in range(len(arr)):
        #     for j in range(len(arr[i])):
        #         arr[i][j] = 1 if random.random() > 0.5 else 2

        self.board = Board(7, )

        self.player = AlphaBetaPlayer(self.board)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.ui.graphicsView.mousePressEvent = self.onClick
        self.screenSize = 0

    def showEvent(self, a0) -> None:
        self.screenSize = 800
        self.render()

    def onClick(self, event : QMouseEvent):
        point =  self.roundToNearestPoint(event.pos())

        if self.board.data[point] == WALL:
            return

        self.board.play(*point, self.board.currentColor)

    def roundToNearestPoint(self, point : QPoint):
        
        gap = self.scene.width() / (self.board.size + 1)
        return (
            math.floor((point.y() + gap/2) / gap),
            math.floor((point.x() + gap/2) / gap),
        )

    def render(
        self,
    ):
        self.scene.clear()

        # background
        self.scene.addRect(0, 0, 800, 800, backgroundColor, backgroundColor)

        # draw grid
        size = self.board.size
        width = self.scene.width()
        height = self.scene.height()
        gap = width / (size + 1)
        pieceSize = gap * 0.7
        half = pieceSize / 2

        for i in range(1, size + 1):
            self.scene.addLine(i * gap, gap - 1, i * gap, height - gap, linePen)

        for i in range(1, size + 1):
            self.scene.addLine(gap, i * gap, width - gap, i * gap, linePen)

        self.ui.graphicsView.fitInView(self.scene.sceneRect())

        # draw pieces

        for r in range(1, size + 1):
            for c in range(1, size + 1):
                color = self.board.data[r][c]
                if color != EMPTY:
                    self.scene.addEllipse(
                        r * gap - half,
                        c * gap - half,
                        pieceSize,
                        pieceSize,
                        brush=(blackColor if color == BLACK else whiteColor),
                    )


if __name__ == "__main__":

    a = QApplication(sys.argv)
    w = NinukiWindow()
    w.show()
    sys.exit(a.exec())
