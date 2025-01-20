import copy
import logging
from copy import deepcopy

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QFrame, QScrollArea, QSizePolicy, QToolButton, QPushButton)

from famegui.ui.ui_input_panel_wrapper import MiniAttributeSpecs
from famegui_runtime_helper.attribute_dict_formatting_helper import get_full_attr_names, StringAttributeType


class SchemaWidget(QWidget):
    """Complex widget to display an attribute from root to n-depth level"""

    def __init__(self, schema_data, is_single_item,
                 attr_row_item=None, parent=None):
        super().__init__(parent)
        self.schema_data = schema_data
        self._is_single_item = is_single_item
        self._attr_row_item = attr_row_item
        self.init_ui()

        self.changed_values_tracker = {}

    def init_ui(self):
        # Create main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add scroll area for better handling of large schemas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create container widget for scroll area
        container = QWidget()
        container_layout = QVBoxLayout()
        container.setLayout(container_layout)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Start the recursive widget building
        self.build_widget(self.schema_data, container_layout)

        scroll.setWidget(container)

        self.main_layout.addWidget(scroll, stretch=1)

    def get_last_widget(self, contents_layout):
        """Returns the last widget from the layout."""
        if contents_layout.count() > 1:  # Exclude the plus button
            return contents_layout.itemAt(contents_layout.count() - 2).widget()
        return None

    def duplicate_last_widget(self, contents_layout):
        """Duplicates the last widget in the contents layout."""

        # Get the last widget from the layout

        last_widget = self.get_last_widget(contents_layout)

        if last_widget is not None:
            # Perform a deep copy of the last widget
            new_widget = copy.deepcopy(last_widget)
            contents_layout.insertWidget(contents_layout.count() - 1, new_widget)

    def on_list_item_added(self, contents_layout, list_schema):
        """Extend the list frame with a new item"""

        contents_layout.count()

        item_frame, item_layout = self.create_block_frame(f"Item {contents_layout.count()}", is_list_item=True,
                                                          list_item_parent_layout=contents_layout)

        list_idx = contents_layout.count()
        list_idx = list_idx - 1  # minus control panel
        list_idx = list_idx - 1  # Due too indexes starting from 0

        self.build_list_item(list_schema, contents_layout, item_frame, item_layout, list_idx,
                             f"Item {contents_layout.count()}")

    def get_list_control_panel(self, contents_layout: QVBoxLayout, list_schema: dict,
                               contents_frame: QFrame) -> QWidget:
        """
        Creates and returns a control panel widget with buttons to manage a list.

        Args:
            contents_layout (QVBoxLayout): The layout containing the list elements.
            list_schema (dict): A schema defining the structure of the list items.

        Returns:
            QWidget: The control panel widget with 'Add' and 'Remove' buttons.
        """
        # Initialize the panel
        panel = QWidget()
        panel_layout = QHBoxLayout()  # Use QHBoxLayout for buttons to be side by side
        panel.setLayout(panel_layout)

        # Configure panel appearance
        panel.setFixedHeight(40)
        panel.setStyleSheet("background-color: #9BC53D; border: 1px solid #ddd;")
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Create and style 'Add' button
        add_list_item_button = QPushButton("Add Item")
        add_list_item_button.setFixedHeight(30)
        add_list_item_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QPushButton:pressed {
                background-color: #E0E0E0;
            }
        """)

        add_list_item_button.clicked.connect(lambda: self.on_list_item_added(contents_layout, list_schema))

        # Create and style 'Remove' button
        remove_list_item_button = QPushButton("Remove Item")
        remove_list_item_button.setFixedHeight(30)
        remove_list_item_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QPushButton:pressed {
                background-color: #E0E0E0;
            }
        """)

        remove_list_item_button.clicked.connect(
            lambda: self.on_list_item_removed(contents_frame, contents_layout, list_schema))

        # Add buttons to the panel layout
        panel_layout.addWidget(add_list_item_button)
        panel_layout.addWidget(remove_list_item_button)

        return panel

    def is_at_least_one_list_item_required(self, data_dict):
        """Perform schema check if at least one list item is required to save the attribute"""

        if isinstance(data_dict["attr"], dict):
            for key, item in data_dict["attr"].items():
                if item["is_mandatory"] and not item["is_list"] == True:
                    return True

                if item["has_nested_attributes"]:
                    if self.is_at_least_one_list_item_required(item):
                        return True

        else:
            if data_dict["is_mandatory"]:
                return True
        return False

    def on_list_item_removed(self, list_item_frame, list_item_parent_layout, list_schema):
        """Remove list item by a click, detach from state( remove reference to input widget """
        to_remove_idx = list_item_parent_layout.count() - 1  # due to indexes starting from 0

        last_item = list_item_parent_layout.itemAt(to_remove_idx)  # Remove the last item
        widget = last_item.widget()  # Get the widget associated with the item

        if (to_remove_idx - 1) == 0:
            if self.is_at_least_one_list_item_required(list_schema):
                widget.setStyleSheet("background-color: #DA2C38")
                return

        if widget:
            uniq_full_names = list(set(get_full_attr_names(list_schema)))

            to_remove_idx = to_remove_idx - 1

            if to_remove_idx == -1:
                return

            self._attr_row_item.remove_state_registers(uniq_full_names, to_remove_idx)

            # list_item_parent_layout.removeWidget(widget)
            widget.setParent(None)
            # widget.deleteLater()  # Delete the widget
            del widget
        else:
            logging.warning("No widget found in the layout item")

    def create_block_frame(self, title: str, is_list_item=False, is_list=False,
                           list_schema: dict = None, is_collapsible=False, list_item_parent_layout=None):

        """Create a styled collapsible frame for blocks"""
        # Main frame
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        frame.setStyleSheet(""" QFrame {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 2px;
            } """)

        # Main layout for frame
        main_layout = QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        frame.setLayout(main_layout)

        header_container = QWidget()
        header_container_layout = QHBoxLayout()

        # Header as a toggle button
        header_button = QToolButton()
        header_button.setText(f"➖ {title}")
        header_button.setCheckable(True)
        header_button.setChecked(True)
        header_button.setStyleSheet(""" QToolButton {
                font-weight: bold;
                color: #2c3e50;
                font-size: 14px;
                text-align: left;
                padding: 4px;
                border: none;
            }  """)

        header_button.toggled.connect(
            lambda checked: self.toggle_contents(checked, contents_frame, header_button, title))

        # Collapsible contents container
        contents_frame = QFrame()
        # contents_frame.setVisible(True)
        contents_layout = QVBoxLayout(contents_frame)

        if is_list:
            contents_layout.addWidget(self.get_list_control_panel(contents_layout, list_schema, contents_frame))

        else:
            contents_frame.setStyleSheet(""" QFrame {
                                        margin-top: 2px;
                                         } """)

        # Add header and contents to the main layout

        if is_list_item:
            left = QWidget()
            left_layout = QHBoxLayout()
            left_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            left.setLayout(left_layout)
            left.setFixedHeight(40)
            left.setStyleSheet("background-color:#F18805")

            # Add the header_button first, before any stretch
            left_layout.addWidget(header_button)

            # Add stretch after the button to push other widgets to the right
            left_layout.addStretch(1)

            close_button = QPushButton("X")
            close_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF; border: none; padding: 5px;")

            close_button.clicked.connect(lambda: self.on_list_item_removed(frame, list_item_parent_layout, list_schema))

            right = QWidget()
            right_layout = QHBoxLayout()
            right_layout.addStretch(1)
            right_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            right_layout.addWidget(close_button)

            right.setFixedHeight(40)
            right.setLayout(right_layout)
            right.setStyleSheet("background-color:#F0A202")
            header_container_layout.addWidget(left)
            header_container_layout.addWidget(right)
            header_container.setLayout(header_container_layout)
            main_layout.addWidget(header_container)

        else:
            main_layout.addWidget(header_button)

        main_layout.addWidget(contents_frame)

        return frame, contents_layout

    def build_list_item_control_panel(self, header_button, header_container,
                                      header_container_layout, main_layout, frame, list_item_parent_layout):
        left = QWidget()
        left_layout = QHBoxLayout()
        left_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        left.setLayout(left_layout)
        left.setFixedHeight(40)
        # Add the header_button first, before any stretch
        left_layout.addWidget(header_button)
        # Add stretch after the button to push other widgets to the right
        left_layout.addStretch(1)
        close_button = QPushButton("X")
        close_button.clicked.connect(lambda: self.on_list_item_removed(frame, list_item_parent_layout))
        right = QWidget()
        right_layout = QHBoxLayout()
        right_layout.addStretch(1)
        right_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(close_button)
        right.setFixedHeight(40)
        right.setLayout(right_layout)
        header_container_layout.addWidget(left)
        header_container_layout.addWidget(right)
        header_container.setLayout(header_container_layout)
        main_layout.addWidget(header_container)

    def toggle_contents(self, checked, contents_frame, header_button, title):
        """Toggle visibility of the contents frame and update button text"""
        contents_frame.setVisible(checked)
        header_button.setText(f"➖ {title}" if checked else f"➕ {title}")

    def build_widget(self, data, parent_layout, parent_key="",
                     primitive_index=-1, is_primitive_list_item=False):
        """Recursively build widgets for arbitrarily deep schema data"""

        if is_primitive_list_item:
            value = data['value'] if (not isinstance(data['value'], dict)
                                      and not isinstance(data["value"], list)) else ""

            label = QLabel(f"{parent_key}:{str(value) if data is not None else 'N/A'}")

            attr_type = data["type"]

            primitive_value = data["value"] if data["value"] is not None else ""

            primitive_value = primitive_value if (not isinstance(primitive_value, list)
                                                  and not isinstance(primitive_value, dict)) else ""

            mini_attr_spec = MiniAttributeSpecs(data["attr"],
                                                attr_type,
                                                data["is_mandatory"],
                                                data["options"] if "options" in data else None)

            prim_input: QWidget = self._attr_row_item.get_primitive_input_panel(None, None,
                                                                                mini_spec=mini_attr_spec,
                                                                                preset_value=primitive_value,
                                                                                list_idx=primitive_index)

            prim_input_group_widget = QWidget()

            prim_input_group_widget.setStyleSheet("""
                background-color: #E0E0E0;
                border: 1px solid #ddd; /* Black fine border */
                border-radius: 1px;       /* Optional: Rounded corners */
                border-radius: 5px;
            """)

            prim_input_group_widget_layout = QVBoxLayout()
            prim_input_group_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            prim_input.setStyleSheet("""
                background-color: #fff;
                border: 1px solid #141414; /* Black fine border */
                border-radius: 1px;       /* Optional: Rounded corners */
                border-radius: 5px;
            """)

            prim_input_group_widget_layout.addWidget(prim_input)
            prim_input_group_widget_layout.addWidget(label)
            prim_input_group_widget.setLayout(prim_input_group_widget_layout)

            parent_layout.addWidget(prim_input_group_widget)

            return

        if isinstance(data, dict):
            # Check if the dict represents a schema node with 'type' and 'attr'
            if "type" in data and "attr" in data:

                attr_type = data["type"]

                # Process BLOCK types, which can contain nested attributes
                if attr_type == StringAttributeType.BLOCK.value:
                    # Create a frame for this block
                    is_list = data.get("is_list", False)
                    frame, frame_layout = self.create_block_frame(parent_key, is_list=is_list,
                                                                  list_schema=data)
                    # If the block is a list, handle each list item
                    if is_list:
                        if data["value"] is None:
                            item_frame, item_layout = self.create_block_frame(f"Item: {0 + 1}")

                            self.build_list_item(data, frame_layout, item_frame, item_layout, 0, parent_key)
                            parent_layout.addWidget(frame)
                            return

                        for list_idx, _ in enumerate(data["value"]):
                            item_frame, item_layout = self.create_block_frame(f"Item {list_idx + 1}")

                            self.build_list_item(data, frame_layout, item_frame, item_layout, list_idx, parent_key)

                    # If this BLOCK has attributes, process them recursively
                    elif isinstance(data["attr"], dict):
                        for key, value in data["attr"].items():
                            self.build_widget(value, frame_layout, key,
                                              primitive_index=primitive_index)

                    # Add the frame to the parent layout
                    parent_layout.addWidget(frame)

                else:
                    # Handle other attribute types (TIME_SERIES, ENUM) by displaying them directly

                    attr_value = data.get('value', 'N/A')

                    label = QLabel()

                    if isinstance(attr_value, list):
                        attr_value = attr_value[primitive_index]

                    if isinstance(attr_value, dict):
                        attr_value = ""

                    if isinstance(data['value'], list) and data["is_list"]:
                        frame, frame_layout = self.create_block_frame(parent_key, is_list=True,
                                                                      list_schema=data)
                        for list_idx, _ in enumerate(data["value"]):
                            item_frame, item_layout = self.create_block_frame(f"ItemAA {list_idx + 1}")

                            if data.get("is_list", False) and isinstance(data["value"], list):
                                copied_data = deepcopy(data)
                                picked_value = copied_data["value"][list_idx]
                                copied_data["value"] = picked_value

                                self.build_list_item(copied_data, frame_layout,
                                                     item_frame, item_layout, list_idx,
                                                     parent_key)

                                continue

                            self.build_list_item(data, frame_layout, item_frame, item_layout, list_idx,
                                                 parent_key)

                        parent_layout.addWidget(frame)
                    elif data["is_list"]:
                        frame, frame_layout = self.create_block_frame(parent_key, is_list=True,
                                                                      list_schema=data)

                        for list_idx in range(1):
                            item_frame, item_layout = self.create_block_frame(f"Item {list_idx + 1}")

                            self.build_list_item(data, frame_layout, item_frame, item_layout, list_idx,
                                                 parent_key)
                        parent_layout.addWidget(frame)

                    else:
                        from famegui.ui.attribute_row_item import AttributeTreeItem

                        self._attr_row_item: AttributeTreeItem

                        primitive_value = data["value"] if data["value"] is not None else ""

                        if isinstance(primitive_value, list):
                            primitive_value = primitive_value[primitive_index]

                        primitive_value = primitive_value if (not isinstance(primitive_value, list)
                                                              and not isinstance(primitive_value, dict)) else ""

                        mini_attr_spec = MiniAttributeSpecs(data["attr"],
                                                            attr_type,
                                                            data["is_mandatory"],
                                                            data["options"] if "options" in data else None)

                        prim_input = self._attr_row_item.get_primitive_input_panel(None, None,
                                                                                   mini_spec=mini_attr_spec,
                                                                                   preset_value=primitive_value)

                        if data["attr"] != StringAttributeType.TIME_SERIES.value:
                            parent_layout.addWidget(label)

                        parent_layout.addWidget(prim_input)

                    data_key = data["type"]

                    label_text = f"{parent_key}: {data_key}"

                    label.setText(label_text)

                    label.setWordWrap(True)

                    label.setStyleSheet("color: #34495e;")

            # Handle generic dictionaries without explicit type
            else:
                for key, value in data.items():

                    if isinstance(value, dict) or isinstance(value, list):
                        frame, frame_layout = self.create_block_frame(key)
                        self.build_widget(value, frame_layout)
                        parent_layout.addWidget(frame)
                    else:
                        # Display simple key-value pairs
                        label = QLabel(f"{key}: {value if value is not None else 'N/A'}")
                        parent_layout.addWidget(label)

        # Handle list items at any depth

        elif isinstance(data, list):
            for idx, item in enumerate(data):
                item_frame, item_layout = self.create_block_frame(f"Item: {idx + 1}")
                if isinstance(item, dict):
                    for subkey, subvalue in item.items():
                        self.build_widget(subvalue, item_layout, subkey)
                else:
                    # Directly show non-dict values in list items
                    label = QLabel(f"{idx + 1}: {item if item is not None else 'N/A'}")
                    item_layout.addWidget(label)

                parent_layout.addWidget(item_frame)

        # Display simple values at leaf nodes (like strings or numbers)
        else:
            label = QLabel(f"{parent_key}: {str(data)}  {data if data is not None else 'N/A'}")
            parent_layout.addWidget(label)

    def get_widget_index(self, layout, widget):
        """
        Get the index of a widget in a layout.

        Args:
            layout (QLayout): The layout containing the widget.
            widget (QWidget): The widget whose index we want to find.

        Returns:
            int: The index of the widget, or -1 if not found.
        """
        for i in range(layout.count()):
            if layout.itemAt(i).widget() == widget:
                return i
        return -1

    def build_list_item(self, data, frame_layout, item_frame,
                        item_layout,
                        list_idx, parent_key):

        if data["type"] != StringAttributeType.BLOCK.value:
            self.build_widget(data, frame_layout, is_primitive_list_item=True,
                              parent_key=parent_key, primitive_index=list_idx)

            return

        for idx, (key_sub, item) in enumerate(data["attr"].items()):

            if item["type"] == StringAttributeType.BLOCK.value:
                sub_data_li = data["attr"][key_sub]

                self.build_widget(sub_data_li, item_layout,
                                  key_sub, primitive_index=list_idx)

            elif isinstance(item["attr"], dict):
                for subkey, subvalue in item["attr"].items():
                    if item["attr"][subkey]["type"] == StringAttributeType.BLOCK.value:
                        self.build_widget(data["attr"][subkey], item_layout,
                                          subkey, primitive_index=list_idx)
                    else:
                        attr_value = subvalue["value"]
                        label_text = ""
                        attr_value = attr_value if attr_value is not None else "N/A"
                        attr_name = subvalue["attr"]
                        label_text += f" ={attr_name} : {attr_value}"
                        label = QLabel(label_text)
                        label.setWordWrap(True)
                        label.setStyleSheet("color: #34495e;")
                        item_layout.addWidget(label)

            else:
                # Display simple values within list items
                label = QLabel(f"{parent_key}: {item if item is not None else 'N/A'}")

                prim_attr_value = item["value"]

                if isinstance(prim_attr_value, list):

                    if list_idx < len(prim_attr_value):
                        prim_attr_value = prim_attr_value[list_idx] if list_idx != -1 else ""
                    else:
                        prim_attr_value = ""

                prim_attr_value = str(prim_attr_value) if prim_attr_value is not None else ""

                mini_attr_spec = MiniAttributeSpecs(
                    item["attr"],
                    item["type"],
                    item["is_mandatory"],
                    item["options"] if "options" in item else None
                )

                prim_input: QWidget = self._attr_row_item.get_primitive_input_panel(None, None,
                                                                                    mini_spec=mini_attr_spec,
                                                                                    preset_value=prim_attr_value,
                                                                                    list_idx=list_idx)

                display_text = item["value_key"] + f":{str(list_idx)}"

                label.setText(display_text)
                label.setWordWrap(True)
                item_layout.addWidget(label)
                prim_input = prim_input if prim_input is not None else QLabel(
                    f"Input type : {item['type']} is not supported ")

                item_layout.addWidget(prim_input)

            frame_layout.addWidget(item_frame)
