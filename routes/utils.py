from trains.models import Train


def dfs_search(graph, start, goal):
    stack = [(start, [start])]

    while stack:
        vertex, path = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    graph = {}

    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)

    return graph


def get_routes(request, form) -> dict:
    qs = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(qs)

    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    travel_time = data['travel_time']
    cities = data['cities']

    all_ways = list(dfs_search(graph, from_city.id, to_city.id))

    if not len(all_ways):
        raise ValueError(f'Из города {from_city.name} в город {to_city.name} маршрутов не существует')

    if cities:
        cities = set([city.id for city in data['cities']])
        right_ways = [way for way in all_ways if cities.issubset(way)]

        if not right_ways:
            raise ValueError('Нет маршрутов, проходящих через заданные города')
    else:
        right_ways = all_ways

    cached_trains = {}
    ways = []

    for way in right_ways:
        total_time = 0
        trains = []

        for i in range(len(way) - 1):
            train = cached_trains.get((way[i], way[i + 1]), None)

            if train is None:
                train = qs.filter(from_city=way[i], to_city=way[i + 1]).first()
                cached_trains[(way[i], way[i + 1])] = train

            total_time += train.travel_time
            trains.append(train)

        ways.append({'trains': trains, 'total_time': total_time})

    ways.sort(key=lambda way: way['total_time'])

    if travel_time:
        ways = list(filter(lambda way: way['total_time'] <= travel_time, ways))

        if not ways:
            raise ValueError('Нет маршрутов, удовлетворяющих времени поездки')

    context = {
        'form': form,
        'ways': ways,
        'cities': {'from_city': from_city, 'to_city': to_city}
    }

    return context
