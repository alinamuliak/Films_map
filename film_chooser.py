import folium
from folium.plugins import MarkerCluster
from copy import deepcopy
from haversine import haversine
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
geolocator = Nominatim(user_agent="map_builder")


def read_file(file_path: str) -> list:
    """
    Read data from file and return the list.
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


# film_list = read_file("small.list")
# print("file readed", flush=True)


def one_year_films(year: int, film_list: list) -> list:
    """
    повертати фільми заданого року
    """
    one_year_films = []

    for film_info in film_list:
        year_here = int(film_info[0].index('(')) + 1
        if not film_info[0][year_here:year_here + 4].isdigit():
            continue
        film_year = int(film_info[0][year_here:year_here + 4])
        if film_year == year:
            one_year_films.append(
                [film_info[0][:year_here - 2], film_info[-1]])
    return one_year_films


# one_year = one_year_films(2000, film_list)
# print("year chosen", len(one_year), flush=True)


def address_to_coordinates(film_list: list) -> list:
    """
    всі адреси у списку замінити на координати цього місця
    """
    global geolocator
    coord_list = []
    for film_info in film_list:
        try:
            location = geolocator.geocode(film_info[-1])
            coord_list.append([
                film_info[0], (location.latitude, location.longitude)])
            print("ok", len(coord_list),
                  (location.latitude, location.longitude), flush=True)
        except GeocoderUnavailable:
            continue
        except AttributeError:
            continue
    return coord_list


def determine_ten_closest(film_list: list, user_location: tuple) -> list:
    """
    визначає відстань від юзера до усіх місць а тоді сортує
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


def map_builder(film_list: list, user_location: tuple, user_year):
    """
    """
    map = folium.Map(location=list(user_location))
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

    map.add_child(flm)
    map.add_child(lines_loc)
    folium.LayerControl().add_to(map)
    map.save(f'{user_year}_film_map.html')


# map_builder(closest_films, (40.730610, -73.935242))
