from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QScrollArea,
    QFrame, QLineEdit, QHBoxLayout, QLabel
)
from icecream import ic

from famegui.data_manager.string_set_manager import get_pre_defined_string_set_values_from_scenario
from famegui.database.db_loader.db_manager import get_string_set_values_from_db
from famegui.models import Scenario
from famegui.scenario_helper import add_string_set_value


class StringSetSelectWidget(QWidget):
    on_string_sets_saved = QtCore.Signal(dict)

    def __init__(self, scenario: Scenario):
        super().__init__()
        self.setWindowTitle("Simple Scroll Area App")

        # Main layout for the app
        self.layout = QVBoxLayout(self)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidgetResizable(True)

        # Scroll content and layout
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Add scroll area to the main layout
        self.layout.addWidget(self.scroll_area)

        self._string_set_from_db = get_string_set_values_from_db()

        # Buttons

        self.setMinimumHeight(500)
        self.setMinimumWidth(650)
        self._scenario = scenario

        string_set_data_dict = get_pre_defined_string_set_values_from_scenario(self._scenario)

        self._string_set_data_dict = string_set_data_dict

        # Connect Add button to create new blocks

        self.input_data_holder = {}

        for item_key, list_of_strings in self._string_set_data_dict.items():
            sub_input_data_holder = []

            self.input_data_holder[item_key] = sub_input_data_holder

            if item_key in self._string_set_from_db:
                list_of_strings.extend(self._string_set_from_db[item_key])

            list_of_strings = set(list(list_of_strings))

            self.add_string_set_group_block(item_key, list_of_strings, sub_input_data_holder=sub_input_data_holder)

        push = QPushButton("Save String Sets")
        push.clicked.connect(self.save_string_sets)

        self.layout.insertWidget(0, push)

    def save_string_sets(self):
        """Save String Sets to db and to Scenario"""

        plain_input_data = {
            string_set_key: [string_set_line_edit.text() for string_set_line_edit in string_set_list] for
            string_set_key, string_set_list in self.input_data_holder.items()
        }

        for string_set_group_name, string_set_value_list in plain_input_data.items():
            for item in string_set_value_list:
                add_string_set_value(self._scenario, string_set_group_name, item)

        self.on_string_sets_saved.emit(plain_input_data)

    def add_list_item(self, layout, default_value="", sub_input_data_holder=None):
        """Add a list item with a text input and a remove button."""
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)

        item_widget.setStyleSheet("background-color:#E0E0E0")

        # Text input
        text_input = QLineEdit(default_value)
        item_layout.addWidget(text_input)

        sub_input_data_holder.append(text_input)

        # Remove button
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.remove_list_item(layout, item_widget))
        item_layout.addWidget(remove_btn)

        # Add the item widget to the layout
        layout.addWidget(item_widget)

    def remove_list_item(self, layout, item_widget):
        """Remove a specific list item."""

        matching_group = ""
        index_to_remove = -1

        for group_name, group_value_list in self.input_data_holder.items():

            if item_widget in group_value_list:
                matching_group = group_name
                break

        if index_to_remove == -1:
            raise ValueError("Index to remove cannot be null")

        self.input_data_holder[matching_group] = [item for item in self.input_data_holder[matching_group] if
                                                  item != item_widget]

        layout.removeWidget(item_widget)
        item_widget.deleteLater()

    def remove_last_list_item(self, layout, sub_input_data_holder=None):
        """Remove the last item from the layout."""
        count = layout.count()
        if count > 0:
            item = layout.itemAt(count - 1).widget()
            if item:
                sub_input_data_holder.pop()
                item.deleteLater()

    def add_string_set_group_block(self, title=None, list_of_strings=None, sub_input_data_holder=None):
        """Add a block with expandable content to the scroll area."""
        holder = QFrame()
        holder.setStyleSheet("border: none; background-color: #F7F7F7; border-radius: 8px;")
        holder_layout = QVBoxLayout(holder)
        holder_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        default_title = title if title is not None else f"Block {self.scroll_layout.count() + 1}"

        # Header with label and chevron button
        header = QWidget()
        header_layout = QHBoxLayout(header)

        header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Title label
        title_label = QLabel(default_title)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #333333;")
        header_layout.addWidget(title_label)

        # Chevron button for expand/collapse
        chevron_button = QPushButton("➖")
        chevron_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                font-size: 16px;
                color: #333333;
                border: none;
            }
            QPushButton:hover {
                color: #DBB957;
            }
        """)

        header_layout.addWidget(chevron_button)

        # Expandable content frame
        expandable_content = QFrame()
        expandable_content_layout = QVBoxLayout(expandable_content)
        expandable_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Horizontal panel at the top of expandable content
        horizontal_panel = QFrame()
        horizontal_panel_layout = QHBoxLayout(horizontal_panel)
        horizontal_panel.setStyleSheet("background-color: #F2F2F2; padding: 5px; border-radius: 4px;")
        horizontal_panel_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Add and Remove buttons in the horizontal panel
        add_item_btn = QPushButton("Add Item")
        add_item_btn.setStyleSheet("""
            QPushButton {
                background-color: #DBB957;
                color: white;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C9A24D;
            }
        """)
        remove_last_item_btn = QPushButton("Remove Last Item")
        remove_last_item_btn.setStyleSheet("""
            QPushButton {
                background-color: #DBB957;
                color: white;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C9A24D;
            }
        """)
        horizontal_panel_layout.addWidget(add_item_btn)
        horizontal_panel_layout.addWidget(remove_last_item_btn)
        expandable_content_layout.addWidget(horizontal_panel)

        # Scroll area for expandable content
        expandable_content_scroll_area = QScrollArea()
        expandable_content_scroll_area.setWidgetResizable(True)

        # Container widget for the scroll area
        scroll_content_widget = QWidget()
        scroll_content_widget.setStyleSheet("background:#FFFFFF; border: none;")
        scroll_content_layout = QVBoxLayout(scroll_content_widget)
        scroll_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        if list_of_strings:
            for string_item in list_of_strings:
                self.add_list_item(scroll_content_layout, string_item, sub_input_data_holder)

        add_item_btn.clicked.connect(lambda: self.add_list_item(scroll_content_layout, "", sub_input_data_holder))
        remove_last_item_btn.clicked.connect(
            lambda: self.remove_last_list_item(scroll_content_layout, sub_input_data_holder))

        scroll_content_widget.setLayout(scroll_content_layout)
        expandable_content_scroll_area.setWidget(scroll_content_widget)
        expandable_content_layout.addWidget(expandable_content_scroll_area)

        holder.setFixedHeight(60 + 200)

        holder_layout.addWidget(header)
        holder_layout.addWidget(expandable_content)

        def toggle_expand():
            if expandable_content.isVisible():
                expandable_content.setVisible(False)
                holder.setFixedHeight(60)
                chevron_button.setText("➕")
            else:
                expandable_content.setVisible(True)
                holder.setFixedHeight(60 + 200)
                chevron_button.setText("➖")

        chevron_button.clicked.connect(toggle_expand)
        self.scroll_layout.addWidget(holder)
