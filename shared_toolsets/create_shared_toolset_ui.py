try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *

import os
import sys
import shared_toolset_api
import nuke
import nukescripts
import shutil
import global_functions as gf


class SharedToolset(QDialog):
    """
    Shared toolset ui, that overrides the nuke base ui, adding features
    for artist to easily share toolset, and update toolsets...
    """

    def __init__(self):
        super(SharedToolset, self).__init__(parent=QApplication.activeWindow())
        self.setWindowTitle('Create Shared Toolset')
        self.setMinimumSize(350, 150)
        self.master_layout()
        self._message = QMessageBox(self)

    def base_window(self):
        """
        Creating the label, combobox and line input...

        :return: layout
        """

        folder_label = QLabel('Toolset Menu:')
        toolset_label = QLabel('Toolset Name:')

        self.toolset_directory = QComboBox()
        self.toolset_name = QLineEdit()

        self._extract_toolset_directory()

        layout = QGridLayout()
        layout.addWidget(folder_label, 0, 0, Qt.AlignRight)
        layout.addWidget(self.toolset_directory, 0, 1)
        layout.addWidget(toolset_label)
        layout.addWidget(self.toolset_name)

        return layout

    def button_layout(self):
        """
        Creating the push button layout...

        :return: layout
        """

        self.create_button = QPushButton('Create')
        self.cancel_button = QPushButton('Cancel')

        self.create_button.pressed.connect(self._create_toolset)
        self.cancel_button.pressed.connect(self.close)

        layout = QHBoxLayout()
        layout.addWidget(self.create_button)
        layout.addWidget(self.cancel_button)

        return layout

    def master_layout(self):
        """
        Adding all the layouts to master and setting to main widget
        (Qdialog)....

        :return: master layout
        """

        master_layout = QVBoxLayout(self)
        master_layout.addLayout(self.base_window())
        master_layout.addLayout(self.button_layout())

        return master_layout

    def _condition(self, name, path):
        """
        Find an array of statement that could prevent the tool from operation...

        :param str name:
        :param str path:
        :return:
        """
        self._message.setText('')

        if name == '.nk':
            self._message.setText('Please insert a Toolset name?')

        elif not nuke.selectedNodes():
            self._message.setText('No nodes have been selected...')

        elif os.path.exists(path):
            self._message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self._message.addButton('Delete', QMessageBox.ResetRole)
            self._message.setText('Toolset already exist! Would you like to replace or delete?')

        if not self._message.text():
            return True

        else:
            flag = self._message.exec_()

        if flag == 0:
            os.remove(path)
            shared_toolset_api.refresh_toolset()
            return False

        elif flag == self._message.No or flag == self._message.Ok or flag == self._message.Cancel:
            return False

    def _create_toolset(self):
        """
        If all condition are met, create a toolset in the selected
        folder...

        :return:
        """

        index = self.toolset_directory.currentIndex()
        name = self.toolset_name.text() + '.nk'

        path = os.path.abspath(os.path.join(self.toolset_directory.itemData(index), name))
        _message = self._condition(name, path)

        if not _message:
            return False

        gf.mkdir(os.path.dirname(path))
        nuke.nodeCopy(path)

        shared_toolset_api.refresh_toolset()
        self._message.setText('Toolset has been created...')
        self._message.exec_()

        return True

    def _extract_toolset_directory(self):
        """
        Retrieving the toolset information from the nuke plugin path
        and appending the item to toolset directory drop down...

        :return:
        """

        for path in shared_toolset_api.find_toolset_path():
            base_name = os.path.basename(os.path.abspath(path))

            if base_name == 'ToolSets' and '.nuke' in path:
                base_name = 'Root'

            elif base_name == 'ToolSets' and 'nuke' in path:
                base_name = 'Shared'

            self.toolset_directory.addItem(base_name, os.path.abspath(path))

        return True


def run():
    for app in qApp.allWidgets():
        if type(app).__name__ == 'SharedToolset':
            app.close()
    st = SharedToolset()
    st.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    toolset = SharedToolset()
    toolset.show()
    sys.exit(app.exec_())

