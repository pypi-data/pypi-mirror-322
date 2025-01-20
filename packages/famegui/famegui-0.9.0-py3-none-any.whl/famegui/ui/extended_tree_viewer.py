import re
import typing

import PySide6
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication

from famegui.config.runtime_consts import CONTRACT_SENDER_ID, CONTRACT_RECEIVER_ID, CONTRACT_PRODUCT_NAME
from famegui.utils import get_product_name_from_contract
from famegui.fame_tools.string_utils import extract_product_name_from_contract_identifier, extract_id_from_contract_identifier


class ExtendedTreeWidget(QTreeWidget):
    """Tree widget that uses custom event signals/triggers to communicate with the main application"""

    all_agents_deletion_requested = QtCore.Signal(str, name="del_all_agents_of_type")
    single_agent_deletion_requested = QtCore.Signal(int, name="del_single_agent")
    single_contract_deletion_requested = QtCore.Signal(
        int, int, str, name="del_single_agent"
    )  # agent_sender_id,agent_receiver_id, product_name
    agent_deletion_requested = QtCore.Signal(int, name="agent_deletion_requested")
    on_multi_contract_selected = QtCore.Signal(list,
                                               name="on_multi_contract_selected")  # list of {ref_agent_id, target_agent_id,

    # product_name, given_contract_type}

    def __init__(self, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)
        self.itemClicked.connect(self.on_item_clicked)

        self._cross_selected_items = {}
        self._cross_selected_items_original_colors = {}


    def on_item_clicked(self, item, column):
        item.setSelected(True)
        item: QTreeWidgetItem

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.KeyboardModifier.ControlModifier

        if ctrl_pressed:

            self._cross_selected_items[id(item)] = item

            self._cross_selected_items_original_colors[id(item)] = item.background(0).color()
            item.setBackground(0, QColor("#FFDF64"))

    def keyReleaseEvent(self, event):

        if event.key() == Qt.Key.Key_Control:

            selected_items = [value for _, value in self._cross_selected_items.items()]

            for item_key, item in self._cross_selected_items.items():
                item.setBackground(0, self._cross_selected_items_original_colors[item_key])

            tree_item_labels = [item.text(0) for item in selected_items]

            if len(selected_items) < 2:
                self._cross_selected_items.clear()
                return

            for item in tree_item_labels:
                if not item.__contains__("#") or not item.__contains__("("):
                    self._cross_selected_items.clear()
                    super().keyReleaseEvent(event)
                    return

            selected_contracts = []

            for item in selected_items:

                parent = item.parent()
                if parent is None:
                    self._cross_selected_items.clear()
                    super().keyReleaseEvent(event)
                    return
                tree_item_label = parent.text(0)
                ref_agent_id = extract_id_from_contract_identifier(parent.text(0))

                given_contract_type = item.data(1, QtCore.Qt.ItemDataRole.UserRole)
                target_agent_id = extract_id_from_contract_identifier(item.text(0))

                product_name = extract_product_name_from_contract_identifier(item.text(0))

                sender_id, receiver_id = None, None

                if given_contract_type == "sender":
                    sender_id = ref_agent_id
                    receiver_id = target_agent_id
                else:
                    sender_id = target_agent_id
                    receiver_id = ref_agent_id

                selected_contract_item = {
                    CONTRACT_SENDER_ID: sender_id,
                    CONTRACT_RECEIVER_ID: receiver_id,
                    CONTRACT_PRODUCT_NAME: product_name
                }


                selected_contracts.append(selected_contract_item)

            self.on_multi_contract_selected.emit(selected_contracts)
            self._cross_selected_items.clear()

            super().keyReleaseEvent(event)

        super().keyReleaseEvent(event)

    def _get_id_from_item_desc(self, text: str):
        # extract id from text
        pattern = r"#(\d+)"
        match = re.search(pattern, text)

        if match:
            result = match.group(1)
            return result
        else:
            return ""

    def process_contract_deletion(
            self, text_of_selected_item: str, current_item, agent_id_ref
    ):
        selected_agent_id = current_item.parent().data(0, QtCore.Qt.UserRole)
        connection_type = current_item.data(1, QtCore.Qt.UserRole)  # sender or receiver
        operator_name_two = get_product_name_from_contract(text_of_selected_item)

        if connection_type == "sender":
            self.single_contract_deletion_requested.emit(
                int(selected_agent_id),
                int(agent_id_ref),
                operator_name_two,
            )
            return
        self.single_contract_deletion_requested.emit(
            int(agent_id_ref),
            int(selected_agent_id),
            operator_name_two,
        )

    def keyPressEvent(self, event):
        """Process key press event to process the deletion of agents and contracts"""
        if event.key() == Qt.Key_Delete:
            selected_items = self.selectedItems()

            for item in selected_items:
                parent = item.parent()
                text_of_selected_item = self.currentItem().text(0)

                if not parent:  # -> check if item has no parent to trigger the deletion of all agents of a certain type
                    self.all_agents_deletion_requested.emit(text_of_selected_item)
                    return

                agent_id_ref = self._get_id_from_item_desc(text_of_selected_item)

                if agent_id_ref:
                    # item has a parent and is a contract or single agent
                    non_agent_root_item = self.currentItem()

                    if not self.currentItem().text(0).__contains__(
                            "("):  # use display id to check if item is a contract

                        self.agent_deletion_requested.emit(int(agent_id_ref))

                        return

                    self.process_contract_deletion(
                        text_of_selected_item, non_agent_root_item, agent_id_ref
                    )

                    return
