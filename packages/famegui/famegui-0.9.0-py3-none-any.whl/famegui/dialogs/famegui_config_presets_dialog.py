import logging
import os.path
import os.path
import typing
from typing import Union, Callable

import yaml
from PySide6.QtGui import Qt, QColor, QBrush
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit, QListWidgetItem, \
    QHBoxLayout, QWidget, QTabWidget, QTableWidget, QTableWidgetItem, \
    QHeaderView, QColorDialog
from sqlalchemy.util import await_only

from famegui.config.config import BASE_DIR
from famegui.config.style_config import LIST_ITEM_STYLE
from famegui.database.db_loader.db_manager import get_existing_table_names, read_all_data, update_db, insert
from famegui.database.settings_db.init_db import Setting, init_db_session
from famegui.famegui_widgets.StringSetSelectWidget import StringSetSelectWidget
from famegui.models import Scenario


class EditFameDbValuesDialog(QDialog):
    settings_data = {}
    agent_type_to_table_cell: typing.Dict[str, dict[str:typing.Union[QTableWidgetItem, str]]] = {}

    def save_settings_to_db(self):

        with init_db_session() as session:
            for setting_name, value in self.settings_data.items():
                setting = session.query(Setting).filter_by(setting_name=setting_name).first()
                setting.value = value

            session.commit()

    def load_dialog(self):
        with init_db_session() as session:
            yaml_file = os.path.join(BASE_DIR, "config", 'settings_config.yaml')  # Path to your YAML file
            with open(yaml_file, 'r') as file:
                data = yaml.safe_load(file)
            # Extract and insert data

            for table_name, table_data in data['db']['tables'].items():
                if table_name == 'setting':
                    table_fields = data['db']['tables']['setting']["preset_values"]

                    for item in table_fields:
                        setting = session.query(Setting).filter_by(
                            setting_name=item['setting_name']).first()

                        if not setting:
                            new_setting = Setting(
                                value=item['value'],
                                setting_name=item['setting_name'],
                                setting_label=item['setting_label'],
                                data_type=item['data_type'])
                            session.add(new_setting)
                        session.commit()

    def load_settings(self):

        with init_db_session() as session:
            settings = session.query(Setting).all()
            for setting in settings:
                # Create the custom widget
                widget = QWidget()
                layout = QHBoxLayout(widget)
                widget.setStyleSheet(LIST_ITEM_STYLE)
                layout.setContentsMargins(0, 0, 0, 20)  # Remove margins

                label = QLabel(setting.setting_label)
                label.setWordWrap(True)  # Enable word wrap for the label

                input = QLineEdit()

                input.textChanged.connect(lambda text: self.on_text_changed(text, setting.setting_name))

                input.setText(setting.value)
                input.setFixedWidth(200)
                input.setStyleSheet("border: 1px solid lightgray; padding: 5px; border-radius: 4px;")

                layout.addWidget(label)
                layout.addWidget(input)

                # Create a QListWidgetItem
                item = QListWidgetItem(self.list_widget)

                # Set the custom widget as the item widget
                self.list_widget.setItemWidget(item, widget)

                # Store the setting object in the item's data
                item.setData(Qt.UserRole, setting)

                # Set a default size for the item
                item.setSizeHint(widget.sizeHint())

    def on_string_sets_saved(self, data_dict: dict):
        with init_db_session() as session:
            for string_set_group_name, string_set_list in data_dict.items():
                for string_set_value in string_set_list:
                    insert(session, "db_string_item", {
                        "parent_string_set_group_name": string_set_group_name,
                        "string_set_item_value": string_set_value
                    })

    def get_strings_set_tab(self) -> QWidget:
        string_set_tab = QWidget()
        string_set_layout = QVBoxLayout()
        string_set_main_container = QWidget()
        string_set_main_container.setStyleSheet("background-color:#A7BBEC")
        string_set_widget = StringSetSelectWidget(self._scenario)
        string_set_widget.on_string_sets_saved.connect(self.on_string_sets_saved)

        string_set_layout.addWidget(string_set_widget, stretch=1)
        string_set_tab.setLayout(string_set_layout)

        return string_set_tab

    def __init__(self, scenario: Scenario,
                 handle_agent_color_change: Callable):
        super().__init__()
        self._scenario = scenario

        self._scenario.string_sets.update()

        self._handle_agent_color_change = handle_agent_color_change

        self.setStyleSheet("""
               QDialog {
                   background-color: #f5f5f5;
               }
               QListWidget {
                   border: 1px solid lightgray;
                   border-radius: 4px;
               }
               QLabel {
                   font-size: 14px;
               }
           """)

        self.setMinimumHeight(400)
        self.setMinimumWidth(600)

        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(self.display_setting)
        self.layout.addWidget(self.list_widget)

        self.input_layout = QVBoxLayout()
        self.layout.addLayout(self.input_layout)
        self.input_layout.setContentsMargins(20, 20, 20, 20)
        self.input_layout.setSpacing(15)

        self.load_dialog()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_setting)
        self.layout.addWidget(self.save_button)
        self.row_idx_to_db_id_mapper = {}

        tab_holder = QVBoxLayout()

        tabs = QTabWidget()

        # Create tab 1
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(self.list_widget)
        tab1.setLayout(tab1_layout)

        # Create tab 2
        yaml_file = os.path.join(BASE_DIR, "config", 'settings_config.yaml')  # Path to your YAML file

        with init_db_session() as session:
            table_name_list = get_existing_table_names(yaml_file, session)

            table_name_list = [item for item in table_name_list if
                               item != "db_string_set_group" and item != "db_string_item"]

            data = read_all_data(session)

            string_set_tab = self.get_strings_set_tab()

            tabs.addTab(string_set_tab, "String Set")

            for table_name in table_name_list:
                table_specific_tab = QWidget()
                table_specific_tab_layout = QVBoxLayout()
                table_widget = self.create_table(data[table_name], table_name)

                table_specific_tab_layout.addWidget(table_widget)

                table_specific_tab.setLayout(table_specific_tab_layout)
                tabs.addTab(table_specific_tab, table_name)

            tab_holder.addWidget(tabs)

            self.setLayout(tab_holder)

            self.load_settings()

    def reject(self):
        """Acts like on close due too no explicit closing/accepting button"""

        color_settings_data = {setting_item_key: setting_item_value for
                               setting_item_key, setting_item_value in
                               self.settings_data.items() if setting_item_key.__contains__("hex")}

        if len(color_settings_data.keys()) != 0:
            self._handle_agent_color_change()

        self.settings_data.clear()
        self.agent_type_to_table_cell.clear()

        super().reject()

    def save_setting(self):

        self.save_settings_to_db()

        # quit dlg

        self.close()

    def on_table_item_changed(self, item: Union[QTableWidgetItem, dict], table_name: str):
        """Handles changes to table items and updates settings_data."""

        row, column, new_value = None, None, None

        db_field_name = None

        if isinstance(item, QTableWidgetItem):
            row, column, new_value = item.row(), item.column(), item.text()

        if isinstance(item, dict):
            row, column, new_value, db_field_name = item["row"], item["column"], item["text"], item["db_field_name"]

        # Get the setting name (column header) and update settings_data
        field_name = item.tableWidget().horizontalHeaderItem(column).text() if db_field_name is None else db_field_name

        # Assuming your data is a list of dictionaries with row-wise settings
        self.settings_data[field_name] = new_value

        updated_record = None

        with init_db_session() as session:
            db_id = self.row_idx_to_db_id_mapper[table_name][row]

            updated_record = update_db(session, table_name, db_id, field_name,
                                       new_value, return_updated_record=True)

        logging.info(f"Updated setting {field_name} at row {row} to {new_value}")

        if not field_name.__contains__("hex"):
            return

        agent_type_name = updated_record["agent_type_name"]

        self.agent_type_to_table_cell[agent_type_name]["cell_widget"].setBackground(QBrush(new_value))

    def open_color_picker(self, row, col, local_value, color_line_edit: QLineEdit):

        color_dlg = QColorDialog(QColor(color_line_edit.text()))
        if color_dlg.exec() != 0:
            selected_color = color_dlg.selectedColor()

            if selected_color is not None:
                hex_without_hash = selected_color.name()[1:]

                hex_without_hash = "#" + hex_without_hash
                color_line_edit.setText(hex_without_hash)

    def get_color_edit_panel(self, initial_color: str, row, cell_idx, table_name, db_field_name) -> [QWidget]:
        container = QWidget()
        container.setFixedHeight(50)
        h_layout = QHBoxLayout()
        container.setLayout(h_layout)
        color_line_edit = QLineEdit(initial_color)
        h_layout.addWidget(color_line_edit)

        btn = QPushButton(f"Pick color : {table_name}")
        h_layout.addWidget(btn)

        color_line_edit.textChanged.connect(lambda new_str: self.on_table_item_changed({
            "row": row,
            "column": cell_idx,
            "text": new_str,
            "db_field_name": db_field_name

        }, table_name))

        btn.clicked.connect(lambda x: self.open_color_picker(row, cell_idx, str(initial_color), color_line_edit))

        return container

    def create_table(self, table_data: [], table_name):
        """Creates a table widget with editable fields for the settings."""
        table = QTableWidget()

        # Two columns: Setting Name and Value

        if len(table_data) == 0:
            return table

        field_names = [field_key for field_key in table_data[0].keys()]

        row_idx_to_ids = {idx: item["id"] for idx, item in enumerate(table_data)}

        self.row_idx_to_db_id_mapper[table_name] = row_idx_to_ids

        field_names = [item for item in field_names if
                       not item.__contains__("id") and not item.__contains__("data_type")]

        table.setColumnCount(len(field_names))
        table.setRowCount(len(table_data))

        table.setHorizontalHeaderLabels(field_names)

        for row, setting in enumerate(table_data):
            # Create the setting name item

            row_values = [setting[item] for item in field_names]

            for idx, item in enumerate(row_values):

                if field_names[idx].lower() == "agent_type_name":
                    painted_cell = QTableWidgetItem(str(item))
                    color_value = row_values[idx - 1]
                    background_color = QColor(color_value)

                    self.agent_type_to_table_cell[str(item)] = {
                        "cell_widget": painted_cell,
                        "agent_type_name": str(item)
                    }

                    brush = QBrush(background_color)
                    painted_cell.setBackground(brush)

                    table.setItem(row, idx, painted_cell)
                    continue

                if field_names[idx].lower().__contains__("hex"):
                    table.setRowHeight(row, 60)

                    db_field_name = field_names[idx]

                    color_input_panel = self.get_color_edit_panel(str(item), row, idx,
                                                                  table_name, db_field_name)
                    table.setItem(row, idx, QTableWidgetItem())

                    table.setCellWidget(row, idx, color_input_panel)
                    continue

                table.setItem(row, idx, QTableWidgetItem(str(item)))

            # Connect the value item change to update the settings_data

        table.itemChanged.connect(lambda item: self.on_table_item_changed(item, table_name))

        # Resize columns to fit content
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return table

    def display_setting(self, current, previous):
        for i in reversed(range(self.input_layout.count())):
            widget = self.input_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def on_text_changed(self, text, setting_name):
        self.settings_data[setting_name] = text

    def on_button_click(self):
        self.label.setText("Button Clicked!")
