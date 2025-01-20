from PySide6 import QtWidgets
from PySide6.QtWidgets import QComboBox


def gen_preset_interval_chooser(choices: list, on_preset_changed, input_field,
                                choices_bundles, preset_choice=None):
    """
    Generates a simple ComboBox/Preset chooser Widget to choose from presets
    """

    choices.append("Custom")
    interval_preset_chooser = QtWidgets.QComboBox()
    interval_preset_chooser.addItems(choices)

    interval_preset_chooser.currentIndexChanged.connect(lambda idx: on_preset_changed(idx, choices[idx]))

    if preset_choice:
        interval_preset_chooser.setCurrentText(preset_choice)

    input_field.textChanged.connect(lambda new_text: _on_delivery_interval_steps_text_input_changed(new_text,
                                                                                                    interval_preset_chooser,
                                                                                                    choices_bundles))

    return interval_preset_chooser


def find_preset_by_seconds(presets, seconds):
    return next(
        (preset for preset in presets if preset['preset_duration_in_seconds'] == str(seconds)),
        None
    )


def _on_delivery_interval_steps_text_input_changed(text: str,
                                                   interval_preset_chooser: QComboBox,
                                                   choices_bundles: list[dict]):
    """Adjust """
    choices = []
    for i in range(interval_preset_chooser.count()):
        choices.append(interval_preset_chooser.itemText(i))

    preset_bundle = find_preset_by_seconds(choices_bundles, text)

    interval_preset_chooser.blockSignals(True)

    if preset_bundle is not None:
        interval_preset_chooser.setCurrentText(preset_bundle["preset_label"])
    else:
        interval_preset_chooser.setCurrentText("Custom")

    interval_preset_chooser.blockSignals(False)
