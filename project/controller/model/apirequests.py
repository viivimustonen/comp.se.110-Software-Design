"""
This file fetches data from digitraffic and the fmi

It works as a model for the application.

For data, a start and end time are required.

For a forecast, the end time of the forecast is required.

Requests are parsed into python dict containers and returned.
"""

from datetime import datetime
from datetime import timedelta
import requests
from collections import Counter
import operator
from fmiopendata.wfs import download_stored_query
import json

import pathlib

fmi_queries = ["fmi::forecast::harmonie::surface::point::multipointcoverage",
               "fmi::observations::weather::multipointcoverage",
               "fmi::observations::weather::daily::multipointcoverage"]
fmi_coordinates = {"TAMPERE": "61.49911,23.78712", "HELSINKI": "60.192059,24.945831", "OULU": "65.01236,25.46816",
                   "TURKU": "60.45451,22.26482", "LAPPEENRANTA": "61.05871,28.18871"}

# minlon, minlat, maxlon, maxlat
fmi_bbox = {"TAMPERE": "23.570322,61.404103,23.634971,61.422669",
            "HELSINKI": "24.936695,60.166345,24.956425,60.177754",
            "OULU": "25.317255,64.919717,25.354000,64.941000",
            "TURKU": "22.095707,60.383664,22.367245,60.486811",
            "LAPPEENRANTA": "28.106238,61.025745,28.166769,61.049718"}

digitrafi_maintenance_base_url = "https://tie.digitraffic.fi/api/maintenance/v1/tracking/routes?endFrom="

digitrafi_coordinates = {"TAMPERE": "23.652361,61.435179,23.865908,61.520098",
                         "HELSINKI": "24.785044,60.134141,25.172312,60.286969",
                         "OULU": "25.398253,64.987359,25.562361,65.037538",
                         "TURKU": "22.197470,60.422136,22.344069,60.474289",
                         "LAPPEENRANTA": "28.106238,61.025745,28.272406,61.071282"}

weather_camera_ids = {"TAMPERE": "C04507", "HELSINKI": "C01675",
                      "OULU": "C12503", "TURKU": "C02520",
                      "LAPPEENRANTA": "C03558"}


def weather_data(city, start_time=datetime.now() - timedelta(days=2), end_time=datetime.now() - timedelta(days=1),
                 timestep="60"):
    """
    This function calls and parses an xml-object from fmi and the corresponding data will be returned in a dictionary
    structure. Parameters apart from city have default values which will return measurements from the past day.

    :param city: Choose between Tampere, Helsinki, Lappeenranta, Oulu and Turku. Parameter is string format and all caps
    :param start_time: Datetime object. Should be earlier than end_time
    :param end_time: Datetime object. Cannot be of higher value than the current time since no measurements will exist.
    :param timestep: Density of return values. Value means minutes in between data-points.
    :return: Nested dictionary which contains temperatures, windspeeds and cloudiness measurements.
    """
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = download_stored_query(fmi_queries[1],
                                 args=["bbox=" + fmi_bbox[city], "timestep=" + timestep, "starttime=" + start,
                                       "endtime=" + end, "parameters=t2m,ws_10min,n_man", "timeseries=True"])
    return data.data


def weather_daily_measurements(city, start_time=datetime.now() - timedelta(days=14),
                               end_time=datetime.now() - timedelta(days=1)):
    """
    Similar function to weather_data, except the timestep is a solid day and the return values signify daily averages.

    :param city: Choose between Tampere, Helsinki, Lappeenranta, Oulu and Turku. Parameter is string format and all caps
    :param start_time: Datetime object. Should be earlier than end_time
    :param end_time: Datetime object. Cannot be of higher value than the current time since no measurements will exist.
    :return: Nested dictionary which contains temperatures, windspeeds and cloudiness measurements.
    """
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = download_stored_query(fmi_queries[2],
                                 args=["bbox=" + fmi_bbox[city], "timestep=1440", "starttime=" + start,
                                       "endtime=" + end, "parameters=t2m,ws_10min,n_man", "timeseries=True"])

    return data.data


def weather_forecast(city, start_time=datetime.now(), end_time=datetime.now() + timedelta(days=1), timestep="60"):
    """
    Used for requesting weather forecasts from fmi. Values are forecasts and not measured data.

    :param city: Choose between Tampere, Helsinki, Lappeenranta, Oulu and Turku. Parameter is string format and all caps
    :param start_time: Datetime object, should be current time or later and before end_time
    :param end_time: Datetime object, should be after current time and later than start time
    :param timestep: Density of return values. Value means minutes in between data-points.
    :return: Nested dictionary which contains temperatures and windspeeds.
    """
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = download_stored_query(fmi_queries[0],
                                 args=["latlon=" + fmi_coordinates[city], "timestep=" + timestep, "starttime=" + start,
                                       "endtime=" + end, "parameters=temperature,windspeedms", "timeseries=True"])
    return data.data


def road_data(city, start_time=datetime.now(), end_time=datetime.now() + timedelta(days=1), task_name="",
              situation_type=""):
    """
    This function calls get functions for maintenance data, traffic messages
    and road condition. Function sends a request to get weather camera image.

    :param city: Choose between Tampere, Helsinki, Lappeenranta, Oulu and Turku. Parameter is string format and all caps.
    :param start_time: Datetime object, should be current time or later and before end_time.
    :param end_time: Datetime object, should be after current time and later than start time.
    :param task_name: String, can be used to search for a specific task from the maintenance data. Default parameter an empty string.
    :param situation_type: String, can describe which type of traffic message is searched for. Default parameter an empty string.
    :return: Three dictionaries in which the retrieved data is formatted for use.
    """
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    maintenance_data = get_maintenance_data(city, start, end, task_name)
    traffic_messages = get_traffic_messages(city, situation_type)
    road_condition = get_road_condition(city)
    camera_success = weather_cameras(city)
    return maintenance_data, traffic_messages, road_condition


def get_maintenance_data(city, start, end, task_name):
    """
    Get function for maintenance data. Saves the API data to json. Calls for
    format_maintenance_data()-function for formatting the data.

    :param city: String all caps, region/city from which data is collected.
    :param start: String. Should be earlier than end_time.
    :param end: String.
    :param task_name: String, default parameter.
    :return: Dictionary which contains formatted maintenance data.
    """
    coordinates = digitrafi_coordinates[city].split(",")
    url = digitrafi_maintenance_base_url + start + "&endBefore=" + end \
          + "&xMin=" + coordinates[0] + "&yMin=" + coordinates[1] + "&xMax=" + coordinates[2] \
          + "&yMax=" + coordinates[3] + "&taskId=" + task_name + "&domain=state-roads"
    response = requests.get(url)
    maintenance_data_temp = response.json()


    maintenance_data = format_maintenance_data(city, maintenance_data_temp)
    return maintenance_data


def format_maintenance_data(city, maintenance_data):
    """
    The function goes through the data retrieved from the API and formats the
    tasks and their start and end times.

    :param city: String all caps, region/city from which data is collected.
    :param maintenance_data: Data retrieved from the API edited in json format.
    :return: Nested dictionary which contains the city as key and tasks, their start and end times as value.
    """
    data = {"tasks": [], "startTime": [], "endTime": []}

    for features in maintenance_data['features']:
        data["tasks"].append(features['properties']['tasks'])
        data["startTime"].append(features['properties']['startTime'])
        data["endTime"].append(features['properties']['endTime'])

    maintenance_data = {city: data}
    return maintenance_data


def get_traffic_messages(city, situation_type=""):
    """
    Get function for traffic messages. Saves the API data to json. Calls for
    format_traffic_messages()-function for formatting the data.

    :param city: String all caps, region/city from which data is collected.
    :param situation_type: String, can describe which type of traffic message
    is searched for. Default parameter empty string.
    :return: Dictionary which contains formatted traffic messages.
    """
    url = "https://tie.digitraffic.fi/api/traffic-message/v1" \
          "/messages?inactiveHours=0&includeAreaGeometry=false&situationType="\
          + situation_type
    response = requests.get(url)
    all_traffic_messages = response.json()
    city_messages = format_traffic_messages(city, all_traffic_messages)

    return city_messages


def format_traffic_messages(city, all_traffic_messages):
    """
    The function goes through the data retrieved from the API and formats the
    situation types and their names and comments from the wanted region/city.

    :param city: String all caps, region/city from which data is collected.
    :param all_traffic_messages: Data retrieved from the API edited in json format.
    :return: Nested dictionary which contains the city as key and situation type, name and comment as value.
    """
    coordinates = digitrafi_coordinates[city].split(",")
    coordinates = [float(c) for c in coordinates]
    messages = {"situationType": [], "name": [], "comment": []}

    for feature in all_traffic_messages['features']:
        if feature['geometry'] != None:
            for coords in feature['geometry']['coordinates']:
                if type(coords) == list:
                    for cordPair in coords:
                        if len(cordPair) == 2:
                            if coordinates[0] < cordPair[0] < coordinates[2] and \
                                    cordPair[1] > coordinates[1] and cordPair[0] < coordinates[3]:
                                messages["situationType"].append(feature['properties']['situationType'])
                                messages["name"].append(feature['properties']['announcements'][0]['features'][0]['name'])
                                messages["comment"].append(feature['properties']['announcements'][0]['comment'])
                                break

    traffic_msg = {city: messages}
    return traffic_msg


def get_road_condition(city):
    """
    Get function for road conditions. Saves the API data to json. Calls for
    format_road_condition()-function for formating the data.

    :param city: String all caps, region/city from which data is collected.
    :return: Dictionary which contains formatted road conditions.
    """
    coordinates = digitrafi_coordinates[city].split(",")
    url = "https://tie.digitraffic.fi/api/v3/data/road-conditions/" \
          + coordinates[0] + "/" + coordinates[1] + "/" + coordinates[2] + "/" + coordinates[3]
    response = requests.get(url)
    all_condition_data = response.json()
    condition_data = format_road_condition(city, all_condition_data)
    return condition_data


def format_road_condition(city, condition_data):
    """
    The function goes through the data retrieved from the API. Formats the road
    conditions by time and wanted data. After collecting wanted data to
    conditions-dictionary it is reviewed and calculate the data averages.
    situation types and their names and comments from the wanted region/city.

    :param city: String all caps, region/city from which data is collected.
    :param condition_data: Data retrieved from the API edited in json format.
    :return: Triple nested dictionary which contains the city, time (0h, 2h,..)
    and wanted data about the road's condition.
    """
    conditions = {"0h": {"daylight": [], "roadTemperature": [],
                         "overallRoadCondition": []},
                  "2h": {"daylight": [], "roadTemperature": [],
                         "overallRoadCondition": [],
                         "precipitationCondition": [], "roadCondition": []},
                  "4h": {"daylight": [], "roadTemperature": [],
                         "overallRoadCondition": [],
                         "precipitationCondition": [], "roadCondition": []},
                  "6h": {"daylight": [], "roadTemperature": [],
                         "overallRoadCondition": [],
                         "precipitationCondition": [], "roadCondition": []},
                  "12h": {"daylight": [], "roadTemperature": [],
                          "overallRoadCondition": [],
                          "precipitationCondition": [], "roadCondition": []}}

    for weatherData in condition_data['weatherData']:
        for roadConditions in weatherData['roadConditions']:
            conditions[roadConditions['forecastName']]["daylight"].append(roadConditions['daylight'])
            conditions[roadConditions['forecastName']]["roadTemperature"] += [float(roadConditions['roadTemperature'])]
            conditions[roadConditions['forecastName']]["overallRoadCondition"].append(roadConditions['overallRoadCondition'])
            if roadConditions['forecastName'] != "0h":
                conditions[roadConditions['forecastName']]["precipitationCondition"].append(
                    roadConditions['forecastConditionReason']['precipitationCondition'])
                conditions[roadConditions['forecastName']]["roadCondition"].append(
                    roadConditions['forecastConditionReason']['roadCondition'])

    for data in conditions.values():
        temp_daylight = Counter(data["daylight"])
        avg_daylight = max(temp_daylight.items(), key=operator.itemgetter(1))[0]
        data["daylight"] = [avg_daylight]

        avg_road_temp = sum(data["roadTemperature"]) / len(data["roadTemperature"])
        data["roadTemperature"] = [avg_road_temp]

        temp_ovcond = Counter(data["overallRoadCondition"])
        avg_ovcond = max(temp_ovcond.items(), key=operator.itemgetter(1))[0]
        data["overallRoadCondition"] = [avg_ovcond]

        if "precipitationCondition" in data:
            temp_precip = Counter(data["precipitationCondition"])
            avg_precip = max(temp_precip.items(), key=operator.itemgetter(1))[0]
            data["precipitationCondition"] = [avg_precip]

        if "roadCondition" in data:
            temp_rd = Counter(data["roadCondition"])
            avg_rd = max(temp_rd.items(), key=operator.itemgetter(1))[0]
            data["roadCondition"] = [avg_rd]

    current_cond = {city: conditions}
    return current_cond


def weather_cameras(city):
    """
    Gets a weather camera image of the wanted city from a specific weather
    camera. And saves the camera image to the project path.

    :param city: String all caps, region/city from which data is collected.
    :return: Boolean value based on the success of image request.
    """
    camera_id = weather_camera_ids[city]
    url = "https://tie.digitraffic.fi/api/weathercam/v1/stations/"+camera_id+"/history"
    response = requests.get(url)
    camera_data = response.json()

    image_url = camera_data['presets'][0]['history'][0]['imageUrl']
    image_response = requests.get(image_url)


    path = pathlib.Path.cwd() / 'controller' / 'saves' / 'images' / 'weather_cam.jpg'


    if image_response.status_code == 200:  # 200 means response OK
        with path.open('wb') as f:
            f.write(image_response.content)
            return True

    return False
