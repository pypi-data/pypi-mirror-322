import random
import typing

import PySide6
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsItem

import weakref
import math
import logging

from famegui.database.prebuild_queries.consts_from_settings import get_setting_value, FameContractGraphItemSettings


class ContractGraphItem(QtWidgets.QGraphicsItem):
    """Graphical representation of a contract between two agents.
    Note: do not register listeners here, instead use -> scenario_graph_view.py"""

    Type = QGraphicsItem.UserType + 1
    _highlight = False
    _single_highlight = False

    def __init__(self, sourceNode, destNode):
        # sourceNode: AgentGraphItem (sender), destNode: AgentGraphItem (receiver)
        QGraphicsItem.__init__(self)
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self._arrow_size = 10.0
        self.CURVE_DEGREE = int(get_setting_value(FameContractGraphItemSettings.CONTRACT_LINE_ANGLE,
                                              20))  # Initialize CURVE_DEGREE here
        self._draw_line = QtCore.QLineF()
        self._control_point = QtCore.QPointF()
        self.source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.source().addEdge(self)
        self.dest().addEdge(self)
        self.adjust()
        self._dotted_line = True  # Randomly choose if line is dotted

    def type(self):
        """override QGraphicsItem.type()"""
        return ContractGraphItem.Type

    def sourceNode(self):
        return self.source()

    def setSourceNode(self, node):
        if node is None:
            self.source = None
            return
        self.source = weakref.ref(node)
        self.adjust()

    def destNode(self):
        return self.dest()

    def setDestNode(self, node):
        if node is None:
            self.dest = None
            return
        self.dest = weakref.ref(node)
        self.adjust()

    def set_highlight_mode(self, highlight_enabled):
        if not highlight_enabled:
            self._single_highlight = False

        self._highlight = highlight_enabled
        self._dotted_line = not highlight_enabled

    def set_single_highlight_mode(self, highlight_enabled):
        self._single_highlight = highlight_enabled

    def adjust(self):
        self._draw_line = QtCore.QLineF()
        if not self.source() or not self.dest():
            return
        radius = 50
        src_center = self.mapFromItem(self.source(), radius, radius)
        dest_center = self.mapFromItem(self.dest(), radius, radius)

        distance_x = dest_center.x() - src_center.x()
        distance_y = dest_center.y() - src_center.y()
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance <= radius * 2:
            return

        offset_ratio = radius / distance
        offset_x = distance_x * offset_ratio
        offset_y = distance_y * offset_ratio

        self.prepareGeometryChange()
        line_start = src_center + QtCore.QPointF(offset_x, offset_y)
        line_end = dest_center - QtCore.QPointF(offset_x, offset_y)
        self._draw_line = QtCore.QLineF(line_start, line_end)

        # Calculate control point for the curve using CURVE_DEGREE
        mid_point = (line_start + line_end) / 2
        angle = math.atan2(distance_y, distance_x) + math.radians(90)  # Perpendicular angle
        curve_distance = distance * math.tan(math.radians(self.CURVE_DEGREE)) / 2
        self._control_point = mid_point + QtCore.QPointF(math.cos(angle) * curve_distance,
                                                         math.sin(angle) * curve_distance)

    def is_in_highlight_mode(self):
        return self._highlight

    def boundingRect(self):
        if not self.source() or not self.dest():
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self._arrow_size) / 2.0
        size = QtCore.QSizeF(
            self._draw_line.x2() - self._draw_line.x1(),
            self._draw_line.y2() - self._draw_line.y1(),
        )

        control_point_bounds = QtCore.QRectF(self._control_point - QtCore.QPointF(extra, extra),
                                             QtCore.QSizeF(extra * 2, extra * 2))

        line_bounds = QtCore.QRectF(self._draw_line.p1(), size).normalized().adjusted(-extra, -extra, extra, extra)

        return line_bounds.united(control_point_bounds)

    def paint(self, painter, option, widget):
        if not self.source() or not self.dest():
            return

        # Draw the curve
        if self._draw_line.length() == 0.0:
            return

        color = QtCore.Qt.black
        pen_stroke = 2

        if self._highlight:
            color = QtGui.QColor("#ff1100")  # Red

        if self._single_highlight:
            pen_stroke = 5

        if self._dotted_line:
            pen_style = QtCore.Qt.DotLine
        else:
            pen_style = QtCore.Qt.SolidLine

        painter.setPen(
            QtGui.QPen(
                color,
                pen_stroke,
                pen_style,
                QtCore.Qt.RoundCap,
                QtCore.Qt.RoundJoin,
            )
        )

        path = QtGui.QPainterPath()
        path.moveTo(self._draw_line.p1())
        path.quadTo(self._control_point, self._draw_line.p2())
        painter.drawPath(path)

        # Draw the arrows if there's enough room.
        angle = math.acos(self._draw_line.dx() / self._draw_line.length())
        if self._draw_line.dy() >= 0:
            angle = (2.0 * math.pi) - angle

        line_end = self._draw_line.p2()
        destArrowP1 = line_end + QtCore.QPointF(
            math.sin(angle - math.pi / 3) * self._arrow_size,
            math.cos(angle - math.pi / 3) * self._arrow_size,
        )
        destArrowP2 = line_end + QtCore.QPointF(
            math.sin(angle - math.pi + math.pi / 3) * self._arrow_size,
            math.cos(angle - math.pi + math.pi / 3) * self._arrow_size,
        )

        painter.setBrush(color)
        painter.drawPolygon(
            QtGui.QPolygonF([self._draw_line.p2(), destArrowP1, destArrowP2])
        )
