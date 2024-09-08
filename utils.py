import datetime


def dict_to_string(d: dict):
    string = ''
    number = 1
    list_play = list()

    for value in d.values():
        for name, date in value.items():
            list_play.append((name, date))
    list_play.sort(key=lambda x: int(x[1]))
    for player in list_play:
        string += (f'{number}) '
                   f'{player[0]}{(30 - len(f'{player[0]}{datetime.datetime.fromtimestamp(int(player[1])).strftime("%H:%M:%S")}')) * "."}'
                   f'{datetime.datetime.fromtimestamp(int(player[1])).strftime("%H:%M:%S")}\n')
        number += 1
    return string
