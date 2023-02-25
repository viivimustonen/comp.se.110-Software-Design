"""
This class visualizes the data for the user.

It works as a view for the application.
It only has access to the controller.
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QToolBox, QTextBrowser
from PyQt5.QtGui import QPixmap
import json
import pathlib

from .graph import GraphWidget

class DataVisualization(QWidget):
    def __init__(self):
        super().__init__()


    def get_view(self, settings, view, data):
        """
        Returns the view based on open tab and selected settings
        :param settings: dict, settings from the side panel
        :param view: int, tab index representing one of the three tabs
        :param data: dict, data from the controller
        :return: QWidget, the view for the current tab
        """

        if view == 0:
            return self.get_current_view(settings, data)
        elif view == 1:
            return self.get_history_view(settings, data)
        else:
            return self.get_saved_view()


    def get_current_view(self, settings, data):
        """
        Returns the view for the current day
        :param settings: dict, settings from the side panel
        :param data: dict, data from the controller
        :return: QWidget, the view for the current tab
        """

        vBox = QtWidgets.QVBoxLayout(self)

        #If weather info box in gui is ticked, graph is created, same goes for rest of the data
        if settings['weatherInfo']:
            weatherGraph = GraphWidget(data["weatherData"])
            vBox.addWidget(weatherGraph)

        if settings['roadInfo']['roadCamera']:
            if data['roadCamera']:
                label = QLabel(self)
                path = pathlib.Path.cwd() / 'controller' / 'saves' / 'images' / 'weather_cam.jpg'
                pixmap = QPixmap(f"{path}")
                label.setPixmap(pixmap)
                vBox.addWidget(label)

        toolbox = QToolBox()
        toolbox.setMinimumHeight(400)
        toolbox.setMaximumWidth(900)

        if settings['roadInfo']['trafficMessages']:
            if len(data['trafficMessages'][settings["city"].upper()]['situationType']) > 0:
                content = data['trafficMessages']
                trafficMessageStr = json.dumps(content, indent=6)
                messageStr = trafficMessageStr.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace(',', '').replace('"', '') 
                messageLabel = QLabel(messageStr)   
            else:
                messageLabel = QLabel("None")

            toolbox.addItem(messageLabel, "TRAFFIC MESSAGES")

        if settings['roadInfo']['roadMaintenance']:
            if len(data['roadMaintenance'][settings["city"].upper()]['tasks']) > 0:
                content = data['roadMaintenance']
                maintenanceStr = json.dumps(content, indent=6)
                maintStr = maintenanceStr.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace(',', '').replace('"', '') 
                maintenanceLabel = QLabel(maintStr)
            else:
                maintenanceLabel = QLabel("None")

            toolbox.addItem(maintenanceLabel, "ROAD MAINTENANCE")

        if settings['roadInfo']['roadCondition']:
            if len(data['roadCondition'][settings["city"].upper()]) > 0:
                content = data['roadCondition']
                roadConditionStr = json.dumps(content, indent = 8)
                condStr = roadConditionStr.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace(',', '').replace('"', '')
                conditionLabel = QLabel(condStr)
            else:
                conditionLabel = QLabel(None)
            toolbox.addItem(conditionLabel, "ROAD CONDITION")

        vBox.addWidget(toolbox)
        contents = QtWidgets.QWidget()
        contents.setLayout(vBox)

        return contents

    def get_history_view(self, settings, data):
        """
        Returns the view for the history
        :param settings: dict, settings from the side panel
        :return: QWidget, the view for the current tab
        """
        vBox = QtWidgets.QVBoxLayout(self)

        if settings['weatherInfo']:
            weatherGraph = GraphWidget(data["weatherData"])
            vBox.addWidget(weatherGraph)

        if settings['roadInfo']['roadCamera']:
            if data['roadCamera']:
                label = QLabel(self)
                path = pathlib.Path.cwd() / 'controller' / 'saves' / \
                    'images' / 'weather_cam.jpg'
                pixmap = QPixmap(f"{path}")
                label.setPixmap(pixmap)
                vBox.addWidget(label)

        toolbox = QToolBox()
        toolbox.setMinimumHeight(400)
        toolbox.setMaximumWidth(900)

        if settings['roadInfo']['trafficMessages']:
            if len(data['trafficMessages'][settings["city"].upper()]['situationType']) > 0:
                content = data['trafficMessages']
                trafficMessageStr = json.dumps(content, indent=6)
                messageStr = trafficMessageStr.replace('(', '').replace(')', '').replace('[', '').replace(
                    ']', '').replace('{', '').replace('}', '').replace(',', '').replace('"', '')
                messageLabel = QLabel(messageStr)
            else:
                messageLabel = QLabel("None")

            toolbox.addItem(messageLabel, "TRAFFIC MESSAGES")

        if settings['roadInfo']['roadMaintenance']:
            if len(data['roadMaintenance'][settings["city"].upper()]['tasks']) > 0:
                content = data['roadMaintenance']
                maintenanceStr = json.dumps(content, indent=6)
                maintStr = maintenanceStr.replace('(', '').replace(')', '').replace('[', '').replace(
                    ']', '').replace('{', '').replace('}', '').replace(',', '').replace('"', '')
                maintenanceLabel = QLabel(maintStr)
            else:
                maintenanceLabel = QLabel("None")

            toolbox.addItem(maintenanceLabel, "ROAD MAINTENANCE")

        if settings['roadInfo']['roadCondition']:
            if len(data['roadCondition'][settings["city"].upper()]) > 0:
                content = data['roadCondition']
                roadConditionStr = json.dumps(content, indent=8)
                condStr = roadConditionStr.replace('(', '').replace(')', '').replace('[', '').replace(
                    ']', '').replace('{', '').replace('}', '').replace(',', '').replace('"', '')
                conditionLabel = QLabel(condStr)
            else:
                conditionLabel = QLabel(None)
            toolbox.addItem(conditionLabel, "ROAD CONDITION")

        vBox.addWidget(toolbox)
        contents = QtWidgets.QWidget()
        contents.setLayout(vBox)

        return contents
        
    def get_saved_view(self):
        """
        Returns the view for the saved data
        :return: QWidget, the view for the current tab
        """

        pass