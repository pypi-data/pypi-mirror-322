import re
import typing

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFrame

from famegui.config.style_config import get_default_input_style, get_default_err_input_style
from famegui.ui.block_item_wrapper import BlockItemWrapper
from famegui.ui.block_type_wrapper import BlockTypeWrapper
from famegui.ui.fame_input_panels import FileChooserWidgetPanel

import fameio.input.schema as schema

from famegui.ui.list_block import CustomListWidget
from famegui.utils import is_exactly_convertible_to_float, is_exactly_convertible_to_int
from famegui_runtime_helper.attribute_dict_formatting_helper import StringAttributeType


class MiniAttributeSpecs(QObject):

    def __init__(self, full_name, attr_type, is_mandatory,
                 options, parent=None):
        super().__init__(parent)
        self._full_name: str = full_name
        self._attr_type: str = attr_type
        self._is_mandatory: bool = is_mandatory
        self._options: list = options

    @property
    def attr_type(self):
        return self._attr_type

    @property
    def full_name(self):
        return self._full_name

    @property
    def is_mandatory(self):
        return self._is_mandatory

    def get_values(self) -> tuple[str, str, bool, typing.Union[None, list[str]]]:
        return self._full_name, self._attr_type, self._is_mandatory, self._options


class InputPanelWrapper(QFrame):
    """Wrapper for all types of input panels.
    It is used to validate input and style it accordingly to their type."""

    def __init__(
            self,
            parent=None,
            inner_widget: typing.Optional[QWidget] = None,
            signal_to_connect: Signal = None,
            validation_error_signal: Signal = None,
            attribute: MiniAttributeSpecs = None,
            attr_name: str = None,
            list_idx: int = None
    ):
        super().__init__(parent)
        self._attribute_spec: MiniAttributeSpecs = attribute
        self._inner_widget = inner_widget
        self.info_panel = QLabel("")
        self.attr_name = attr_name
        self._list_index = list_idx
        self.original_stylesheet = None
        self.validation_error_signal = validation_error_signal
        self.setContentsMargins(0, 0, 0, 0)

        if attr_name is None:
            matches = re.findall(r"(?<=\.)[^.]*$", self._attribute_spec.full_name)

            attr_short_name = matches[0]
            self.attr_name = attr_short_name

        if not self.validation_error_signal:
            assert False, "validation_error_signal is None"

        self._init_layout()
        if inner_widget:
            self._inner_layout.addWidget(inner_widget)

        self._inner_layout.setSpacing(0)

        if signal_to_connect:
            signal_to_connect.connect(self.validate_input)
        else:
            raise ValueError("signal_to_connect is None")

        self._inner_layout.addWidget(self.info_panel)

        uniq_obj_name = f"myUniqueWidget-{id(inner_widget)}"
        inner_widget.setObjectName(uniq_obj_name)
        inner_widget.setStyleSheet(
            get_default_input_style(uniq_obj_name)
        )
        self.original_stylesheet = inner_widget.styleSheet()
        self._signal_to_connect = signal_to_connect



    def get_attribute_spec(self):
        """Return attribute spec"""
        return self._attribute_spec

    def get_short_attr_name(self):
        """Return short attribute name"""
        return self.attr_name

    def get_attribute_full_name(self) -> str:
        """Return full attribute name"""
        return self._attribute_spec.full_name

    def _init_layout(self):
        self._inner_layout = QVBoxLayout()
        self.setLayout(self._inner_layout)

        self._inner_layout.setContentsMargins(0, 0, 0, 0)
        self._inner_layout.setSpacing(0)

    def set_list_index(self, list_idx: int):
        self._list_index = list_idx

    @property
    def list_index(self):
        if self._list_index == -1:
            raise ValueError("List index value err")

        return self._list_index

    def _has_more_than_two_dots(self, s: str) -> bool:
        """Helper function to get the short name of an attribute"""

        return s.count(".") > 0

    def validate_input(self):
        """validate input and style input panel accordingly to their type"""

        if self._attribute_spec.is_mandatory:
            if self.get_input_value() is None:

                if self._inner_widget:
                    if self._attribute_spec.attr_type == schema.AttributeType.BLOCK:
                        return

                    self.info_panel.setText(
                        f'<font color="red">Please fill in {self._attribute_spec.full_name}</font>')

                    if isinstance(self._inner_widget, FileChooserWidgetPanel):
                        self._inner_widget: FileChooserWidgetPanel
                        self._inner_widget.set_validation_state(False)

                    if self._inner_widget.objectName():
                        obj_name = self._inner_widget.objectName()
                        self._inner_widget.setStyleSheet(
                            get_default_err_input_style(obj_name)

                        )
                        self.validation_error_signal.emit(
                            False, self._attribute_spec.full_name
                        )

                        return False
                    uniq_obj_name = f"myUniqueWidget-{id(self._inner_widget)}"
                    self._inner_widget.setObjectName(uniq_obj_name)
                    self._inner_widget.setStyleSheet(
                        get_default_err_input_style(uniq_obj_name)

                    )
                self.validation_error_signal.emit(False, self._attribute_spec.full_name)

                return False

        self._inner_widget.setStyleSheet(self.original_stylesheet)
        self.info_panel.setText(f"")

        if isinstance(self._inner_widget, FileChooserWidgetPanel):
            self._inner_widget: FileChooserWidgetPanel
            self._inner_widget.set_validation_state(True)
        self.validation_error_signal.emit(True, self._attribute_spec.full_name)

        return True

    def convert_text_to_type(self, text: str, attr_type: str):
        """Convert text to the type of attribute to save it to the scenario"""

        if not text:
            return None

        if attr_type == StringAttributeType.INTEGER.value or attr_type == StringAttributeType.LONG.value:
            return int(text) if text else None
        elif attr_type == StringAttributeType.DOUBLE.value:
            return float(text) if text else None

        return text

    def get_input_value(self):
        """Get input values in form of a dict"""

        if isinstance(self._inner_widget, QLineEdit):
            return (
                self.convert_text_to_type(
                    self._inner_widget.text(), self._attribute_spec.attr_type
                )
                if self._inner_widget.text() != ""
                else None
            )

        elif isinstance(self._inner_widget, QComboBox):
            return (
                self._inner_widget.currentText()
                if self._inner_widget.currentText() != ""
                else None
            )

        elif isinstance(self._inner_widget, FileChooserWidgetPanel):
            plain_value = self._inner_widget.get_path()
            if len(plain_value) == 0:
                return None

            if is_exactly_convertible_to_float(plain_value):
                return float(self._inner_widget.get_path())

            if is_exactly_convertible_to_int(plain_value):
                return float(self._inner_widget.get_path())

            return (
                self._inner_widget.get_path()
                if self._inner_widget.get_path() != ""
                else None
            )

        elif isinstance(self._inner_widget, BlockTypeWrapper):
            self._inner_widget: BlockTypeWrapper

            return (
                self._inner_widget.get_data()
                if self._inner_widget.get_data() != ""
                else None
            )

        elif isinstance(self._inner_widget, BlockItemWrapper):
            self._inner_widget: BlockItemWrapper
            block_item_data = self._inner_widget.get_data()

            if isinstance(block_item_data, dict):
                return (
                    self._inner_widget.get_data()
                    if self._inner_widget.get_data() != ""
                    else None
                )
            if isinstance(block_item_data, str):
                return (
                    self.convert_text_to_type(
                        self._inner_widget.get_data(), self._attribute_spec.attr_type
                    )
                    if self._inner_widget.get_data() != ""
                    else None
                )

        elif isinstance(self._inner_widget, CustomListWidget):
            self._inner_widget: CustomListWidget

            return (
                self._inner_widget.get_data()
                if self._inner_widget.get_data() != ""
                else None
            )

        else:
            return f"Soon ... {str(type(self._inner_widget))}"
