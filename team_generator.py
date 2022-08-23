import random


def random_name():
    # open the file
    with open("app/static/txt/team_names.csv") as f:
        # Assigns all the lines
        name_list = f.readlines()
        # Random assignation of a single name from the list
        new_name = name_list[random.randint(0,len(name_list))]
    # Returns a new randome name
    return new_name

def get_teams(team_names, players):
    randomly_ordered_players = random.sample(players, len(players))
    number_of_teams = len(team_names)
    return {
        team_names[i]: randomly_ordered_players[i::number_of_teams]
        for i in range(number_of_teams)
    }


with open("app/static/txt/player_names.csv") as file:
    p = file.readlines()

players =[]
for i in p:
    players.append(i.removesuffix("\n"))

number_of_teams = int(len(players)/4) +1
team_mates = int(len(players)/number_of_teams)

print("players = "+str(len(players)))
print("teams =" +str(number_of_teams))

team_names=[]
for i in range(0,number_of_teams):
    name = random_name()
    print(name)
    team_names.append(name.removesuffix("\n"))

teams = get_teams(team_names, players)

print("##############################################")

