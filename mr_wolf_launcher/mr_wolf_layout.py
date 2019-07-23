from PySide.QtCore import *
from PySide.QtGui import *

import mr_wolf_pref
import mr_wolf_css as css
import sys
import glob
import os
import subprocess
from functools import partial

ICON_EXTENSION = '[.png | .ico]'
TOOL_DIR = os.path.join(os.path.dirname(__file__).split('prod', 1)[0], 'tools', 'mr_wolf_tools')
SPAN = 3


class CustomTabWidget(QTabWidget):
    def __init__(self):
        super(CustomTabWidget, self).__init__()
        self.setStyleSheet(css.main_style)
        self.populate_tabs()

    @staticmethod
    def button_execute(script):
        """
        Setting up the button connection to an executable function which
        will start a new process based of the current python path.
        """

        import platform
        python_exe_path = sys.executable

        if platform.system() == 'Windows':
            cmd = '{} {}'.format(python_exe_path, script)
        else:
            cmd = [python_exe_path, script]

        subprocess.Popen(cmd, shell=False)
        return 1

    def create_tool_widget(self, name, icon_path, script):
        """
        Create the tool widget button...
        """

        # Create push button
        button = QPushButton()
        button.setObjectName('ToolButton')
        button.pressed.connect(partial(self.button_execute, script))

        icon = QIcon()
        icon.addPixmap(QPixmap(icon_path))
        button.setIcon(icon)
        button.setIconSize(QSize(75, 75))

        # Create label - center frame
        tool_label = QLabel(name)
        tool_label.setMinimumHeight(25)
        tool_label.setAlignment(Qt.AlignCenter)
        tool_label.setObjectName('ToolLabel')

        # Creating layout
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(button)
        layout.addWidget(tool_label)

        tool_widget = QWidget()
        tool_widget.setMaximumWidth(175)
        tool_widget.setLayout(layout)

        return tool_widget

    def populate_tabs(self):
        """
        Populate the tab bars...
        """

        for tab_name in sorted(os.listdir(TOOL_DIR)):
            tab_title = tab_name.title()
            grid_layout = QGridLayout()
            grid_layout.setSpacing(5)
            grid_layout.setAlignment(Qt.AlignTop)

            scripts_dir = os.path.join(TOOL_DIR, tab_name)
            scripts_list = filter(lambda x: x.endswith('.py'), os.listdir(scripts_dir))

            for r, script_basename in enumerate(scripts_list):
                r, c = r / SPAN, r % SPAN

                strip_name = script_basename.strip('.py')
                name = strip_name.title().replace('_', ' ')
                full_script_path = os.path.join(scripts_dir, script_basename)

                expr = os.path.abspath(os.path.join(scripts_dir, strip_name + '*' + ICON_EXTENSION))
                icon_list = glob.glob(expr)

                try:
                    icon_path = icon_list[-1]
                except IndexError:
                    icon_path = './unknown.png'

                button = self.create_tool_widget(name, icon_path, full_script_path)
                grid_layout.addWidget(button, r, c)

            widget = QDialog()
            widget.setContentsMargins(0, 30, 0, 0)
            widget.setLayout(grid_layout)
            self.addTab(widget, tab_title)

        return 1


class MrWolfLayout(QWidget):
    def __init__(self):
        super(MrWolfLayout, self).__init__()
        self.master_layout()
        self.setStyleSheet(css.main_style)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('MainMenu')

        self.setFixedSize(600, 1000)

        try:
            x, y = mr_wolf_pref.load_pref()
            self.move(x, y)
        except (IOError, AttributeError):
            pass

    def create_title_layout(self):
        """
        Creating the title card top widget for tool launcher...
        """

        icon = QLabel()
        icon.setGeometry(10, 10, 50, 50)
        icon.setPixmap(QPixmap('./mrwolftools.png'))

        # Creating the minimize button and icon
        mini_button = QPushButton('-')
        mini_button.setObjectName('MinimizeButton')
        mini_button.pressed.connect(self.showMinimized)

        # Create the layout
        layout = QHBoxLayout()
        layout.addWidget(icon)
        layout.addWidget(mini_button)

        # Creating the widget and setting layout
        widget = QDialog()
        widget.setObjectName('HeaderMenu')
        widget.setLayout(layout)
        widget.setFixedHeight(100)

        return widget

    def create_bottom_widget(self):
        """
        Creating the bottom tool layout...
        """

        cancel = QPushButton('Cancel')
        cancel.setObjectName('CancelButton')
        cancel.pressed.connect(self.close)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)
        layout.addWidget(cancel)

        bottom_widget = QDialog()
        bottom_widget.setObjectName('BottomMenu')
        bottom_widget.setLayout(layout)
        bottom_widget.setFixedHeight(100)

        return bottom_widget

    def master_layout(self):
        """
        Combining the layout and widgets of the tool...
        """

        master_layout = QVBoxLayout(self)
        self.custom_tab = CustomTabWidget()

        master_layout.addWidget(self.create_title_layout())
        master_layout.addWidget(self.custom_tab)
        master_layout.addWidget(self.create_bottom_widget())

        return master_layout

    def mousePressEvent(self, event):
        """
        Find the mouse position and to move the main window...
        """

        self.old_pos = event.globalPos()

        return 1

    def mouseMoveEvent(self, event):
        """
        Moving the main window...
        """

        delta = QPoint(event.globalPos() - self.old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()

        return 1

    def closeEvent(self, event):
        """
        Save tab and tool position on close...
        """

        pos = self.pos().x(), self.pos().y()
        mr_wolf_pref.save_pref(pos)

        return 1


def run():
    app = QApplication(sys.argv)
    w = MrWolfLayout()
    w.show()
    sys.exit(app.exec_())

