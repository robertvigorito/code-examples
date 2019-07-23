"""
EDL Separate UI

Production tool to split duplicated edl data...

TODO:
Create Ui:
    Add Drag and drop
    Add Directory find
    Add Insert Directory
    Add Progress Bar

Re Write EDL Class to make it more readable

"""

import sys
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
from edl_separator_func import EdlSeparator
import os
import glob
import json
from getpass import getuser


class EdlSeperatorUI(QMainWindow):
    pref_dir = os.path.dirname(__file__)
    pref_path = os.path.join(pref_dir, 'pref.json')

    def __init__(self):
        super(EdlSeperatorUI, self).__init__()
        self.setWindowTitle('EDL Separator BETA')

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.master_layout())
        self.setAcceptDrops(True)
        self.setCentralWidget(self.main_widget)
        self.resize(600, 350)
        self.set_pref()

    # ----------------------------------------- Pref --------------------------------------------

    def set_pref(self):
        try:
            with open(self.pref_path, 'r') as open_pref_path:
                data = json.load(open_pref_path)

            self.move(*data.get(getuser()))
        except (ValueError, IOError, TypeError):
            pass

    # -------------------------------------- Layouts ----------------------------------------------

    def layout_1(self):
        self.find_label = QLabel('Find:')
        self.line_edit = QLineEdit()

        self.find_dir_button = QPushButton()
        self.find_dir_button.pressed.connect(QFileDialog.getOpenFileNames)

        layout = QHBoxLayout()
        layout.addWidget(self.find_label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.find_dir_button)
        return layout

    def layout_2(self):
        self.edl_files_list = QListWidget()
        self.edl_files_list.setAcceptDrops(True)
        self.edl_files_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.clear = QPushButton('Clear')
        self.clear.pressed.connect(self.edl_files_list.clear)
        self.run = QPushButton('Separate EDL')
        self.run.pressed.connect(self.run_edl_separate)

        button_layout = QHBoxLayout()
        button_layout.addSpacing(200)
        button_layout.addWidget(self.clear)
        button_layout.addWidget(self.run)
        layout = QVBoxLayout()

        layout.addWidget(self.edl_files_list)
        layout.addSpacing(20)
        layout.addLayout(button_layout)
        layout.addSpacing(10)

        return layout

    def master_layout(self):
        master_layout = QVBoxLayout()
        m = [15] * 4
        master_layout.setContentsMargins(*m)

        # master_layout.addLayout(self.layout_1())
        master_layout.addLayout(self.layout_2())
        return master_layout

    # ------------------------------ Functions ------------------------------------------------
    def _get_listwigdet_item(self):
        for c in range(self.edl_files_list.count()):
            yield self.edl_files_list.item(c).text()

    def run_edl_separate(self):
        for path in self._get_listwigdet_item():
            e = EdlSeparator()
            e.file_path = path
            e.run()

        else:
            self.message = QMessageBox()
            v = self.frameGeometry().center()
            self.message.move(v)
            self.message.setText('EDL Separator complete...')
            self.message.exec_()

    def _delete_list_item(self):
        for item in self.edl_files_list.selectedItems():
            row = self.edl_files_list.row(item)
            self.edl_files_list.takeItem(row)

    def _add_items(self, paths):
        if isinstance(paths, (str, unicode)):
            paths = [paths]

        _temp_list = []

        for c in range(self.edl_files_list.count()):
            _temp_list.append(self.edl_files_list.item(c).text())

        for path in paths:
            if path in _temp_list:
                continue

            self.edl_files_list.addItem(path)

    # ------------------------------- Events -------------------------------------------------

    def closeEvent(self, event):
        data = {getuser(): (self.pos().x(), self.pos().y())}
        with open(self.pref_path, 'w') as open_pref_file:
            json.dump(data, open_pref_file, indent=4)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()

            if os.path.isfile(path):
                self._add_items(path)

            elif os.path.isdir(path):
                paths = glob.glob(os.path.join(path, '*.edl'))
                paths = [path.replace('\\', '/')for path in paths]
                self._add_items(paths)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            self._delete_list_item()


app = QApplication(sys.argv)
edl = EdlSeperatorUI()
edl.show()
sys.exit(app.exec_())
