c = int(input())

cities = {}

for _ in range(c):
    city, n = input().split()
    n = int(n)

    free_room = [None] * 24

    for _ in range(n):
        t, room = input().split()

        for hour in range(24):
            if t[hour] == "." and free_room[hour] is None:
                free_room[hour] = room

    cities[city] = free_room

m = int(input())

for _ in range(m):
    query = input().split()
    need_cities = query[1:]

    answer_rooms = None

    for hour in range(24):
        rooms = []
        ok = True

        for city in need_cities:
            room = cities[city][hour]

            if room is None:
                ok = False
                break

            rooms.append(room)

        if ok:
            answer_rooms = rooms
            break

    if answer_rooms is None:
        print("No")
    else:
        print("Yes", *answer_rooms)