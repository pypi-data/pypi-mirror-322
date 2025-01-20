def get_pre_defined_string_set_values_from_scenario(scenario_model):
    assert scenario_model is not None

    string_set_data_dict = {}

    for item_key, item in scenario_model.string_sets.items():
        string_set_data_dict[item_key] = [key for key in item.to_dict()["values"].keys()]

    return string_set_data_dict
