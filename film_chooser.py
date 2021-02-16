"""
This module contains functions to read data from file,
find locations of film scene, determine ten closest locations
and build map, based on those analysis.
"""


import folium
from folium.plugins import MarkerCluster
from haversine import haversine
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
geolocator = Nominatim(user_agent="map_builder")


def read_file(file_path: str) -> list:
    """
    Read data from file and return the list of lists, where
    the firts element of smaller lists is name, year and (if is) a series of film,
    and the second contains the address where it was filmed.
    """

    with open(file_path, 'r', errors='ignore') as film_list:
        lines = film_list.readlines()
    lines = lines[14:-2]
    films = []
    for line in lines:
        line = line.strip().split('\t')
        if str(line[-1][0]) + str(line[-1][-1]) == '()':
            films.append([line[0], line[-2]])
            continue
        films.append([line[0], line[-1]])
    return films


def one_year_films(year: int, film_list: list) -> list:
    """
    Return the list of lists that contains name of films
    and its location made in guven year.
    >>> one_year_films(2015, [['"Wow" (2011)', 'USA'],\
                              ['"Princess" (2015)', "Berlin, Germany"],\
                              ['"Hithere" (2015)', "Paris, France"]])
    [['"Princess"', 'Berlin, Germany'], ['"Hithere"', 'Paris, France']]
    """
    same_year_films = []

    for film_info in film_list:
        year_here = int(film_info[0].index('(')) + 1
        if not film_info[0][year_here:year_here + 4].isdigit():
            continue
        film_year = int(film_info[0][year_here:year_here + 4])
        if film_year == year:
            same_year_films.append(
                [film_info[0][:year_here - 2], film_info[-1]])
    return same_year_films


def address_to_coordinates(film_list: list) -> list:
    """
    Return a list of lists where all locations are replaced by the coordinates
    in format (lat, lon).
    If geopy cannot find such a location, this film will not be included in returned list.

    >>> address_to_coordinates([['"Wow" (2015)', 'USA'],\
                              ['"Princess" (2015)', "Berlin, Germany"],\
                              ['"Hithere" (2015)', "Paris, France"]])
    [['"Wow" (2015)', (39.7837304, -100.4458825)], \
['"Princess" (2015)', (52.5170365, 13.3888599)], \
['"Hithere" (2015)', (48.8566969, 2.3514616)]]
    """
    global geolocator
    coord_list = []
    for film_info in film_list:
        try:
            location = geolocator.geocode(film_info[-1])
            coord_list.append([
                film_info[0], (location.latitude, location.longitude)])
        except GeocoderUnavailable:
            continue
        except AttributeError:
            continue
    return coord_list


def determine_ten_closest(film_list: list, user_location: tuple) -> list:
    """
    Return a list of lists with the information
    of ten tags of the nearest filming locations.
    """
    closest_locations = []
    for film_info in film_list:
        film_location = film_info[-1]
        distance = haversine(user_location, film_location)
        if len(closest_locations) == 0:
            closest_locations.append((film_info[0], distance, film_location))
        elif len(closest_locations) <= 10:
            closest_locations.append((film_info[0], distance, film_location))
            if len(closest_locations) == 10:
                closest_locations.sort(key=lambda x: x[1])
        elif (len(closest_locations) > 10 and
              distance < closest_locations[-1][1]):
            closest_locations[-1] = (film_info[0], distance, film_location)
            closest_locations.sort(key=lambda x: x[1])
    return closest_locations[:10]


def map_builder(film_list: list, user_location: tuple, user_year: int) -> None:
    """
    Built a map with 3 layers and saves it to the '(user_year)_film_map.html' file.
    """
    mapa = folium.Map(location=list(user_location))
    lat = [x[-1][0] for x in film_list]
    lon = [x[-1][1] for x in film_list]
    names = [x[0] for x in film_list]
    flm = folium.FeatureGroup(name="Films Marker")
    lines_loc = folium.FeatureGroup(name="Connected with you")
    marker_cluster = MarkerCluster().add_to(flm)

    for lt, ln, nm in zip(lat, lon, names):
        folium.Marker(location=[lt, ln],
                      popup=nm,
                      icon=folium.Icon(color='red')).add_to(marker_cluster)
        folium.PolyLine(
            locations=[list(user_location), [lt, ln]], weight=2).add_to(lines_loc)

    mapa.add_child(flm)
    mapa.add_child(lines_loc)
    folium.LayerControl().add_to(mapa)
    mapa.save(f'{user_year}_film_map.html')
