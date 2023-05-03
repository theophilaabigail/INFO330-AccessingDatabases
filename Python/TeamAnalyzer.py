import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()
    
# initialize team    
team = []

# connect to db
connection = sqlite3.connect('/Users/theophilasetiawan/Documents/INFO 330/HW5/INFO330-AccessingDatabases/Python/pokemon.sqlite')
table = connection.cursor()

# loop through the arguments and add them to the team list
args = sys.argv[1:]
for arg in args:
    # check if the argument is a number
    if arg.isdigit():
        # if it is, assume it's a Pokedex number
        # pokemon name
        name = table.execute('SELECT name FROM pokemon WHERE pokedex_number = ?', (arg,)).fetchone()
    else:
        # otherwise, assume it's a Pokemon name
        # pokemon name
        name = table.execute('SELECT name FROM pokemon WHERE name = ?', (arg.capitalize(),)).fetchone()
    
    # type1 and type2
    type1 = table.execute('SELECT type1 FROM pokemon_types_view WHERE name = ?', (name[0],)).fetchone()
    type2 = table.execute('SELECT type2 FROM pokemon_types_view WHERE name = ?', (name[0],)).fetchone()
    
    # against
    if type1 is not None and type2 is not None:
        against = table.execute('SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM battle WHERE type1name = ? AND type2name = ?', (type1[0], type2[0])).fetchone()
    
    # strong against and weak against
    strong_against = []
    weak_against = []
    
    for n, t in zip(against, types):
        if n > 1:
            strong_against.append(t)
        elif n < 1:
            weak_against.append(t)
    
    # add the pokemon to the team list
    team.append((name[0], type1[0], type2[0], strong_against, weak_against))

# print the team
for i, pokemon in enumerate(team):
    print(f"Analyzing {i+1}")
    print(f"{pokemon[0]} ({pokemon[1]} {pokemon[2]}) is strong against {pokemon[3]} but weak against {pokemon[4]}")

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

