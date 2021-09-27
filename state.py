from naming import *
from relation import *
import math

command_explanation_dictionary = {
    "build" : "Construct a building",
    "research" : "Research a field, gaining certain bonuses",
    "help" : "You're using this command now!",
    "info" : "Show information about the nation",
    "war" : "Declare war on a foreign nation",
    "invade" : "Invade a nation you're at war with",
    "rename" : "Rename aspects of your nation",
    "demobilize" : "Turn your combat-ready people into regular civilians"
}

class State:

    states = []
    
    def do_invasion(invader,defender):
        invader_power = random.randint(0,invader.manpower)
        defender_power = random.randint(0,defender.manpower)
        defender.state_print(defender.leadership_title+" of "+defender.official_name+", we are being invaded by "+invader.official_name+"!")

        invader_civilian_losses = 0
        defender_civilian_losses = 0

        invader.manpower -= defender_power
        defender.manpower -= invader_power

        if defender.manpower<0:
            defender.manpower = 0
            defender.population -= defender.manpower * 10

        if invader.manpower<0:
            invader.manpower = 0
        
        if invader_power>defender_power:
            invader.state_print(invader.leadership_title+", we are victorious! Hail "+invader.official_name+"!")
            State.annex(invader,defender)
        else:
            invader.state_print(invader.leadership_title+", our invasion was repelled!")
        
    def annex(perpetrator,victim):
        perpetrator.population+=victim.population
        perpetrator.scientists+=random.randint(0,victim.scientists)
        perpetrator.food+=victim.food
        perpetrator.money+=victim.money
        perpetrator.farms+=victim.farms
        perpetrator.banks+=victim.banks
        perpetrator.firms+=victim.firms
        perpetrator.businesses+=victim.businesses
        perpetrator.food_research = max(perpetrator.food_research,victim.food_research)
        perpetrator.money_research = max(perpetrator.money_research,victim.money_research)
        print(perpetrator.official_name+" has invaded and annexed "+victim.official_name+"!")
        victim.game_over()

    def has_relation(self,other,name):
        for i in self.diplomatic_relations:
            if ((i.receiver==self and i.giver==other) or (i.giver==self and i.receiver==other)) and i.name==name:
                return True
        return False
    
    def __init__(self):
        self.controller = 1 #The "controller" of the nation - 0 = player, 1 = AI, 2 = The Nation is "Dead" and ready to be deleted from the Game on the next turn
        self.population = 100 #The population of the nation
        self.manpower = 0 #The "manpower" of the nation - the military-capable population, because you can't have a civilization game without war!
        self.scientists = 0 #The "scientist" population of the nation - each scientist provides 1 unit of food or money research randomly - note, they appear VERY late in game!
        self.food = 1000 #The amount of food the nation has stored
        self.money = 10000 #The amount of money the nation has
        self.farms = 1 #The amount of farms the nation has - each produces 10 food per turn
        self.banks = 1 #The amount of banks the nation has - each one produces 100 money per turn
        self.firms = 0 #The amount of building firms the nation has - each one produces either a farm or bank per turn
        self.businesses = 0 #The amount of businesses the nation has - each one produces a firm per turn
        self.food_research = 0 #The level of food research - each level provides 1% to food output per turn
        self.money_research = 0 #The level of money research - each level provides 1% to money output per turn
        
        self.name = ""
        self.demonym = ""
        self.official_name = ""
        self.leadership_title = ""
        self.currency = ""
        self.turn_finished = False
        self.diplomatic_relations = []

        State.states.append(self)

    def game_over(self):
        print("IT IS GAME OVER FOR "+self.official_name.upper()+"! THE "+self.leadership_title.upper() + " HAS "+random.choice(["PERISHED","ESCAPED","GONE INTO EXILE","BEEN MURDERED","BEEN OVERTHROWN"])+"!")
        self.controller = 2
        for i in self.diplomatic_relations:
            relation_loser = i.get_other_side(self)
            if i in relation_loser.diplomatic_relations:
                relation_loser.diplomatic_relations.remove(i)
        State.states.remove(self)

    def add_namings(self,name,demonym,official_name,leadership_title,currency):
        self.name = name
        self.demonym = demonym
        self.official_name = official_name
        self.leadership_title = leadership_title
        self.currency = currency

    def generate_namings(self,name,demonym):
        self.name = name
        self.demonym = demonym
        self.official_name = generate_official_name(name,demonym)
        self.leadership_title = generate_title()
        self.currency = generate_gibberish().capitalize()

    def generate_random_name(self):
        self.name = countrify(generate_gibberish().capitalize())
        self.demonym = demonymize(self.name)
        self.official_name = generate_official_name(self.name,self.demonym)
        self.leadership_title = generate_title()
        self.currency = generate_gibberish().capitalize()

    def set_base_values(self,population,food,money):
        self.population = population
        self.food = food
        self.money = money

    def set_buildings(farms,banks,firms,businesses):
        self.farms = farms
        self.banks = banks
        self.firms = firms
        self.businesses = businesses

    def set_research(food,money):
        self.food_research = food
        self.money_research = money

    def print_namings(self):
        print("All hail "+self.official_name+"!")
        print("Our "+self.leadership_title+" greets you!")
        print("We have lots of "+self.demonym+" "+pluralize(self.currency)+" in our coffers!")

    def iterate_values(self):
        if self.controller!=2:
            if self.population<=0:
                self.game_over()
            else:
                self.turn_finished = False

                self.food -= self.population
                self.food -= (self.manpower * 3)
                self.food -= (self.scientists * 4)
                
                if self.food<=0:
                    self.food = 0
                    population_growth = math.ceil(self.population * 0.9) - self.population
                    manpower_growth = -50
                    scientist_growth = -10
                else:
                    population_growth = math.ceil(self.population * 1.01) - self.population + 1
                    manpower_growth = math.floor(math.sqrt(population_growth)/10) - 1
                    scientist_growth = math.floor(int(population_growth ** (1/5))/100) - 1
                    population_growth -= manpower_growth

                self.population += population_growth
                self.manpower += manpower_growth
                self.scientists += scientist_growth

                if self.manpower<0:
                    self.manpower = 0
                if self.scientists<0:
                    self.scientists = 0

                self.food+=int(self.farms * 10 * (1+ 0.01 * self.food_research))
                self.money+=int(self.banks * 100 * (1 + 0.01 * self.money_research))
                
                self.farms += math.ceil(self.firms/2)
                self.banks += math.floor(self.firms/2)
                self.firms += self.businesses

                self.food_research += math.ceil(self.scientists/2)
                self.money_research += math.floor(self.scientists/2)

    def get_food_research_cost(self):
        cost = 2 ** self.food_research
        cost = cost * 100
        cost = int(cost)
        return cost

    def get_money_research_cost(self):
        cost = 3 ** self.money_research
        cost = cost * 100
        cost = int(cost)
        return cost

    def state_print(self,text):
        if self.controller==0:
            print(text)

    def get_currency(self):
        return self.demonym+" "+pluralize(self.currency)

    def build_building(self,building):
        building = building.lower()
        if building=="farm":
            if self.money>=1000:
                self.money -= 1000
                self.state_print("A farm has been built!")
                self.farms+=1
                self.turn_finished = True
            else:
                self.state_print("You cannot afford a farm - it costs 1000 "+self.get_currency()+", but you only have "+beautify_number(self.money)+"!")
        elif building=="bank":
            if self.money>=1000:
                self.money -= 1000
                self.state_print("A bank has been constructed!")
                self.banks+=1
                self.turn_finished = True
            else:
                self.state_print("You cannot afford a bank - it costs 1000 "+self.get_currency()+", but you only have "+beautify_number(self.money)+"!")
        elif building=="firm":
            if self.money>=10000:
                self.money -= 10000
                self.state_print("A building firm has been constructed!")
                self.firms += 1
                self.turn_finished = True
            else:
                self.state_print("You cannot afford a building firm - it costs 10,000 "+self.get_currency()+", but you only have "+beautify_number(self.money)+"!")
        elif building=="business":
            if self.money>=1000000:
                self.money -= 1000000
                self.state_print("A business has been founded!")
                self.businesses += 1
                self.turn_finished = True
            else:
                self.state_print("You cannot afford a business - it costs 1,000,000 "+self.get_currency()+", but you only have "+beautify_number(self.money)+"!")
        else:
            self.state_print("A "+building+"? Never heard of it, "+self.leadership_title+".")

    def do_research(self,typ):
        typ=typ.lower()
        if typ=="food":
            cost = self.get_food_research_cost()
            if self.money>=cost:
                self.money-=cost
                self.food_research+=1
                self.turn_finished = True
            else:
                self.state_print("You cannot afford to research food - it costs "+beautify_number(self.get_food_research_cost())+" "+self.get_currency()+", but you only have "+beautify_number(self.money)+"!")
        elif typ=="money":
            cost = self.get_money_research_cost()
            if self.money>=cost:
                self.money-=cost
                self.money_research+=1
                self.turn_finished = True
            else:
                self.state_print("You cannot afford to research money - it costs "+beautify_number(self.get_money_research_cost())+" "+self.get_currency()+", but you only have "+beautify_number(self.money)+"!")
        else:
            self.state_print(typ.capitalize()+"? I've never heard of that scientific field, "+self.leadership_title+".")
            
    def take_turn(self):
        if self.controller!=2:
            commands = []
            buildables = []
            researchables = []
            invadables = {}
            command = ""
            if self.money>=1000:
                buildables+=["farm","bank"]
            if self.money>=10000:
                buildables.append("firm")
            if self.money>=1000000:
                buildables.append("business")
            if self.money>=self.get_food_research_cost():
                researchables.append("food")
            if self.money>=self.get_money_research_cost():
                researchables.append("money")
            for i in self.diplomatic_relations:
                if i.name=="war":
                    invadables[i.get_other_side(self).official_name] = i.get_other_side(self)
            if len(buildables)>0:
                commands.append("build")
            if len(researchables)>0:
                commands.append("research")
            if self.manpower>100 and (len(State.states)>1):
                commands.append("war")
            if len(invadables)>0:
                commands.append("invade")
            if self.manpower>0:
                commands.append("demobilize")
            if self.controller==0:
                commands.append("info")
                commands.append("help")
                commands.append("rename")
            else:
                commands.append("")
            while not self.turn_finished:
                if self.controller==0:
                    command = input("Enter your command, "+self.leadership_title+"(enter \"help\" for a list of available commands):")
                else:
                    if self.money>=1000000 and random.randint(1,2)==1:
                        command = "build business"
                    elif self.money>=10000 and random.randint(1,2)==1:
                        command = "build firm"
                    else:
                        command = random.choice(commands)
                command = command.replace(" ","")
                if "build" in command and "build" in commands:
                    command = command.replace("build","")
                    if "farm" in command:
                        self.build_building("farm")
                    elif "bank" in command:
                        self.build_building("bank")
                    elif "firm" in command:
                        self.build_building("firm")
                    elif "business" in command:
                        self.build_building("business")
                    else:
                        if self.controller==0:
                            print("Here are the buildings you can afford to build:")
                            for i in buildables:
                                print(i)
                            building = input("Enter the building you want to build:")
                            self.build_building(building)
                        else:
                            self.build_building(random.choice(buildables))
                elif "research" in command and "research" in commands:
                    command = command.replace("research","")
                    if "food" in command:
                        self.do_research("food")
                    elif "money" in command:
                        self.do_research("money")
                    else:
                        if self.controller==0:
                            print("Here are the fields you can afford to research:")
                            for i in researchables:
                                print(i)
                            research = input("Enter the field you want to research:")
                            self.do_research(research)
                        else:
                            self.do_research(random.choice(researchables))
                elif "help" in command:
                    print("Gladly, "+self.leadership_title+"!")
                    print("\n")
                    for i in commands:
                        print(i + " - "+command_explanation_dictionary[i])
                elif "info" in command:
                    print("Here is some information about "+self.official_name+", "+self.leadership_title+":")
                    print("\n")
                    print("We have a population of "+beautify_number(self.population)+" "+pluralize(self.demonym)+". They will consume "+beautify_number(self.population)+" units of food per turn!")
                    if self.manpower>0:
                        print("We also have "+beautify_number(self.manpower)+" combat-ready people, ready to defend "+self.name+"! They will consume "+beautify_number(self.manpower*3)+" units of food per turn!")
                    if self.scientists>0:
                        print("There are "+beautify_number(self.scientists)+" scientifically-astute people in "+self.name+". Per turn, they will produce "+beautify_number(math.ceil(self.scientists/2))+" levels of food research per turn, and "+beautify_number(math.floor(self.scientists/2))+" levels of money research per turn.")
                        print("They will, however, consume "+beautify_number(self.scientists*4)+" units of food per turn!")
                    print("There are "+beautify_number(self.food)+" units of food stored in our stockpiles.")
                    print("Our treasury holds "+beautify_number(self.money)+" "+self.get_currency()+".")
                    print("\n")
                    print("We have "+beautify_number(self.farms)+" farms. They will provide "+beautify_number(self.farms*10)+" units of food per turn!")
                    print("We have "+beautify_number(self.banks)+" banks. They will provide "+beautify_number(self.banks*100)+" "+self.get_currency()+" per turn!")
                    if self.firms>0:
                        print("We have "+beautify_number(self.firms)+" building firms. They will build "+beautify_number(math.ceil(self.firms/2))+" farms and "+beautify_number(math.floor(self.firms/2))+" banks per turn!")
                    if self.businesses>0:
                        print("We have "+beautify_number(self.businesses)+" businesses. They will build "+beautify_number(self.businesses)+" building firms per turn!")      
                    print("\n")
                    print("We have "+beautify_number(self.food_research)+" levels of research in the food field. This gives us a "+beautify_number(self.food_research)+"% bonus to all food produced by farms!")
                    print("We have "+beautify_number(self.money_research)+" levels of research in the money field. This gives us a "+beautify_number(self.money_research)+"% bonus to all money generated by banks!")
                elif "invade" in command and "invade" in commands:
                    if self.controller==0:
                        print("Here are the nations we can invade:")
                        for i in list(invadables.keys()):
                            print(i)
                        invasion = input("Enter the name of the nation you want to invade, "+self.leadership_title+":")
                    else:
                        invasion = random.choice(list(invadables.keys()))
                    if invasion in list(invadables.keys()):
                        State.do_invasion(self,invadables[invasion])
                        self.turn_finished = True
                    else:
                        self.state_print(invasion+"? That must be a fictional nation, "+self.leadership_title+".")
                elif "war" in command and "war" in commands:
                    victim = ""
                    if self.controller==0:
                        country_dictionary = {}
                        for i in State.states:
                            if self.has_relation(i,"war")==False and i!=self:
                                country_dictionary[i.official_name] = i
                        for i in list(country_dictionary.keys()):
                            print(i)
                        choice = input("Enter the nation you wish to invade, "+self.leadership_title+":")
                        if choice in list(country_dictionary.keys()):
                            victim = country_dictionary[choice]
                    else:
                        victim = random.choice(State.states)
                        while victim==self or self.has_relation(victim,"war"):
                            victim = random.choice(State.states)
                    if victim!="":
                        victim.state_print(victim.leadership_title+" of "+victim.official_name+"! "+self.official_name+" declared war on us!")
                        r = Relation(self,victim)
                        r.name = "war"
                        self.turn_finished = True
                elif "rename" in command:
                    def yes_no(text):
                        answer = input(text)
                        if "ye" in answer:
                            return True
                        return False
                    if yes_no("Change the name of your nation?")==True:
                        self.name = input("Enter the new name of your nation:")
                    if yes_no("Change the demonym of your nation?")==True:
                        self.demonym = input("Enter the new demonym of your nation:")
                    if yes_no("Change the official name of your nation?")==True:
                        self.official_name = input("Enter your nation's new official name:")
                    if yes_no("Change the leadership title of your nation?")==True:
                        self.leadership_title = input("Enter your nation's new leadership title:")
                    if yes_no("Change the currency name of your nation?")==True:
                        self.currency = input("Enter your nation's new currency name:")
                elif "demobilize" in command and "demobilize" in commands:
                    self.state_print(str(self.manpower)+" "+self.demonym+" soldiers have been demobilized into the citizen population!")
                    self.population+=self.manpower
                    self.manpower = 0
                elif command=="":
                    self.turn_finished = True
                if self.controller==0:
                    print("\n")
