from PySide.QtGui import *
from PySide.QtCore import *

import ssc_ui_css as css
import sys


class TitleWidget(QDialog):
    """
    Creating the tool title Widget...
    """
    def __init__(self):
        super(TitleWidget, self).__init__()
        icon = QLabel()
        icon.setGeometry(10, 10, 50, 50)
        icon.setPixmap(QPixmap('./mrwolfnew.png'))

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        layout.addWidget(icon)

        self.setFixedHeight(100)
        self.setObjectName('Title')
        self.setLayout(layout)


class DropWidget(QWidget):
    """
    Creating the drop down Widget...
    """
    def __init__(self):
        super(DropWidget, self).__init__()
        self.setAcceptDrops(True)
        self.setObjectName('DragDrop')

        self.setStyleSheet(css.style_sheet)
        self.setLayout(self.master_layout())

    def create_table_widget(self):
        """

        """
        self.table_widget = QTableWidget()

        self.table_widget.setRowCount(50)
        self.table_widget.setColumnCount(12)

        self.table_widget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().hide()

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        return self.table_widget

    def create_drop_widget(self):
        """

        """

        self.drag_drop_button = QPushButton('Drag n drop or select a file!')
        self.drag_drop_button.setObjectName('DropButton')
        self.drag_drop_button.setFixedWidth(200)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.drag_drop_button)

        self.drag_drop = QPushButton()
        self.drag_drop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.drag_drop.setObjectName('DragDrop')
        self.drag_drop.setLayout(layout)

        return self.drag_drop

    def master_layout(self):
        """
        Adding the table and drop window to the master layout...
        """

        master_layout = QVBoxLayout()

        master_layout.addWidget(self.create_table_widget())
        master_layout.addWidget(self.create_drop_widget())

        self.table_widget.hide()

        return master_layout

    def reset_drop_widget(self):
        """
        Reset the drag and drop widget to the default state and remove any table
        data...
        """

        self.drag_drop.show()
        self.table_widget.hide()

        return 1

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()

        self.table_widget.show()
        self.drag_drop.hide()

    def keyPressEvent(self, event):
        table_data = QClipboard().text()

        if not event.matches(QKeySequence.Paste) or not table_data:
            return 0

        self.table_widget.show()
        self.drag_drop.hide()

        return 1


class ShotCreatorLayout(QMainWindow):
    def __init__(self):
        super(ShotCreatorLayout, self).__init__()

        self.resize(1600, 1000)
        self.setObjectName('Main')

        self.widget = QWidget()
        self.master_layout()
        self.setCentralWidget(self.widget)
        self.setStyleSheet(css.style_sheet)

        m = [-15]*4
        self.setContentsMargins(*m)

    def create_project_spec_layout(self):
        """
        Creating a groupbox displaying all the valid fields required
        to create a nuke base script...
        """

        self.show_code = QLineEdit()
        self.fps = QLineEdit()
        self.fps.setValidator(QDoubleValidator())
        self.handles = QLineEdit()
        self.handles.setValidator(QIntValidator())
        self.colorspace = QComboBox()
        self.start_frame = QLineEdit()
        self.start_frame.setValidator(QIntValidator())
        self.slate = QRadioButton()

        # Editorial details
        self.editorial_format = QComboBox()

        self.editorial_height = QLineEdit()
        self.editorial_height.setAlignment(Qt.AlignCenter)
        self.editorial_height.setPlaceholderText('Height')
        self.editorial_height.setValidator(QIntValidator())

        self.editorial_width = QLineEdit()
        self.editorial_width.setAlignment(Qt.AlignCenter)
        self.editorial_width.setPlaceholderText('Width')
        self.editorial_width.setValidator(QIntValidator())

        editorial_layout = QHBoxLayout()
        editorial_layout.addWidget(QLabel('H:'))
        editorial_layout.addWidget(self.editorial_height)
        editorial_layout.addWidget(QLabel('W:'))
        editorial_layout.addWidget(self.editorial_width)

        # Final details
        self.final_format = QComboBox()

        self.final_height = QLineEdit()
        self.final_height.setAlignment(Qt.AlignCenter)
        self.final_height.setPlaceholderText('Height')
        self.final_height.setValidator(QIntValidator())

        self.final_width = QLineEdit()
        self.final_width.setAlignment(Qt.AlignCenter)
        self.final_width.setPlaceholderText('Width')
        self.final_width.setValidator(QIntValidator())

        final_layout = QHBoxLayout()
        final_layout.addWidget(QLabel('H:'))
        final_layout.addWidget(self.final_height)
        final_layout.addWidget(QLabel('W:'))
        final_layout.addWidget(self.final_width)

        self.final_bit_depth = QComboBox()

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(QLabel('Show Code:'), 0, 0), layout.addWidget(self.show_code, 0, 1)
        layout.addWidget(QLabel('FPS:'), 1, 0), layout.addWidget(self.fps, 1, 1)
        layout.addWidget(QLabel('Handle:'), 2, 0), layout.addWidget(self.handles, 2, 1)
        layout.addWidget(QLabel('Color-space:'), 3, 0), layout.addWidget(self.colorspace)
        layout.addWidget(QLabel('Slate:'), 4, 0), layout.addWidget(self.slate, 4, 1)

        layout.addWidget(QLabel(''), 5, 0, 1, 2)
        layout.addWidget(QLabel('Editorial Format:')), layout.addWidget(self.editorial_format)
        layout.addLayout(editorial_layout, 7, 1)
        layout.addWidget(QLabel('Final Format:')), layout.addWidget(self.final_format)
        layout.addLayout(final_layout, 9, 1)
        layout.addWidget(QLabel('Final Bit Depth:'), 10, 0), layout.addWidget(self.final_bit_depth)

        m = 28
        layout.setContentsMargins(m, m, m, m)

        group_box = QGroupBox('Project Specs')
        group_box.setLayout(layout)
        group_box.setCheckable(True)

        return group_box

    def create_new_project_layout(self):
        """
        Display layout for a new shotgun project...
        """

        self.new_project_name = QLineEdit()
        self.project_folder_name = QLineEdit()
        self.project_type = QComboBox()

        layout = QGridLayout()

        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(QLabel('Project Name:'), 0, 0, alignment=Qt.AlignRight)
        layout.addWidget(QLabel('Folder Name:'), 1, 0, alignment=Qt.AlignRight)
        layout.addWidget(QLabel('Project Type:'), 2, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.new_project_name, 0, 1, )
        layout.addWidget(self.project_folder_name, 1, 1, )
        layout.addWidget(self.project_type, 2, 1, )
        layout.addWidget(QLabel('\n'))
        layout.addWidget(self.create_project_spec_layout(), 4, 0, 1, 2)

        m = 28
        layout.setContentsMargins(m, m*1.5, m, m)

        widget = QDialog()
        widget.setObjectName('Project')
        widget.setFixedWidth(400)
        widget.setLayout(layout)

        return widget

    def create_project_layout(self):
        """
        Creating the project spec layout, which will query shotgun
        and populate the combobox.

        If you would like to create a new project it will allow you
        update the project specs to assist in nuke shot creation.
        """

        project_label = QLabel('Project:')
        project_label.setMaximumWidth(50)

        self.current_project = QComboBox()
        self.current_episode = QComboBox()

        layout = QGridLayout()

        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(project_label, alignment=Qt.AlignRight), layout.addWidget(self.current_project, 0, 1)
        layout.addWidget(QLabel('Episode:'), alignment=Qt.AlignRight), layout.addWidget(self.current_episode)

        m = 28
        layout.setContentsMargins(m, m*1.5, m, m)

        project_widget = QWidget()
        project_widget.setLayout(layout)

        return project_widget

    def create_button_layout(self):
        """
        Creating the foot layout with create and cancel button...
        """

        self.create_shot_button = QPushButton('Create')

        reset = QPushButton('Reset')
        reset.pressed.connect(self.drop_widget.reset_drop_widget)

        cancel = QPushButton('Cancel')
        cancel.pressed.connect(self.close)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)
        layout.addWidget(self.create_shot_button)
        layout.addWidget(reset)
        layout.addWidget(cancel)

        widget = QDialog()
        widget.setObjectName('Footer')
        widget.setFixedHeight(100)
        widget.setLayout(layout)
        widget.setContentsMargins(0, 0, 25, 0)

        return widget

    def master_layout(self):
        """
        Creating the splitter widget appending table widget
        and project spec option. Combine all the widget and layouts...
        """

        tab_widget = QTabWidget()
        tab_widget.setFixedWidth(400)
        tab_widget.addTab(self.create_project_layout(), 'Current Project')
        tab_widget.addTab(self.create_new_project_layout(), 'Create New Project')

        splitter = QSplitter()

        self.drop_widget = DropWidget()
        splitter.addWidget(self.drop_widget)
        splitter.addWidget(tab_widget)

        master_layout = QVBoxLayout(self.widget)
        master_layout.addWidget(TitleWidget())
        master_layout.addWidget(splitter)
        master_layout.addWidget(self.create_button_layout())

        return master_layout


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ssc = ShotCreatorLayout()
    ssc.show()
    sys.exit(app.exec_())
