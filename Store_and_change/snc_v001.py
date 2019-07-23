import os
import json
import nuke

INPUT_MESSAGE = 'Please insert the name of the preference?'
ERROR_MESSAGE = 'Please select a ColorCorrect node to save preference!'
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
    data = json_read(CC_DATA_FILE)
    nuke.thisNode()['TimeOfDay'].setValues(sorted(data.keys()))

    return 1


def get_colorcorrect_data():
    color_correct_data = dict()
    sel_node = nuke.selectedNode()

    if sel_node.Class() != 'ColorCorrect':
        raise ValueError(ERROR_MESSAGE)

    for knob in sel_node.knobs():
        if type(sel_node[knob]) is not nuke.AColor_Knob:
            continue

        value = sel_node[knob].getValue()
        color_correct_data[knob] = value

    return color_correct_data


def add_pref():
    pref_key = nuke.getInput(INPUT_MESSAGE)

    if not pref_key:
        return 0

    data = json_read(CC_DATA_FILE)

    if not isinstance(data, dict):
        data = dict()

    data.update({pref_key: get_colorcorrect_data()})
    json_write(CC_DATA_FILE, data)
    update_pulldown()

    return 1


def update_group_nodes():

    key = nuke.thisNode()['TimeOfDay'].value()
    pref_data = json_read(CC_DATA_FILE).get(key, dict()
                                            )
    for group_node in nuke.allNodes('Group'):
        group_node.begin()

        for colorcorrect_node in nuke.allNodes('ColorCorrect'):
            for knob, value in pref_data.items():
                colorcorrect_node[knob].setValue(value)

        group_node.end()

    return 1


def remove_pref():

    key = nuke.thisNode()['TimeOfDay'].value()

    data = json_read(CC_DATA_FILE)
    data.pop(key)

    json_write(CC_DATA_FILE, data)
    update_pulldown()

    return 1


update_pulldown()
