import ast
import os

#read in game info
f = open("maps.txt","r")
maps = f.read().splitlines()
f.close()

f = open("characters.txt",'r')
characters = f.read().splitlines()
f.close()

def game_input():
    #Inputs information a new game and writes to 2games.txt and 1games.txt

    date = input('What date was the game (mm/dd/yy) ')

    while True:
        size = input('Was this game 1v1 or 2v2 (enter 1 or 2): ')
        if size != '1' and size != '2':
            print("Invalid game size")
            continue
        else:
            break

    print(maps)

    while True:
        map = input('What map did the game take place on? ')
        if map not in maps:
            print("Invalid map")
            continue
        else:
            break

    print(characters)

    if size == '2':
        while True:
            w1 = input('Name the first winner ("name,Character"): ').split(',')
            if w1[1] not in characters:
                print("Invalid character")
                continue
            else:
                break
        while True:
            w2 = input('Name the second winner ("name,Character"): ').split(',')
            if w2[1] not in characters:
                print("Invalid character")
                continue
            else:
                break
        while True:
            l1 = input('Name the first loser ("name,Character"): ').split(',')
            if l1[1] not in characters:
                print("Invalid character")
                continue
            else:
                break
        while True:
            l2 = input('Name the second loser ("name,Character"): ').split(',')
            if l2[1] not in characters:
                print("Invalid character")
                continue
            else:
                break

        f = open('2games.txt','r')
        gamelist = f.read().splitlines()
        f.close()
        if len(gamelist) == 0:
            gamenumber = 1
            f = open('2games.txt','w')
            data = [gamenumber,date,map,w1[0],w1[1],w2[0],w2[1],l1[0],l1[1],l2[0],l2[1]]
            f.write(str(data)+'\n')
            f.close()
        else:
            gamenumber = int(gamelist[-1].strip('][').split(',')[0])+1
            f = open('2games.txt','a')
            data = [gamenumber,date,map,w1[0],w1[1],w2[0],w2[1],l1[0],l1[1],l2[0],l2[1]]
            f.write(str(data)+'\n')
            f.close()
    elif size == '1':
        w = input('Name the winner ("name,Character"): ').split(',')
        if w[1] not in characters:
            raise ValueError('Invalid character name')
        l = input('Name the loser ("name,Character"): ').split(',')
        if l[1] not in characters:
            raise ValueError('Invalid character name')
        
        f = open('1games.txt','r')
        gamelist = f.read().splitlines()
        f.close()
        if len(gamelist) == 0:
            gamenumber = 1
            f = open('1games.txt','w')
            data = [gamenumber,date,map,w[0],w[1],l[0],l[1]]
            f.write(str(data)+'\n')
            f.close()
        else:
            gamenumber = int(gamelist[-1].strip('][').split(',')[0])+1
            f = open('1games.txt','a')
            data = [gamenumber,date,map,w[0],w[1],l[0],l[1]]
            f.write(str(data)+'\n')
            f.close()
    else:
        raise ValueError('Invalid game size')
    return

def stats_update():
    f = open('2games.txt','r')
    gamelist2 = f.read().splitlines()
    f.close()
    f = open('1games.txt','r')
    gamelist1 = f.read().splitlines()
    f.close()
    for i in range(len(gamelist2)):
        gamelist2[i] = ast.literal_eval(gamelist2[i])
    for i in range(len(gamelist1)):
        gamelist1[i] = ast.literal_eval(gamelist1[i])
    players = set()
    characters = set()
    for game in gamelist2:
        players.add(game[3])
        players.add(game[5])
        players.add(game[7])
        players.add(game[9])
        characters.add(game[4])
        characters.add(game[6])
        characters.add(game[8])
        characters.add(game[10])
    for game in gamelist1:
        players.add(game[3])
        players.add(game[5])
        characters.add(game[4])
        characters.add(game[6])
    players = list(players)

    f = open('players.txt','w')
    f.write(players[0]+'\n')
    g = open('players.txt','a')
    for player in players[1:]:
        g.write(player+'\n')

    elo_dict = calculate_2elos(gamelist2,players)

    for player in players:
        ngames = 0
        nwins = 0
        for game in gamelist2:
            if player in game:
                ngames+=1
                if game[3]==player or game[5]==player:
                    nwins+=1
        if ngames:
            winrate=str(round(100*nwins/ngames,2))+'%'
        else:
            winrate=None
        ngames1 = 0
        nwins1 = 0
        for game in gamelist1:
            if player in game:
                ngames1+=1
                if game[3]==player:
                    nwins1+=1
        if ngames1:
            winrate1=str(round(100*nwins1/ngames1))+'%'
        else:
            winrate1=None

        char_dict = {}
        ctotal_dict = {}
        char_dict1 = {}
        ctotal_dict1 = {}
        for char in characters:
            cngames = 0
            cnwins = 0
            cngames1 = 0
            cnwins1 = 0
            for game in gamelist2:
                if (game[3] == player and game[4] == char) or (game[5] == player and game[6] == char):
                    cngames += 1
                    cnwins += 1
                elif (game[7] ==player and game[8] == char) or (game[9] == player and game[10] == char):
                    cngames += 1
            if cngames>0:
                char_dict[char]=round(100*cnwins/cngames,2)
                ctotal_dict[char] = cngames
            for game in gamelist1:
                if game[3] == player and game[4] == char:
                    cngames1 += 1
                    cnwins1 += 1
                elif game[5] == player and game[6] == char:
                    cngames1 += 1
            if cngames1>0:
                char_dict1[char]=round(100*cnwins1/cngames1,2)
                ctotal_dict1[char] = cngames1
        char_sorted = {k: v for k, v in sorted(char_dict.items(), key=lambda x: x[1])}
        char_sorted1 = {k: v for k, v in sorted(char_dict1.items(), key=lambda x: x[1])}
        ctotal_sorted = {}
        ctotal_sorted1 = {}
        for key in char_sorted.keys():
            ctotal_sorted[key] = ctotal_dict[key]
        for key in char_sorted1.keys():
            ctotal_sorted1[key] = ctotal_dict1[key]

        partner_dict = {}
        ptotal_dict = {}
        for partner in players:
            if partner == player:
                continue
            pngames = 0
            pnwins = 0
            for game in gamelist2:
                if (game[3]==player or game[5]==player) and (game[3]==partner or game[5]==partner):
                    pngames += 1
                    pnwins += 1
                elif (game[7]==player or game[9]==player) and (game[7]==partner or game[9]==partner):
                    pngames +=1
            if pngames>0:
                partner_dict[partner]=round(100*pnwins/pngames,2)
            ptotal_dict[partner] = pngames
        partner_sorted = {k: v for k, v in sorted(partner_dict.items(), key=lambda x: x[1])}
        ptotal_sorted = {}
        for key in partner_sorted.keys():
            ptotal_sorted[key] = ptotal_dict[key]
            
        f = open('player_stat_sheets/'+player+'.txt','w')
        f.write(f"{player.capitalize()}\n\n2v2 Stats:\nElo: {round(elo_dict[player])}\nGames Played: {ngames}\nWinrate: {winrate}\n\nWinrate by Character:\n")
        f.write('{:<25}{:<10}{:<3}'.format('Character','Winrate','GP')+'\n')
        for char in reversed(char_sorted.keys()):
            f.write('{:<25}{:<10}{:<3}'.format(char,str(char_sorted[char])+'%',ctotal_sorted[char])+'\n')
        f.write('\nWinrate by Partner:\n')
        f.write('{:<10}{:<10}{:<3}'.format('Partner','Winrate','GP')+'\n')
        for partner in reversed(partner_sorted.keys()):
            f.write('{:<10}{:<10}{:<3}'.format(partner.capitalize(),str(partner_sorted[partner])+'%',ptotal_sorted[partner])+'\n')
        f.write(f'\n1v1 Stats:\nGames Played: {ngames1}\nWinrate: {winrate1}\n\nWinrate by Character\n')
        f.write('{:<25}{:<10}{:<3}'.format('Character','Winrate','GP')+'\n')
        for char in reversed(char_sorted1.keys()):
            f.write('{:<25}{:<10}{:<3}'.format(char,str(char_sorted1[char])+'%',ctotal_sorted1[char])+'\n')

    for character in characters:
        ngames = 0
        nwins = 0
        for game in gamelist2:
            if character in game:
                ngames+=1
                if game[4]==character or game[6]==character:
                    nwins+=1
        if ngames:
            winrate=str(round(100*nwins/ngames,2))+'%'
        else:
            winrate=None
        ngames1 = 0
        nwins1 = 0
        for game in gamelist1:
            if character in game:
                ngames1+=1
                if game[4]==character:
                    nwins1+=1
        if ngames1:
            winrate1=str(round(100*nwins1/ngames1))+'%'
        else:
            winrate1=None
        
        player_dict = {}
        ptotal_dict = {}
        player_dict1 = {}
        ptotal_dict1 = {}
        for player in players:
            pngames = 0
            pnwins = 0
            pngames1 = 0
            pnwins1 = 0
            for game in gamelist2:
                if (game[3] == player and game[4] == character) or (game[5] == player and game[6] == character):
                    pngames += 1
                    pnwins += 1
                elif (game[7] ==player and game[8] == character) or (game[9] == player and game[10] == character):
                    pngames += 1
            if pngames>0:
                player_dict[player]=round(100*pnwins/pngames,2)
                ptotal_dict[player] = pngames
            for game in gamelist1:
                if game[3] == player and game[4] == character:
                    pngames1 += 1
                    pnwins1 += 1
                elif game[5] == player and game[6] == character:
                    pngames1 += 1
            if pngames1>0:
                player_dict1[player]=round(100*pnwins1/pngames1,2)
                ptotal_dict1[player] = pngames1
        player_sorted = {k: v for k, v in sorted(player_dict.items(), key=lambda x: x[1])}
        player_sorted1 = {k: v for k, v in sorted(player_dict1.items(), key=lambda x: x[1])}
        ptotal_sorted = {}
        ptotal_sorted1 = {}
        for key in player_sorted.keys():
            ptotal_sorted[key] = ptotal_dict[key]
        for key in player_sorted1.keys():
            ptotal_sorted1[key] = ptotal_dict1[key]
            
        f = open('character_stat_sheets/'+character+'.txt','w')
        f.write(f"{character.capitalize()}\n\n2v2 Stats:\nGames Played: {ngames}\nWinrate: {winrate}\n\nWinrate by Player:\n")
        f.write('{:<25}{:<10}{:<3}'.format('Player','Winrate','GP')+'\n')
        for player in reversed(player_sorted.keys()):
            f.write('{:<25}{:<10}{:<3}'.format(player.capitalize(),str(player_sorted[player])+'%',ptotal_sorted[player])+'\n')
        f.write(f'\n1v1 Stats:\nGames Played: {ngames1}\nWinrate: {winrate1}\n\nWinrate by Player\n')
        f.write('{:<25}{:<10}{:<3}'.format('Player','Winrate','GP')+'\n')
        for player in reversed(player_sorted1.keys()):
            f.write('{:<25}{:<10}{:<3}'.format(player.capitalize(),str(player_sorted1[player])+'%',ptotal_sorted1[player])+'\n')
        f.close()

    return

def calculate_2wars():
    temp_dict = {}
    war_dict = {}
    rates = []
    directory = os.fsencode('player_stat_sheets')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        f = open('player_stat_sheets/'+filename,'r')
        lines = f.read().splitlines()
        player = lines[0]
        games_played = int(lines[4].split(' ')[-1])
        if games_played == 0:
            rate = 0
        else:
            rate = float(lines[5].split(' ')[-1][:-1])/100
        rates.append(rate)
        temp_dict[player] = (round(games_played*rate), games_played)
    avg_rate = sum(rates)/len(rates)
    for player in temp_dict.keys():
        war_dict[player] = round(temp_dict[player][0] - avg_rate * temp_dict[player][1],2)
    war_sorted = {k: v for k, v in sorted(war_dict.items(), key=lambda x: x[1])}
    f = open('war_score.txt','w')
    f.write('WAR Score ranking\nGiven the average win rate of all players:\n(Number of games won) - (Avg. win rate) * (Number of games played)\n\nPlayer WAR Scores:\n')
    for player in reversed(war_sorted.keys()):
        if war_sorted[player] >= 0:
            f.write("{:<15}{:<5}".format(player,'+'+str(war_sorted[player]))+'\n')
        else:
            f.write("{:<15}{:<5}".format(player,war_sorted[player])+'\n')

def calculate_2elos(gamelist,players):
    elo_dict = {}
    for player in players:
        elo_dict[player] = 1000
    
    for game in gamelist:
        winner1 = game[3]
        winner2 = game[5]
        loser1 = game[7]
        loser2 = game[9]
        exw = 1 / ( 1 + 10 ** ( 0.5 * ( elo_dict[loser1] + elo_dict[loser2] - elo_dict[winner1] - elo_dict[winner2] ) / 500 ) )
        elo_dict[winner1] += 100 * (1 - exw)
        elo_dict[winner2] += 100 * (1 - exw)
        elo_dict[loser1] -= 100 * exw
        elo_dict[loser2] -= 100 * exw
    return elo_dict

def main():

    query = input('Input new game? (y or n)')
    if query == 'y':
        game_input()
    stats_update()
    calculate_2wars()

if __name__ == '__main__':
    main()