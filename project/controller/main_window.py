"""
This class is the main window of the application.

It works as a controller for the application.
It's responsible for the communication between the view and the model.
It's the only class that has access to the model and the view.

"""
import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from components.side_panel import SidePanel
from components.view_panel import ViewPanel

from view.data_visualization import *
from view.graph import *
from model.apirequests import*


class UiMainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.folder = pathlib.Path.cwd()
        self.side_panel_object = None
        self.view_panel_object = None

        self.setup_ui()


    def setup_ui(self):
        """
        Sets up the main window
        :return:
        """

        hBox = QtWidgets.QHBoxLayout()
        hBox.setContentsMargins(0, 1, 0, 0)
        hBox.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.side_panel_object = SidePanel()
        side_panel_widget = self.side_panel_object.get_side_panel()
        hBox.addWidget(side_panel_widget)

        self.side_panel_object.search_push_button.clicked.connect(self.search_with_selected_data)
        self.side_panel_object.save_timeline_push_button.clicked.connect(self.save_timeline)
        self.side_panel_object.load_timeline_push_button_1.clicked.connect(self.display_timeline_left)
        self.side_panel_object.load_timeline_push_button_2.clicked.connect(self.display_timeline_right)

        self.view_panel_object = ViewPanel()
        self.view_panel_widget = self.view_panel_object.view_panel
        self.view_panel_widget.currentChanged.connect(self.change_tab)
        hBox.addWidget(self.view_panel_widget)

        frame = QtWidgets.QFrame()
        frame.setLayout(hBox)
        self.setCentralWidget(frame)

        self.setGeometry(0, 0, 1600, 900)
        self.setMinimumSize(QtCore.QSize(1600, 900))
        self.setWindowTitle("Road Watch")


    def change_tab(self):
        """
        Connects tab change in view panel to side panel
        :return: None
        """

        self.side_panel_object.set_tab_index(self.view_panel_widget.currentIndex())


    def search_with_selected_data(self):
        """
        Connects search button in side panel to view panel
        :return: None
        """

        # controller kutsuu modelia eli apirequestia parametreilla ja saa takaisin dataa
        # sen jälkeen controller kutsuu data visualizationia eli viewiä saadulla datalla ja saa takaisin kuvaajia
        # sitten controller näyttää datan.

        # VIEW JA MODEL EIVÄT SAA KOSKAAN KOMMUNIKOIDA SUORAAN KESKENÄÄN


        settings = self.side_panel_object.get_current_settings()
        data = {}

        if settings["startDate"] != None:
            #OBSERVED DATA
            data['weatherData'] = weather_daily_measurements(settings["city"].upper(), datetime.strptime(settings["startDate"],'%Y-%m-%d'),
                                                             datetime.strptime(settings["endDate"],'%Y-%m-%d'))
            data['roadMaintenance'], data['trafficMessages'], data['roadCondition'] = road_data(
                settings["city"].upper(), datetime.strptime(settings["startDate"], '%Y-%m-%d'), datetime.strptime(settings["endDate"], '%Y-%m-%d'))
        else:
            #WEATHER FORECAST
            data['weatherData'] = weather_forecast(settings["city"].upper())
            data['roadMaintenance'], data['trafficMessages'], data['roadCondition'] = road_data(settings["city"].upper())

        data['roadCamera'] = weather_cameras(settings["city"].upper())

        visualization = DataVisualization()
        tabContentWidget = visualization.get_view(settings, self.view_panel_widget.currentIndex(), data)
        
        if settings["startDate"] != None:
            self.view_panel_object.set_history_tab_content(tabContentWidget)
            
        else:
            self.view_panel_object.set_today_tab_content(tabContentWidget)



    def save_timeline(self):
        """
        Saves the timeline in json format
        :return:
        """


        settings = self.side_panel_object.get_current_settings()
        # Save data of all the graphs and plots, messages, etc. with the settings

        data = {
            "settings": settings,
            "data": None,
        }

        title = settings["city"] + " " + settings["startDate"] + " - " + settings["endDate"]
        file_name = f"{title}.json"
        path = self.folder / 'controller' / 'saves' / 'timelines' / file_name
        f = open(path, "w")
        f.write(json.dumps(data, indent=4))
        f.close()


    def load_timeline(self):
        """
        Loads timeline in json format
        :return:
        """

        path = self.folder / 'controller' / 'saves' / 'timelines'
        response = QFileDialog.getOpenFileName(
            caption='Select saved timeline',
            directory=str(path),
            filter='JSON files (*.json)',
            initialFilter='JSON files (*.json)'
        )
        if response and response[0] != '':
            f = open(response[0], "r")
            data = json.load(f)
            f.close()

    def display_timeline_left(self):
        """
        Loads the timeline in json format and requests visualization from the view
        Displays the timeline in the left compare tab
        :return: None
        """

        timeline = self.load_timeline()
        # Display data


    def display_timeline_right(self):
        """
        Loads the timeline in json format and requests visualization from the view
        Displays the timeline in the right compare tab
        :return: None
        """

        timeline = self.load_timeline()
        # Display data



def main():
    app = QApplication(sys.argv)
    window = UiMainWindow()
    window.show()
    app.exec_()

    # delete road camera image
    try:
        os.remove(pathlib.Path.cwd() / 'controller' / 'saves' / 'images' / 'weather_cam.jpg')
    except:
        pass

if __name__ == "__main__":
    main()
