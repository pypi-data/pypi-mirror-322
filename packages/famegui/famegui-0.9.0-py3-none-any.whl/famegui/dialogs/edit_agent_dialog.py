import copy
import logging

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import QDialog, QTreeWidget, QSizePolicy, QVBoxLayout, QWidget, QDialogButtonBox
from PySide6.QtWidgets import QTreeWidgetItem
from fameio.input.scenario import Attribute
from fameio.input.schema import AttributeSpecs

from famegui.models import Agent, Scenario
from famegui.ui.attribute_row_item import AttributeTreeItem
from famegui.ui.quick_modals import gen_quick_warning_modal
from famegui_runtime_helper.attribute_dict_formatting_helper import get_sub_attr


class EditAgentDialog(QDialog):
    """Dialog for editing agent attributes"""

    trigger_input_validation = QtCore.Signal()
    handle_agent_attr_value_change_signal = QtCore.Signal(int, str, str)
    validation_error_signal = QtCore.Signal(bool, str)

    def __init__(self, scenario, working_dir, agents: [Agent], main_ctrl, ui_loader):
        super().__init__()

        self._loader = ui_loader
        self.default_agent_flat_value_dict = None
        self.validation_list = []
        self.setWindowTitle("EditAgentDialog")

        self.attr_top_tree_items = []
        self.validation_data = []

        self._agents = agents
        self._scenario = scenario
        self._working_dir = working_dir
        self._main_ctrl = main_ctrl
        self._schema = scenario.schema

        self._button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self._button_box.accepted.connect(self.accept)  # Close the dialog with `Accepted` result
        self._button_box.rejected.connect(self.reject)  # C

        self.init_ui()
        for item in self._agents:
            item: Agent
            tree_item = QTreeWidgetItem(self.treeWidgetShowSelectedAgents)
            tree_item.setCheckState(0, Qt.Checked)
            tree_item.setText(1, str(item.id))
            tree_item.setText(2, item.type_name)
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.Window
        )

        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)

        self.undo_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)  # Qt.ApplicationShortcut context

        self.exec_()

    def init_ui(self):
        # Main vertical layout for the dialog

        # Set the main layout to the dialog

        self.setMinimumHeight(800)
        self.setMinimumWidth(950)

        self.treeWidget = QTreeWidget()
        self.treeWidgetShowSelectedAgents = QTreeWidget()

        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels([self.tr("Attribute"), self.tr("Value")])
        self.treeWidget.setColumnWidth(0, 200)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidgetShowSelectedAgents.setRootIsDecorated(False)

        self.treeWidgetShowSelectedAgents: QTreeWidget
        self.treeWidgetShowSelectedAgents.setStyleSheet(
            "QTreeWidget::item { padding: 5px; }"
        )

        self.treeWidgetShowSelectedAgents.setFixedHeight(200)
        self.treeWidgetShowSelectedAgents.setColumnCount(3)
        self.treeWidgetShowSelectedAgents.setHeaderLabels(
            [self.tr("selected"), self.tr("#id"), self.tr("agent type")]
        )
        self.treeWidgetShowSelectedAgents.setColumnWidth(0, 200)
        self.treeWidgetShowSelectedAgents.setAlternatingRowColors(True)

        self.treeWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.validation_error_signal.connect(self.on_err_validation)
        self.handle_agent_attr_value_change_signal.connect(self.on_agent_attr_changed)

        font = QFont()
        font.setBold(True)
        font.setPointSize(12)

        if len(self._agents) == 1:
            preloaded_agent = self._agents[0]
            preloaded_agent: Agent
            self.default_agent_flat_value_dict = preloaded_agent.get_flat_agent_attributes_dict()

            self.init_agent_data(preloaded_agent)
        else:
            first_agent: Agent = self._agents[0]
            current_agent_type = first_agent.type_name

            sub_dict = get_sub_attr(self._scenario.schema.agent_types[current_agent_type].attributes.items(),
                                    None, current_agent_type)

            self.default_agent_flat_value_dict = sub_dict
            self._reset_attributes()

        main_layout = QVBoxLayout(self)

        top_widget = QWidget()
        top_widget_layout = QVBoxLayout()
        top_widget_layout.addWidget(self.treeWidgetShowSelectedAgents)
        top_widget.setLayout(top_widget_layout)

        bottom_widget = QWidget()

        bottom_layout = QVBoxLayout()
        bottom_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        bottom_layout.setStretch(0, 1)
        bottom_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        bottom_layout.addWidget(self.treeWidget, stretch=1)

        bottom_widget.setLayout(bottom_layout)
        scroll_area = QWidget()

        scroll_area.setLayout(bottom_layout)
        bottom_area = QtWidgets.QWidget()

        bottom_scroll_area = QVBoxLayout()
        bottom_scroll_area.addWidget(scroll_area, stretch=1)
        bottom_scroll_area.addWidget(self._button_box)

        bottom_area.setLayout(bottom_scroll_area)

        # Add widgets to layout with equal stretch factors
        main_layout.addWidget(top_widget, stretch=1)
        main_layout.addWidget(bottom_area, stretch=4)

        self.treeWidget.setUniformRowHeights(False)

        self._bottom_area = bottom_area

        self.setLayout(main_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        current_height = self.get_tree_content_height(self.treeWidget)

        new_max_bottom_area_height = self._bottom_area.height()

        if len(self.attr_top_tree_items) == 0:
            return

        attr_tree_item = self.attr_top_tree_items[0]

        attr_tree_item: AttributeTreeItem

        attr_tree_item.set_schema_widget_height(new_max_bottom_area_height)

    def reject(self):

        self._reset_attributes()
        super().reject()

    def accept(self):
        self._on_accept()
        # super().accept()

    def get_ui(self):
        return self

    def get_tree_content_height(self, tree_widget):
        total_height = 0
        for i in range(tree_widget.topLevelItemCount()):
            item = tree_widget.topLevelItem(i)
            total_height += tree_widget.visualItemRect(item).height()
            # Add height of expanded children
            if item.isExpanded():
                for j in range(item.childCount()):
                    child = item.child(j)
                    total_height += tree_widget.visualItemRect(child).height()
        return total_height

    def _group_invalid_data(self):
        """Group invalid data into a string to be displayed in a modal"""
        start_str = "The Following attributes are not valid:\n"

        for item in self.validation_data:
            for item_key, item_value in item.items():
                if item_key != "msg":
                    continue
                if not item["is_valid"]:
                    start_str += "- {}\n".format(item["msg"])

        return start_str

    def on_agent_attr_changed(self, agent_id, new_value, attr_name):

        """Receive signal from a panel item and print the new value"""

        logging.info(f"Attribute changed to: {new_value} for attribute: {attr_name}")

    def on_err_validation(self, is_valid, attr_name):
        """Receive validation error signal from  a panel item and append to validation data to be checked later"""

        self.validation_data = [
            item for item in self.validation_data if item["msg"] != attr_name
        ]

        self.validation_data.append({"is_valid": is_valid, "msg": attr_name})

    def init_agent_data(self, agent: Agent):
        """Initialize agent default data by building the rows of  tree widget"""
        self.treeWidget.clear()

        schema_attributes = self._scenario.schema.agent_types[
            agent.type_name

        ].attributes.items()

        for attr_name, attr_spec in schema_attributes:
            default_attr = None
            attr_spec: AttributeSpecs

            if attr_spec.has_nested_attributes:
                default_attr = agent.attributes.items()

                for item_key, item_value in agent.attributes.items():
                    if item_key == attr_name:
                        default_attr = item_value
                        break

                if not isinstance(default_attr, Attribute):
                    default_attr = None

            else:
                if attr_name in agent.attributes:
                    default_attr = agent.attributes[attr_name]

            if self.validation_error_signal is None:
                raise Exception("self.validation_error_signal is None")

            flat_values = agent.get_flat_agent_attributes_dict()

            agent_type = self._schema.agent_type_from_name(agent.type_name)

            sub_dict = get_sub_attr(agent_type.attributes.items(), flat_values, agent.type_name)

            item = AttributeTreeItem(
                self.treeWidget,
                attr_name,
                attr_spec,
                self._scenario,
                self._working_dir,
                onInputChanged=self.handle_agent_attr_value_change_signal,
                validation_signal=self.trigger_input_validation,
                validation_error_signal=self.validation_error_signal,
                default_value=default_attr,
                flat_default_values=sub_dict[attr_name],
                is_single_item=len(schema_attributes) == 1
            )

            self.attr_top_tree_items.append(item)

    def _on_cancel(self):
        """Close dialog"""

        self.close()

    @staticmethod
    def _match_type_and_id(agent_type, checked_agents_ids_set: set, agent: Agent):
        """Check if agent is of given type and id is in checked_agents_ids_set"""
        return agent.type_name == agent_type and agent.id in checked_agents_ids_set

    def _save_changes(self):
        '''Save changes to scenario'''

        top_lvl_tree_agents = [
            self.treeWidgetShowSelectedAgents.topLevelItem(i)
            for i in range(self.treeWidgetShowSelectedAgents.topLevelItemCount())
        ]

        checked_agents = [item for item in top_lvl_tree_agents if item.checkState(0) == Qt.Checked]
        checked_agents_ids = set([int(item.text(1)) for item in checked_agents])

        self._scenario: Scenario

        matching_agents = [
            agent
            for agent in copy.deepcopy(self._scenario.agents)
            if self._match_type_and_id(agent.type_name, checked_agents_ids, agent)
        ]

        for agent in matching_agents:
            agent.attributes.clear()
            for item in self.attr_top_tree_items:
                item: AttributeTreeItem

                if item.attr_value is not None:
                    value = item.attr_value
                    if isinstance(value, dict):
                        value: dict
                        if not value:
                            continue

                    agent.attributes[item.attr_name] = item.attr_value

            self._scenario.update_agent(agent)

        self._main_ctrl.set_unsaved_changes(True)

        self._reset_attributes()

        self.close()

    def _on_accept(self):
        '''Apply entered changes and close dialog if all data is valid'''
        self.validation_data.clear()
        self.trigger_input_validation.emit()

        # Notify the user if there are any invalid attributes with an Alert
        for validated_item in self.validation_data:
            for item_key, item_value in validated_item.items():
                if isinstance(item_value, bool):
                    if not item_value:
                        gen_quick_warning_modal(self, "Validation error", self._group_invalid_data())

                        return

        self._save_changes()

    def _reset_attributes(self):
        """Reset UI to default state"""
        self.treeWidget.clear()
        self.attr_top_tree_items.clear()
        current_agent_type = self._agents[0].type_name

        self.attr_top_tree_items.clear()

        for idx, (attr_name, attr_spec) in enumerate(self._scenario.schema.agent_types[
                                                         current_agent_type
                                                     ].attributes.items()):
            item = AttributeTreeItem(
                self.treeWidget,
                attr_name,
                attr_spec,
                self._scenario,
                self._working_dir,
                onInputChanged=self.handle_agent_attr_value_change_signal,
                validation_signal=self.trigger_input_validation,
                validation_error_signal=self.validation_error_signal,
                flat_default_values=self.default_agent_flat_value_dict if len(self._agents) == 1 else self.default_agent_flat_value_dict[attr_name]

            )
            self.attr_top_tree_items.append(item)

    def update(self) -> None:
        """Update tree view and adjust size"""
        super().update()
