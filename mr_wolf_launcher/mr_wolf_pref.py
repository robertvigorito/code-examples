from getpass import getuser
import global_functions as gf
import os

PREF_DIR = os.path.dirname(__file__)
PREF_BASENAME = 'mr_wolf_prefs.json'
PREF_FILE_PATH = os.path.abspath(os.path.join(PREF_DIR, PREF_BASENAME))


def save_pref(data):
    """
    Saving the data to allocated preference file path...
    """

    data = {getuser(): data}
    gf.json_write(PREF_FILE_PATH, data)

    return 1


def load_pref():
    """
    Loading the data saved within the preference
    file...
    """

    data = gf.json_read(PREF_FILE_PATH)
    data = data.get(getuser())

    return data





