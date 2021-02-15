import folium
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
            # for film_info in coord_list:
            # print(film_info[-1], flush=True)
            location = geolocator.geocode(film_info[-1])
            # print("location =", location, flush=True)
            coord_list.append([
                film_info[0], (location.latitude, location.longitude)])
            print("ok", (location.latitude, location.longitude), flush=True)
        except GeocoderUnavailable:
            # print("geoexc", film_info, flush=True)
            continue
        except AttributeError:
            # print("attr", film_info, flush=True)
            continue
    return coord_list


# coord_list = address_to_coordinates(one_year)
# print(coord_list, flush=True)
# print("address to coord", flush=True)


def determine_ten_closest(film_list: list, user_location: tuple) -> list:
    """
    визначає відстань від юзера до усіх місць а тоді сортує
    """
    closest_locations = []
    for film_info in film_list:
        film_location = film_info[-1]
        # print((user_location, film_location), flush=True)
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
    return closest_locations


# coord_list = [['"#ActorsLife"', (40.7127281, -74.0060152)], ['"#Fuga"', (-22.9997404, -43.3659929)], ['"#KillTorrey"', (34.1816482, -118.3258554)], ['"#LoveMyRoomie"', (40.7127281, -74.0060152)], ['"#LoveMyRoomie"', (40.6501038, -73.9495823)], ['"#MyCurrentSituation: Atlanta"', (33.7489924, -84.3902644)], ['"#MyCurrentSituation: Atlanta"', (35.1490215, -90.0516285)], ['"#SmurTv"', (37.270973, -79.9414313)], ['"#SmurTv"', (35.2272086, -80.8430827)], ['"#SmurTv"', (33.7489924, -84.3902644)], ['"#SpongeyLeaks"', (34.2345615, -118.5369316)], ['"#SpongeyLeaks"', (34.2345615, -118.5369316)], ['"#VanLifeAttila"', (61.0666922, -107.991707)], ['"#VanLifeAttila"', (36.7014631, -118.755997)], ['"#VanLifeAttila"', (51.0, 10.0)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0962821, -121.5323561)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0962821, -121.5323561)], ['"#VanLifeAttila"', (49.2433804, -122.9725459)], ['"#VanLifeAttila"', (49.2842958, -122.793281)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (52.9794279, -122.4936273)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (52.9794279, -122.4936273)], ['"#VanLifeAttila"', (49.8879177, -119.4959025)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (49.2842958, -122.793281)], ['"#VanLifeAttila"', (49.2842958, -122.793281)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)],
#               ['"#VanLifeAttila"', (49.163168, -123.137414)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.0962821, -121.5323561)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (50.8367991, -118.9826386)], ['"#VanLifeAttila"', (51.0534234, -114.0625892)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (49.3799438, -121.4413515)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (50.8367991, -118.9826386)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2433804, -122.9725459)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (49.3019112, -123.14154052837662)], ['"#VanLifeAttila"', (55.001251, -115.002136)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (47.4983815, 19.0404707)], ['"#VanLifeAttila"', (47.4983815, 19.0404707)], ['"#VanLifeAttila"', (53.0962821, -121.5323561)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2842958, -122.793281)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.0402309, -121.718755)], ['"#VanLifeAttila"', (52.9794279, -122.4936273)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.1173414, -121.49901337494916)]]
# closest_films = determine_ten_closest(coord_list, (40.730610, -73.935242))
# print("closest 10 - done", flush=True)


def map_builder(film_list: list, user_location: tuple):
    """
    """
    map = folium.Map(location=list(user_location))
    lat = [x[-1][0] for x in film_list]
    lon = [x[-1][1] for x in film_list]
    names = [x[0] for x in film_list]
    flm = folium.FeatureGroup(name="Films Marker")
    for lt, ln, nm in zip(lat, lon, names):
        flm.add_child(folium.Marker(location=[lt, ln],
                                    popup=nm,
                                    icon=folium.Icon()))
    map.add_child(flm)
    map.save('film_map.html')


# map_builder(closest_films, (40.730610, -73.935242))
# print("map - done")
