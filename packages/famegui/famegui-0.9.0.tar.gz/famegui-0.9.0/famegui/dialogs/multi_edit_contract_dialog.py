import logging
import os

from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QPushButton, QComboBox, QDateTimeEdit, QVBoxLayout, \
    QScrollArea, QWidget

from famegui.config.config import CUSTOM_DELIVERY_STEPS_TIME_OPTION
from famegui.config.contract_consts import PRESET_DURATION_IN_SECONDS
from famegui.config.runtime_consts import UPDATED_CONTRACT_KEY, OLD_CONTRACT_KEY, \
    CONTRACT_FIELD_DELIVERY_INTERVAL_IN_STEPS, CONTRACT_RECEIVER_ID, CONTRACT_SENDER_ID, CONTRACT_PRODUCT_NAME
from famegui.database.prebuild_queries.interval_presets import get_delivery_interval_presets
from famegui.maincontroller import MainController
from famegui.models import Contract, Scenario, Agent
from famegui.ui.fame_input_panels import (
    get_string_chooser_panel,
    FameCalendarInputPanelWidget,
)
from famegui.ui.fame_ui_elements import QFameBoldLabel
from famegui.ui.helper import gen_preset_interval_chooser
from famegui.ui.quick_modals import gen_quick_warning_modal
from famegui.utils import contract_fields_to_natural_types

DISPLAY_DATE_FORMAT = "yyyy-MM-dd"

DISPLAY_DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss"


class MultiEditContractDialog(QtWidgets.QDialog):
    """Dialog for editing a contract"""

    on_contract_edited = QtCore.Signal(dict)

    def __init__(
            self,
            selected_contracts: [Contract],
            scenario: Scenario,
            controller: MainController,
            on_contract_edited_slot,
            parent=None,
    ):
        super(MultiEditContractDialog, self).__init__(parent)

        # Set up the user interface from Designer
        self._selected_contracts = selected_contracts
        self._scenario = scenario
        self._controller = controller
        self.on_contract_edited.connect(on_contract_edited_slot)
        self._product_changed = False

        self._delivery_interval_presets = get_delivery_interval_presets()

        # Load UI
        loader = QtUiTools.QUiLoader()
        file = QFile(os.path.join(os.path.dirname(__file__), "edit_contract_dialog.ui"))
        file.open(QtCore.QFile.OpenModeFlag.ReadOnly)
        self.ui = loader.load(file, self)

        file.close()
        self._input_fields = []
        self.ui.verticalLayout: QtWidgets.QVBoxLayout

        self._init_static_ui()
        self._generate_input_items()
        self.create_btn_panel()

        # Create a scroll area
        selected_contracts_panel_scroll_area = QScrollArea(self)
        selected_contracts_panel_scroll_area.setWidgetResizable(True)
        selected_contracts_panel_scroll_area.setMaximumHeight(90)  # Cap the height
        selected_contracts_panel_scroll_area.setMinimumHeight(90)  # Fix the height

        # Create the child widget for the scroll area
        selected_contracts_panel = QWidget()
        selected_contracts_panel.setStyleSheet("background-color:#E0E0E0")

        # Set a vertical layout for the child widget
        selected_contracts_panel_layout = QVBoxLayout(selected_contracts_panel)

        # Add contract labels to the layout
        for selected_contract in self._selected_contracts:
            label = QLabel(
                f"Sender Id: {selected_contract.sender_id} - Receiver Id: {selected_contract.receiver_id} ({selected_contract.product_name})"
            )
            selected_contracts_panel_layout.addWidget(label)

        # Set the child widget as the content of the scroll area
        selected_contracts_panel_scroll_area.setWidget(selected_contracts_panel)

        # Add the scroll area to the main layout
        self.ui.verticalLayout.insertWidget(0, selected_contracts_panel_scroll_area)

        # Add a note below the scroll area
        self.ui.verticalLayout.insertWidget(1, QLabel(
            "! Only fill the fields you wish to apply on all selected contracts"
        ))

        self.ui.exec_()

    def setup_layout(self):
        """Set up the layout frame of the dialog"""
        self.ui.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.ui.verticalLayout.setSpacing(20)

    def _set_product_changed(self):
        """Helper to flag that the product was changed """
        self._product_changed = True

    def _init_static_ui(self):
        """Set up the static UI elements of the dialog"""
        self.setup_layout()

    def _construct_product_chooser(self, layout, field_name):
        """construct product chooser widget"""

        sender_type = self._scenario.schema.agent_type_from_name(
            self._controller.get_agent_ctrl(self._selected_contracts[0].sender_id).type_name
        )

        sender_type_products = sender_type.products

        inner_layout, comboBox = get_string_chooser_panel(sender_type_products, Contract.KEY_PRODUCT,
                                                          preset_value="",
                                                          on_input_changed=lambda text: self._set_product_changed())

        layout.addLayout(inner_layout)
        self._input_fields.append((field_name, comboBox))

    def _construct_date_time_chooser(self, layout, field_name, contract_data):
        """construct product time chooser widget"""

        saved_fame_datetime = None

        if contract_data is not None:
            if field_name in contract_data:
                saved_fame_datetime = contract_data[field_name]

        fame_calender_input_panel = FameCalendarInputPanelWidget(
            self, field_name, saved_fame_datetime
        )
        (
            inner_layout,
            date_time_edit,
        ) = fame_calender_input_panel.get_input_related_widgets()
        layout.addWidget(fame_calender_input_panel)

        self._input_fields.append((field_name, date_time_edit))

    def on_preset_changed(self, index, selected_option: str):
        """
        Handles the change event when a new preset is selected
        """
        # Do something with the selected preset

        for field_name, input in self._input_fields:

            if field_name == CONTRACT_FIELD_DELIVERY_INTERVAL_IN_STEPS:
                if selected_option == "Custom":
                    continue
                input.setText(self._delivery_interval_presets[index][PRESET_DURATION_IN_SECONDS])


    def _construct_default_input_field(self, layout, field_name, contract_data):
        """construct default input field"""
        label = QFameBoldLabel(text=field_name)
        label.setMinimumWidth(int(self.width() * 0.3))  # Set the maximum width to 30% of the dialog's width
        label.setMaximumWidth(int(self.width() * 0.3))  # Set the maximum width to 30% of the dialog's width
        label.setWordWrap(True)  # Enable word wrap

        input_field = QLineEdit()

        if contract_data is not None:
            if field_name in contract_data:
                input_field.setText(str(contract_data[field_name]))

        inner_layout = QHBoxLayout()
        inner_layout.addWidget(label)

        choices = [item["preset_label"] for item in self._delivery_interval_presets]

        choices_bundles = [item for item in self._delivery_interval_presets]

        interval_preset_chooser = gen_preset_interval_chooser(choices, self.on_preset_changed,
                                                              input_field, choices_bundles,
                                                              CUSTOM_DELIVERY_STEPS_TIME_OPTION)
        if field_name.lower() == "deliveryintervalinsteps":
            inner_layout.addWidget(interval_preset_chooser)

        inner_layout.addWidget(input_field)

        layout.addLayout(inner_layout)
        self._input_fields.append((field_name, input_field))

    def _generate_input_items(self):
        """Entry point for generating input items"""

        layout = self.ui.verticalLayout

        # Create input rows dynamically based on the item list
        for field_name in self._selected_contracts[0].get_fields_to_edit():
            if field_name == Contract.KEY_PRODUCT:
                self._construct_product_chooser(layout, field_name)

                continue

            field_type = self._selected_contracts[0].get_field_type(field_name)

            if field_type == self._selected_contracts[0].FIELD_TYPE_DATE_TIME:
                self._construct_date_time_chooser(layout, field_name, None)

                continue
            self._construct_default_input_field(layout, field_name, None)

    def create_btn_panel(self):
        """Construct the button panel"""
        cancel_button = QPushButton("Cancel", self)
        confirm_button = QPushButton("Confirm", self)
        cancel_button.clicked.connect(self.cancel)
        confirm_button.clicked.connect(self.confirm)

        # Create a QHBoxLayout for the buttons
        button_layout = QHBoxLayout()

        # Add the buttons to the button layout
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(confirm_button)

        self.ui.verticalLayout.addLayout(button_layout)

    def init_ui(self):
        input = QLineEdit(self)
        self.ui.verticalLayout.addWidget(input)

    def cancel(self):
        """Cancel the applied changes and close the dialog"""
        self.ui.close()

    def _check_if_agent_exists(self, agent_id) -> bool:

        if not self._scenario.agent_exists(agent_id):
            gen_quick_warning_modal(
                self, "Agent does not exist", "Agent with id " + str(agent_id) + " does not exist"
            )
            return False

        return True

    def _check_for_product_support(self, agent: Agent) -> bool:

        if not self._scenario.schema.agent_supports_product(
                self._scenario.schema.agent_types[agent.type_name], self._selected_contracts[0].product_name
        ):
            message = f"Agent with id '{str(agent.id)}' does not support the product: {self._selected_contracts[0].product_name}"
            gen_quick_warning_modal(self, "Sender does not support product", message)
            return False
        return True

    def confirm(self):
        """Confirm the applied changes and close the dialog"""
        data_dict = {}

        for field_name, input_field in self._input_fields:
            if isinstance(input_field, QLineEdit):
                input_field: QLineEdit
                data_dict[field_name] = input_field.text()

                try:
                    input_data = int(input_field.text())
                except Exception as exce:
                    logging.debug(F"OPTIONAL FIELD NOT SET {str(exce)}")
                    continue

                if field_name == Contract.KEY_SENDER or field_name == Contract.KEY_SENDER:
                    if not self._scenario.agent_exists(input_data):
                        if not self._check_if_agent_exists(input_data):
                            return

                    agent: Agent = self._scenario.get_agent_by_id(input_data)

                    if not self._check_for_product_support(agent):
                        return

            if isinstance(input_field, QDateTimeEdit):
                input_field: QDateTimeEdit
                data_dict[field_name] = input_field.dateTime().toString(DISPLAY_DATETIME_FORMAT)
            if isinstance(input_field, QComboBox):
                input_field: QComboBox
                data_dict[field_name] = input_field.currentText()

        for contract in self._selected_contracts:
            old_agent_dict = contract.to_dict()

            dict_to_send = {
                OLD_CONTRACT_KEY: old_agent_dict.copy(),
            }

            for key, value in data_dict.items():

                if value is None:
                    continue
                if str(value) == "":
                    continue
                if key == CONTRACT_PRODUCT_NAME:
                    if not self._product_changed:
                        continue

                if key == CONTRACT_RECEIVER_ID:
                    continue
                if key == CONTRACT_SENDER_ID:
                    continue
                old_agent_dict[key] = value

            old_agent_dict = contract_fields_to_natural_types(
                old_agent_dict, contract
            )
            updated_contract = Contract.from_dict(old_agent_dict)

            dict_to_send[UPDATED_CONTRACT_KEY] = updated_contract.to_dict()

            self._scenario.update_contract(
                old_contract=contract, updated_contract=updated_contract
            )

            self.on_contract_edited.emit(dict_to_send)

        self._controller.set_unsaved_changes(True)

        self.ui.accept()

    @staticmethod
    def select_date(date, line_edit):
        selected_date = date.toString(DISPLAY_DATE_FORMAT)
        line_edit.setText(selected_date)
