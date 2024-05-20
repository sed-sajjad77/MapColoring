import sys
from operator import itemgetter
import operator


def build_graph(map):
    # key: (X, Bool). X means city AND Bool means Colored Or Not
    # value: [(X, ''), (Y, '')]. List of neighbours. Second item of tuple is color of city
    graph = {}

    with open(map, 'r') as cities_file:
        cities = cities_file.readlines()
        cities = [city.strip('\n').replace(" ", "") for city in cities if len(
            city.strip('\n').replace(" ", "")) != 0]

    for city_neighbours in cities:
        city, neighbours = city_neighbours.split(":")
        neighbours = neighbours.replace(
            "[", "").replace("]", "").replace("\n", "").split(",")

        # Converting format of neighbours. [X, Y] => [('X', ''), ('Y', '')]
        neighbours = [(neighbour, '')
                      for neighbour in neighbours if neighbour != '']
        graph[(city, False)] = neighbours

    return graph


# Differences between two list
def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


# Get allowed colors for a city
def get_allowed_colors(graph, city, colors):
    not_allowed_colors = [city[1]
                          for city in graph[(city, False)] if city[1] != '']
    allowed_colors = diff(colors, not_allowed_colors)
    return allowed_colors


# Degree heuristic.
# return index of city or cities with max neighbours.
def degree_heuristic(graph):
    index_neighbour_len = [(index, len(l[1])) for index,
                           l in enumerate(graph.items()) if l[0][1] is False]
    max_neighbour = max(index_neighbour_len, key=itemgetter(1))[1]
    max_index_neighbour_len = [t[0]
                               for t in index_neighbour_len if t[1] == max_neighbour]
    cities = [list(graph)[index][0] for index in max_index_neighbour_len]
    return cities


# MRV.
# return city or cities with minimum remaining values/colors
def mrv(graph, colors):
    cities_without_color = [(city[0])
                            for city, colored in graph.items() if city[1] is False]
    allowed_color_each_city = {}
    for city in cities_without_color:
        allowed_color_each_city[city] = get_allowed_colors(graph, city, colors)

    min_available_color_len = min(
        [len(allowed_colors) for city, allowed_colors in allowed_color_each_city.items()])
    cities = [city for city, colors in allowed_color_each_city.items() if len(
        colors) is min_available_color_len]
    return cities


# Least constraining value
# Return color or colors which used much
def lcv(graph, colors):
    city_color = []
    color_number = {}

    for neighbours in graph.values():
        [city_color.append(c) for c in neighbours if c[1] != '']

    all_used_colors = list(dict.fromkeys(city_color))

    # First iteration
    if not all_used_colors:
        return colors

    for cc in all_used_colors:
        if cc[1] not in color_number:
            color_number[cc[1]] = 1
        else:
            color_number[cc[1]] += 1

    # Number of max color. {'A': 3, 'B': 3, 'C': 1} => ['A', 'B']
    number_of_max = max(color_number.items(), key=operator.itemgetter(1))[1]
    colors = [key for (key, value) in color_number.items()
              if value is number_of_max]

    return colors


# Color selected city
def coloring(graph, city, color):

    neighbours = graph[(city, False)]
    del graph[(city, False)]
    graph[(city, True)] = neighbours

    for nei_list in graph.values():

        for n in nei_list:
            if n[0] == city:
                l = list(n)
                l[1] = color
                t = tuple(l)
                nei_list.remove(n)
                nei_list.append(t)


# main
map = 'map-iran.txt'

if map == 'map-iran.txt':
    colors = ['red', 'green', 'blue', 'yellow']
else:
    colors = ['red', 'green', 'blue']

# Build graph from file
graph = build_graph(map)
# print(graph)

for _ in range(len(graph)):
    cities_with_max_degree = degree_heuristic(graph)
    # print(cities_with_max_degree)
    cities_with_minimum_remaining_colors = mrv(graph, colors)
    # print(cities_with_minimum_remaining_colors)
    much_used_colors = lcv(graph, colors)
    # print(much_used_colors)

    if len(set(cities_with_max_degree).intersection(set(cities_with_minimum_remaining_colors))) != 0:
        selected_city = set(cities_with_max_degree).intersection(
            set(cities_with_minimum_remaining_colors)).pop()
    else:
        selected_city = set(cities_with_minimum_remaining_colors).pop()

    # Get allowed color for selected city
    colors_of_selected_city = get_allowed_colors(
        graph, selected_city, colors)

    # Final chosen color
    common_color = set(much_used_colors).intersection(
        set(colors_of_selected_city))

    if common_color:
        color = common_color.pop()
    elif colors_of_selected_city:
        color = colors_of_selected_city.pop()

    coloring(graph, selected_city, color)


alone_cities = [graph[city].append(
    "Any Color") for city, neighbours in graph.items() if len(neighbours) == 0]

coloring_map = []
for value in graph.values():
    for val in value:
        if val not in coloring_map:
            coloring_map.append(val)

j = 0
for i in range(len(coloring_map)):
    if coloring_map[i][1] == '':
        pass
    else:
        print(coloring_map[i])
        j += 1
print(j)
