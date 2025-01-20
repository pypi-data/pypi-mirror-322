from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout

from famegui import models
from famegui.agent_controller import AgentController
from famegui.config.config import CUSTOM_DELIVERY_STEPS_TIME_OPTION
from famegui.config.contract_consts import PRESET_DURATION_IN_SECONDS
from famegui.config.static_ui_components import build_new_contract_dlg
from famegui.config.style_config import FAME_LINE_EDIT_STYLE_ERR_STATE, FAME_LINE_EDIT_STYLE_DEFAULT, \
    ERROR_TEXT_STYLE_LABEL
from famegui.database.prebuild_queries.interval_presets import get_delivery_interval_presets
from famegui.generated.ui_dialog_newcontract import Ui_DialogNewContract
from famegui.time_utils import (
    convert_fame_time_to_gui_datetime,
    convert_gui_datetime_to_fame_time,
)
from famegui.ui.helper import gen_preset_interval_chooser


class DialogNewContract(QDialog):
    """Dialog for creating a single contract"""

    fame_to_datetime_conversion_triggered: bool = False
    WIDGET_DATE_FORMAT = "dd/MM/yyyy hh:mm:ss"

    def _configure_line_edit_for_unsigned_int(self, line_edit: QtWidgets.QLineEdit):
        line_edit.setText("0")
        regex_uint64 = QtCore.QRegularExpression("\\d{1,20}")
        line_edit.setValidator(QtGui.QRegularExpressionValidator(regex_uint64))
        line_edit.textChanged.connect(self._update_ok_button_status)

    def on_preset_changed(self, index, selected_option: str):
        """
        Handles the change event when a new preset is selected
        """
        # Do something with the selected preset
        if selected_option == "Custom":
            return

        value = self.interval_presets[index][PRESET_DURATION_IN_SECONDS]

        self._ui.lineDeliveryInterval.setText(value)


    def _configure_line_edit_for_signed_int(self, line_edit: QtWidgets.QLineEdit):
        line_edit.setText("0")
        regex_uint64 = QtCore.QRegularExpression("-?\\d{1,20}")
        line_edit.setValidator(QtGui.QRegularExpressionValidator(regex_uint64))
        line_edit.setStyleSheet("background-color: #EBEBEB;")
        line_edit.textChanged.connect(self._update_ok_button_status)

    def gen_preset_interval_chooser(self):
        """
        Generates a simple ComboBox/Preset chooser Widget to choose from presets
        """

        choices = [item["preset_label"] for item in self.interval_presets]
        choices_bundles = [item for item in self.interval_presets]

        interval_preset_chooser = gen_preset_interval_chooser(choices, self.on_preset_changed,
                                                              self._ui.lineDeliveryInterval,
                                                              choices_bundles,
                                                              CUSTOM_DELIVERY_STEPS_TIME_OPTION)

        return interval_preset_chooser

    def _setup_delivery_interval_chooser_input(self):
        """
        Insert a simple ComboBox/Preset chooser Widget
        into the delivery interval chooser box to choose from Interval presets
        """

        chooser = self.gen_preset_interval_chooser()

        chooser_holder_layout = QHBoxLayout()

        chooser_holder_layout.addWidget(chooser)
        chooser_holder_layout.setContentsMargins(0, 0, 0, 0)

        self._ui.delivery_interval_chooser.setLayout(chooser_holder_layout)

    def _configure_line_edit_for_optional_signed_int(self, line_edit: QtWidgets.QLineEdit):
        line_edit.setText("")
        line_edit.setPlaceholderText(self.tr("optional"))
        regex_uint64 = QtCore.QRegularExpression("-?\\d{0,20}")
        line_edit.setValidator(QtGui.QRegularExpressionValidator(regex_uint64))
        line_edit.textChanged.connect(self._update_ok_button_status)

    def __init__(
            self,
            sender: AgentController,
            receiver: AgentController,
            schema: models.Schema,
            parent=None,
    ):
        QDialog.__init__(self, parent)
        self._ui = Ui_DialogNewContract()
        self._ui.setupUi(self)
        self._sender = sender
        self._receiver = receiver

        self.interval_presets = get_delivery_interval_presets()

        self.setWindowTitle(self.tr("New contract"))
        self._ui.labelDescr.setText(
            self.tr(self.tr(self.tr(build_new_contract_dlg(self._sender, self._receiver)))))

        # force the user to select a product except if only one is available
        if self._ui.comboBoxProduct.count() != 1:
            self._ui.comboBoxProduct.setCurrentIndex(-1)

        self._ui.comboBoxProduct.currentIndexChanged.connect(self._update_ok_button_status)
        self._update_ok_button_status()

        self._prep_input_line_edits()

        # fill possible products to select based on the sender schema agent type
        sender_type = schema.agent_type_from_name(sender.type_name)
        assert sender_type is not None
        self._ui.comboBoxProduct.addItems(list(set(sender_type.products)))

        # force the user to select a product except if only one is available
        if self._ui.comboBoxProduct.count() != 1:
            self._ui.comboBoxProduct.setCurrentIndex(-1)

        # connect
        self._ui.comboBoxProduct.currentIndexChanged.connect(
            self._update_ok_button_status
        )

        self._update_ok_button_status()

        self._ui.lineFirstDeliveryTime.textChanged.connect(
            self._update_fame_time_text_areas
        )

        self._ui.lineExpirationTime.textChanged.connect(
            self._update_fame_time_text_areas
        )

    def accept(self):
        delivery_fame_time = int(self._ui.lineDeliveryInterval.text())

        if delivery_fame_time == 0:
            self._ui.lineDeliveryInterval.setStyleSheet(FAME_LINE_EDIT_STYLE_ERR_STATE)
            self._ui.labelErrorDeliveryInterval.setText("Delivery Interval must be greater then 0!")

            return

        self._ui.lineDeliveryInterval.setStyleSheet(FAME_LINE_EDIT_STYLE_DEFAULT)
        self._ui.labelErrorDeliveryInterval.setText("")

        super().accept()

    def _prep_date_time_fields(self):
        """Configure date time fields to use the correct format and to trigger the update of the fame time fields"""
        self._ui.lineFirstDeliveryNonFameTime.setCalendarPopup(True)
        self._ui.lineFirstDeliveryNonFameTime.setDisplayFormat(self.WIDGET_DATE_FORMAT)
        self._ui.lineFirstDeliveryNonFameTime.dateTimeChanged.connect(
            self._update_fame_times
        )

        self._ui.lineExpirationTimeNonFameTime.setCalendarPopup(True)
        self._ui.lineExpirationTimeNonFameTime.setDisplayFormat(self.WIDGET_DATE_FORMAT)
        self._ui.lineExpirationTimeNonFameTime.dateTimeChanged.connect(
            self._update_fame_times
        )

    def _prep_input_line_edits(self):
        """Accept uint64 numbers as specified in protobuf schema"""
        self._configure_line_edit_for_unsigned_int(self._ui.lineDeliveryInterval)
        self._configure_line_edit_for_signed_int(self._ui.lineFirstDeliveryTime)
        self._configure_line_edit_for_optional_signed_int(self._ui.lineExpirationTime)

        self._setup_delivery_interval_chooser_input()

    def make_new_contract(self) -> models.Contract:
        expiration_time_str = self._ui.lineExpirationTime.text()
        expiration_time = int(expiration_time_str) if expiration_time_str else None

        return models.Contract(
            self._sender.id,
            self._receiver.id,
            self._ui.comboBoxProduct.currentText(),
            int(self._ui.lineDeliveryInterval.text()),
            int(self._ui.lineFirstDeliveryTime.text()),
            expiration_time,
        )

    def _update_fame_time_text_areas(self):
        self.fame_to_datetime_conversion_triggered = True

        fame_first_delivery_time: str = self._ui.lineFirstDeliveryTime.text()
        if fame_first_delivery_time == "":
            return
        gui_start_time = convert_fame_time_to_gui_datetime(
            int(fame_first_delivery_time))
        self._ui.lineFirstDeliveryNonFameTime.setDateTime(gui_start_time)

        fame_expiration_time: str = self._ui.lineExpirationTime.text()
        if fame_expiration_time == "":
            return

        gui_expiration_time_time = convert_fame_time_to_gui_datetime(int(fame_expiration_time))

        self._ui.lineExpirationTimeNonFameTime.setDateTime(gui_expiration_time_time)

    def _update_fame_times(self):
        if self.fame_to_datetime_conversion_triggered:
            self.fame_to_datetime_conversion_triggered = False
            return
        self._ui.lineExpirationTime.setText(
            str(convert_gui_datetime_to_fame_time(
                self._ui.lineExpirationTimeNonFameTime.text()
            )))

        self._ui.lineFirstDeliveryTime.setText(
            str(
                convert_gui_datetime_to_fame_time(
                    self._ui.lineFirstDeliveryNonFameTime.text()
                )))

    def _update_ok_button_status(self):
        all_fields_ok = (
                self._ui.comboBoxProduct.currentText() != ""
                and self._ui.lineDeliveryInterval.text() != ""
                and self._ui.lineFirstDeliveryTime.text() != ""
        )
        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(all_fields_ok)
