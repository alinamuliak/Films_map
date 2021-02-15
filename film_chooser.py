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
    with open(file_path) as film_list:
        lines = film_list.readlines()
    lines = lines[14:]
    films = []
    for line in lines:
        line = line.strip().split('\t')
        if str(line[-1][0]) + str(line[-1][-1]) == '()':
            films.append([line[0], line[-2]])
            continue
        films.append([line[0], line[-1]])
    return films


film_list = read_file("small.list")


def one_year_films(year: int, film_list: list) -> list:
    """
    повертати фільми заданого року
    """
    one_year_films = []

    for film_info in film_list:
        year_here = int(film_info[0].index('(')) + 1
        film_year = int(film_info[0][year_here:year_here + 4])
        if film_year == year:
            one_year_films.append(
                [film_info[0][:year_here - 2], film_info[-1]])
    return one_year_films


one_year = one_year_films(2016, film_list)


def address_to_coordinates(film_list: list) -> list:
    """
    всі адреси у списку замінити на координати цього місця
    """
    global geolocator
    while True:
        try:
            coord_list = deepcopy(film_list)
            for film_info in coord_list:
                location = geolocator.geocode(film_info[-1])
                film_info[-1] = (location.latitude, location.longitude)
            return coord_list
        except GeocoderUnavailable:
            continue


# print(address_to_coordinates(one_year))

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
    return closest_locations


# coord_list = [['"#ActorsLife"', (40.7127281, -74.0060152)], ['"#Fuga"', (-22.9997404, -43.3659929)], ['"#KillTorrey"', (34.1816482, -118.3258554)], ['"#LoveMyRoomie"', (40.7127281, -74.0060152)], ['"#LoveMyRoomie"', (40.6501038, -73.9495823)], ['"#MyCurrentSituation: Atlanta"', (33.7489924, -84.3902644)], ['"#MyCurrentSituation: Atlanta"', (35.1490215, -90.0516285)], ['"#SmurTv"', (37.270973, -79.9414313)], ['"#SmurTv"', (35.2272086, -80.8430827)], ['"#SmurTv"', (33.7489924, -84.3902644)], ['"#SpongeyLeaks"', (34.2345615, -118.5369316)], ['"#SpongeyLeaks"', (34.2345615, -118.5369316)], ['"#VanLifeAttila"', (61.0666922, -107.991707)], ['"#VanLifeAttila"', (36.7014631, -118.755997)], ['"#VanLifeAttila"', (51.0, 10.0)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0962821, -121.5323561)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0962821, -121.5323561)], ['"#VanLifeAttila"', (49.2433804, -122.9725459)], ['"#VanLifeAttila"', (49.2842958, -122.793281)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (52.9794279, -122.4936273)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (52.9794279, -122.4936273)], ['"#VanLifeAttila"', (49.8879177, -119.4959025)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (49.2842958, -122.793281)], ['"#VanLifeAttila"', (49.2842958, -122.793281)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)],
#               ['"#VanLifeAttila"', (49.163168, -123.137414)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.0962821, -121.5323561)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (50.8367991, -118.9826386)], ['"#VanLifeAttila"', (51.0534234, -114.0625892)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (49.3799438, -121.4413515)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (50.8367991, -118.9826386)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2433804, -122.9725459)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (49.3019112, -123.14154052837662)], ['"#VanLifeAttila"', (55.001251, -115.002136)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (47.4983815, 19.0404707)], ['"#VanLifeAttila"', (47.4983815, 19.0404707)], ['"#VanLifeAttila"', (53.0962821, -121.5323561)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (49.2842958, -122.793281)], ['"#VanLifeAttila"', (49.3206294, -123.0737925)], ['"#VanLifeAttila"', (49.2608724, -123.1139529)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.0402309, -121.718755)], ['"#VanLifeAttila"', (52.9794279, -122.4936273)], ['"#VanLifeAttila"', (53.0666687, -121.5166749)], ['"#VanLifeAttila"', (53.1044428, -121.5723679)], ['"#VanLifeAttila"', (53.1173414, -121.49901337494916)]]
# print(determine_ten_closest(coord_list, (40.730610, -73.935242)))
