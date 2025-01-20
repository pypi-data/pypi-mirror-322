import logging
from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QTextCursor, Qt
from PySide6.QtWidgets import QTextEdit, QPushButton

from famegui.config.style_config import FAME_CONSOLE_TEXT_STYLE
from famegui.time_utils import WIDGET_DATE_FORMAT_CONSOLE


class GUIConsoleHandler(logging.StreamHandler):
    """A custom logging handler that writes to a QTextEdit to display the log messages in the GUI"""

    def __init__(self, text_edit: QTextEdit, clear_button: QPushButton):
        super().__init__()
        self._text_edit = text_edit
        self._text_edit.setReadOnly(True)

        font = QFont()
        font.setPointSize(10)
        self._text_edit.setFont(font)

        self._text_edit.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)

        self._text_edit.setStyleSheet(FAME_CONSOLE_TEXT_STYLE)

        # Add a clear button
        clear_button.clicked.connect(self.clear_logs)

    def emit(self, record):
        """On new log message, append it to the QTextEdit and scroll to the bottom"""
        msg = self.format(record)
        current_time = datetime.now().strftime(WIDGET_DATE_FORMAT_CONSOLE)

        log_entry = f"{current_time}: {record.levelname}: {msg}\n"

        self._text_edit.moveCursor(QTextCursor.MoveOperation.End)
        self._text_edit.insertPlainText(log_entry)

        # Limit the number of lines to 150
        document = self._text_edit.document()
        if document.lineCount() > 150:
            cursor = QTextCursor(document)
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.KeepAnchor, document.lineCount() - 150)
            cursor.removeSelectedText()

        QTimer.singleShot(0, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        """Scroll to the bottom of the text edit"""
        self._text_edit.verticalScrollBar().setValue(
            self._text_edit.verticalScrollBar().maximum()
        )

    def clear_logs(self):
        """Clear all log messages from the text edit"""
        self._text_edit.clear()
