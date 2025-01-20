import PySide6
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QGraphicsView


class MainGraphicsWidget(QGraphicsView):
    unselect_contracts = QtCore.Signal(name="unselect_contracts")
    agent_deletion_requested = QtCore.Signal(object)
    zoom_level_changed = QtCore.Signal(int)  # Signal to communicate zoom level changes

    def __init__(self, parent=None):
        super(MainGraphicsWidget, self).__init__(parent)
        self.startPos = None
        self._zoom_factor = 1.0  # Initialize zoom factor
        self.grabGesture(QtCore.Qt.GestureType.PanGesture)
        self.grabGesture(QtCore.Qt.GestureType.PinchGesture)

    def _get_local_widget_position(self) -> QPoint:
        """transforms the global mouse position to the local widget position"""
        mouse_position = QCursor.pos()
        local_position = self.mapFromGlobal(mouse_position)
        return local_position

    def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        """triggers agent deletion when delete key is pressed"""


        key = event.key()
        if key == Qt.Key.Key_Delete:
            self.agent_deletion_requested.emit(self._get_local_widget_position())
        super().keyPressEvent(event)

    def event(self, event):
        if event.type() == QtCore.QEvent.Type.Gesture:
            return self.gestureEvent(event)
        return super().event(event)

    def keyReleaseEvent(self, event):

        super().keyReleaseEvent(event)

    def get_agent_from_current_loc(self):
        """
        Retrieves the agent/item at the current mouse position in the scene.
        Returns:
            QGraphicsItem or None: The item at the current mouse position, or None if no item exists.
        """
        # Get global mouse position
        global_pos = QCursor.pos()

        # Convert to local widget position
        local_pos = self.mapFromGlobal(global_pos)

        # Convert to scene position
        scene_pos = self.mapToScene(local_pos)

        # Retrieve the item at the scene position
        if self.scene():
            item = self.scene().itemAt(scene_pos, self.transform())

            return item
        return None

    def gestureEvent(self, event):
        pan = event.gesture(QtCore.Qt.PanGesture)
        if pan:
            self.handlePanGesture(pan)
            return True
        pinch = event.gesture(QtCore.Qt.PinchGesture)
        if pinch:
            self.handlePinchGesture(pinch)
            return True
        return False

    def handlePanGesture(self, pan):
        delta = pan.delta()
        transform = self.transform()
        deltaX = delta.x() / transform.m11()
        deltaY = delta.y() / transform.m22()
        self.setSceneRect(self.sceneRect().translated(-deltaX, -deltaY))

    def handlePinchGesture(self, gesture):
        if gesture.changeFlags() & QtWidgets.QPinchGesture.ChangeFlag.ScaleFactorChanged:
            scale_factor = gesture.scaleFactor()
            self._zoom_factor *= scale_factor
            self._zoom_factor = max(0.000001, min(self._zoom_factor, 10))  # Clamp zoom factor
            self.resetTransform()
            self.scale(self._zoom_factor, self._zoom_factor)
            # Emit the zoom level changed signal
            zoom_level = int(self._zoom_factor * 1000)
            self.zoom_level_changed.emit(zoom_level)

    def mousePressEvent(self, event):
        """event handler for remounting the scene origin point int the canvas"""

        self.unselect_contracts.emit()
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier and event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.pos()


        else:
            super(MainGraphicsWidget, self).mousePressEvent(event)

    def wheelEvent(self, event: PySide6.QtGui.QWheelEvent) -> None:
        """prevent from unwanted movement/ side effects when scrolling with"""
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:  # bitwise comparison necessary, due to the fact that multiple
            # modifiers can be pressed at the same time
            return
        super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        """compute the difference between the current cursor position and the
        previous saved origin point"""
        if self.startPos is not None:
            delta = self.startPos - event.pos()
            transform = self.transform()
            deltaX = delta.x() / transform.m11()
            deltaY = delta.y() / transform.m22()
            self.setSceneRect(self.sceneRect().translated(deltaX, deltaY))
            self.startPos = event.pos()
        else:
            super(MainGraphicsWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """resets the alternative origin point"""
        self.startPos = None
        super().mouseReleaseEvent(event)
