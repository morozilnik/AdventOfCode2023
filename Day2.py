from functools import reduce


def strip_endings(text):
    return [x.replace("\n", "") for x in text]

def parse_input(text):
    games = []
    for line in text:
        line = line[line.index(':') + 1:] # Strip Game N:
        turns = line.split(';')
        turn_list = []
        for turn in turns:
            turn_dict = {"red": 0, "green": 0, "blue": 0}
            cubes = turn.split(',')
            for cube in cubes:
                num, col = cube.split()
                turn_dict[col] = int(num)
            turn_list.append(turn_dict)
        games.append(turn_list)
    return games


def solve1(games):
    max_dict = {"red": 12, "green": 13, "blue": 14}
    good_games = 0
    for num, game in enumerate(games, 1):
        bad_game = False
        for turn in game:
            for col, amount in turn.items():
                if amount > max_dict[col]:
                    bad_game = True
        if not bad_game:
            good_games += num
    return good_games

def solve2(games):
    total_power = 0
    for num, game in enumerate(games, 1):
        min_dict = {"red": 0, "green": 0, "blue": 0}
        for turn in game:
            for col, amount in turn.items():
                if amount > min_dict[col]:
                    min_dict[col] = amount
        game_power = reduce(lambda x,y: x * y, min_dict.values())
        total_power += game_power

    return total_power

if __name__ == "__main__":
    path = "Day2.txt"
    with open(path) as f:
        text_input = f.readlines()
    text_input = strip_endings(text_input)
    dict_input = parse_input(text_input)
    print(solve2(dict_input))
        