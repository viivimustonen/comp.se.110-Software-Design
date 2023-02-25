# Project readme

## Purpose
In this project, I design and implement a piece of software for monitoring how weather
affects road maintenance and condition. Weather has a direct impact on required maintenance and
road condition particularly during wintertime. The application will also allow for monitoring road
condition forecasts and weather separately. 

## Setup

This project is python based so python version 3.9 and corresponding version of pip must be installed.

All third party dependencies are located in requirements.txt and they can
be installed by running the command 

`python3 -m pip install -r requirements.txt`

In command line terminal in the root folder of the project.

## Startup

The program is started by running the file main_window.py. This can be done in an IDE or by running it in the command line.


First navigate to folder "project" by typing

`cd project/`

Next run the program by running

`python3 controller/main_window.py`

in the terminal.

If you are instead using an IDE to run the main_window.py file make sure to configure the entire git repository as the project. Otherwise the path variables won't work properly.

## Usage

In the main window of the program you can look up data by selecting the city, selecting the data to be shown and pressing the search selected data -button.

Configurations can be saved by pressing "Save as favourite" -button on the left. This will save a json file into the saves folder found within the project.

The history tab in the top row allows you to select a single day for measured weather data. If you attempt to get data for multiple days the application will crash. It was intended to be adjustable but we didn't have time to implement it properly.

The compare tab was meant to allow you to select two saved JSON objects and compare data stored within them. Due to time limitations we didn't have time to implement this properly so it won't work.

To close the program, hit the x-button on the top right or find a bug that adequately crashes the application.