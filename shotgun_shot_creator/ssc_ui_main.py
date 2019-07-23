from PySide.QtGui import *
from PySide.QtCore import *

from ssc_ui_layout import ShotCreatorLayout
import sys
import ssc_shotgun_data


class ShotCreatorMain(ShotCreatorLayout):
    def __init__(self):
        super(ShotCreatorMain, self).__init__()

        self.project_dict = ssc_shotgun_data.project_dict()
        self.populate_widgets()
        self.set_connection()

    def populate_widgets(self):
        """
        Add all data to the layout widgets...
        """

        # Adding the project name to the project field
        project_list = sorted([x[0] for x in self.project_dict.keys()])
        self.current_project.addItems(project_list)

        return 1

    def set_connection(self):
        """
        Setting up the tool connection...
        """

        self.current_project.currentIndexChanged.connect(self.project_action)

        return 1

    def project_action(self):
        """
        On item changed on the project combobox will trigger this
        action that will fill out the episode, if the project has no episode,
        it will be acted as a film...

        But if they want to add a new episode we need to find a way to create a new episode.
        """

        item = self.current_project.currentText()
        key = [x for x in self.project_dict if x[0] == item][0]
        episode_list = sorted(self.project_dict.get(key, list()), reverse=True)

        self.current_episode.clear()
        self.current_episode.addItems(list(episode_list))

        return 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ssc = ShotCreatorMain()
    ssc.show()
    sys.exit(app.exec_())