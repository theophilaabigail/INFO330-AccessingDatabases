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

team = []

    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

connection = sqlite3.connect('/Users/maansisurve/Desktop/INFO330/INFO330-AccessingDatabases/pokemon.sqlite')
table = connection.cursor()

for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    table.execute('SELECT name FROM imported_pokemon_data WHERE pokedex_number = ?', (arg,))
    name = table.fetchone()

    # EXTRA CREDIT
    table.execute('SELECT pokedex_number FROM imported_pokemon_data WHERE name = ?', (arg,))
    number = table.fetchone()

    table.execute('SELECT type1 FROM imported_pokemon_data WHERE pokedex_number = ?', (arg,))
    type1 = table.fetchone()

    # EXTRA CREDIT
    table.execute('SELECT type1 FROM imported_pokemon_data WHERE name = ?', (arg,))
    ec_type1 = table.fetchone()

    table.execute('SELECT type2 FROM imported_pokemon_data WHERE pokedex_number = ?', (arg,))
    type2 = table.fetchone()

    table.execute('SELECT type2 FROM imported_pokemon_data WHERE name = ?', (arg,))
    ec_type2 = table.fetchone()

    strong_values = []
    for type in types:
        table.execute(f"SELECT against_{type} FROM imported_pokemon_data WHERE against_{type} > 1 AND pokedex_number = ?", (arg,))
        collection = table.fetchall()

        if collection:
            strong_values.append(type)

    # EXTRA CREDIT
    strong_valuesA = []
    for type in types:
        table.execute(f"SELECT against_{type} FROM imported_pokemon_data WHERE against_{type} > 1 AND name = ?", (arg,))
        collection = table.fetchall()

        if collection:
            strong_valuesA.append(type)

    weak_values = []
    for type in types:
        table.execute(f"SELECT against_{type} FROM imported_pokemon_data WHERE against_{type} < 1 AND pokedex_number = ?", (arg,))
        collection = table.fetchall()

        if collection:
            weak_values.append(type)

    # EXTRA CREDIT
    weak_valuesA = []
    for type in types:
        table.execute(f"SELECT against_{type} FROM imported_pokemon_data WHERE against_{type} < 1 AND name = ?", (arg,))
        collection = table.fetchall()

        if collection:
            weak_valuesA.append(type)

    if type1 and type2 and name and strong_values and weak_values:
        print(f"Analyzing {arg}")
        print(f"{name[0]} ({type1[0]} {type2[0]}) is strong against {strong_values} but weak against {weak_values}")
    elif ec_type1 and ec_type2 and number and strong_valuesA and weak_valuesA: # EXTRA CREDIT
        print(f"Analyzing {number[0]}")
        print(f"{arg} ({ec_type1[0]} {ec_type2[0]}) is strong against {strong_valuesA} but weak against {weak_valuesA}")
    else:
        print(f"Pokedex number {arg} not found.")

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")
