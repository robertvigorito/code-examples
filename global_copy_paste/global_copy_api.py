import config
import nuke
import global_functions as gf
import glob
import os
import scandir

INPUT_MESSAGE = 'Please insert your name? A re-log on is required to save the new environment!'
SAVED_SCRIPT_DIR = os.path.join(config.find('.pipeline').next(), 'tools', 'nuke', 'global_copy_paste')
PREF_FILE_PATH = os.path.join(SAVED_SCRIPT_DIR, 'pref.json')
CALL_FUNCTION = 'global_copy_paste.GlobalCopyPaste().'

TOOLTIP_CLEAR = 'This will clear all the saved scripts with in the {} directory...'.format(SAVED_SCRIPT_DIR)
TOOLTIP_RESET = 'Reset the username you will see within the paste menu...'

MESSAGE_QUICK_PASTE = 'No last paste found, please selected a user to paste from to save preference!'
ICON = os.path.join(os.path.dirname(__file__), 'copy_paste.png')


class GlobalCopyPaste(object):
    """
    Global copy node tree from one artist to another, instantly...
    """

    def __init__(self):
        self.USERNAME = os.environ.get('mrwolfuser')

    def set_environment(self):
        """
        Get the username from nuke input and save to .bashrc
        """

        from platform import system

        self.USERNAME = nuke.getInput(INPUT_MESSAGE)
        assert self.USERNAME, 'Please add an input...'
        os.environ['mrwolfuser'] = self.USERNAME

        if system() == 'Windows':
            os.system("SETX mrwolfuser {}".format(self.USERNAME))
        else:
            os.system("echo 'export mrwolfuser={}' >> ~/.bashrc".format(self.USERNAME))

        return 1

    def set_pref(self, user):
        """
        Setting the preference for quick paste operation...
        """
        try:
            data = gf.json_read(PREF_FILE_PATH)

        except IOError:
            data = dict()

        data.update({self.USERNAME: user})
        gf.json_write(PREF_FILE_PATH, data)

        return 1

    def quick_paste_nodes(self):
        """
        Paste the last user selected...
        """

        data = gf.json_read(PREF_FILE_PATH)
        user = data.get(self.USERNAME) if isinstance(data, dict) else None
        nuke.message(MESSAGE_QUICK_PASTE) if user is None else self.paste_nodes(user)

        return 1

    def save_nodes(self):
        """
        Save selected nodes to the saved script dir, with the name extracted from
        mrwolfuser...
        """

        if self.USERNAME is None:
            self.set_environment()

        if not os.path.exists(SAVED_SCRIPT_DIR):
            os.makedirs(SAVED_SCRIPT_DIR)

        global_copy_script = os.path.join(SAVED_SCRIPT_DIR, self.USERNAME + '.nk')
        nuke.nodeCopy(global_copy_script)
        self.update_menu()

        return 1

    def paste_nodes(self, user):
        """
        Select from a list generated from the current users that have added to
        directory, once the selection has been made added selected script to
        current nuke script...
        """

        path_to_paste = os.path.join(SAVED_SCRIPT_DIR, user + '.nk')
        nuke.nodePaste(path_to_paste)
        self.set_pref(user)

        return 1

    def refresh(self):
        """
        Refresh the copy paste menu if a new user has added a copy script...
        """

        self.update_menu()

        return 1

    def clear(self):
        """
        Clear saved paste scripts...
        """

        glob_expression = os.path.join(SAVED_SCRIPT_DIR, '*.nk')

        for saved_script in glob.glob(glob_expression):
            os.remove(saved_script)

        self.update_menu()

        return 1

    def update_menu(self):
        """
        Updating the global menu...
        """

        m = nuke.menu('Nodes').addMenu('Copy Paste', icon=ICON)
        m.clearMenu()

        m.addCommand('Copy', CALL_FUNCTION + 'save_nodes()', 'shift+alt+c')
        p = m.addMenu('Paste')

        m.addSeparator()
        m.addCommand('Quick Paste', CALL_FUNCTION + 'quick_paste_nodes()', 'shift+alt+v')

        m.addSeparator()

        s = m.addMenu('Settings')
        s.addCommand('Refresh', CALL_FUNCTION + 'refresh()')
        s.addCommand('Clear', CALL_FUNCTION + 'clear()', tooltip=TOOLTIP_CLEAR)
        s.addCommand('Reset', CALL_FUNCTION + 'set_environment()', tooltip=TOOLTIP_RESET)

        global_copy_users = [user.replace('.nk', '') for user in scandir.listdir(SAVED_SCRIPT_DIR)
                             if user.endswith('.nk')]

        for name in sorted(global_copy_users):
            cmd = CALL_FUNCTION + 'paste_nodes("{}")'.format(name)
            p.addCommand(name, cmd)

        return 1









