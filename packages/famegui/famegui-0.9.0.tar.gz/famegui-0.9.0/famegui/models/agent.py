import typing

import fameio.input.scenario as fameio
from fameio.input.scenario import Attribute, Agent

from famegui_runtime_helper.attribute_dict_formatting_helper import flatten_dict


class Agent(fameio.Agent):
    """Extends fameio.Agent with the features required for the GUI"""

    def __init__(self, agent_id: int, type_name: str):
        super().__init__(agent_id, type_name)
        self._inputs = []
        self._outputs = []
        self._display_xy = None

    @property
    def inputs(self) -> typing.List[int]:
        return self._inputs

    def add_input(self, agent_id: int) -> None:
        self._inputs.append(agent_id)

    @property
    def outputs(self) -> typing.List[int]:
        return self._outputs

    def add_output(self, agent_id: int) -> None:
        self._outputs.append(agent_id)

    def has_display_xy(self):
        return self._display_xy is not None

    @property
    def display_xy(self) -> typing.Optional[typing.List[float]]:
        return self._display_xy

    def set_display_xy(self, x: float, y: float) -> None:
        self._display_xy = [x, y]

    @classmethod
    def from_dict(cls, definitions: dict) -> Agent:

        agent_model = super().from_dict(definitions)

        x_y_coords = None

        if "ext" in definitions:
            if "DisplayXY" in definitions["ext"]:
                x_y_coords =  definitions["ext"]["DisplayXY"]

        if x_y_coords is not None:
            agent_model.set_display_xy(x_y_coords[0], x_y_coords[1])

        return agent_model

    def build_nested_sub_list(self, final_dict, item):
        res_list = []
        for sub_dict in item.nested_list:
            list_item = {}
            for sub_dict_key, sub_dict_item in sub_dict.items():
                if isinstance(sub_dict_item, Attribute):
                    if sub_dict_item.has_value:
                        list_item[sub_dict_key] = sub_dict_item.value

                    if sub_dict_item.has_nested:
                        list_item[sub_dict_key] = self.build_attributes_dict(final_dict, sub_dict_item.nested)

            res_list.append(list_item)

        return res_list

    def get_flat_agent_attributes_dict(self):
        final_dict = {}
        result = self.build_attributes_dict(final_dict, self.attributes)

        flat_dict = flatten_dict(self.attributes, result)
        return flat_dict

    def build_attributes_dict(self, final_dict: dict, obj: dict[str, Attribute], depth=0):
        """Recursively build a dictionary of an object's attributes."""
        attributes_dict = {}

        for item_key, item in obj.items():
            if isinstance(item, Attribute):
                if item.has_nested:
                    attr_dict = self.build_attributes_dict(attributes_dict, item.nested)
                    attributes_dict[item_key] = attr_dict

                if item.has_value:
                    attributes_dict[item_key] = item.value

                if item.has_nested_list:
                    attributes_dict[item_key] = self.build_nested_sub_list(final_dict, item)
            else:
                attributes_dict[item_key] = item

        return attributes_dict

    def to_simple_attr_dict(self) -> dict:
        final_dict = {}
        final_dict = self.build_attributes_dict(final_dict, self.attributes)

        return final_dict

    def to_fame_gui_adjusted_dict(self):
        result = super().to_dict()

        result["ext"] = {
            "DisplayXY": self.display_xy
        }

        return result
