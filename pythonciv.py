#Tikhon the Great's PythonCivilization!

from state import *

def iinput(text,default_value):
    try:
        return int(input(text))
    except:
        return default_value

player_number = iinput("Enter the number of player-controlled nations:",1)

for p in range(player_number):
    new_state = State()
    new_state.controller = 0
    randomize = input("Do you want to randomize your nation's name?")
    if "ye" in randomize.lower():
        new_state.generate_random_name()
    else:
        country_name = input("Enter the name of your nation:")
        country_demonym = input("Enter the demonym of your nation(leave blank to automatically generate one):")
        if country_demonym=="":
            country_demonym = demonymize(country_name)
        country_official_name = input("Enter the official name of your nation(e.g. \"The X-an Empire\" - leave blank to generate a random one):")
        if country_official_name=="":
            country_official_name = generate_official_name(country_name,country_demonym)
        country_leadership_title = input("Enter the leadership title of your nation(e.g. The Emperor - leave blank to generate a random title):")
        if country_leadership_title=="":
            country_leadership_title = generate_title()
        country_currency = input("Enter the currency of your nation(e.g. Ruble - leave blank to generate a random currency):")
        if country_currency=="":
            country_currency = perturb(generate_gibberish()).capitalize()
        new_state.add_namings(country_name,country_demonym,country_official_name,country_leadership_title,country_currency)

ai_number = iinput("Enter the number of computer-controlled nations:",1)

for p in range(ai_number):
    new_state = State()
    new_state.generate_random_name()

turn = 1

while len(State.states)>1:
    print("THERE ARE "+str(len(State.states))+" NATIONS REMAINING!")
    for i in State.states:
        i.iterate_values()
        i.take_turn()
    turn+=1

input(State.states[0].official_name+" is Eternally Victorious! Glory to the "+State.states[0].leadership_title+" of "+State.states[0].name+"!")
