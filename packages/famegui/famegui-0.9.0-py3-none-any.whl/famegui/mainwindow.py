# This Python file uses the following encoding: utf-8
import getpass
import logging
import os
import re
import typing
from functools import partial

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QModelIndex, Qt, QPointF, QPoint, QSize, QEvent
from PySide6.QtGui import QColor, QKeySequence
from PySide6.QtGui import QShortcut, QAction, QBrush, QPixmap, QPainter, QFont, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMessageBox,
    QLabel,
    QTreeWidgetItem,
    QGraphicsScene)
from PySide6.QtWidgets import QPushButton, QWidget, QTreeWidget, QHBoxLayout, QVBoxLayout, \
    QScrollArea, QTextEdit, QGraphicsView, QFrame, QSlider
from PySide6.QtWidgets import QSizePolicy
from fameio.input.scenario import Attribute
from fameio.input.schema import AttributeType

""" needs to be imported to load the resources """
""" Some IDEs may mark this as unused, but it is needed to load the resources """
# noinspection PyUnresolvedReferences
import famegui.generated.qt_resources_rc
from famegui import models
from famegui.agent_controller import AgentController
from famegui.appworkingdir import AppWorkingDir
from famegui.config.runtime_consts import CONTRACT_RECEIVER_ID, UPDATED_CONTRACT_KEY, OLD_CONTRACT_KEY, \
    CONTRACT_SENDER_ID, CONTRACT_PRODUCT_NAME
from famegui.data_manager.loader import load_db_data
from famegui.database.db_management import (
    get_recently_opened_projects,
    manage_path_for_db)
from famegui.database.prebuild_queries.general import get_stored_shortcuts
from famegui.dialogs.ask_for_agent_deletion_dialog import DeletionDialog
from famegui.dialogs.dialog_new_multi_dialog import DialogNewMultiContract
from famegui.dialogs.dialog_newagent import DialogNewAgent
from famegui.dialogs.dialog_newcontract import DialogNewContract
from famegui.dialogs.dialog_scenario_properties import DialogScenarioProperties
from famegui.dialogs.edit_agent_dialog import EditAgentDialog
from famegui.dialogs.edit_contract_dialog import EditContractDialog
from famegui.dialogs.famegui_config_presets_dialog import EditFameDbValuesDialog
from famegui.dialogs.multi_edit_contract_dialog import MultiEditContractDialog
from famegui.famegui_widgets.TimeSeriesPlotCanvasWidget import TimeSeriesPlotCanvas
from famegui.generated.ui_mainwindow import Ui_MainWindow
from famegui.maincontroller import MainController
from famegui.model_utils.contract_helper import get_contract_from_fields
from famegui.models import Agent, Contract
from famegui.path_resolver import FameGuiPathResolver
from famegui.scenario_canvas_elements.agent_canvas_item import AgentGraphItem
from famegui.scenario_canvas_elements.contract_canvas_item import ContractGraphItem
from famegui.scenario_graph_view import ScenarioGraphView
from famegui.ui.fame_ui_elements import QFameBoldLabel
from famegui.ui.main_graphics_widget import MainGraphicsWidget
from famegui.ui.quick_modals import gen_quick_warning_modal
from famegui.ui.ui_utils import GUIConsoleHandler
from famegui.utils import get_product_name_from_contract
from famegui_runtime_helper.dict_hash_helper import hash_dict


class PropertyTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(
            self,
            parent: QtWidgets.QTreeWidget,
            attr_name: str,
            attr_value: Attribute,
    ):
        super().__init__(parent, [attr_name, str(attr_value.value)])
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

    def setData(self, column, role, value):
        """Override QTreeWidgetItem.setData()"""
        if role == QtCore.Qt.EditRole:
            # review: Can we remove this code? It seems to be unused at the moment and not necessary.
            # logging.info("new value: {}".format(value))
            pass

        QtWidgets.QTreeWidgetItem.setData(self, column, role, value)


class MainWindow(QMainWindow):
    """Application entry point"""

    def __init__(self, working_dir: AppWorkingDir, ui_file_loader):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._ui_file_loader = ui_file_loader
        self._working_dir = working_dir
        self._path_resolver = FameGuiPathResolver(self._working_dir)
        self._tree_items_for_agent_types = {}
        self._controller = MainController(self._working_dir)

        # init
        self._init_ui()
        self._connect_actions()
        self._connect_slots()
        self._on_project_closed()

        self._graph_view.installEventFilter(self)

        load_db_data()

        self._setup_shortcuts()

    def on_ctrl_x_activated(self):
        modifiers = QApplication.keyboardModifiers()

        # Check if Shift modifier was held down
        if modifiers == QtCore.Qt.KeyboardModifier.ShiftModifier:
            logging.info("Shift key was pressed along with the shortcut!")
        else:
            logging.info("Shortcut activated without Shift.")

        self.rearrange_layout()

    def handle_redo(self):
        """Performs redo OP if it's triggered by the toolbar or a shortcut"""
        logging.info("Performing redo ...")
        self._controller.perform_redo()

    def handle_undo(self):
        """Performs undo OP if it's triggered by the toolbar or a shortcut"""

        if not self._controller.is_open:
            return

        self._controller.perform_undo()
        self._graph_view.update_all_contracts()

    def set_item_background_color_till_depth(self, item, color, current_depth=0):
        """
        Set the background color for QTreeWidgetItems explicit agents (agent nodes)
        """
        if current_depth <= 1:  # Apply color only if depth is 0 or 1
            for col in range(item.columnCount()):
                item.setBackground(col, color)

        if current_depth < 1:  # Recursively handle children if depth is less than 1
            for i in range(item.childCount()):
                self.set_item_background_color_till_depth(item.child(i), color, current_depth + 1)

    def handle_agent_color_change(self):
        """Apply newly assigned agent type color on all associated ui elements"""

        agent_ids_to_type = self._controller.get_agent_ids_to_type()

        ui_type_to_color_mapping, agent_type_names_from_db = (
            self._controller.get_agent_type_to_color_with_type_listing())

        for agent_graph_item in self._graph_view.get_agent_items()[:]:
            agent_graph_item: AgentGraphItem
            color = ui_type_to_color_mapping[agent_ids_to_type[agent_graph_item.agent_id]]

            agent_graph_item.set_bg_color(color)
            agent_graph_item.update()

        for i in range(self.ui.treeProjectStructure.topLevelItemCount()):
            tree_widget_item = self.ui.treeProjectStructure.topLevelItem(i)
            agent_type = tree_widget_item.text(0)

            color = QColor(ui_type_to_color_mapping[agent_type])

            self.set_item_background_color_till_depth(tree_widget_item, color)

    def handle_db_load_shortcut(self):

        load_db_data()

    def _init_ui(self):
        self._setup_tool_bar_nav_items()
        logging.debug("initializing main window UI")
        self.setWindowIcon(QtGui.QIcon(":/icons/nodes-128px.png"))

        # create and attach the scene
        self.fame_graphicsView = MainGraphicsWidget()
        self.fame_graphicsView.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.fame_graphicsView.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)

        self._graph_view = ScenarioGraphView(
            self._on_agent_dragged,
            self)

        self._graph_view.setSceneRect(self._controller.compute_scene_rect())
        self.fame_graphicsView.setScene(self._graph_view)
        # important: set the index method to NoIndex, otherwise the scene will not be updated correctly and crash
        self._graph_view.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)

        # customize main window
        self.ui.labelUserName.setText(getpass.getuser())
        self.fame_graphicsView.setBackgroundBrush(QtGui.QColor(194, 194, 194))

        self.fame_graphicsView.unselect_contracts.connect(self.clear_contract_highlights)
        self.ui.consoleLogTextEdit.setStyleSheet("background: #2D2D2D;")
        self.ui.consoleLogTextEdit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.ui.consoleLogTextEdit.setMinimumSize(300, 100)
        self.fame_graphicsView.setMinimumSize(400, 400)
        self.fame_graphicsView.setBaseSize(600, 600)

        self.setWindowTitle(QtWidgets.QApplication.instance().applicationDisplayName())

        # Zoom-related setup
        self.fame_graphicsView.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.fame_graphicsView.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.fame_graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.fame_graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.fame_graphicsView.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        # May enhance performance with hardware acceleration
        # However Anti-Aliasing is not kicking in on far distances
        # self.fame_graphicsView.setViewport(QOpenGLWidget())

        self.fame_graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.fame_graphicsView.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.ui.centralwidget.setStretchFactor(0, 1)  # Top frame
        self.ui.centralwidget.setStretchFactor(1, 4)  # Graphics view
        self.ui.centralwidget.setStretchFactor(2, 2)  # Console

        bottom_box = QWidget()

        logger = logging.getLogger()
        clearButton = QPushButton("Clear")
        self.ui.verticalLayoutBottomDeep.addWidget(clearButton)
        label_main = QTextEdit()
        bottom_box_layout_v = QVBoxLayout()
        self.sliderZoomFactor = QSlider()

        self.labelZoomFactor = QLabel()
        font2 = QFont()
        font2.setPointSize(10)
        self.labelZoomFactor.setFont(font2)

        zoom_lvl_layout = QHBoxLayout()
        zoom_lvl_layout.addWidget(self.labelZoomFactor)
        zoom_lvl_layout.addWidget(self.sliderZoomFactor)

        slider_control_panel_widget = QWidget()
        slider_control_panel_widget.setLayout(zoom_lvl_layout)

        bottom_box_layout_v.addWidget(slider_control_panel_widget)
        bottom_box_layout_v.addWidget(label_main)

        bottom_box.setLayout(bottom_box_layout_v)

        logger.addHandler(GUIConsoleHandler(label_main, clearButton))

        for i in reversed(range(self.ui.centralwidget.count())):
            widget = self.ui.centralwidget.widget(i)
            if widget is not None:
                widget.setParent(None)

        top_box = QWidget()
        top_box.setStyleSheet("background-color: lightblue;")

        top_box_layout = QVBoxLayout()
        graphics_frame = QFrame()

        top_box_layout.addWidget(self.fame_graphicsView)

        # top_box.setLayout(top_box_layout)
        graphics_frame.setLayout(top_box_layout)

        self.ui.centralwidget.addWidget(graphics_frame)
        self.ui.centralwidget.addWidget(bottom_box)

        self.sliderZoomFactor.setObjectName(u"sliderZoomFactor")
        self.sliderZoomFactor.setMaximumSize(QSize(200, 1000))
        self.sliderZoomFactor.setMinimum(10)
        self.sliderZoomFactor.setMaximum(200)
        self.sliderZoomFactor.setSingleStep(10)
        self.sliderZoomFactor.setValue(100)
        self.sliderZoomFactor.setOrientation(Qt.Orientation.Horizontal)

        # allowed zoom range
        self.sliderZoomFactor.setRange(10, 1000)
        # status bar
        self._status_label_icon = QtWidgets.QLabel()
        self.statusBar().addWidget(self._status_label_icon)

        # project structure tree view
        self.ui.treeProjectStructure.all_agents_deletion_requested.connect(
            self._del_all_agents_of_type
        )

        self.ui.treeProjectStructure.setColumnCount(1)
        self.ui.treeProjectStructure.setHeaderLabels(["Agents"])
        # attributes tree view
        self.ui.treeAttributes.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )

        self.ui.treeAttributes.setRootIsDecorated(False)
        self.ui.treeAttributes.setColumnCount(2)
        self.ui.treeAttributes.setHeaderLabels(["Attribute", "Value"])
        self.ui.treeAttributes.setColumnWidth(0, 140)
        self.ui.treeAttributes.setAlternatingRowColors(True)
        self.ui.treeAttributes.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # console
        self.ui.consoleLogTextEdit.setMinimumHeight(70)

        # init global logger
        logger = logging.getLogger()
        self.ui.treeProjectStructure.clicked.connect(self.on_clicked_tree)

        # recently opened projects
        recently_opened_projects = get_recently_opened_projects()

        if len(recently_opened_projects) == 0:
            return

        another_menu = QMenu("Recently opened projects", self)

        for project in recently_opened_projects:
            action = QAction(project.path, self)
            action.triggered.connect(partial(self.open_project, project.path))
            another_menu.addAction(action)

        self.ui.menuok.addMenu(another_menu)

    def _setup_tool_bar_nav_items(self):
        self._undo_action = QAction(QIcon(), "Perform Undo", self)

        self._redo_action = QAction(QIcon(), "Perform Redo", self)

        self._undo_action.triggered.connect(self.handle_undo)
        self._redo_action.triggered.connect(self.handle_redo)

        self.ui.menu_Edit.addAction(self._undo_action)
        self.ui.menu_Edit.addAction(self._redo_action)
        self.ui.menu_Edit.addAction(self.ui.actionConfigMenu)

    def _on_agent_dragged(self, agent_id, agent_x, agent_y, agent_x_t, agent_y_t):

        self._controller.agent_model_was_modified(agent_id, agent_x, agent_y)

    def open_project(self, file_path):

        if not self._confirm_current_project_can_be_closed():
            return
        if file_path != "":
            manage_path_for_db(file_path)

            self.load_scenario_file(file_path)

    def _del_all_agents_of_type(self, agent_type_name: str):
        selected_agent_type_list = self._controller.get_all_agents_by_type_name(
            agent_type_name
        )
        DeletionDialog(
            selected_agent_type_list,
            scenario=self._controller.scenario,
            working_dir=self._working_dir,
            parent_widget=self.ui.widget,
            main_controller=self._controller,
        )

    def _connect_actions(self):
        logging.debug("connecting main window actions")
        # new
        self.ui.actionNewProject.triggered.connect(self.new_project)
        # open
        self.ui.actionOpenProject.triggered.connect(self.show_open_scenario_file_dlg)
        # save (enabled only when a change has been done)
        self.ui.actionSaveProject.triggered.connect(self.save_project)
        # save as
        self.ui.actionSaveProjectAs.triggered.connect(self.save_project_as)
        # close
        self.ui.actionCloseProject.triggered.connect(self.close_project)

        self.ui.actionCloseProject.setVisible(False)
        # generate protobuf
        self.ui.actionMakeRunConfig.triggered.connect(self.make_run_config)
        # exit
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.actionSchemaValidation.triggered.connect(self.revalidate_scenario)

        self.ui.actionGeneralProperties.triggered.connect(
            self._on_edit_scenario_properties
        )

        self.ui.actionConfigMenu.triggered.connect(
            self._on_edit_fame_gui_settings
        )

        # tree
        self.ui.treeProjectStructure.agent_deletion_requested.connect(
            self._on_single_agent_deletion_requested
        )
        self.ui.treeProjectStructure.single_contract_deletion_requested.connect(
            self._on_single_contract_deletion_requested
        )

        self.ui.treeProjectStructure.on_multi_contract_selected.connect(
            self._on_multi_contract_edit_requested
        )

        # self.ui.

    def _setup_shortcuts(self):
        """Setup Global Shortcuts with by user created preferences or defaults"""
        shortcut_data = get_stored_shortcuts()

        for item in shortcut_data:

            if item["shortcut_name"] == "undo":
                self._undo_action.triggered.connect(self.handle_undo)
                self._undo_action.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_redo":
                self._redo_action.triggered.connect(self.handle_redo)
                self._redo_action.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_load_yaml_into_db":
                self.load_from_db_shortcut = QShortcut(QKeySequence(item["shortcut_key"]), self)

                self.load_from_db_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
                self.load_from_db_shortcut.activated.connect(self.handle_db_load_shortcut)

            if item["shortcut_name"] == "rearrange_layout":
                self.ctrl_x_shortcut = QShortcut(QKeySequence(item["shortcut_key"]), self)
                self.ui.actionReArrangeLayout.triggered.connect(self.rearrange_layout)

                self.ctrl_x_shortcut.activated.connect(self.on_ctrl_x_activated)

            if item["shortcut_name"] == "action_new_project":
                self.ui.actionNewProject.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_open_project":
                self.ui.actionOpenProject.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_save_project":
                self.ui.actionSaveProject.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_quit_app":
                self.ui.actionExit.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_database_properties":
                self.ui.actionConfigMenu.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_config_properties":
                self.ui.actionGeneralProperties.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_make_run_config":
                self.ui.actionMakeRunConfig.setShortcut(QKeySequence(item["shortcut_key"]))

            if item["shortcut_name"] == "action_schema_validation":
                self.ui.actionSchemaValidation.setShortcut(QKeySequence(item["shortcut_key"]))

    def _on_multi_contract_edit_requested(self, selected_contracts: list[dict]):
        """opens up a multi edit  dialog for several selected contracts"""

        selected_contract_models = [get_contract_from_fields(self._controller.scenario,
                                                             contract_data[CONTRACT_PRODUCT_NAME],
                                                             contract_data[CONTRACT_RECEIVER_ID],
                                                             contract_data[CONTRACT_SENDER_ID])
                                    for contract_data in selected_contracts]

        MultiEditContractDialog(selected_contract_models, self._controller.scenario,
                                self._controller,
                                on_contract_edited_slot=self._on_contract_edited)

    def _on_single_agent_deletion_requested(self, agent_id: int):
        """opens up a deletion dialog for a single agent"""
        DeletionDialog(
            [self._controller.agent_from_id(agent_id)],
            scenario=self._controller.scenario,
            working_dir=self._working_dir,
            parent_widget=self.ui.widget,
            main_controller=self._controller,
        )

    def _get_contract_tree_items(
            self, sender_agent: Agent, receiver_agent: Agent, product_name: str
    ) -> typing.List[QTreeWidgetItem]:
        """returns a list of tree leaf items that represent the contract between the two agents"""

        contract_ids = {sender_agent.id, receiver_agent.id}
        contract_tree_items = []
        agent_type_names = {sender_agent.type_name, receiver_agent.type_name}
        for i in range(self.ui.treeProjectStructure.topLevelItemCount()):
            top_lvl_item = self.ui.treeProjectStructure.topLevelItem(i)
            agent_type = top_lvl_item.text(0)

            if agent_type not in agent_type_names:
                continue
            for agent_child_idx in range(top_lvl_item.childCount()):
                selected_node = top_lvl_item.child(agent_child_idx)
                selected_node_id = int(
                    top_lvl_item.child(agent_child_idx).data(0, Qt.ItemDataRole.UserRole)
                )

                if selected_node_id not in contract_ids:
                    continue
                for contract_child_idx in range(selected_node.childCount()):
                    selected_contract_leaf = selected_node.child(contract_child_idx)
                    contract_description = selected_contract_leaf.text(0)
                    if product_name not in contract_description:
                        continue
                    if (
                            str(sender_agent.id) not in contract_description
                            and str(receiver_agent.id) not in contract_description
                    ):
                        continue
                    contract_tree_items.append(selected_contract_leaf)

        return contract_tree_items

    def _remove_contract_tree_items(
            self, sender_agent: Agent, receiver_agent: Agent, product_name: str
    ):
        """removes the contract leaf items between the two agents from the tree"""
        contract_ids = {sender_agent.id, receiver_agent.id}
        contract_leafs_to_remove_idx = []
        contract_to_removes = []

        agent_type_names = {sender_agent.type_name, receiver_agent.type_name}
        for i in range(self.ui.treeProjectStructure.topLevelItemCount()):
            top_lvl_item = self.ui.treeProjectStructure.topLevelItem(i)
            agent_type = top_lvl_item.text(0)

            if agent_type not in agent_type_names:
                continue
            for agent_child_idx in range(top_lvl_item.childCount()):
                selected_node = top_lvl_item.child(agent_child_idx)
                selected_node_id = int(
                    top_lvl_item.child(agent_child_idx).data(0, Qt.ItemDataRole.UserRole)
                )

                if selected_node_id not in contract_ids:
                    continue
                contract_children = [
                    selected_node.child(contract_child_idx)
                    for contract_child_idx in range(selected_node.childCount())
                ]
                for idx, selected_contract_leaf in enumerate(contract_children[:]):
                    contract_description = selected_contract_leaf.text(0)
                    if product_name not in contract_description:
                        continue
                    if (
                            str(sender_agent.id) not in contract_description
                            and str(receiver_agent.id) not in contract_description
                    ):
                        continue

                    contract_leafs_to_remove_idx.append(idx)

                for contract_leaf_to_remove in contract_leafs_to_remove_idx:
                    contract_to_removes.append(
                        {
                            "sender_id": sender_agent.id,
                            "receiver_id": receiver_agent.id,
                            "product_name": get_product_name_from_contract(
                                contract_description
                            ),
                        }
                    )

                    selected_node.removeChild(
                        selected_node.child(contract_leaf_to_remove)
                    )

    def _remove_contract_tree_items_using_contract(self, contract: Contract):
        """removes the contract leaf items between the two agents from the tree using a contract object"""

        self._remove_contract_tree_items(
            self._controller.get_agent_ctrl(contract.sender_id).model,
            self._controller.get_agent_ctrl(contract.receiver_id).model,
            contract.product_name,
        )

    def _on_single_contract_deletion_requested(
            self, sender_agent_id: int, receiver_agent_id: int, product_name: str
    ):
        """opens up a deletion dialog for a single contract"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(
            f"Do you want to delete the contract with the sender: {sender_agent_id}\n.And the receiver: {receiver_agent_id}\nwith the product name:  ({product_name}) ?"
        )
        msg_box.setWindowTitle("Confirmation")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        msg_box.setDefaultButton(QMessageBox.No)

        response = msg_box.exec()

        alert_badge = QLabel()
        alert_badge.setText("Alert!")
        alert_badge.setStyleSheet(
            "background-color: red;"
            "color: white;"
            "border-radius: 8px;"
            "padding: 4px 8px;"
        )

        if response == QMessageBox.Yes:
            self._controller.remove_contract(
                sender_agent_id, receiver_agent_id, product_name
            )
            self.ui.treeProjectStructure.blockSignals(True)
            self._graph_view.blockSignals(True)

            self._controller.set_unsaved_changes(True)

            self._remove_contract_tree_items(
                self._controller.get_agent_ctrl(sender_agent_id).model,
                self._controller.get_agent_ctrl(receiver_agent_id).model,
                product_name,
            )

            self._graph_view.remove_contract(sender_agent_id, receiver_agent_id)

            self.ui.treeProjectStructure.blockSignals(False)
            self._graph_view.blockSignals(False)

    def revalidate_scenario(self):
        if not self._controller.is_open:
            return
        schema_valid = self._controller.revalidate_scenario()

        if schema_valid:
            gen_quick_warning_modal(
                self.parentWidget(),
                "Schema Validation",
                "The scenario is valid according to the schema",
            )

    # Contract UI Utils
    def rearrange_layout(self):
        """adjust the layout of the graph view in circular orbital mode"""
        if not self._controller.is_open:
            return
        self._controller.rearrange_layout()
        for item in self.fame_graphicsView.items():
            if issubclass(type(item), ContractGraphItem):
                item: ContractGraphItem
                item.adjust()

    def clear_contract_highlights(self):
        """Resets the highlight mode of all contract items in the graph view"""
        for item in self._graph_view.get_contract_items():
            if item.is_in_highlight_mode():
                item.set_highlight_mode(False)
                item.adjust()

    def _connect_slots(self):
        """Event handling for the main window"""
        logging.debug("initializing main window slots")

        agent_graph_items = self._graph_view

        self.sliderZoomFactor.valueChanged.connect(self._on_zoom_value_changed)

        self._graph_view.contract_creation_requested.connect(
            self._on_contract_creation_requested
        )

        self._graph_view.agent_creation_requested.connect(
            self._on_agent_creation_requested
        )

        self.fame_graphicsView.agent_deletion_requested.connect(
            self._on_agent_deletion_requested
        )

        self._graph_view.agent_edition_requested.connect(
            self._on_agent_edition_requested
        )

        self._graph_view.agent_multi_edition.connect(
            self._on_agent_multi_edition
        )

        self.ui.treeProjectStructure.currentItemChanged.connect(
            self._on_tree_view_current_item_changed
        )

        self.ui.treeProjectStructure.itemDoubleClicked.connect(
            self._on_tree_view_current_item_double_clicked
        )

        self.ui.lineFilterPattern.textChanged.connect(self._filter_pattern_changed)
        self._graph_view.zoom_in_requested.connect(
            lambda: self.sliderZoomFactor.setValue(
                self.sliderZoomFactor.value() + 10
            )
        )
        self._graph_view.released_multi_selection_mode.connect(
            self.on_multi_agent_select
        )

        self._graph_view.released_multi_selection_mode_no_valid.connect(
            self.clear_graph_from_multi_selection
        )
        self._graph_view.zoom_out_requested.connect(
            lambda: self.sliderZoomFactor.setValue(
                self.sliderZoomFactor.value() - 10
            )
        )

        self._controller.project_properties.changed.connect(
            self._on_scenario_status_changed
        )
        self._controller.agent_added.connect(self._on_agent_added)
        self._controller.contract_added.connect(self._on_contract_added)
        self._controller.contract_edited.connect(self._on_contract_edited)
        self._controller.contracts_deleted.connect(self._on_contract_removed)
        self._controller.agents_deleted.connect(self._on_agents_deleted)
        self._controller.selected_agent_changed.connect(self._on_selected_agent_changed)

        self._graph_view.selected_agent_changed.connect(
            self._controller.set_selected_agent_id)

        # undo

    def _on_agents_deleted(self, agent_ids: typing.List[int]):
        """initiates removal of agents from the graph view and the tree view"""
        self._graph_view.clearSelection(True)
        self.clear_contract_highlights()
        self.ui.treeAttributes.clear()
        self.remove_all_except_tree()

        self.ui.treeProjectStructure.blockSignals(True)

        for agent_id in agent_ids:
            agent_ctrl = self._controller.get_agent_ctrl(agent_id)
            self.remove_agent_tree_item(agent_ctrl)

        self._graph_view.remove_agents(agent_ids)

        self.ui.treeProjectStructure.blockSignals(False)

    def _on_agent_multi_edition(self, agent_list: list[str]):

        if not self._controller.check_if_all_agents_have_same_type(agent_list):
            gen_quick_warning_modal(
                self.parentWidget(),
                "Agent Type Mismatch",
                "All agents must have the same type",
            )
            return

        EditAgentDialog(
            agents=[self._controller.agent_from_id(agent_id).model for agent_id in agent_list],
            scenario=self._controller.scenario,
            working_dir=self._working_dir,
            main_ctrl=self._controller,
            ui_loader=self._ui_file_loader,
        )

    def _on_agent_edition_requested(self, agent_id: int):
        """initiates the agent edition dialog"""

        EditAgentDialog(
            agents=[self._controller.agent_from_id(agent_id).model],
            scenario=self._controller.scenario,
            working_dir=self._working_dir,
            main_ctrl=self._controller,
            ui_loader=self._ui_file_loader,
        )

    def _on_agent_deletion_requested(self, q_point: QPoint):
        """initiates the agent deletion dialog"""
        map_point: QPointF = self.fame_graphicsView.mapToScene(q_point)
        agent_id = self._graph_view.get_agent_id(map_point)
        if not agent_id:
            gen_quick_warning_modal(
                self.parentWidget(),
                "No Agent Selected",
                "Please select at least one agent\n"
                "or navigate your mouse to an agent",
            )
            return
        selected_agent = self._controller.agent_from_id(agent_id)
        DeletionDialog(
            [selected_agent],
            scenario=self._controller.scenario,
            working_dir=self._working_dir,
            parent_widget=self.ui.widget,
            main_controller=self._controller,
        )

    def _on_zoom_value_changed(self):
        zoom_factor = self.sliderZoomFactor.value()
        assert zoom_factor > 0
        scale_factor = zoom_factor * 0.001
        self.fame_graphicsView.setTransform(
            QtGui.QTransform.fromScale(scale_factor, scale_factor)
        )
        self.labelZoomFactor.setText("{} %".format(zoom_factor))

    def clear_graph_from_multi_selection(self):
        """Clears the graph view from multi selection mode by clearing the selection and the highlights"""
        self._graph_view.clearSelection(True)
        self.clear_contract_highlights()

    def _get_agent_list_from_ids(
            self, agent_id_list: typing.List[int]
    ) -> typing.List[Agent]:
        """Fetches the agent object list from the agent id list"""
        agent_list = []
        for agent_id in agent_id_list:
            agent_list.append(self._controller.agent_from_id(agent_id))
        return agent_list

    def on_multi_agent_select(self, sender_list: list, receiver_list: list):
        """Initiates the multi contract creation dialog"""

        self.clear_graph_from_multi_selection()
        sender_agent_list = self._get_agent_list_from_ids(sender_list)
        receiver_agent_list = self._get_agent_list_from_ids(receiver_list)

        dlg = DialogNewMultiContract(
            receiver_agent_list,
            sender_agent_list,
            self._controller.scenario.schema,
            self,
        )

        if dlg.exec_() != 0:
            for contract in dlg.make_new_contracts():
                self._controller.add_new_contract(contract)

    def _on_tree_view_current_item_double_clicked(self):
        """initiates a matching edition dialog"""
        assert self._controller.is_open
        tree_item = self.ui.treeProjectStructure.currentItem()

        if tree_item is not None:
            # note: the given id value can be None
            selected_agent_id = tree_item.data(0, QtCore.Qt.ItemDataRole.UserRole)

            if selected_agent_id:
                agent_ctrl_list = [self._controller.agent_from_id(selected_agent_id)]
                agent_model_list = [agent_ctrl.model for agent_ctrl in agent_ctrl_list]

                EditAgentDialog(
                    agents=agent_model_list,
                    scenario=self._controller.scenario,
                    working_dir=self._working_dir,

                    main_ctrl=self._controller,
                    ui_loader=self._ui_file_loader,

                )

                return
            agent_type = tree_item.text(0)
            if agent_type:
                selected_agents = self._controller.get_all_agents_by_type_name(
                    agent_type
                )
                if len(selected_agents) != 0:
                    EditAgentDialog(
                        agents=selected_agents,
                        scenario=self._controller.scenario,
                        working_dir=self._working_dir,
                        main_ctrl=self._controller,
                        ui_loader=self._ui_file_loader,
                    )
                    return

            # single contract selection
            parent_agent_item = tree_item.parent()
            selected_con_agent_id = tree_item.data(2, QtCore.Qt.ItemDataRole.UserRole)
            parent_agent_item_id = parent_agent_item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            product_name = get_product_name_from_contract(
                tree_item.data(1, QtCore.Qt.ItemDataRole.UserRole)
            )

            if tree_item.data(1, QtCore.Qt.ItemDataRole.UserRole) == "receiver":
                edit_contract_dlg = EditContractDialog(
                    self._controller.get_contract(
                        selected_con_agent_id, parent_agent_item_id, product_name
                    ),
                    self._controller.scenario,
                    self._controller,
                    on_contract_edited_slot=self._on_contract_edited,
                )
                edit_contract_dlg.on_contract_edited.connect(self._on_contract_edited)

                return

            EditContractDialog(
                self._controller.get_contract(
                    parent_agent_item_id, selected_agent_id, product_name
                ),
                self._controller.scenario,
                self._controller,
                on_contract_edited_slot=self._on_contract_edited,
            )

    def _on_contract_removed(self, agent_id: int):
        """Clears the graph view and the tree view from the given agent id after removing it from the scenario"""
        related_contracts = self._controller.get_all_related_contracts(agent_id)
        self.ui.treeProjectStructure.blockSignals(True)
        self._graph_view.blockSignals(True)

        for related_contract in related_contracts:
            self._graph_view.remove_contract(
                related_contract.sender_id, related_contract.receiver_id
            )
            self._remove_contract_tree_items_using_contract(related_contract)

        self.ui.treeProjectStructure.blockSignals(False)
        self._graph_view.blockSignals(False)
        self._controller.set_unsaved_changes(True)

    def _on_contract_edited(self, contracts: dict):
        """Updates the graph view and the tree view after editing a contract"""
        self._graph_view.clearSelection()
        old_contract_sender_ctrl = self._controller.get_agent_ctrl(contracts[OLD_CONTRACT_KEY][CONTRACT_SENDER_ID])
        old_contract_receiver_ctrl = self._controller.get_agent_ctrl(contracts[OLD_CONTRACT_KEY][CONTRACT_RECEIVER_ID])
        new_contract_sender_ctrl = self._controller.get_agent_ctrl(contracts[UPDATED_CONTRACT_KEY][CONTRACT_SENDER_ID])
        new_contract_receiver_ctrl = self._controller.get_agent_ctrl(
            contracts[UPDATED_CONTRACT_KEY][CONTRACT_RECEIVER_ID])

        self._graph_view.remove_contract(
            old_contract_sender_ctrl.id,
            old_contract_receiver_ctrl.id,
        )

        self._graph_view.add_contract(
            new_contract_sender_ctrl,
            new_contract_receiver_ctrl,
        )

        self._remove_contract_tree_items(
            old_contract_sender_ctrl.model,
            old_contract_receiver_ctrl.model,
            contracts[OLD_CONTRACT_KEY]["productname"]
        )

        self._create_tree_view_contract(
            new_contract_sender_ctrl,
            new_contract_receiver_ctrl,
            Contract.from_dict(contracts[UPDATED_CONTRACT_KEY])
        )

    def _on_tree_view_current_item_changed(self):
        assert self._controller.is_open
        selected_agent_id = None
        tree_item = self.ui.treeProjectStructure.currentItem()
        self.ui.treeProjectStructure.indexFromItem(tree_item, 0)

        if tree_item is not None:
            # note: the given id value can be None
            selected_agent_id = tree_item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        self._controller.set_selected_agent_id(selected_agent_id)

    def _on_agent_creation_requested_accepted(
            self, dlg: DialogNewAgent, x: int, y: int
    ):
        new_agent = dlg.make_new_agent(self._controller.generate_new_agent_id())
        self._controller.add_new_agent(new_agent, x, y)
        self._graph_view.setSceneRect(self._controller.compute_scene_rect())

        dlg.save_data_in_scenario(data=self._controller.scenario, agent_id=new_agent.id)

    def _on_agent_creation_requested(self, x: int, y: int):
        assert self._controller.is_open

        dlg = DialogNewAgent(
            self._controller.schema, self._working_dir, self._controller.scenario
        )

        if dlg._ui.exec_() != 0:
            new_agent = dlg.make_new_agent(self._controller.generate_new_agent_id())

            self._controller.add_new_agent(new_agent, x, y)

            self._graph_view.setSceneRect(self._controller.compute_scene_rect())

    def _on_contract_creation_requested(self, sender_id: int, receiver_id: int):
        sender = self._controller.agent_from_id(sender_id)
        receiver = self._controller.agent_from_id(receiver_id)

        dlg = DialogNewContract(
            sender, receiver, self._controller.scenario.schema, self
        )

        if dlg.exec_() != 0:
            self._controller.add_new_contract(dlg.make_new_contract())

    def highlight_all_contracts_from_agent(self, agent_id):
        """Highlighting all contracts from a given agent in graph view"""
        for graphic_item in self._graph_view.get_contract_items():
            graphic_item: ContractGraphItem
            if graphic_item.sourceNode().agent_id.__eq__(
                    agent_id
            ) or graphic_item.destNode().agent_id.__eq__(agent_id):
                graphic_item.set_highlight_mode(True)
                graphic_item.adjust()

    def adjust_tree_widget_height(self):
        total_height = self.calculate_tree_widget_height()
        self.ui.treeAttributes.setFixedHeight(total_height)
        self.ui.treeAttributes.resizeColumnToContents(0)
        # self.ui.dockWidgetContents.setFixedHeight(total_height + 30)
        self.ui.dockWidgetContents.updateGeometry()

    def calculate_tree_widget_height(self):
        total_height = self.ui.treeAttributes.header().height()  # Start with the header height

        def get_item_height(item):
            return self.ui.treeAttributes.visualItemRect(item).height()

        def calculate_height(item):
            height = get_item_height(item)
            if item.isExpanded():
                for i in range(item.childCount()):
                    height += calculate_height(item.child(i)) + 10
            return height

        for i in range(self.ui.treeAttributes.topLevelItemCount()):
            total_height += calculate_height(self.ui.treeAttributes.topLevelItem(i)) + 10

        return total_height

    def get_widget_by_name(self, name):
        return self.findChild(QWidget, name)

    def remove_all_except_tree(self):
        # Iterate over all items in the layout
        for i in reversed(range(self.ui.verticalLayout_3.count())):
            widget = self.ui.verticalLayout_3.itemAt(i).widget()
            # Check if the widget is a QTreeWidget
            if not isinstance(widget, QTreeWidget):
                # If not, remove it from the layout and delete it
                self.ui.verticalLayout_3.takeAt(i)
                widget.deleteLater()

    class ListManager:
        def __init__(self):
            self.container = QWidget()
            self.layout = QVBoxLayout(self.container)

            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setWidget(self.container)
            self.widgets = []

        def add_item(self, widget):
            self.layout.addWidget(widget)
            self.widgets.append(widget)

        def remove_item(self):
            if self.widgets:
                widget = self.widgets.pop()
                self.layout.removeWidget(widget)
                widget.deleteLater()

        def clear_items(self):
            while self.widgets:
                self.remove_item()

        def get_scroll_area(self):
            return self.scroll_area

    def can_open_file(self, file_path, mode='r'):
        try:
            with open(file_path, mode):
                return True
        except (FileNotFoundError, IOError, PermissionError) as e:
            logging.error(f"Error: {e}")
            return False

    def eventFilter(self, source, event):
        """Catch Key Release to cancel graph selection mode"""

        if event.type() == QEvent.Type.KeyRelease:
            if event.key() == Qt.Key.Key_Shift:
                self._graph_view.clearSelection(True)

                self._graph_view.set_multi_selection_mode(False)

        # Perform any additional actions here

        # Otherwise, call the base class implementation
        return super().eventFilter(source, event)

    def _on_selected_agent_changed(self, agent_ctrl: AgentController):
        agent: AgentGraphItem

        self.clear_contract_highlights()

        if self._graph_view.is_in_multi_selection_mode():
            return

        if agent_ctrl is None:
            # clear selection
            self.ui.treeProjectStructure.clearSelection()
            self._graph_view.clearSelection()
            self.ui.treeAttributes.clear()
            self.remove_all_except_tree()

            return
        # block signals
        self.ui.treeProjectStructure.blockSignals(True)
        self._graph_view.blockSignals(True)

        # update graph view
        if self._graph_view.is_in_multi_selection_mode():
            return
        self._graph_view.clearSelection()
        agent_ctrl.scene_item.setSelected(True)

        # update tree view
        self.ui.treeProjectStructure.setCurrentItem(agent_ctrl.tree_item)

        # update agent view
        self.ui.treeAttributes.clear()
        self.remove_all_except_tree()

        item_type = QtWidgets.QTreeWidgetItem(
            self.ui.treeAttributes, ["Type", agent_ctrl.type_name]
        )

        item_type.setBackground(1, QBrush(agent_ctrl.svg_color))
        QtWidgets.QTreeWidgetItem(self.ui.treeAttributes, ["ID", agent_ctrl.display_id])

        time_series_dict = {}

        for item1, item2 in self._controller.schema.agent_type_from_name(agent_ctrl.type_name).attributes.items():

            if item2.attr_type == AttributeType.TIME_SERIES:
                time_series_dict[item1] = item2.attr_type

        for attr_name, attr_value in agent_ctrl.attributes.items():

            if attr_name in time_series_dict:
                if attr_value.has_value:
                    time_series_dict[attr_name] = attr_value.value

            PropertyTreeItem(self.ui.treeAttributes, attr_name, attr_value).setToolTip(
                0,
                self._controller.get_help_text_for_attr(
                    agent_ctrl.type_name, attr_name
                ),
            )

        total_height = 0

        list_manager = self.ListManager()

        self.ui.dockWidgetContents.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.ui.dockWidgetContents.updateGeometry()

        for idx, (key, value) in enumerate(time_series_dict.items()):

            value = str(value)
            if not value.endswith(".csv"):
                continue

            holder = QWidget()
            holder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            obj_name = f"object_plot_{key}"
            holder.setObjectName(obj_name)
            holder.setMinimumHeight(350)

            # Set horizontal layout for the holder widget
            h_layout = QVBoxLayout(holder)
            h_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
            h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
            holder.setLayout(h_layout)

            # Add the holder widget to the main vertical layout

            merged_path = os.path.join(str(self._working_dir.root_dir), value)
            merged_path = os.path.normpath(merged_path)

            # Assuming TimeSeriesPlotCanvas is a custom widget that plots the time series
            if self.can_open_file(merged_path):
                TimeSeriesPlotCanvas(holder, merged_path, key)
            else:
                QLabel(f"Path can \n not be opened: {merged_path}", holder)

            combo_holder = QWidget()
            v_item_layout = QVBoxLayout(combo_holder)
            v_item_layout.setContentsMargins(0, 0, 0, 0)
            v_item_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            v_item_layout.addWidget(holder)

            list_manager.add_item(combo_holder)

            if idx == 0:
                total_height += holder.height()

        self.ui.verticalLayout_3.addWidget(list_manager.get_scroll_area())
        list_manager.get_scroll_area()

        self.ui.verticalLayout_3.addWidget(list_manager.get_scroll_area())

        self.ui.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.ui.dockWidgetContents.setStyleSheet("background-color: #A3A3A3;")

        self.ui.verticalLayout_3.setSpacing(10)

        self.ui.verticalLayout_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        for graphic_item in self._graph_view.get_contract_items():
            graphic_item: ContractGraphItem
            if graphic_item.sourceNode().agent_id.__eq__(
                    agent_ctrl.id
            ) or graphic_item.destNode().agent_id.__eq__(agent_ctrl.id):
                graphic_item.set_highlight_mode(True)
                graphic_item.adjust()

        self.adjust_tree_widget_height()

        # unblock signals
        self.ui.treeProjectStructure.blockSignals(False)
        self._graph_view.blockSignals(False)

    def _filter_pattern_changed(self):
        pattern = self.ui.lineFilterPattern.text().lower()
        for a in self._controller.agent_list:
            hide = a.type_name.lower().find(pattern) == -1
            a.tree_item.setHidden(hide)

    def _tree_item_parent_for_agent(self, agent_ctrl) -> QtWidgets.QTreeWidgetItem:
        # return existing if it already exists
        if agent_ctrl.type_name in self._tree_items_for_agent_types:
            return self._tree_items_for_agent_types[agent_ctrl.type_name]
        item = QtWidgets.QTreeWidgetItem(
            self.ui.treeProjectStructure, [agent_ctrl.type_name]
        )

        item.setExpanded(True)
        item.setBackground(0, QBrush(agent_ctrl.svg_color))
        self._tree_items_for_agent_types[agent_ctrl.type_name] = item

        return item

    def remove_agent_tree_item(self, agent_ctrl: AgentController):
        """removes second stage agents from the tree view + top lvl items if there are no more children left"""
        parent_item = self._tree_item_parent_for_agent(agent_ctrl)
        parent_item.removeChild(agent_ctrl.tree_item)
        child_count = parent_item.childCount()

        if child_count != 0:
            return
        for idx in range(0, self.ui.treeProjectStructure.topLevelItemCount()):
            if self.ui.treeProjectStructure.topLevelItem(idx) == parent_item:
                self.ui.treeProjectStructure.takeTopLevelItem(idx)
                del self._tree_items_for_agent_types[agent_ctrl.type_name]

        self.ui.treeProjectStructure.blockSignals(True)
        self._graph_view.blockSignals(True)
        self.ui.treeProjectStructure.blockSignals(False)
        self._graph_view.blockSignals(False)

    def _create_agent_tree_item(self, agent_ctrl: AgentController):
        parent_item = self._tree_item_parent_for_agent(agent_ctrl)
        # create tree item
        item = QtWidgets.QTreeWidgetItem(parent_item, [agent_ctrl.display_id])
        item.setBackground(0, QBrush(agent_ctrl.svg_color))

        item.setData(0, QtCore.Qt.ItemDataRole.UserRole, agent_ctrl.id)
        item.setToolTip(0, agent_ctrl.tooltip_text)
        # add item

        agent_ctrl.tree_item = item
        self.ui.treeProjectStructure.addTopLevelItem(item)

    def _on_agent_added(self, agent_ctrl: AgentController):
        logging.debug("agent_added: {}".format(agent_ctrl.display_id))
        self._graph_view.add_agent(agent_ctrl)
        self._create_agent_tree_item(agent_ctrl)

    def highlight_contract(
            self, sender_id, receiver_id, single_highlight_mode=False
    ):
        """Highlights the contract in the graph view between selected agents"""

        for graphic_item in self._graph_view.get_contract_items():
            graphic_item: ContractGraphItem
            if graphic_item.sourceNode().agent_id.__eq__(
                    sender_id
            ) and graphic_item.destNode().agent_id.__eq__(receiver_id):
                graphic_item.set_highlight_mode(True)
                if single_highlight_mode:
                    graphic_item.set_single_highlight_mode(True)
                graphic_item.adjust()
                return
            elif graphic_item.sourceNode().agent_id.__eq__(
                    receiver_id
            ) and graphic_item.destNode().agent_id.__eq__(sender_id):
                graphic_item.set_highlight_mode(True)
                if single_highlight_mode:
                    graphic_item.set_single_highlight_mode(True)
                graphic_item.adjust()
                return

    def on_clicked_tree(self, pos: QModelIndex):
        """Handles the click event on the agent tree view.
        Process all types of tree items"""

        pos.parent().data(QtCore.Qt.ItemDataRole.UserRole)
        parent_agent_id = pos.parent().data(
            QtCore.Qt.ItemDataRole.UserRole
        )  # get Id from selected agent level

        if parent_agent_id is None:
            return
        results = re.findall(
            r"\d+", str(pos.data(0))
        )  # extract Id of partner agent from the 1 to 1 contract
        if len(results) == 0:  # prevent mismatching
            return
        agent_id = results[0]

        if parent_agent_id is None:
            return

        self.highlight_contract(int(parent_agent_id), int(agent_id), True)

    def _create_tree_view_contract(
            self,
            sender: AgentController,
            receiver: AgentController,
            contract: models.Contract,
    ):
        sender_tree_item = QtWidgets.QTreeWidgetItem(
            sender.tree_item,
            ["{} ({})".format(receiver.display_id, contract.product_name)],
        )

        sender_tree_item.setIcon(0, QtGui.QIcon(":/icons/16px-login.png"))
        sender_tree_item.setData(1, QtCore.Qt.ItemDataRole.UserRole, "sender")
        sender_tree_item.setData(2, QtCore.Qt.ItemDataRole.UserRole, receiver.id)
        sender_tree_item.setBackground(0, QColor(0, 255, 0, 100))  # green color sender

        receiver_tree_item = QtWidgets.QTreeWidgetItem(
            receiver.tree_item,
            [" ({}) {}".format(contract.product_name, sender.display_id)],
        )

        receiver_tree_item.setBackground(
            0, QColor(255, 0, 0, 100)
        )  # red color receiver

        receiver_tree_item.setData(1, QtCore.Qt.ItemDataRole.UserRole, "receiver")
        receiver_tree_item.setData(2, QtCore.Qt.ItemDataRole.UserRole, sender.id)
        receiver_tree_item.setIcon(0, QtGui.QIcon(":/icons/16px-logout.png"))

    def _on_contract_added(
            self,
            sender: AgentController,
            receiver: AgentController,
            contract: models.Contract,
    ):
        """Handles the event when a new contract is added to the scenario by creating UI elements"""
        # update scene graph
        self._graph_view.add_contract(sender, receiver)
        # update tree view
        self._create_tree_view_contract(sender, receiver, contract)

    def _confirm_current_project_can_be_closed(self) -> bool:
        if self._controller.has_unsaved_changes:
            choice = QtWidgets.QMessageBox.warning(
                self,
                self.tr("Modifications will be lost"),
                self.tr(
                    "Modifications done to the current scenario have not been saved!\n\nWhat do you want to do?"
                ),
                QtWidgets.QMessageBox.StandardButtons(
                    QtWidgets.QMessageBox.Save
                    | QtWidgets.QMessageBox.Discard
                    | QtWidgets.QMessageBox.Cancel
                ),
                QtWidgets.QMessageBox.Cancel,
            )
            if choice == QtWidgets.QMessageBox.Save:
                return self.save_project()
            elif choice == QtWidgets.QMessageBox.Discard:
                return True
            else:
                return False
        return True

    def _on_project_closed(self):
        self._graph_view.clear()
        # reset zoom
        self.sliderZoomFactor.setValue(50)
        # reset attributes
        self._tree_items_for_agent_types = {}
        # reset scenario
        self._controller.reset()
        # reset ui
        self.ui.treeProjectStructure.clear()
        self.ui.treeAttributes.clear()
        self.remove_all_except_tree()
        self.ui.lineFilterPattern.clear()
        self.ui.labelProjectName.clear()

    def display_error_msg(self, msg: str) -> None:
        logging.error(msg)
        if not msg.endswith("."):
            msg += "."
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), msg)

    def new_project(self):
        if not self._confirm_current_project_can_be_closed():
            return
        self._on_project_closed()

        dlg = DialogScenarioProperties(
            models.GeneralProperties.make_default(), self._working_dir, self
        )
        dlg.setWindowTitle(self.tr("New scenario"))
        # ask user to choose which schema to use for that new scenario
        dlg.enable_schema_selection()

        if dlg.exec_() != 0:
            schema_path = dlg.get_selected_schema_full_path()

            schema = models.Schema.load_yaml_file(schema_path)
            scenario = models.Scenario(schema, dlg.make_properties())
            self._controller.reset(scenario)

    def save_project(self) -> bool:
        if not self._controller.is_open:
            return False
        return self._do_save_project_as(self._controller.project_properties.file_path)

    def save_project_as(self) -> bool:
        if not self._controller.is_open:
            return False
        return self._do_save_project_as("")

    def _do_save_project_as(self, file_path: str) -> bool:
        assert self._controller.is_open

        if file_path == "":
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                self.tr("Save scenario file"),
                self._working_dir.scenarios_dir,
                "Scenario file (*.yaml *.yml)",
            )
            if file_path == "":
                return False

        schema_is_valid = self._controller.revalidate_scenario()

        if not schema_is_valid:
            gen_quick_warning_modal(
                self.parentWidget(),
                "Schema Validation",
                "The scenario is valid according to the schema",
            )
            return False

        self._controller.save_to_file(file_path)
        self._graph_view.setSceneRect(self._controller.compute_scene_rect())
        self._controller.set_unsaved_changes(False)

        return True

    def close_project(self) -> None:
        if self._confirm_current_project_can_be_closed():
            self._on_project_closed()

    def show_open_scenario_file_dlg(self):
        if not self._confirm_current_project_can_be_closed():
            return
        logging.debug("show_open_scenario_file_dlg")

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open scenario file"),
            self._working_dir.scenarios_dir,
            self.tr("Scenario (*.yaml *.yml)"),
        )
        if file_path != "":
            self.load_scenario_file(file_path)

    def _on_scenario_status_changed(self):
        logging.debug(
            "scenario status changed: agents={}, contracts={}".format(
                self._controller.agent_count, self._controller.contract_count
            )
        )

        is_open = self._controller.is_open
        self.ui.treeProjectStructure.setEnabled(is_open)
        self.ui.treeAttributes.setEnabled(is_open)
        self.ui.lineFilterPattern.setEnabled(is_open)
        self.fame_graphicsView.setEnabled(is_open)
        self.sliderZoomFactor.setEnabled(is_open)

        props = self._controller.project_properties
        if is_open:
            if props.file_path != "":
                self.ui.labelProjectName.setText(props.file_path)
            else:
                self.ui.labelProjectName.setText(self.tr("Unsaved scenario"))
        else:
            self.ui.labelProjectName.setText("")

        self.ui.actionSaveProject.setEnabled(props.has_unsaved_changes)

        self.ui.actionGeneralProperties.setEnabled(is_open)
        self.ui.actionConfigMenu.setEnabled(is_open)
        self.ui.actionMakeRunConfig.setEnabled(is_open)

        # update status bar
        if self._controller.agent_count > 0:
            if props.is_validation_successful:
                self._status_label_icon.setPixmap(QPixmap(":/icons/success-16px.png"))
                self._status_label_icon.setToolTip(
                    self.tr("Schema validation succeeded")
                )
            else:
                self._status_label_icon.setPixmap(QPixmap(":/icons/warning-16px.png"))
                all_errors = "\n".join(props.validation_errors)
                self._status_label_icon.setToolTip(
                    self.tr("Schema validation failed:\n{}".format(all_errors))
                )
        else:
            self._status_label_icon.clear()

    def load_scenario_file(self, file_path):
        self._on_project_closed()
        file_path = os.path.abspath(file_path)

        try:
            logging.info("opening scenario file {}".format(file_path))
            # TODO Future: prevent freezing UI at this place with Multithreading/Async IO -> Freezing place number 1

            scenario_model = models.ScenarioLoader.load_yaml_file(
                file_path, self._path_resolver,
                self._working_dir.root_dir)

            self._controller.init_scenario_model(scenario_model, file_path)
        except Exception as e:
            self._on_project_closed()
            self.display_error_msg("Failed to open scenario file: {}".format(e))
            return

        props = self._controller.project_properties
        if not props.is_validation_successful:
            QtWidgets.QMessageBox.warning(
                self,
                self.tr("Validation failure"),
                self.tr("The loaded scenario does not fulfill the schema:\n\n")
                + "\n".join(props.validation_errors),
            )
        self.ui.actionCloseProject.setVisible(True)

    def _on_edit_scenario_properties(self):
        dlg = DialogScenarioProperties(
            self._controller.scenario.general_properties, self._working_dir, self
        )

        dlg.setWindowTitle(self.tr("Scenario properties"))

        if dlg.exec_() != 0:
            edited_properties = dlg.make_properties().to_dict()
            original_properties = self._controller.scenario.general_properties.to_dict()

            if hash_dict(edited_properties) != hash_dict(original_properties):
                self._controller.save_project_properties_manipulation(
                    original_properties, edited_properties
                )

                self._controller.update_scenario_properties(dlg.make_properties())

    def _on_edit_fame_gui_settings(self):
        """Open up FAME GUI PRESETS and Preferences Settings Dialog"""
        dialog = EditFameDbValuesDialog(self._controller.scenario,

                                        self.handle_agent_color_change)
        dialog.exec_()

    def make_run_config(self):

        if self._controller.has_unsaved_changes:
            logging.info("Project unsaved, saving project to prepare for protobuf compilation")
            self._do_save_project_as(self._controller.project_properties.file_path)

        assert self._controller.can_export_protobuf
        scenario_name = os.path.basename(
            self._controller.project_properties.file_path
        ).replace(".yaml", "")
        output_path = "{}/{}.pb".format(self._working_dir.protobuf_dir, scenario_name)
        output_path = self._working_dir.make_relative_path(output_path)

        dlg = DialogScenarioProperties(
            self._controller.scenario.general_properties, self._working_dir, self
        )

        dlg.setWindowTitle(self.tr("Make run config"))
        dlg.enable_outputfile_selection(output_path)
        if dlg.exec() != 0:
            self._controller.update_scenario_properties(dlg.make_properties())
            self.save_project()
            output_path = self._working_dir.make_full_path(dlg.get_output_file_path())

            # display progress dialog
            progress_dlg = QtWidgets.QProgressDialog(self)
            progress_dlg.setLabelText(self.tr("Generating protobuf file..."))
            progress_dlg.setRange(0, 0)
            progress_dlg.setCancelButton(None)
            progress_dlg.show()
            QApplication.processEvents()

            try:
                models.write_protobuf_output(
                    self._controller.scenario, output_path, self._path_resolver
                )
                progress_dlg.close()
                QtWidgets.QMessageBox.information(
                    self,
                    self.tr("Success"),
                    self.tr(
                        "The following file was successfully generated:\n\n{}"
                    ).format(output_path),
                )

                self._controller.set_unsaved_changes(False)
            except Exception as e:
                progress_dlg.close()
                logging.error("failed to generate protobuf output: {}".format(e))
                QtWidgets.QMessageBox.critical(
                    self,
                    self.tr("Error"),
                    self.tr("Failed to generate the protobuf output.\n\n{}").format(e),
                )
            finally:
                progress_dlg.close()

    # prevent data loss when closing the main window
    def closeEvent(self, event):
        if not self._confirm_current_project_can_be_closed():
            event.ignore()
        else:
            event.accept()
