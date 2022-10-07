import random
import re
# This function assigns a random name to the teams
def get_questions():
    left=[]
    right=[]
    spectrum_list=[]
    with open("app/static/txt/spectrum_bank.csv") as f:
        spectrums = f.readlines()
        for spectrum in spectrums:
            spectrum_word = spectrum.split(",")
            spectrum_list.append(spectrum_word)
        
        for i in spectrum_list:
            left.append(i[0].removesuffix('\t'))
            right_word= i[1].removesuffix('\n')
            right_nobasht=right_word.removesuffix('\t')
            right.append(right_nobasht.removeprefix('\t'))

        all_spectrums = list(zip(left, right))

        return all_spectrums

# print(get_questions())
data = get_questions()

for spectrum in data:
    print(spectrum[0])
    print(spectrum[1])


# # ################################## Exists #######################################
# # This function assigns a random name to the teams
# def random_name():
#     # open the file
#     with open("app/static/txt/team_names.csv") as f:
#         # Assigns all the lines
#         name_list = f.readlines()
#         # Random assignation of a single name from the list
#         new_name = name_list[random.randint(0,len(name_list))]
#     # Returns a new randome name
#     return new_name
# ####################################################################################

# # This function assignes the players to the teams, taking the number of possible teams and the amount of players as arguments
# def get_teams(team_names, players):
#     # randomly shuffles all the players
#     randomly_ordered_players = random.sample(players, len(players))
#     # stores the number of possible teams
#     number_of_teams = len(team_names)

#     return {
#         # Returns a list of players randomly assigned to the team index 
#         # Slice the information into team with random name as first value and then seperates it by ":" 
#         # and assigns as many players as they can fit per team [first player:second:third:team_number]
#         team_names[i]: randomly_ordered_players[i::number_of_teams]
#         for i in range(number_of_teams)
#     }

# # open the random list of players
# with open("app/static/txt/player_names.csv") as file:
#     p = file.readlines()

# #Cleaning the name by iterating into the list and removing the "\n"
# players =[]
# for i in p:
#     # removing the suffix('\n')
#     players.append(i.removesuffix("\n"))

# # Calculating the amount of teams and distributions
# # number of players/4 players per team and +1 to round number
# number_of_teams = int(len(players)/4) +1
# team_mates = int(len(players)/number_of_teams)

# print("players = "+str(len(players)))
# print("teams =" +str(number_of_teams))

# team_names=[]
# for i in range(0,number_of_teams):
#     name = random_name()
#     # print(name)
#     team_names.append(name.removesuffix("\n"))

# teams = get_teams(team_names, players)
# for team_nm, playing in teams.items():
#     print(team_nm)
#     # print(p for p in playing)
#     print(v for v in playing)

# print("##############################################")
# # print(teams)
