import random

vowels = ['a','e','i','o','u']
consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z','sh','ch','ph','zh','gh']
normal_consonants = ['b','c','d','f','g','h','k','l','m','n','p','r','s','t','v','y']
doublable = ["e","c","l","p","o","s","r","z"]
government_titles = ["Nation","Clan","Horde","Republic","Kingdom","Empire","State","Federation","Confederation","Union","Tribe","Duchy","Imperium","Senate","Congress","Diarchy","Monarchy","Tetrarchy","Confederacy","House","Dynasty"]
government_adjectives = ["Union","Combined","Serene","Great","Grand","Everlasting","Eternal","United","Unified","Federated","Confederal","People's","National","Nationalist","Socialist","Communist","Holy","Plurinational"]

leadership_titles = ["Master","Ruler","Khan","President","King","Emperor","Administrator","Consul","Executive","Secretary","Chieftain","Duke","Imperator","Minister","Manager","Monarch","Leader","Commander","Father"]
leadership_modifiers = ["Grand *","Serene *","*-in-Chief","Vice-*","Arch-*","Chief *","Immortal *","Eternal *","Great *","People's *","General *","Executive *","* Regnant","Perpetual *","Holy *","Revered *","Prime *","First *"]

def generate_gibberish():
    #Generates a gibberish word by alternating between a vowel and consonant
    is_vowel = random.choice([True,False])
    word_length = random.randint(3,5)
    result = ""
    for x in range(word_length):
        if is_vowel==True:
            result+=random.choice(vowels)
        else:
            result+=random.choice(consonants)
        is_vowel = not is_vowel
    return result

def generate_palindrome():
    #Generates a palindrome(a word that is unchanged if reversed)
    pal = random.choice(normal_consonants)+random.choice(normal_consonants)
    return pal+random.choice(vowels)+pal[::-1]

def combine_fluently(part1,part2):
    #Combines two words fluently
    result = ""
    if part1[-1] in consonants and part2[0] in consonants:
        if part1[-2:] in consonants:
            result = part1[:-2]+part2
        else:
            result = part1[:-1]+part2
    elif part1[-1] in vowels and part2[0] in vowels:
        result = part1[:-2]+part2
    else:
        result = part1+part2
    return result
    
def countrify(word):
    #Turns a gibberish word into something resembling the name of a country, e.g. Uhalo --> Uhaloburgh
    result = combine_fluently(word,random.choice(["land","burgh","ia","ium","stan"]))
    return result

def demonymize(word):
    #Simply removes the last letter of the word if a vowel, and then adds a suffix that makes it a demonym. 
    result = word
    if word[-2:]=="ia":
        result = word[:-2]
    elif word[-1] in vowels:
        result = word[:-1]
    if word[-4:]=="stan":
        return random.choice([word+"i",word[:-5]+"i"])
    result+=random.choice(["ian","an","ite","er","ish","ic","ine"])
    return result

def generate_title():
    way = random.randint(1,2) #If it's 1, it'll JUST get a title, if it's 2, it will "fancy it up"
    if way==1:
        return random.choice(leadership_titles)
    if way==2:
        return random.choice(leadership_modifiers).replace("*",random.choice(leadership_titles))

def pluralize(word):
    #Make the word stated plural in a way that makes sense
    if word[-2:]=="us":
        return word[:-2]+"i"
    if word[-2:]=="um":
        return word[:-2]+"a"
    if word[-1]=="y":
        return word[:-1]+"ies"
    if word[-1]=="s" or word[-1]=="z" or word[-1]=="h":
        return word+"es"
    if word[-1]=="x":
        return word[:-1]+"ces"
    if word[-1]=="f":
        return word[:-1]+"ves"
    return word+"s"

def perturb(word):
    #Change the word up in a certain way to make it similar but different
    result = word.lower()
    if "j" in result and random.randint(1,3)==1:
        result = result.replace("j","i")
    if "q" in result and random.randint(1,3)==1:
        result = result.replace("q","k")
    if "x" in result and random.randint(1,3)==1:
        result = result.replace("x","k")
    if "k" in result and random.randint(1,3)==1:
        result = result.replace("k","c")
    if "w" in result and random.randint(1,3)==1:
        result = result.replace("w","v")
    if "f" in result and random.randint(1,3)==1:
        result = result.replace("f","ph")
    return result
    
def generate_official_name(name,demonym):
    #Generates an official name for a given name and demonym, e.g. Rome, Roman --> The Roman Empire
    name_order = random.randint(1,2) #Determines the order of the official name, e.g. whether it's the Roman Empire or the Empire of Rome
    generate_adjective = random.choice([True,False,False]) #If true, will add an adjective, e.g. The Holy Empire of Rome
    plural_government = random.choice([True,False,False,False]) #If true, will make the government plural via the pluralize function, e.g. The United StateS of America

    government = random.choice(government_titles) #The name of the Government, e.g. "Empire"
    if plural_government==True:
        government = pluralize(government)

    if name_order==1:
        if generate_adjective==True:
            return "The "+demonym+" "+random.choice(government_adjectives)+" "+government
        else:
            return "The "+demonym+" "+government
    if name_order==2:
        if generate_adjective==True:
            return "The "+random.choice(government_adjectives)+" "+government+" of "+name
        else:
            return "The "+government+" of "+name

def beautify_number(amount):
    #Adds commas in between long numbers if necessary, to make them more readable.
    pretty_number = str(amount)
    result = ""
    if len(pretty_number)>3:
        shortened = int(pretty_number)
        parts = []
        while len(str(shortened))>3:
            integer_part = str(float(shortened)/1000).split(".")[0]
            float_part = str(float(shortened)/1000).split(".")[1]
            while len(float_part)<3:
                float_part+="0"
            print(integer_part)
            print(float_part)
            parts.append(float_part)
            shortened = int(integer_part)
            print(len(str(shortened)))
        result += str(shortened)
        parts = parts[::-1]
        for i in parts:
            result+=","+i
        return result
    else:
        return pretty_number
