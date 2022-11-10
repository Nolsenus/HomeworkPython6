def get_values(string):
    result = []
    if string.count(';') != 3:
        print('Вы ввели что-то лишнее или не ввели что-то необходимое, попробуйте снова.')
        return False
    part = string[:string.find(';')]
    result.append(part)
    string = string.removeprefix(part + ';')
    part = string[:string.find(';')]
    try:
        score1 = int(part)
        if score1 < 0:
            raise ValueError
        result.append(score1)
        string = string.removeprefix(str(score1) + ';')
        part = string[:string.find(';')]
        result.append(part)
        string = string.removeprefix(part + ';')
        score2 = int(string)
        if score2 < 0:
            raise ValueError
        result.append(score2)
        return result
    except ValueError:
        print('Количество голов, забитых обеими командами должно быть одним целым неотрицательным числом.')
        return False


def main():
    try:
        count = int(input('Введите количество матчей (одно неотрицательное целое число): '))
        if count < 0:
            print('Вы ввели отрицательное число.')
        else:
            teams = dict({})
            i = 0
            while i < count:
                line = input(f'Введите результат матча номер {i + 1} '
                             f'(Команда 1;Забито командой 1;Команда 2;Забито командой 2): ')
                values = get_values(line)
                if values:
                    team1 = values[0]
                    score1 = values[1]
                    team2 = values[2]
                    score2 = values[3]
                    if team1 not in teams.keys():
                        teams[team1] = [0] * 5
                    if team2 not in teams.keys():
                        teams[team2] = [0] * 5
                    teams[team1][0] += 1
                    teams[team2][0] += 1
                    if score2 > score1:
                        teams[team2][1] += 1
                        teams[team2][4] += 3
                        teams[team1][3] += 1
                    elif score1 > score2:
                        teams[team1][1] += 1
                        teams[team1][4] += 3
                        teams[team2][3] += 1
                    else:
                        teams[team1][2] += 1
                        teams[team1][4] += 1
                        teams[team2][2] += 1
                        teams[team2][4] += 1
                    i += 1
            for team in teams.keys():
                scores = teams[team]
                print(f'{team} - М:{scores[0]} В:{scores[1]} Н:{scores[2]} П:{scores[3]} О:{scores[4]}')
    except ValueError:
        print('Вы ввели не целое число.')


if __name__ == '__main__':
    main()
