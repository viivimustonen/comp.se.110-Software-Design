"""
This class implements the view panel component of the main_window.

It is responsible for the display of the tabs in the main window.
The view panel displays graphs and plots of the data, messages and images.

There are three tabs: Today, History and Compare.

Today:
    Displays the timeline of the current day.
    Display consist of the weather forecast and the weather and road data of the current day.

History:
    Displays the timeline between selected days.
    Display consist of the weather and road data between selected days.

Compare:
    Displays two different saved timelines between selected days that have been loaded to the application.
    Display consist of the weather and road data between selected days.

"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget


class ViewPanel(QWidget):

    def __init__(self,):
        super(ViewPanel, self).__init__()

        self.view_panel = QtWidgets.QTabWidget()

        self.today_tab = QtWidgets.QWidget()
        self.today_tab_scroll_area = QtWidgets.QScrollArea()

        self.history_tab_scroll_area = QtWidgets.QScrollArea()

        self.compare_tab_scroll_area = QtWidgets.QScrollArea()
        self.compare_tab_content_left = QtWidgets.QWidget()
        self.compare_tab_content_right = QtWidgets.QWidget()

        self.setup_view_panel()


    def set_today_tab_content(self, visualizations):
        """
        Sets content to today tab.
        :param visualizations: QWidget, visualizations of the data
        :return:
        """

        self.today_tab_scroll_area.setWidget(visualizations)


    def setup_today_tab(self):
        """
        Sets up the today tab.
        :return: QWidget, today tab
        """

        self.today_tab_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.today_tab_scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 900))
        self.today_tab_scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.today_tab_scroll_area.setWidgetResizable(True)

        scroll_area_layout = QtWidgets.QHBoxLayout()
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area_layout.addWidget(self.today_tab_scroll_area)
        self.today_tab.setLayout(scroll_area_layout)

        return self.today_tab


    def set_history_tab_content(self, visualizations):
        """
        Sets content to history tab.
        :param visualizations: QWidget, visualizations of the data
        :return:
        """

        self.history_tab_scroll_area.setWidget(visualizations)


    def setup_history_tab(self):
        """
        Sets up the history tab.
        :return: QWidget, history tab
        """

        self.history_tab_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.history_tab_scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 900))
        self.history_tab_scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.history_tab_scroll_area.setWidgetResizable(True)

        scroll_area_layout = QtWidgets.QHBoxLayout()
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area_layout.addWidget(self.history_tab_scroll_area)
        self.history_tab = QtWidgets.QWidget()
        self.history_tab.setLayout(scroll_area_layout)

        return self.history_tab


    def set_compare_tab_content(self, visualizations, side):
        """
        Sets content to compare tab.
        :param visualizations: QWidget, visualizations of the data
        :param side: str, left or right side of the compare tab
        :return:
        """

        if side == "left":
            self.compare_tab_content_left = visualizations

        elif side == "right":
            self.compare_tab_content_right = visualizations

        compare_layout = QtWidgets.QHBoxLayout()
        compare_layout.addWidget(self.compare_tab_content_left)
        compare_layout.addWidget(self.compare_tab_content_right)

        content = QtWidgets.QWidget()
        content.setLayout(compare_layout)

        self.compare_tab_scroll_area.setWidget(content)


    def setup_compare_tab(self):
        """
        Sets up the compare tab.
        :return: QWidget, compare tab
        """

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setGeometry(QtCore.QRect(0, 0, 1300, 900))
        scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        scroll_area_layout = QtWidgets.QHBoxLayout()
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area_layout.addWidget(scroll_area)
        self.compare_tab = QtWidgets.QWidget()
        self.compare_tab.setLayout(scroll_area_layout)

        return self.compare_tab


    def setup_view_panel(self):
        """
        Sets up the view panel.
        :return: QWidget, view panel
        """

        self.view_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.view_panel.addTab(self.setup_today_tab(), "Today")
        self.view_panel.addTab(self.setup_history_tab(), "History")
        self.view_panel.addTab(self.setup_compare_tab(), "Compare")
        self.view_panel.setCurrentIndex(0)


    def get_view_panel(self):
        """
        Creates the view panel.
        :return: QTabWidget, view panel
        """

        return self.view_panel