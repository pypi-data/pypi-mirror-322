import random
import typing

import PySide6
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsItem

import weakref
import math
import logging


class AgentGraphItem(QtWidgets.QGraphicsItem, QtCore.QObject):
    """A Agent node in the graph."""

    Type = QGraphicsItem.UserType + 2

    def zValue(self) -> float:
        z_value = 100
        return z_value

    # use a lambda rather than a Qt signal because we don't inherit from QObject
    position_changed = lambda self, x, y: None

    selected_for_edit = False
    start_pos = None

    def set_bg_color(self, color: str):
        self._color = color

    def set_selected_for_edit(self, selected: bool):
        self.selected_for_edit = selected
        self.update()

    def is_selected_for_edit(self):
        return self.selected_for_edit

    def setSelected(self, selected: bool, sender: bool = True) -> None:
        self._in_receiver_mode = sender
        super().setSelected(selected)

    def mousePressEvent(self, event):
        # Capture the start position
        self.start_pos = self.scenePos()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Capture the end position
        self.end_pos = self.scenePos()
        # Emit the signal with start and end positions


        super().mouseReleaseEvent(event)

    def __init__(self, agent_id, label, color):
        QtCore.QObject.__init__(self)  # Initialize QObject

        QGraphicsItem.__init__(self)
        # public
        self.edgeList = []
        # private / read only
        self._label = "#{}".format(agent_id)
        self._color = color
        self._radius = 50
        self._agent_id = agent_id
        self._links = []
        self._highlight_border = False
        self._in_receiver_mode = True
        # customize graphics item
        self._on_agent_dragged = None
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

    def set_on_agent_dragged(self, func):
        self._on_agent_dragged = func

    def type(self):
        """override QGraphicsItem.type()"""
        return AgentGraphItem.Type

    def addEdge(self, edge):
        self.edgeList.append(weakref.ref(edge))
        edge.adjust()

    def set_border_highlight(self, highlight: bool):
        self._highlight_border = highlight

    @property
    def agent_id(self) -> int:
        return self._agent_id

    def add_link(self, link):
        self._links.append(link)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self._radius * 2, self._radius * 2)

    def adjust_contracts(self):
        for contract in self.edgeList:
            contract().adjust()

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for edge in self.edgeList:
                if not edge():
                    continue
                edge().adjust()
            self.position_changed(self.x(), self.y())
        return QGraphicsItem.itemChange(self, change, value)

    def paint(self, painter, option, widget=None):
        """Qt paint method"""
        # main rectangle with its border
        if option.state & QtWidgets.QStyle.StateFlag.State_Selected:
            background_color = QtGui.QColor(self._color).darker()
            border_color = QtGui.QColor("#ff009a")  # red
            border_width = 3
        else:
            background_color = QtGui.QColor(self._color)
            border_color = QtGui.QColor(0, 0, 0)
            border_width = 2
        if not self._in_receiver_mode:
            background_color = QtGui.QColor(self._color).darker()
            border_color = QtGui.QColor("#40ff00")
            border_width = 3

        if self.selected_for_edit:
            background_color = QtGui.QColor(self._color).darker()
            border_color = QtGui.QColor("#4062BB")
            border_width = 4

        item_rect = self.boundingRect()

        painter.setBrush(QtGui.QBrush(background_color))
        painter.setPen(QtGui.QPen(border_color, border_width))
        painter.drawEllipse(item_rect)

        # label
        font = QtGui.QFont("Arial", 14)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.ForceOutline)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
        painter.drawText(item_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self._label)
