from naming import *
import math

class State:
    def __init__(self):
        self.controller = 1 #The "controller" of the nation - 0 = player, 1 = AI
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
