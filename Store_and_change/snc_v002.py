import os
import json
import nuke

INPUT_MESSAGE = 'Please insert the name of the preference?'
ERROR_MESSAGE = 'Please select TOTS_LIGHTING node to save preference!'
ERROR_DIR_MESSAGE = 'Invalid preference directory, please add to a valid directory'

PREF_DIR = nuke.thisNode()['pref_dir'].getValue()
assert os.path.exists(PREF_DIR), ERROR_DIR_MESSAGE

PREF_BASENAME = 'cc_data'
EXTENSION = '.json'
CC_DATA_FILE = os.path.join(PREF_DIR, PREF_BASENAME + EXTENSION)


def json_write(json_file_path, data):
    with open(json_file_path, 'w') as open_json_file:
        json.dump(data, open_json_file, indent=4)
    return True


def json_read(json_file_path):
    try:
        with open(json_file_path, 'r') as open_json_file:
            data = json.load(open_json_file)
        return data

    except (ValueError, IOError):
        return dict()


def update_pulldown():
    """
    Updating the node pulldown from the key values of the preference sheet...
    """

    data = json_read(CC_DATA_FILE)
    nuke.thisNode()['TimeOfDay'].setValues(sorted(data.keys()))

    return 1


def extract_node_info():
    """
    Extract user knob data from node...
    """

    node = nuke.selectedNode()
    if 'TOTS_LIGHTING' not in node.name():
        raise ValueError(ERROR_MESSAGE)

    for knob in node.writeKnobs().split('\n'):
        if not knob:
            continue

        knob = knob.split(' ')[0]
        value = node[knob].getValue()

        yield knob, value


def add_to_pref():
    """
    Save to json preference sheet...
    """

    pref_key = nuke.getInput(INPUT_MESSAGE)

    if not pref_key:
        return 0

    data = json_read(CC_DATA_FILE)

    if not isinstance(data, dict):
        data = dict()

    node_data = {pref_key: {key: item for key, item in extract_node_info()}}
    data.update(node_data)

    json_write(CC_DATA_FILE, data)
    update_pulldown()

    return 1


def update_group_nodes():
    """
    Updating the tots lighting group.
    """

    key = nuke.thisNode()['TimeOfDay'].value()
    pref_data = json_read(CC_DATA_FILE).get(key, dict())

    for node in nuke.allNodes('Group'):
        if 'TOTS_LIGHTING' not in node.name():
            continue

        for name, value in pref_data.items():
            if type(node.knob(name)) == nuke.Enumeration_Knob:
                value = int(value)

            elif type(node.knob(name)) == nuke.Tab_Knob:
                continue

            node[name].setValue(value)

    return 1


def remove_from_pref():
    """
    Delete selected data from json preference sheet...
    """
    try:
        key = nuke.thisNode()['TimeOfDay'].value()
        data = json_read(CC_DATA_FILE)
        data.pop(key)

        json_write(CC_DATA_FILE, data)
        update_pulldown()

    except KeyError:
        pass


update_pulldown()
