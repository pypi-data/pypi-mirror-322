
import logging
import re
import typing

import fameio.input.schema as schema
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSizePolicy
from fameio.input.scenario import Attribute
from fameio.input.schema import AttributeSpecs

from famegui.appworkingdir import AppWorkingDir
from famegui.config.static_ui_descriptions import NO_SUPPORTED_EDIT_WIDGET_TEXT
from famegui.config.style_config import get_color_for_type, get_border_for_type, ERROR_TEXT_STYLE_LABEL, \
    ERROR_TEXT_STYLE_LINE_EDIT
from famegui.data_manager.string_set_manager import get_pre_defined_string_set_values_from_scenario
from famegui.database.db_loader.db_manager import get_string_set_values_for_group
from famegui.fame_tools.dict_tools import remove_none_values_and_empty_elements
from famegui.fame_tools.string_utils import get_last_substring
from famegui.famegui_widgets.complex_attribute_schema_widget import SchemaWidget
from famegui.ui.block_item_wrapper import BlockItemWrapper
from famegui.ui.block_type_wrapper import BlockTypeWrapper
from famegui.ui.fame_input_panels import FileChooserWidgetPanel
from famegui.ui.fame_ui_elements import QFameBoldLabel, DescriptionLabel
from famegui.ui.list_block import CustomListWidget
from famegui.ui.ui_input import set_placeholder_text
from famegui.ui.ui_input_panel_wrapper import InputPanelWrapper, MiniAttributeSpecs
from famegui_runtime_helper.attribute_dict_formatting_helper import StringAttributeType


class RootAttributeInputPanelWrapper(QtWidgets.QWidget):
    """Wrapper for the root level attribute input panels. It is used to toggle the visibility
    of the input panels and mange all nested input panels.
    """

    def __init__(self, row, panel, parent=None):
        super(RootAttributeInputPanelWrapper, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout = QVBoxLayout(self)
        self.layout = layout
        self.layout.setSpacing(10)
        self.content_frame: QtWidgets.QWidget = QtWidgets.QWidget(self)

        self.row: AttributeTreeItem = row
        button = QPushButton("Collapse/Expand")
        layout.addWidget(button)
        button.clicked.connect(self.toggle_content)
        layout.addWidget(self.content_frame)

        content_layout = QVBoxLayout(self.content_frame)

        self.panel = panel

        content_layout.addWidget(self.panel)

        self.initial_width = self.width()

        self.content_frame.setVisible(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def toggle_size_adjustment(self):
        """Toggle the size adjustment of the parent widget."""
        self.adjustSize()

        self.updateGeometry()
        self.row.setSizeHint(0, QSize(-1, 60))
        self.row.setSizeHint(1, QSize(-1, 60))
        self.parent().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.parent().updateGeometry()
        self.parent().adjustSize()

    def toggle_content(self):
        """Toggle the visibility of the input panel by triggering layout updates."""

        if self.content_frame.isVisible():
            self.content_frame.hide()

        else:
            self.content_frame.show()

        self.parent().updateGeometry()
        self.parent().adjustSize()
        self.parent().update()

    def height(self):
        """Get the pre-calculated height of the input panel."""
        return self.content_frame.sizeHint().height() + 50


class AttributeTreeItem(QtWidgets.QTreeWidgetItem):
    """Root Holder class for all attribute tree items.
    It is used to create a tree of attributes and their input panels to access all attributes .
    """

    def simple_attr_build(self, attr_spec: schema.AttributeSpecs, result_dict):

        if attr_spec.attr_type == schema.AttributeType.BLOCK:
            result_dict_sub = {}

    def set_schema_widget_height(self, height: int):

        if self.is_single_item:
            self.ui_parent.itemWidget(self, 1).setFixedHeight(int(height))
            self.ui_parent.itemWidget(self, 1).update()
            self.ui_parent.itemWidget(self, 1).updateGeometry()
            height = height - 90
            self._schema_widget.setFixedHeight(int(height))



    def __init__(
            self,
            parent: QtWidgets.QTreeWidget,
            attr_name: str,
            attr_spec: schema.AttributeSpecs,
            scenario,  # Scenario
            working_dir: AppWorkingDir,
            onInputChanged: Signal = None,
            validation_signal: Signal = None,
            validation_error_signal: Signal = None,
            default_value=None,
            flat_default_values: dict = None,
            is_single_item: bool = False
    ):
        self.state_value_dict = {}
        self._attr_name = attr_name
        self._attr_spec: AttributeSpecs = attr_spec
        self.validation_signal: Signal = validation_signal
        self.validation_error_signal: Signal = validation_error_signal
        self._working_dir = working_dir
        self._default_value = default_value
        self._attr_value = None
        self._display_error = lambda has_error: None
        self.initial_height = 0
        self.schema = scenario.schema
        self.scenario = scenario
        self.holder_widget = None
        self.default_agent_flat_value_dict = flat_default_values

        self.is_single_item = is_single_item

        self.onInputChanged = onInputChanged

        QtWidgets.QTreeWidgetItem.__init__(self, parent, [attr_name])

        font = self.font(0)
        if self._attr_spec.is_mandatory:
            font.setBold(True)

            tooltip = self.tr("{} (mandatory)").format(self._attr_name)
        else:
            font.setItalic(True)
            tooltip = self.tr("{} (optional)").format(self._attr_name)

        self.setFont(0, font)
        self.setToolTip(0, tooltip)
        self.ui_parent = parent
        self.panel = QLabel("Hello")  # ForeCastAPi -> return None

        self.panel = QLabel()

        self.holder_widget = QtWidgets.QWidget()

        layout = QVBoxLayout()
        placeholder = QtWidgets.QWidget()
        placeholder.setStyleSheet("background-color: #0A0A0A;")
        placeholder.setContentsMargins(0, 0, 0, 0)  # Adds padding inside the placeholder layout
        inner_layout = QVBoxLayout()

        placeholder.setLayout(inner_layout)

        layout.addWidget(placeholder, stretch=1)

        self.holder_widget.setLayout(layout)

        color_str = get_color_for_type(self._attr_spec)

        self.holder_widget.setStyleSheet(
            f"RootAttributeInputPanelWrapper {{  background:{color_str}; border-radius: 5px;"
            "margin-top:10px; ; margin-left: 5px; margin-right: 5px; }}"
        )

        # Create a boundary container
        boundary_container = QtWidgets.QWidget()
        boundary_layout = QVBoxLayout(boundary_container)
        boundary_layout.setContentsMargins(0, 0, 0, 0)
        boundary_layout.setSpacing(0)

        # Set maximum height to constrain the widget
        # boundary_container.setMaximumHeight(400)  # Adjust the height as needed

        # Add the SchemaWidget to the boundary container
        self._schema_widget = SchemaWidget(self.default_agent_flat_value_dict,
                                           is_single_item=is_single_item,
                                           attr_row_item=self)

        self._schema_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        boundary_layout.addWidget(self._schema_widget)
        boundary_layout.addStretch(1)
        parent.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        parent.header().setStretchLastSection(True)

        example_widget = QtWidgets.QWidget()
        example_layout_v = QVBoxLayout()
        example_layout_v.setAlignment(Qt.AlignmentFlag.AlignTop)
        example_layout_v.setContentsMargins(0, 0, 0, 0)  # Remove margins
        example_layout_v.setSpacing(0)  # Remove spacing
        # Add stretch to fill space dynamically

        example_widget.setLayout(example_layout_v)

        example_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        boundary_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set the boundary container as the item widget
        example_layout_v.addWidget(boundary_container, stretch=1)

        parent.setItemWidget(self, 1, example_widget)

        # Set the size hint for the tree widget item to match the boundary container
        # self.setSizeHint(1, boundary_container.sizeHint())

    def get_attr_spec(self):
        """Get the root AttributeSpecs of the row."""
        return self._attr_spec

    @property
    def attr_name(self) -> str:
        """Get the attribute short name of the root attribute ."""
        return self._attr_name

    def remove_none_values(self, d):
        """Helper function to remove None values from a dictionary."""
        if not isinstance(d, dict):
            return d
        return {k: self.remove_none_values(v) for k, v in d.items() if v is not None}



    @staticmethod
    def get_substring_after_last_dot(s):
        if "." in s:
            return s.rsplit(".", 1)[-1]
        return s

    def build_it(self, attr: AttributeSpecs, li_idx=-1):

        res_dict = {}



        if attr.is_list and attr.has_nested_attributes:

            max_inputs = 0
            data_count = 0

            list_data = []

            while data_count <= max_inputs:
                sub_list_item = {}

                for sub_key, sub_item in attr.nested_attributes.items():

                    if sub_item.attr_type == schema.AttributeType.BLOCK:
                        sub_list_item[sub_key] = self.build_it(sub_item, li_idx=data_count)
                        continue

                    sub_full_name = sub_item.full_name

                    value_list = self.state_value_dict[
                        sub_full_name] if sub_full_name in self.state_value_dict else None  # fallback in case optional list nodes where removed

                    if value_list is None:
                        continue

                    if isinstance(value_list, InputPanelWrapper):
                        sub_list_item[sub_key] = value_list.get_input_value()
                        continue

                    if not isinstance(value_list, list):
                        sub_list_item[sub_key] = value_list[data_count].get_input_value()
                        continue

                    amount_of_inputs = len(value_list) if value_list is not None else 0

                    if amount_of_inputs == 0:
                        break
                    if max_inputs == 0:
                        max_inputs = (amount_of_inputs - 1)

                    sub_list_item[sub_key] = value_list[data_count].get_input_value()

                data_count += 1
                list_data.append(sub_list_item)

            attr_name = self.get_substring_after_last_dot(attr.full_name)

            res_dict[attr_name] = list_data

        elif attr.has_nested_attributes:
            for sub_key, sub_item in attr.nested_attributes.items():

                if sub_item.attr_type == schema.AttributeType.BLOCK:
                    res_dict[sub_key] = self.build_it(sub_item)
                    continue

                value = self.state_value_dict[
                    sub_item.full_name] if sub_item.full_name in self.state_value_dict else None

                if value is None:
                    res_dict[sub_key] = None
                    continue

                if sub_item.is_list:
                    if isinstance(value, list):
                        res_dict[sub_key] = [
                            list_iter_item.get_input_value() for list_iter_item in value]
                        continue
                    res_dict[sub_key] = [value.get_input_value()]  # single value case

                    continue

                if isinstance(value, list):
                    if len(value) == 0:
                        res_dict[sub_key] = None
                        continue

                res_dict[sub_key] = value.get_input_value() if not isinstance(value, list) else value[
                    li_idx].get_input_value()

        else:
            res_dict[self.attr_name] = self.state_value_dict[self._attr_spec.full_name].get_input_value()

        return res_dict

    @property
    def attr_value(self) -> typing.Any:
        """Get clean attribute value from a complete row"""

        res_dict = self.build_it(self._attr_spec)

        cleaned_data = remove_none_values_and_empty_elements(res_dict)

        if self._attr_spec.attr_type != schema.AttributeType.BLOCK:
            return cleaned_data[next(iter(cleaned_data.keys()))] if len(cleaned_data.keys()) != 0 else cleaned_data

        cleaned_data = cleaned_data[self.attr_name] if self.attr_name in cleaned_data else cleaned_data

        return cleaned_data

    @property
    def validation_error(self) -> typing.Optional[str]:
        if self._attr_spec.is_mandatory and self._attr_value is None:
            return "mandatory attribute '{}' is missing".format(self.attr_name)
        return None

    _supported_list_types = [
        schema.AttributeType.INTEGER,
        schema.AttributeType.LONG,
        schema.AttributeType.DOUBLE,
        schema.AttributeType.STRING,
        schema.AttributeType.STRING_SET,
    ]

    @property
    def _attr_enum_values(self) -> typing.List[str]:
        """Returns the enum values of the attached AttributeSpecs"""
        assert self._attr_spec.attr_type == schema.AttributeType.ENUM
        assert not self._attr_spec.is_list
        assert not self._attr_spec.has_nested_attributes
        return self._attr_spec.values

    def build_parent_container(self, attr_spec_inner, attr_name: str, holder_widget) -> QtWidgets.QWidget:
        """Build a parent container for a block type attribute with an n depth of nested attributes"""

        value = attr_spec_inner.help_text or ""
        desc = DescriptionLabel(text=value)

        label = QFameBoldLabel(
            text=f"{attr_name}:x: {attr_spec_inner.attr_type.name} "
        )

        label.setWordWrap(True)

        parent_layout = QVBoxLayout()

        parent_container = BlockTypeWrapper(
            block_type_layout=parent_layout,
            spec=attr_spec_inner,
            attr_name=attr_name,
        )

        layout_header = QVBoxLayout()
        header_widget = QtWidgets.QWidget()

        header_widget.setLayout(layout_header)

        layout_header.insertWidget(0, label)
        layout_header.insertWidget(1, desc)
        parent_layout.insertWidget(0, header_widget)

        # Wrap holder_widget with a parent container and chevron icon

        # Set the stylesheet for the specific widget using its object name

        chevron_button = QPushButton(
            "Expand/Collapse"
        )  # Using a triangle as a placeholder for the chevron icon

        chevron_button.setCheckable(True)

        # Set the initial checked state to match the initial visibility of holder_widget
        chevron_button.setChecked(True)

        chevron_button.toggled.connect(holder_widget.setVisible)
        parent_layout.addWidget(chevron_button)
        parent_layout.addWidget(holder_widget)

        return parent_container

    def build_child_sub_block_list(self, attr_spec_inner, attr_name, holder: QVBoxLayout, list_data=None):
        """Build a child list block panel for a block"""

        preset_value_list = self.get_default_value(
            attr_spec_inner, attr_spec_inner.full_name, list_data
        )

        block_list = self.build_sub_block_list(
            attr_spec_inner, preset_value_list
        )

        dynamic_list = CustomListWidget(
            block_list, attr_spec_inner, self.schema,
            attr_name=attr_name
        )

        dynamic_list.row_creation_requested.connect(self._add_list_row)

        holder.addWidget(dynamic_list)

        # dynamic_list.setLayout(holder)

    def build_primitive_block_child(self, attr_spec_inner: AttributeSpecs,
                                    attr_name: str, holder: QVBoxLayout,
                                    list_data=None):
        """Build a primitive child input panel for a block"""
        default_row = QFameBoldLabel(
            text=f"{attr_name}: {attr_spec_inner.attr_type.name}"
        )

        default_row.setWordWrap(True)
        value = attr_spec_inner.help_text or ""

        desc = DescriptionLabel(text=value)

        parent_widget = BlockItemWrapper(spec=attr_spec_inner, attr_name=attr_name)

        parent_widget.add_widget(default_row)
        parent_widget.add_widget(desc)
        prim_widget = self.get_primitive_input_panel(attr_spec_inner, list_data)

        uniq_widget = f"myUniqueWidget-{id(parent_widget)}"

        parent_widget.setObjectName(uniq_widget)

        color_str = get_color_for_type(attr_spec_inner)

        border_style = get_border_for_type(attr_spec_inner)

        parent_widget.setStyleSheet(
            f"#{uniq_widget} {{"
            f"    background-color: {color_str};"
            f"    {border_style}"
            "    border-radius: 5px;"
            "}"
        )

        parent_widget.add_input_widget(prim_widget)

        holder.addWidget(parent_widget)

    def build_sub_block_list(self, attr_data: AttributeSpecs, list_data=None):
        """Build a list of sub blocks for a block type attribute with an n depth of nested attributes"""
        holder = QVBoxLayout()

        if attr_data.has_nested_attributes:
            for item, attr_spec_inner in attr_data.nested_attributes.items():
                attr_spec_inner: AttributeSpecs

                if attr_spec_inner.attr_type == schema.AttributeType.BLOCK:
                    holder_widget = self.build_sub_block_list(attr_spec_inner, list_data)

                    parent_container = self.build_parent_container(
                        attr_spec_inner, item, holder_widget
                    )

                    input_wrapper = InputPanelWrapper(
                        inner_widget=parent_container,
                        signal_to_connect=self.validation_signal,
                        validation_error_signal=self.validation_error_signal,
                        attr_name=item,
                        attribute=attr_spec_inner,
                    )

                    holder.addWidget(input_wrapper)
                    continue

                if attr_spec_inner.is_list:
                    self.build_child_sub_block_list(attr_spec_inner, item, holder, list_data)

                    continue

                self.build_primitive_block_child(attr_spec_inner, item, holder, list_data)

                ## here

        default_data_dict = self.get_default_value(
            attr_data, self._attr_spec.full_name, list_data
        )

        holder_wrapper = BlockTypeWrapper(
            block_type_layout=holder,
            spec=attr_data,
            attr_name=self.attr_name,
            dict_data=default_data_dict,
        )

        return holder_wrapper

    @staticmethod
    def get_substring_from_last_dot(s):
        return s[s.rfind('.') + 1:] if '.' in s else s

    def get_list_capable_int_or_long_input_panel(self, spec: MiniAttributeSpecs,
                                                 nested_list, full_name=None,
                                                 preset_value=None, list_idx=None):

        full_name = full_name if full_name is not None else spec.full_name

        line_edit = self._create_line_edit("0", None)
        line_edit.setText(str(preset_value))
        line_edit.setValidator(QtGui.QIntValidator())

        input_wrapper = InputPanelWrapper(
            inner_widget=line_edit,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
            list_idx=list_idx
        )

        if full_name in self.state_value_dict:
            item = self.state_value_dict[full_name]

            if isinstance(item, list):
                item.append(input_wrapper)
                return line_edit
            new_list = [item]
            new_list.append(input_wrapper)
            self.state_value_dict[full_name] = new_list

            return line_edit

        self.state_value_dict[full_name] = input_wrapper

        return input_wrapper



    def get_list_capable_time_series_input_panel(self, spec: MiniAttributeSpecs, nested_list,
                                                 full_name, preset_value=None, list_idx=None):
        # preset_value = self.get_default_value(spec, spec.full_name, nested_list)

        file_chooser = FileChooserWidgetPanel(
            self._working_dir,
            get_last_substring(full_name),
            preset_value,
            self.ui_parent,
        )

        self._display_error = file_chooser.display_error

        input_wrapper = InputPanelWrapper(
            inner_widget=file_chooser,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
            list_idx=list_idx
        )

        if full_name in self.state_value_dict:
            item = self.state_value_dict[full_name]

            if isinstance(item, list):
                item.append(input_wrapper)
                return file_chooser
            new_list = [item]
            new_list.append(input_wrapper)
            self.state_value_dict[full_name] = new_list

            return file_chooser

        self.state_value_dict[full_name] = input_wrapper

        return file_chooser

    def get_list_capable_enum_input_panel(self, spec: MiniAttributeSpecs,
                                          nested_list, full_name=None,
                                          options=None, preset_value=None, list_idx=None):
        combo_box = QtWidgets.QComboBox()

        # self.schema.get
        full_name, attr_type, is_mandatory, enum_values = spec.get_values()

        combo_box.addItems(enum_values)
        if len(enum_values) == 1:
            combo_box.setCurrentIndex(0)
            self._attr_value = enum_values[0]
        else:
            combo_box.setCurrentIndex(-1)

        preset_value = preset_value if preset_value is not None else None
        set_placeholder_text(combo_box, preset_value, enum_values)

        full_name = full_name if full_name is not None else spec.full_name

        input_wrapper = InputPanelWrapper(
            inner_widget=combo_box,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
            list_idx=list_idx
        )

        if full_name in self.state_value_dict:
            item = self.state_value_dict[full_name]

            if isinstance(item, list):
                item.append(input_wrapper)
                return combo_box
            new_list = [item]
            new_list.append(input_wrapper)
            self.state_value_dict[full_name] = new_list

            return combo_box

        self.state_value_dict[full_name] = input_wrapper

        return combo_box

    def remove_state_registers(self, remove_state_registers,
                               to_remove_idx):

        for full_name in remove_state_registers:
            item = self.state_value_dict[full_name]

            if isinstance(item, list):
                selected = item[to_remove_idx]
                new_list = [sub_item for sub_item in item if sub_item is not selected]
                self.state_value_dict[full_name] = new_list
                continue

            if to_remove_idx != 0:
                raise ValueError("Not possible case")

            del self.state_value_dict[full_name]

    def get_list_capable_double_input_panel(self, spec: MiniAttributeSpecs,
                                            nested_list, preset_value=None, list_idx=None):
        # preset_value = self.get_default_value(spec, spec.full_name, nested_list)
        full_name, attr_type, is_mandatory, _ = spec.get_values()

        line_edit = self._create_line_edit(preset_value, None)

        line_edit.setText(str(preset_value))
        validator = QtGui.QDoubleValidator()
        # accept '.' as decimal separator
        validator.setLocale(QtCore.QLocale.Language.English)
        line_edit.setValidator(validator)

        input_wrapper = InputPanelWrapper(
            inner_widget=line_edit,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
            list_idx=list_idx

        )

        if full_name in self.state_value_dict:
            item = self.state_value_dict[full_name]

            if isinstance(item, list):
                item.append(input_wrapper)
                return line_edit
            new_list = [item]
            new_list.append(input_wrapper)
            self.state_value_dict[full_name] = new_list

            return line_edit

        self.state_value_dict[full_name] = input_wrapper

        return line_edit

    def get_primitive_input_panel(self, spec: typing.Union[AttributeSpecs, None], nested_list,
                                  mini_spec: MiniAttributeSpecs = None, preset_value=None, list_idx=None):

        """Get a primitive input panel for a given attribute spec"""
        full_name, attr_type, is_mandatory, options = mini_spec.get_values()

        preset_value = preset_value if preset_value is not None else ""

        current_attr_type = attr_type
        full_name = full_name

        if current_attr_type == StringAttributeType.ENUM.value:

            # exi 1
            return self.get_list_capable_enum_input_panel(mini_spec, nested_list,
                                                          full_name=full_name, options=options,
                                                          preset_value=preset_value, list_idx=list_idx)

        elif current_attr_type == StringAttributeType.TIME_SERIES.value:

            # exi 2

            resultTS = self.get_list_capable_time_series_input_panel(mini_spec, nested_list,
                                                                     full_name, preset_value, list_idx)

            return resultTS

        elif (current_attr_type == StringAttributeType.INTEGER.value
              or current_attr_type == StringAttributeType.LONG.value):

            # exi 3

            return self.get_list_capable_int_or_long_input_panel(mini_spec, nested_list,
                                                                 full_name, preset_value, list_idx)

        elif current_attr_type == StringAttributeType.DOUBLE.value:

            # exi 4

            return self.get_list_capable_double_input_panel(mini_spec, nested_list, preset_value, list_idx)

        elif current_attr_type == StringAttributeType.STRING.value:

            # exi 5

            return self._get_string_input(mini_spec, nested_list, preset_value, list_idx)

        elif current_attr_type == StringAttributeType.STRING_SET.value:

            # exi 5

            return self._get_string_set_input(mini_spec, nested_list, preset_value, list_idx, self.scenario)

        elif current_attr_type == schema.AttributeType.BLOCK:

            return self.build_scroll_block_edit_widget(spec, nested_list)

    def _get_string_input(self, spec: MiniAttributeSpecs,
                          nested_list, preset_value=None, list_idx=None):
        full_name, attr_type, is_mandatory, _ = spec.get_values()

        line_edit = self._create_line_edit(preset_value, None)

        line_edit.setText(str(preset_value))
        # validator = QtGui.Va()
        # accept '.' as decimal separator
        # validator.setLocale(QtCore.QLocale.Language.English)
        # line_edit.setValidator(validator)

        input_wrapper = InputPanelWrapper(
            inner_widget=line_edit,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
            list_idx=list_idx

        )

        if full_name in self.state_value_dict:
            item = self.state_value_dict[full_name]

            if isinstance(item, list):
                item.append(input_wrapper)
                return line_edit
            new_list = [item]
            new_list.append(input_wrapper)
            self.state_value_dict[full_name] = new_list

            return line_edit

        self.state_value_dict[full_name] = input_wrapper

        return line_edit

    def _get_string_set_input(self, spec: MiniAttributeSpecs,
                              nested_list, preset_value=None, list_idx=None,
                              scenario: object = None):
        full_name, attr_type, is_mandatory, _ = spec.get_values()

        combo_box = QtWidgets.QComboBox()

        sub_string = get_last_substring(full_name)

        string_set_data_dict = get_pre_defined_string_set_values_from_scenario(scenario)

        string_set_data_dict = string_set_data_dict[sub_string]

        partial_result = get_string_set_values_for_group(sub_string)

        string_set_data_dict.extend(partial_result)

        string_set_data_dict = list(set(string_set_data_dict))

        combo_box.addItems(string_set_data_dict)

        input_wrapper = InputPanelWrapper(
            inner_widget=combo_box,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
            list_idx=list_idx

        )

        if full_name in self.state_value_dict:
            item = self.state_value_dict[full_name]

            if isinstance(item, list):
                item.append(input_wrapper)
                return combo_box
            new_list = [item]
            new_list.append(input_wrapper)
            self.state_value_dict[full_name] = new_list

            return combo_box

        self.state_value_dict[full_name] = input_wrapper

        return combo_box

    def _add_list_row(self, spec: AttributeSpecs, widget: QtWidgets.QWidget):
        """Add a new row to a list after the user clicked the add button"""
        widget: CustomListWidget
        block_list = self.build_sub_block_list(spec)

        input_wrapper = InputPanelWrapper(
            inner_widget=block_list,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,

        )

        widget.set_widget(input_wrapper)

        self.ui_parent.updateGeometry()

    def _create_edit_widget(self) -> QtWidgets.QWidget:
        """Create a input panel edit widget for the attribute"""
        spec = self._attr_spec

        if spec.is_list:
            return self.build_list_edit_widget(spec)

        if spec.attr_type == schema.AttributeType.ENUM:

            return self.build_enum_chooser_input_panel(spec)

        elif spec.attr_type == schema.AttributeType.TIME_SERIES:

            return self.build_time_series_edit_widget(spec)

        # INT INPUT PANEL

        elif (spec.attr_type == schema.AttributeType.INTEGER
              or spec.attr_type == schema.AttributeType.LONG):

            return self.build_int_or_long_edit_widget(spec)

        # DOUBLE  INPUT PANEL
        elif spec.attr_type == schema.AttributeType.DOUBLE:

            return self.build_double_edit_widget(spec)

        elif spec.attr_type == schema.AttributeType.BLOCK:

            return self.build_block_edit_widget(spec)

        elif spec.attr_type == schema.AttributeType.STRING:
            return self.build_string_edit_widget(spec)

    def build_block_edit_widget(self, spec: AttributeSpecs):
        block_list = self.build_sub_block_list(spec)

        input_wrapper = InputPanelWrapper(
            inner_widget=block_list,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
        )
        self.state_value_dict = {spec.full_name: input_wrapper}

        return input_wrapper

    def build_double_edit_widget(self, spec: AttributeSpecs):
        preset_value = self.get_default_value(spec, spec.full_name)

        line_edit = self._create_line_edit(preset_value, None)

        line_edit.setText(str(preset_value))
        validator = QtGui.QDoubleValidator()
        # accept '.' as decimal separator
        validator.setLocale(QtCore.QLocale.English)
        line_edit.setValidator(validator)

        input_wrapper = InputPanelWrapper(
            inner_widget=line_edit,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,

        )

        full_name, attr_type, is_mandatory, _ = spec.get_values()

        if full_name in self.state_value_dict:
            item = self.state_value_dict[full_name]

            if isinstance(item, list):
                item.append(input_wrapper)
                return line_edit
            new_list = [item]
            new_list.append(input_wrapper)
            self.state_value_dict[full_name] = new_list

            return line_edit

        self.state_value_dict[full_name] = input_wrapper

    def build_enum_chooser_input_panel(self, spec: AttributeSpecs):
        combo_box = QtWidgets.QComboBox()
        enum_values = self._attr_enum_values
        combo_box.addItems(enum_values)
        if len(enum_values) == 1:
            combo_box.setCurrentIndex(0)
            self._attr_value = enum_values[0]
        else:
            combo_box.setCurrentIndex(-1)

        preset_value = self.get_default_value(
            spec,
            spec.full_name,
        )

        set_placeholder_text(combo_box, preset_value, enum_values)

        input_wrapper = InputPanelWrapper(
            inner_widget=combo_box,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
        )

        self.state_value_dict["int_input"] = input_wrapper

        return input_wrapper

    def build_scroll_block_edit_widget(self, spec: AttributeSpecs, nested_list):
        # scroll_area = QtWidgets.QScrollArea()
        scroll_area = QtWidgets.QWidget()
        # scroll_area.setWidgetResizable(True)
        block_list = self.build_sub_block_list(spec, nested_list)

        scroll_area.setLayout(block_list)

        input_wrapper = InputPanelWrapper(
            inner_widget=block_list,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
        )

        self.state_value_dict[spec.full_name] = input_wrapper
        return input_wrapper

    def build_time_series_edit_widget(self, spec: AttributeSpecs):
        preset_value = self.get_default_value(spec, spec.full_name)

        file_chooser = FileChooserWidgetPanel(
            self._working_dir, spec.attr_type.name, preset_value, self.treeWidget()
        )

        self._display_error = file_chooser.display_error

        input_wrapper = InputPanelWrapper(
            inner_widget=file_chooser,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
        )

        self.state_value_dict[spec.full_name] = input_wrapper

        return input_wrapper

    def build_int_or_long_edit_widget(self, spec: AttributeSpecs):
        line_edit = self._create_line_edit("0", None)
        preset_value = self.get_default_value(spec, spec.full_name)
        line_edit.setText(str(preset_value))
        line_edit.setValidator(QtGui.QIntValidator())

        input_wrapper = InputPanelWrapper(
            inner_widget=line_edit,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
        )

        self.state_value_dict[spec.full_name] = input_wrapper
        return input_wrapper

    def build_string_edit_widget(self, spec: AttributeSpecs):
        line_edit = self._create_line_edit("", None)
        preset_value = self.get_default_value(spec, spec.full_name)
        line_edit.setText(preset_value)

        input_wrapper = InputPanelWrapper(
            inner_widget=line_edit,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
        )

        self.state_value_dict[spec.full_name] = input_wrapper
        return input_wrapper

    def build_list_edit_widget(self, spec: AttributeSpecs):
        preset_value = self.get_nested_list_data()

        if preset_value is None:
            preset_value = []

        for item, idx in zip(preset_value, range(len(preset_value))):
            item: dict
            for k, v in item.items():
                v: Attribute

        if isinstance(preset_value, list):
            dynamic_list = None

            for item, idx in zip(preset_value, range(len(preset_value))):
                if idx == 0:
                    block_list = self.build_sub_block_list(spec, [item])

                    dynamic_list = CustomListWidget(
                        block_list, spec, self.schema, self.attr_name
                    )
                    continue

                item: dict

                block_list = self.build_sub_block_list(spec, [item])

                input_wrapper = InputPanelWrapper(
                    inner_widget=block_list,
                    validation_error_signal=self.validation_error_signal,
                    signal_to_connect=self.validation_signal,
                    attribute=spec,
                )

                dynamic_list.set_widget(input_wrapper)

            if dynamic_list is None:
                block_list = self.build_sub_block_list(spec)

                dynamic_list = CustomListWidget(
                    block_list, spec, self.schema, self.attr_name
                )

            dynamic_list.row_creation_requested.connect(self._add_list_row)

            input_wrapper = InputPanelWrapper(
                inner_widget=dynamic_list,
                validation_error_signal=self.validation_error_signal,
                signal_to_connect=self.validation_signal,
                attribute=spec,
            )

            self.state_value_dict[spec.full_name] = input_wrapper

            return input_wrapper

        block_list = self.build_sub_block_list(spec, preset_value)

        dynamic_list = CustomListWidget(
            block_list, spec, self.schema, self.attr_name
        )

        dynamic_list.row_creation_requested.connect(self._add_list_row)

        input_wrapper = InputPanelWrapper(
            inner_widget=dynamic_list,
            validation_error_signal=self.validation_error_signal,
            signal_to_connect=self.validation_signal,
            attribute=spec,
        )
        self.state_value_dict = {spec.full_name: input_wrapper}

        return input_wrapper

    def search_attr_recursively(self, attr: Attribute, attr_full_name: str):
        """Search for a specific and primitive  nested attribute recursively"""
        for nested_key, nested_item in attr.nested.items():
            nested_item: Attribute

            if attr_full_name == str(nested_key):
                return nested_item

            if nested_item.has_nested:
                temp_result = self.search_attr_recursively(nested_item, attr_full_name)
                if temp_result:
                    return temp_result
                continue

        return None

    def recursive_search(self, data, key):
        """Search for a specific and primitive  nested attribute recursively for any data type"""
        if isinstance(data, list):
            for item in data:
                result = self.recursive_search(item, key)
                if result:
                    return result
        elif isinstance(data, dict):
            if key in data:
                return data[key]
            for k, v in data.items():
                result = self.recursive_search(v, key)
                v: Attribute
                if v.has_nested:
                    result = self.recursive_search(v.nested, key)

                if result:
                    return result
        return None

    def get_nested_list_data(self):
        """Get the nested list data from the root attribute spec
        Since one row can have multiple nested lists,
        we need to get the data from the root attribute spec and then search for the specific nested list data recursively
        """
        if self._default_value:
            if self._default_value.has_nested_list:
                nested_list = self._default_value.nested_list

                return nested_list
        return None

    def is_primitive_attr(self, spec: AttributeSpecs):
        """Check if the Attribute is a final node within the attribute tree /
        Check if the node can be related to a plain value
        """

        if spec.attr_type == schema.AttributeType.BLOCK or spec.attr_type:
            return False
        return True

    def get_default_value(
            self, spec: AttributeSpecs, attr_full_name, nested_list_data=None
    ):
        """Get the saved value for a given attribute spec ( if it exists)"""

        if self.default_agent_flat_value_dict is not None:
            pre = attr_full_name.split('.')[0]
            dict_key = attr_full_name.replace(pre + ".", "")
            if self.is_primitive_attr(spec):
                if dict_key in self.default_agent_flat_value_dict:
                    default_value = self.default_agent_flat_value_dict[dict_key]
                    return default_value

        self._default_value: Attribute

        if nested_list_data:
            matches = re.findall(r"(?<=\.)[^.]*$", attr_full_name)

            attr_short_name = matches[0]

            result = self.recursive_search(nested_list_data, attr_short_name)
            if result:
                return result.value

        if self._default_value:
            if self._default_value.has_nested_list:
                matches = re.findall(r"(?<=\.)[^.]*$", attr_full_name)

                attr_short_name = matches[0]

                nested_list = self._default_value.nested_list

                result = self.recursive_search(nested_list, attr_short_name)
                if result:
                    if result.has_value:
                        return result.value

                return None

        matches = re.findall(r"(?<=\.)[^.]*$", attr_full_name)

        attr_short_name = matches[0]

        if self._default_value:
            if self._default_value.has_nested:
                search_attr_recursively = self.search_attr_recursively(
                    self._default_value, attr_short_name
                )

                if search_attr_recursively:
                    if search_attr_recursively.has_value:
                        return search_attr_recursively.value

        spec_attr_fallback_value = ""

        if not self._default_value:
            return spec_attr_fallback_value

        default_value = ""

        self._default_value: Attribute

        if self._default_value.has_nested:
            for nested_key, nested_item in self._default_value.nested.items():
                nested_item: Attribute

                if attr_full_name.__contains__(str(nested_key)):
                    if nested_item.has_value:
                        default_value = nested_item.value

                    return default_value

        if self._default_value.has_value:
            default_value = self._default_value.value

        default_value = (
            default_value if default_value is not None else spec_attr_fallback_value
        )

        return default_value


    def _create_line_edit(self, placeholder_text: str, handler) -> QtWidgets.QLineEdit:
        """Create a line edit widget for the attribute"""
        line_edit = QtWidgets.QLineEdit()
        line_edit.setText(str(placeholder_text))


        self._display_error = (
            lambda has_error: line_edit.setStyleSheet(
                ERROR_TEXT_STYLE_LINE_EDIT
            )
            if has_error
            else line_edit.setStyleSheet("")
        )
        return line_edit

    def _create_unsupported_edit_widget(self, type_name: str) -> QtWidgets.QLabel:
        """Create a label widget for an unsupported attribute type (Leave for future implementation for new kinds of
        attributes)"""

        logging.error(
            NO_SUPPORTED_EDIT_WIDGET_TEXT.format(
                type_name
            )
        )

        label = QtWidgets.QLabel()

        label.setText(
            self.tr(NO_SUPPORTED_EDIT_WIDGET_TEXT.format(type_name))
        )
        label.setStyleSheet(ERROR_TEXT_STYLE_LABEL)
        return label

    def get_input_value(self):

        state_value_dict = {key: item for key, item in self.state_value_dict.items()}

        if self._attr_spec.attr_type != schema.AttributeType.BLOCK:
            return state_value_dict[next(iter(state_value_dict.keys()))]

        return state_value_dict

    def _get_data_from_input(self):
        """Get the data from the input panel"""
        attr_data = self.get_input_value()

        return attr_data

    def tr(self, msg: str) -> str:
        return QtCore.QCoreApplication.translate("AttributeTreeItem", msg)
