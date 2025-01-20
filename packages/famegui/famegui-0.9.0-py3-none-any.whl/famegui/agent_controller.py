import typing

from PySide6 import QtCore

from famegui import models, colorpalette
import fameio.input.scenario.attribute as fameio

from famegui.scenario_canvas_elements.agent_canvas_item import AgentGraphItem


class AgentController(QtCore.QObject):
    """Controller attached to a FAME Agent to sync it with the views and manage the Business logic of the agent"""

    model_was_modified = QtCore.Signal()
    model_was_moved = QtCore.Signal(float, float)

    def __init__(self, agent: models.Agent, assigned_svg_color: typing.Union[str, None] = None):
        super().__init__()
        assert agent is not None
        self.model = agent
        self._scene_item = None
        self.assigned_svg_color = assigned_svg_color

        self.tree_item = None

    def set_svg_color(self, svg_color):
        self.assigned_svg_color = svg_color

    def blockSignals(self, b) -> bool:
        if b:
            self.model_was_modified.disconnect()
            self.model_was_moved.disconnect()

        return super().blockSignals(b)

    @property
    def id(self) -> int:
        return self.model.id

    @property
    def display_id(self) -> str:
        return self.model.display_id

    @property
    def type_name(self) -> str:
        return self.model.type_name

    @property
    def attributes(self) -> typing.Dict[str, fameio.Attribute]:
        return self.model.attributes

    def set_display_xy(self, x: int, y: int):
        self.model.set_display_xy(x, y)

    @property
    def tooltip_text(self) -> str:
        text = "<font size='4'><b>{}</b></font>".format(self.model.type_name)

        text += (
            "<table border=0 cellpadding=2 style='border-collapse: collapse'><tbody>"
        )
        text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(
            "ID", self.model.display_id
        )
        for attr_name, attr_value in self.model.attributes.items():
            text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(
                attr_name, attr_value.value
            )

        text += "</tbody></table>"
        return text

    @property
    def svg_color(self) -> str:
        return self.assigned_svg_color if self.assigned_svg_color is not None \
            else colorpalette.color_for_agent_type(self.type_name)

    @property
    def x(self):
        assert self.model.display_xy is not None
        return self.model.display_xy[0]

    @property
    def y(self):
        assert self.model.display_xy is not None
        return self.model.display_xy[1]

    @property
    def scene_item(self) -> AgentGraphItem:
        assert self._scene_item is not None
        return self._scene_item

    def set_scene_item(self, item: AgentGraphItem):
        assert item.type() == AgentGraphItem.Type

        assert self._scene_item is None  # should be attached to an item only once
        self._scene_item = item
        self._scene_item.position_changed = lambda x, y: self._item_position_changed(
            x, y)

    def position_changed(self):
        """Called when the data of a model is changed"""
        self.model_was_modified.emit()

    def _item_position_changed(self, x: int, y: int):
        self.model.set_display_xy(x, y)
        self.model_was_moved.emit(x, y)
