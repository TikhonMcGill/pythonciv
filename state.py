from naming import *
import math

class State:
    def __init__(self):
        self.controller = 1 #The "controller" of the nation - 0 = player, 1 = AI, 2 = The Nation is "Dead" and ready to be deleted from the Game on the next turn
        self.population = 100 #The population of the nation
        self.manpower = 0 #The "manpower" of the nation - the military-capable population, because you can't have a civilization game without war!
        self.food = 1000 #The amount of food the nation has stored
        self.money = 10000 #The amount of money the nation has
        self.farms = 0 #The amount of farms the nation has - each produces 10 food per turn
        self.banks = 0 #The amount of banks the nation has - each one produces 100 money per turn
        self.firms = 0 #The amount of building firms the nation has - each one produces either a farm or bank per turn
        self.businesses = 0 #The amount of businesses the nation has - each one produces a firm per turn
        self.food_research = 0 #The level of food research - each level provides 1% to food output per turn
        self.money_research = 0 #The level of money research - each level provides 1% to money output per turn
        
        self.name = ""
        self.demonym = ""
        self.official_name = ""
        self.leadership_title = ""
        self.currency = ""

    def game_over(self):
        print("IT IS THE END OF "+self.official_name.upper()+"! THE "+self.leadership_title.upper() + " HAS "+random.choice(["PERISHED","ESCAPED","GONE INTO EXILE","BEEN MURDERED","BEEN OVERTHROWN"])+"!")
        
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
        if self.population<=0:
            self.game_over()
        else:
            population_growth = math.ceiltoint(self.population * 1.01)
            manpower_growth = math.floortoint(math.sqrt(population_growth))
            population_growth -= manpower_growth

            if self.food<=0:
                self.food = 0
                population_growth = 0
                manpower_growth = 0

            self.population += population_growth
            self.manpower += manpower_growth

            self.food+=int(self.farms * 10 * (1+ 0.01 * food_research))
            self.money+=int(self.banks * 100 * (1 + 0.01*money_research))
            self.farms += mathf.ceiltoint(self.firms/2)
            self.banks += mathf.floortoint(self.firms/2)
            self.firms += self.businesses

    def get_food_research_cost():
        cost = 1.5 ** self.food_research
        cost = cost * 100
        cost = int(cost)
        return cost

    def get_money_research_cost():
        cost = 1.75 ** self.money_research
        cost = cost * 100
        cost = int(cost)
        return cost

    def state_print(self,text):
        if self.state==0:
            print(text)

    def get_currency(self):
        return self.demonym+" "+pluralize(self.currency)

    def build_building(building):
        building = building.lower()
        if building=="farm":
            if self.money>=1000:
                self.money -= 1000
                self.state_print("A farm has been built!")
                self.farms+=1
            else:
                self.state_print("You cannot afford a farm - it costs 1000 "+get_currency()+", but you only have "+beautify_number(self.money)+"!")
        elif building=="bank":
            if self.money>=1000:
                self.money -= 1000
                self.state_print("A bank has been constructed!")
                self.banks+=1
            else:
                self.state_print("You cannot afford a bank - it costs 1000 "+get_currency()+", but you only have "+beautify_number(self.money)+"!")
        elif building=="firm":
            if self.money>=10000:
                self.money -= 10000
                self.state_print("A building firm has been constructed!")
                self.firms += 1
            else:
                self.state_print("You cannot afford a building firm - it costs 10,000 "+get_currency()+", but you only have "+beautify_number(self.money)+"!")
        elif building=="business":
            if self.money>=1000000:
                self.money -= 1000000
                self.state_print("A business has been founded!")
                self.businesses += 1
            else:
                self.state_print("You cannot afford a business - it costs 1,000,000 "+get_currency()+", but you only have "+beautify_number(self.money)+"!")
        else:
            self.state_print("A "+building+"? Never heard of it, "+self.leadership_title+".")
            
    def take_turn(self):
        commands = []
        buildables = []
        researchables = []
        command = ""
        if self.money>=1000:
            buildables+=["farm","bank"]
        if self.money>=10000:
            buildables.append("firm")
        if self.money>=1000000:
            buildables.append("business")
        if self.money>=get_food_research_cost():
            researchables.append("food")
        if self.money>=get_money_research_cost():
            researchables.append("money")
        if len(buildables)>0 or self.state==0:
            commands.append("build")
        if len(researchables)>0 or self.state==0:
            commands.append("research")
        if self.state==0:
            pass
        else:
            if self.money>=1000000:
                command = "build firm"
            elif self.money>=10000:
                command = "build business"
            else:
                command = random.choice(commands)
