import film_chooser as flmc
from time import sleep

# NEED TO ADD ONE MORE LAYER !!!!!!!!!!!!!!!


def slow(message):
    for letter in message:
        print(letter, end='', flush=True)
        sleep(0.1)


def main():
    year = int(input("Please enter a year you would like to have a map for: "))
    user_location_str = input(
        "Please enter your location(format: lat, long): ")
    user_location = (float(user_location_str.split(',')[0][1:]),
                     float(user_location_str.split(',')[1][:-1]))
    slow("Map is generating...\n")
    # TRY WITH LOCATION.LIST !!!&!^$%#@#$%#@!@#$%
    film_list = flmc.read_file("locations.list")
    one_year = flmc.one_year_films(year, film_list)
    coord_list = flmc.address_to_coordinates(one_year)
    slow("Please wait...\n")
    closest_films = flmc.determine_ten_closest(coord_list, user_location)
    flmc.map_builder(closest_films, user_location)
    slow("Finished. Please have look at the map movies_map.html\n")


if __name__ == "__main__":
    main()
