"""
This class implements the side panel component of the main_window.

Side panel has multiple selections that are only displayed at the corresponding tab.

User can select location, data types to show and timeline.
Settings can be saved as favourite and those favourites can be easily selected from the favourite views combo box.
Timelines can be saved and the saved files loaded back to the program in order to compare different timelines side by side.

"""

import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import json


class SidePanel(QWidget):

    def __init__(self):
        super(SidePanel, self).__init__()

        self.folder = pathlib.Path.cwd()
        self.tab_index = 0

        self.city_selection_widget = QtWidgets.QWidget()
        self.data_selection_widget = QtWidgets.QWidget()
        self.favourite_selection_widget = QtWidgets.QWidget()
        self.timeline_selection_widget = QtWidgets.QWidget()
        self.save_timeline_widget = QtWidgets.QWidget()
        self.search_data_widget = QtWidgets.QWidget()
        self.load_timeline_widget = QtWidgets.QWidget()

        self.handle_side_panel_items_visibility()


    def set_tab_index(self, index):
        """
        Sets the tab index and changes the side panel view accordingly
        :param index: int, index of the current tab
        :return:
        """

        self.tab_index = index
        self.handle_side_panel_items_visibility()


    def get_side_panel(self):
        """
        Lays out the side panel
        :return:
        """

        side_panel = QtWidgets.QWidget(self)
        side_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        side_panel.setGeometry(QtCore.QRect(0, 0, 300, 900))
        side_panel.setMinimumWidth(300)
        side_panel.setMaximumWidth(300)
        side_panel.setMinimumHeight(900)
        side_panel_items = QtWidgets.QWidget(side_panel)
        side_panel_items.setGeometry(QtCore.QRect(0, 0, 300, 900))
        side_panel_items_layout = QtWidgets.QVBoxLayout(side_panel_items)
        side_panel_items_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        side_panel_items_layout.setContentsMargins(18, 6, 18, 0)

        application_title_label = QtWidgets.QLabel("Road Watch")
        font = QtGui.QFont()
        font.setPointSize(20)
        application_title_label.setFont(font)
        application_title_label.setContentsMargins(6, 0, 6, 0)
        side_panel_items_layout.addWidget(application_title_label)

        city_selection_layout = QtWidgets.QVBoxLayout()
        city_label = QtWidgets.QLabel("Select city")
        city_label.setContentsMargins(0, 0, 0, 6)
        font = QtGui.QFont()
        font.setPointSize(14)
        city_label.setFont(font)
        city_selection_layout.addWidget(city_label)
        self.city_selection_combo_box = QtWidgets.QComboBox()
        self.city_selection_combo_box.addItems(["Tampere", "Helsinki", "Oulu", "Turku", "Lappeenranta"])
        self.city_selection_combo_box.currentIndexChanged.connect(self.city_selection_combo_box_changed)
        city_selection_layout.addWidget(self.city_selection_combo_box)

        self.city_selection_widget.setLayout(city_selection_layout)
        side_panel_items_layout.addWidget(self.city_selection_widget)

        data_selection_layout = QtWidgets.QVBoxLayout()
        data_selection_label = QtWidgets.QLabel("Select data")
        data_selection_label.setFont(font)
        data_selection_label.setContentsMargins(0, 0, 0, 6)
        data_selection_layout.addWidget(data_selection_label)
        self.weather_info_checkbox = QtWidgets.QCheckBox("Weather info")
        self.weather_info_checkbox.stateChanged.connect(self.weather_info_checkbox_changed)
        data_selection_layout.addWidget(self.weather_info_checkbox)
        self.road_info_checkbox = QtWidgets.QCheckBox("Road info")
        self.road_info_checkbox.stateChanged.connect(self.select_all_sub_selections)
        data_selection_layout.addWidget(self.road_info_checkbox)
        road_info_sub_selection_layout = QtWidgets.QVBoxLayout()
        road_info_sub_selection_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        road_info_sub_selection_layout.setContentsMargins(18, 0, 0, 0)
        road_info_sub_selection_layout.setSpacing(5)
        self.road_camera_checkbox = QtWidgets.QCheckBox("Road camera")
        self.road_camera_checkbox.stateChanged.connect(self.change_sub_selection_state)
        road_info_sub_selection_layout.addWidget(self.road_camera_checkbox)
        self.traffic_messages_checkbox = QtWidgets.QCheckBox("Traffic messages")
        self.traffic_messages_checkbox.stateChanged.connect(self.change_sub_selection_state)
        road_info_sub_selection_layout.addWidget(self.traffic_messages_checkbox)
        self.road_maintenance_checkbox = QtWidgets.QCheckBox("Road maintenance")
        self.road_maintenance_checkbox.stateChanged.connect(self.change_sub_selection_state)
        road_info_sub_selection_layout.addWidget(self.road_maintenance_checkbox)
        self.road_condition_checkbox = QtWidgets.QCheckBox("Road condition")
        self.road_condition_checkbox.stateChanged.connect(self.change_sub_selection_state)
        road_info_sub_selection_layout.addWidget(self.road_condition_checkbox)
        self.road_info_sub_selection_checkboxes = [self.road_camera_checkbox, self.traffic_messages_checkbox,
                                                   self.road_maintenance_checkbox, self.road_condition_checkbox]
        data_selection_layout.addLayout(road_info_sub_selection_layout)
        self.data_selection_widget.setLayout(data_selection_layout)
        side_panel_items_layout.addWidget(self.data_selection_widget)

        favourite_selection_layout = QtWidgets.QVBoxLayout()
        save_favourite_layout = QtWidgets.QHBoxLayout()
        save_favourite_layout.setContentsMargins(0, 0, 0, 24)
        save_favourite_layout.setSpacing(18)
        save_favourite_label = QtWidgets.QLabel("Save as favourite")
        save_favourite_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        save_favourite_layout.addWidget(save_favourite_label)
        self.save_favourite_push_button = QtWidgets.QPushButton("Save")
        self.save_favourite_push_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.save_favourite_push_button.clicked.connect(self.set_favourite_settings)
        save_favourite_layout.addWidget(self.save_favourite_push_button)
        save_favourite = QtWidgets.QWidget()
        save_favourite.setLayout(save_favourite_layout)
        favourite_selection_layout.addWidget(save_favourite)
        favourite_label = QtWidgets.QLabel("Favourite views")
        favourite_label.setContentsMargins(0, 0, 0, 6)
        favourite_label.setFont(font)
        favourite_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        favourite_selection_layout.addWidget(favourite_label)
        self.favourite_selection_combo_box = QtWidgets.QComboBox()
        self.favourite_selection_combo_box.setCurrentText("Select view")
        self.initialize_favourite_selection_combo_box()  # Adds saved favourites to the combo box
        self.favourite_selection_combo_box.currentIndexChanged.connect(self.load_favourite_settings)
        favourite_selection_layout.addWidget(self.favourite_selection_combo_box)
        self.favourite_selection_widget.setLayout(favourite_selection_layout)
        side_panel_items_layout.addWidget(self.favourite_selection_widget)

        timeline_selection_layout = QtWidgets.QVBoxLayout()
        timeline_label = QtWidgets.QLabel("Select timeline")
        timeline_label.setFont(font)
        timeline_selection_layout.addWidget(timeline_label)

        date_selections_layout = QtWidgets.QHBoxLayout()
        date_selections_layout.setSpacing(8)

        start_date_selection_layout = QtWidgets.QVBoxLayout()
        start_date_label = QtWidgets.QLabel("Start date")
        start_date_selection_layout.addWidget(start_date_label)
        self.start_date_edit = QtWidgets.QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        date = QtCore.QDate.currentDate()
        self.start_date_edit.setDate(date)
        self.start_date_edit.setMaximumDate(date)
        self.start_date_edit.dateChanged.connect(self.set_max_min_dates)
        start_date_selection_layout.addWidget(self.start_date_edit)
        date_selections_layout.addLayout(start_date_selection_layout)

        end_date_selection_layout = QtWidgets.QVBoxLayout()
        end_date_label = QtWidgets.QLabel("End date")
        end_date_selection_layout.addWidget(end_date_label)
        self.end_date_edit = QtWidgets.QDateEdit(side_panel_items)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(date)
        self.end_date_edit.setMinimumDate(date)
        self.end_date_edit.setMaximumDate(date)
        self.end_date_edit.dateChanged.connect(self.set_max_min_dates)
        end_date_selection_layout.addWidget(self.end_date_edit)

        date_selections_layout.addLayout(end_date_selection_layout)
        timeline_selection_layout.addLayout(date_selections_layout)

        self.timeline_selection_widget.setLayout(timeline_selection_layout)
        side_panel_items_layout.addWidget(self.timeline_selection_widget)

        save_timeline_layout = QtWidgets.QHBoxLayout()
        save_timeline_layout.setSpacing(18)
        save_timeline_label = QtWidgets.QLabel("Save timeline")
        save_timeline_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        save_timeline_layout.addWidget(save_timeline_label)
        self.save_timeline_push_button = QtWidgets.QPushButton("Save")
        self.save_timeline_push_button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        save_timeline_layout.addWidget(self.save_timeline_push_button)
        self.save_timeline_widget.setLayout(save_timeline_layout)
        side_panel_items_layout.addWidget(self.save_timeline_widget)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(18)
        search_label = QtWidgets.QLabel("Search selected data")
        search_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        search_layout.addWidget(search_label)
        self.search_push_button = QtWidgets.QPushButton("Search")
        self.search_push_button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        search_layout.addWidget(self.search_push_button)
        self.search_data_widget.setLayout(search_layout)
        side_panel_items_layout.addWidget(self.search_data_widget)

        load_timeline_layout = QtWidgets.QVBoxLayout()
        load_button_layout_1 = QtWidgets.QHBoxLayout()
        load_button_layout_1.setSpacing(18)
        select_timeline_label_1 = QtWidgets.QLabel("Load timeline")
        select_timeline_label_1.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        load_button_layout_1.addWidget(select_timeline_label_1)
        self.load_timeline_push_button_1 = QtWidgets.QPushButton("Load")
        self.load_timeline_push_button_1.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        load_button_layout_1.addWidget(self.load_timeline_push_button_1)
        load_timeline_layout.addLayout(load_button_layout_1)
        load_button_layout_2 = QtWidgets.QHBoxLayout()
        load_button_layout_2.setSpacing(18)
        select_timeline_label_2 = QtWidgets.QLabel("Load timeline")
        select_timeline_label_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        load_button_layout_2.addWidget(select_timeline_label_2)
        self.load_timeline_push_button_2 = QtWidgets.QPushButton("Load")
        self.load_timeline_push_button_2.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        load_button_layout_2.addWidget(self.load_timeline_push_button_2)
        load_timeline_layout.addLayout(load_button_layout_2)
        self.load_timeline_widget.setLayout(load_timeline_layout)
        side_panel_items_layout.addWidget(self.load_timeline_widget)

        spacerItem = QtWidgets.QSpacerItem(300, 200, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        side_panel_items_layout.addItem(spacerItem)

        return side_panel


    def clear_all_info_selections(self):
        """
        Clears all checkboxes
        :return:
        """

        self.weather_info_checkbox.setChecked(not QtCore.Qt.Checked)
        self.road_info_checkbox.setChecked(not QtCore.Qt.Checked)


    def city_selection_combo_box_changed(self):
        """
        Resets the favourite selection combo box when city selection combo box changes
        :return:
        """

        self.favourite_selection_combo_box.setCurrentIndex(0)


    def weather_info_checkbox_changed(self):
        """
        Resets the favourite selection combo box when weather info checkbox changes
        :return:
        """

        self.favourite_selection_combo_box.setCurrentIndex(0)


    def select_all_sub_selections(self):
        """
        Changes all sub selection checkbox checks for road info when the road info checkbox is clicked
        :return:
        """

        if self.road_info_checkbox.checkState() == QtCore.Qt.PartiallyChecked:
            self.road_info_checkbox.blockSignals(True)
            self.road_info_checkbox.setCheckState(QtCore.Qt.Checked)
            self.road_info_checkbox.blockSignals(False)

        for checkbox in self.road_info_sub_selection_checkboxes:
            if checkbox.isChecked() != self.road_info_checkbox.isChecked():
                checkbox.blockSignals(True)
                checkbox.setChecked(not checkbox.isChecked())
                checkbox.blockSignals(False)


    def change_sub_selection_state(self):
        """
        Handles the road info checkbox status based on sub selections checked
        :return:
        """

        self.favourite_selection_combo_box.setCurrentIndex(0)

        sub_selections_checked = len(list(filter(lambda cb: cb.isChecked(), self.road_info_sub_selection_checkboxes)))
        if sub_selections_checked == 0:
            self.road_info_checkbox.blockSignals(True)
            self.road_info_checkbox.setCheckState(not QtCore.Qt.Checked)
            self.road_info_checkbox.blockSignals(False)
        elif 0 < sub_selections_checked < 4:
            self.road_info_checkbox.blockSignals(True)
            self.road_info_checkbox.setCheckState(QtCore.Qt.PartiallyChecked)
            self.road_info_checkbox.blockSignals(False)
        else:
            self.road_info_checkbox.blockSignals(True)
            self.road_info_checkbox.setCheckState(QtCore.Qt.Checked)
            self.road_info_checkbox.blockSignals(False)


    def set_max_min_dates(self):
        """
        Sets min and max dates for the timeline selection to prevent odd timelines
        :return:
        """

        min_end_date = self.start_date_edit.date()
        self.end_date_edit.setMinimumDate(min_end_date)

        max_start_date = self.end_date_edit.date()
        self.start_date_edit.setMaximumDate(max_start_date)


    def handle_side_panel_items_visibility(self):
        """
        Changes side panel view based on the tab currently open
        :return:
        """

        if self.tab_index == 0:
            self.city_selection_widget.show()
            self.data_selection_widget.show()
            self.favourite_selection_widget.show()
            self.search_data_widget.show()
            self.timeline_selection_widget.hide()
            self.save_timeline_widget.hide()
            self.load_timeline_widget.hide()
        elif self.tab_index == 1:
            self.city_selection_widget.show()
            self.data_selection_widget.show()
            self.favourite_selection_widget.hide()
            self.search_data_widget.show()
            self.timeline_selection_widget.show()
            self.save_timeline_widget.show()
            self.load_timeline_widget.hide()
        elif self.tab_index == 2:
            self.city_selection_widget.hide()
            self.data_selection_widget.hide()
            self.favourite_selection_widget.hide()
            self.search_data_widget.hide()
            self.timeline_selection_widget.hide()
            self.save_timeline_widget.hide()
            self.load_timeline_widget.show()


    def get_current_settings(self):
        """
        Collects current side panel settings and returns them
        :return: dict, side panel settings
        """

        return {
            "city": self.city_selection_combo_box.currentText(),
            "weatherInfo": self.weather_info_checkbox.isChecked(),
            "roadInfo": {
                "roadCamera": self.road_camera_checkbox.isChecked(),
                "trafficMessages": self.traffic_messages_checkbox.isChecked(),
                "roadMaintenance": self.road_maintenance_checkbox.isChecked(),
                "roadCondition": self.road_condition_checkbox.isChecked(),
            },
            "startDate": (self.start_date_edit.date().toString(
                QtCore.Qt.ISODate) if self.tab_index == 1 else None),
            "endDate": (
                self.end_date_edit.date().toString(QtCore.Qt.ISODate) if self.tab_index == 1 else None),
        }


    def set_favourite_settings(self):
        """
        Saves settings as favourite in json format
        :return:
        """

        selection = self.get_current_settings()

        key = selection['city']
        path = self.folder / 'controller' / 'saves' / 'selections' / 'settings.json'
        f = open(path, "r")
        settings = json.load(f)
        f.close()

        settings[key] = selection
        f = open(path, "w")
        json.dump(settings, f, indent=4)
        f.close()

        for i in range(self.favourite_selection_combo_box.count()):
            if self.favourite_selection_combo_box.itemText(i) == key:
                self.favourite_selection_combo_box.setCurrentIndex(i)
                return
        self.favourite_selection_combo_box.addItem(key)
        self.favourite_selection_combo_box.setCurrentText(key)


    def load_favourite_settings(self):
        """
        Loads favourite settings
        :return:
        """

        path = self.folder / 'controller' / 'saves' / 'selections' / 'settings.json'
        f = open(path, "r")
        settings = json.load(f)
        f.close()
        key = self.favourite_selection_combo_box.currentText()
        if key == "Select view":
            return

        self.city_selection_combo_box.setCurrentText(key)
        self.weather_info_checkbox.setChecked(settings[key]["weatherInfo"])
        self.road_camera_checkbox.setChecked(settings[key]["roadInfo"]["roadCamera"])
        self.traffic_messages_checkbox.setChecked(settings[key]["roadInfo"]["trafficMessages"])
        self.road_maintenance_checkbox.setChecked(settings[key]["roadInfo"]["roadMaintenance"])
        self.road_condition_checkbox.setChecked(settings[key]["roadInfo"]["roadCondition"])

        self.favourite_selection_combo_box.setCurrentText(key)



    def initialize_favourite_selection_combo_box(self):
        """
        Sets up values for favourite selection combo box when the component is created
        :return:
        """

        path = self.folder / 'controller' / 'saves' / 'selections' / 'settings.json'
        f = open(path, "r")
        settings = json.load(f)
        f.close()
        for key in settings.keys():
            self.favourite_selection_combo_box.addItem(key)

