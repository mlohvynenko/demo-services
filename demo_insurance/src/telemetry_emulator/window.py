#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

import sys
from collections import deque

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication
from emulator import Emulator, VertexPool


class MainWindow(QWidget):
    PADDING = 40
    TIMER_INTERVAL = 0.4
    EMULATOR_UPDATE_TIME = 0.4
    WIDTH = 1000
    HEIGHT = 700
    CAR_SIZE = 5
    VERTEX_SIZE = 2
    _draw_distance = 500

    KMPH_TO_MPS = 0.277777777777
    MPS_TO_KMPH = 1 / KMPH_TO_MPS

    def __init__(self, emulator):
        # self.file = open('points.txt', 'w')
        super(MainWindow, self).__init__()
        self.setFixedWidth(self.WIDTH + 200)
        self.setFixedHeight(self.HEIGHT)
        self.emulator = emulator
        self._derive_graph_bounds()
        self.i = 0
        self.setWindowTitle("Some title")
        self.fuel_plot = deque(maxlen=200)
        self.steering_wheel_plot = deque(maxlen=200)
        self.timer = QtCore.QBasicTimer()
        self.timer.start(self.TIMER_INTERVAL * 1000, self)

    def _derive_graph_bounds(self):
        vertices = self.emulator.vertex_pool
        self.min_x = min(v.x for v in vertices)
        self.max_x = max(v.x for v in vertices)
        self.min_y = min(v.y for v in vertices)
        self.max_y = max(v.y for v in vertices)

    def timerEvent(self, event, *args, **kwargs):
        self.setWindowTitle("hello {}".format(self.i))
        self.i += 1
        self.emulator.update(self.EMULATOR_UPDATE_TIME)
        self.fuel_plot.append(self.emulator.fuel_consumption)
        self.steering_wheel_plot.append(self.emulator.steering_wheel_angle)
        self.repaint()

        # for debug on site http://share.mapbbcode.org/
        # data = self.emulator.get_data()
        # if self.i % 50:
        #     self.file.write("{},{} ".format(data['lat'], data['lon']))
        # if self.i % 1000 == 0:
        #     self.file.flush()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(QtCore.Qt.gray)
        self._draw_graph(painter)
        self._draw_car(painter)
        self._draw_data(painter)
        if self.fuel_plot:
            self._draw_plot(painter, self.fuel_plot, QtCore.QRect(self.width()-200, self.height()-300, 200, 100), max_value=100)
        if self.steering_wheel_plot:
            self._draw_plot(painter, self.steering_wheel_plot, QtCore.QRect(self.width()-200, self.height()-200, 200, 100), max_value=2000, min_value=-2000)
        painter.end()

    def _draw_graph(self, painter):
        painter.setBrush(QtCore.Qt.black)
        for vertex in self.emulator.vertex_pool:
            if 0 <= self.get_x(vertex.x) <= self.WIDTH and 0 <= self.get_y(vertex.y) <= self.HEIGHT:
                for neighbor_id in vertex.neighbors:
                    neighbor = self.emulator.vertex_pool[neighbor_id]
                    painter.drawLine(
                        self.get_x(vertex.x),
                        self.get_y(vertex.y),
                        self.get_x(neighbor.x),
                        self.get_y(neighbor.y)
                    )

        for vertex in self.emulator.vertex_pool:
            if 0 <= self.get_x(vertex.x) <= self.WIDTH and 0 <= self.get_y(vertex.y) <= self.HEIGHT:
                painter.drawEllipse(QtCore.QRect(
                    self.get_x(vertex.x) - self.VERTEX_SIZE,
                    self.get_y(vertex.y) - self.VERTEX_SIZE,
                    self.VERTEX_SIZE * 2,
                    self.VERTEX_SIZE * 2
                ))
                # painter.drawText(QtCore.QRect(self.get_x(vertex.x), self.get_y(vertex.y), 100, 20), QtCore.Qt.AlignTop, str(vertex.id))

    def _draw_car(self, painter):

        if self.emulator.turn_signal == 0:
            painter.setBrush(QtCore.Qt.transparent)
        elif self.emulator.turn_signal == 1:
            painter.setBrush(QtCore.Qt.red)
        elif self.emulator.turn_signal == 2:
            painter.setBrush(QtCore.Qt.blue)
        elif self.emulator.turn_signal == 3:
            painter.setBrush(QtCore.Qt.green)

        car_rect = QtCore.QRect(
            self.get_x(self.emulator.x) - self.CAR_SIZE,
            self.get_y(self.emulator.y) - self.CAR_SIZE,
            self.CAR_SIZE * 2,
            self.CAR_SIZE * 2
        )
        painter.drawEllipse(car_rect)

    def _draw_data(self, painter):
        painter.setPen(QtCore.Qt.black)
        fields = ['turn_angle', 'x','y', 'lat', 'lon',
                  'madness', 'ticks_till_next_driver', 'xxxx','xxxx',
                  'max_speed', 'max_break', 'stop_signal', 'turn_signal',
                  'acceleration', 'fuel_consumption', 'speed', 'speed_kmph', 'max_turn_speed', 'gear', 'rpm',
                  'odometer', '_distance_till_turn']
        text = []
        for field in fields:
            text.append("{}: {}".format(field, getattr(self.emulator, field, 'WRONG_NAME')))
        text = '\n'.join(text)
        text_rect = QtCore.QRect(self.WIDTH, 0, 200, self.HEIGHT)
        painter.drawText(text_rect, QtCore.Qt.AlignTop, text)

    def _draw_plot(self, painter, plot, rect, max_value, min_value=0):
        c = rect.height() / (max_value - min_value)
        painter.drawLine(rect.left(), rect.top(), rect.right(), rect.top())
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())
        painter.setPen(QtCore.Qt.darkCyan)
        plot_iter = iter(plot)
        prev_value = next(plot_iter)
        for i, value in enumerate(plot_iter):
            painter.drawLine(
                rect.left() + i,
                rect.bottom() - (prev_value - min_value) * c,
                rect.left() + i + 1,
                rect.bottom() - (value - min_value) * c
            )
            prev_value = value
        painter.drawText(rect, QtCore.Qt.AlignTop, str(prev_value))


    def get_x2(self, x):
        return (x - self.min_x) / self._draw_distance * (self.WIDTH - self.PADDING * 2) + self.PADDING
        # return (x - self.min_x) / (self.max_x - self.min_x) * (self.WIDTH - self.PADDING * 2) + self.PADDING

    def get_x(self, x):
        return self.get_x2(x) - self.get_x2(self.emulator.x) + self.WIDTH / 2

    def get_y2(self, y):
        return self.HEIGHT - (y - self.min_y) / self._draw_distance * (self.HEIGHT - self.PADDING * 2) - self.PADDING
        # return self.HEIGHT - (y - self.min_y) / (self.max_y - self.min_y) * (self.HEIGHT - self.PADDING * 2) - self.PADDING

    def get_y(self, y):
        return self.get_y2(y) - self.get_y2(self.emulator.y) + self.HEIGHT / 2

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:  # space
            self.emulator.command_to_stop = not self.emulator.command_to_stop
        elif event.key() == QtCore.Qt.Key_QuoteLeft:  # `
            self.emulator.change_madness_periodically = not self.emulator.change_madness_periodically
        elif event.key() == QtCore.Qt.Key_1:  # 1-key
            self.emulator.madness = 0.1
        elif event.key() == QtCore.Qt.Key_2:  # 2-key
            self.emulator.madness = 1.0

    def wheelEvent(self, event):
        self._draw_distance -= event.angleDelta().y()
        if self._draw_distance <= 0:
            self._draw_distance = 120


sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook


def main():
    vp = VertexPool('map.json')
    emulator = Emulator(vp)

    application = QApplication(sys.argv)
    window = MainWindow(emulator)
    window.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
