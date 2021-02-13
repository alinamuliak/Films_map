def read_file(file_path: str) -> list:
    """
    Read data from file and return the list.
    """
    with open(file_path) as film_list:
        lines = film_list.readlines()
    lines = lines[14:]
    films = []
    for line in lines:
        line = line.strip().replace('\n', '\t').replace('{', '\t').split('\t')
        needed_info_films = line.copy()
        for i in range(len(line)):
            if line[i] == '' or '}' in line[i]:
                needed_info_films.remove(line[i])
        films.append(needed_info_films)
    return films


print(read_file("small.list"))


def one_year_films(year: int, film_list: list) -> list:
    """
    повертати фільми заданого року
    """
    pass
