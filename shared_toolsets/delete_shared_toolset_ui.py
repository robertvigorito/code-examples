try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *

import nuke
import os
import sys
import scandir
import shutil
import shared_toolset_api as api
import global_functions as gf


VERSION = nuke.NUKE_VERSION_STRING


class DeleteSharedToolset(QDialog):
    def __init__(self):
        super(DeleteSharedToolset, self).__init__(parent=QApplication.activeWindow())
        self.setWindowTitle('Delete Shared Toolset')
        self.setMinimumSize(300, 500)
        self.master_layout()

    def tree_layout(self):
        """
        Creating the layout of the QTreeWidget...

        :return:
        """

        self.tree_widget = QTreeWidget()
        self.tree_widget.setSelectionMode(self.tree_widget.ExtendedSelection)
        self._find_tree_items()
        self.tree_widget.setHeaderLabel('')

        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)

        return layout

    def button_layout(self):
        """
        Creating delete and run button...

        :return:
        """

        self.delete = QPushButton('Delete')
        self.cancel = QPushButton('Cancel')

        self.delete.pressed.connect(self._delete_toolset)
        self.cancel.pressed.connect(self.close)

        layout = QHBoxLayout()
        layout.addWidget(self.delete)
        layout.addWidget(self.cancel)

        return layout

    def _message(self):
        """
        Creating a custom message box...

        :return:
        """

        message = QMessageBox(self)

        message.setText('Are you sure you would like to delete the toolset?')
        message.setIcon(QMessageBox.Warning)
        message.setStandardButtons(message.Yes | message.No)

        return message

    def master_layout(self):
        """
        Combine all layouts...

        :return:
        """

        master_layout = QVBoxLayout(self)
        master_layout.addLayout(self.tree_layout())
        master_layout.addLayout(self.button_layout())

        return master_layout

    def _find_tree_items(self):
        """

        :return:
        """

        for path in nuke.pluginPath():
            path = os.path.abspath(os.path.join(path, 'ToolSets'))

            if not os.path.exists(path) or VERSION in path:
                continue

            for base, folder, files in scandir.walk(path):
                name = os.path.basename(base)

                if 'ToolSets' != name:
                    item = QTreeWidgetItem(self.tree_widget, [name])
                    item.setData(0, Qt.UserRole, base)

                else:
                    item = self.tree_widget

                for f in files:
                    name = os.path.basename(f)
                    file_item = QTreeWidgetItem(item, [name])
                    file_item.setData(0, Qt.UserRole, os.path.join(base, f))

        return True

    def _find_and_delete(self):
        """
        Loop through the selected items and remove the files...

        :return:
        """

        for item in self.tree_widget.selectedItems():
            path = item.data(0, Qt.UserRole)

            if os.path.isdir(path):
                shutil.rmtree(path)

            elif os.path.exists(path):
                os.remove(path)

        return True

    def _delete_toolset(self):
        """
        Delete function....

        :return:
        """

        if self._message().exec_() == QMessageBox.No:
            return False

        self._find_and_delete()
        api.refresh_toolset()
        self.close()

        return True


def run():
    """
    Custom Run, which removes the widget if its already open...

    :return:
    """

    for app in qApp.allWidgets():
        if type(app).__name__ == 'DeleteSharedToolset':
            app.close()

    st = DeleteSharedToolset()
    st.show()

    return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    delete = DeleteSharedToolset()
    delete.show()
    sys.exit(app.exec_())
