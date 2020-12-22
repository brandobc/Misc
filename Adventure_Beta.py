"""
Author: Brandon James Curl
Contact: brandoncurl@utexas.edu
Date: 20-Dec-2020
Version: 3.2
"""

from sys import exit
from math import ceil
from random import randint

items = {
"Ashbringer": [1000, 0, 100],
"sword": [220, 300, 30],
"axe": [120, 200, 20],
"shovel": [20, 100, 10],
"stick": [1, 5, 5],
"fists": [0, 0, 2],
"diamond": [2000, 0, 100],
"platinum": [350, 500, 50],
"gold": [150, 300, 40],
"silver": [50, 75, 30],
"bronze": [15, 25, 10],
"leather": [5, 0, 2],
"food": [0, 5, 10],
"golden egg": [500, 0, 0]
}

weapon_types = ['Ashbringer', 'sword', 'axe', 'shovel', 'stick', 'fists']

armour_types = ['leather', 'bronze', 'silver', 'gold', 'platinum', 'diamond']

player = {
"item_level": 4,
"life_points": 100,
"gold": 10,
"food": 1,
"weapon": "fists",
"armour": "leather",
"bag": []
}

first_drink = True
wolf_count = 0
gone_to_prision = False

def report():
    print(f"""
    Life Points: \t{player['life_points']}
    Gold: \t\t{player['gold']}
    Item Level: \t{player['item_level']}
    Weapon: \t\t{player['weapon']}
    Armour: \t\t{player['armour']}
    Bag: \t\t{player['bag']}
    Food: \t\t{player['food']} piece(s) of bread
    """)

def play():

    while True:
        report()

        print("""
        What would you like to do?
        1. Go on an Adventure
        2. Visit the Merchant
        3. Eat Food
        4. Change Gear
        5. Quit
        """)

        choice = input('> ')

        if choice == '1':
            adventure()

        elif choice == '2':
            merchant()

        elif choice == '3':
            eat_food()

        elif choice == '4':
            change_gear()

        elif choice == '5':
            exit(0)

        else:
            print('Please enter a number.')

def set_item_level():
    global player
    player['item_level'] = items.get(player['weapon'])[2] + items.get(player['armour'])[2]

def adventure():
    print("""
    Select an adventure to go on!
    1. Woods
    2. Cave
    3. Prison
    4. Witch's House
    5. Dungeon
    6. King's Palace
    """)
    choice = input("> ")

    if choice == '1':
        woods()

    elif choice == '2':
        cave()

    elif choice == '3':
        prison()

    elif choice == '4':

        if player['item_level'] >= 50:
            witch()

        else:
            print("As you approach the witch's house, you hear the murmurs of the dead. It frightens you so much, you run back home. Perhaps you should come back after facing lesser foes.")
            input()
            adventure()

    elif choice == '5':

        if player['item_level'] >= 60:
            dungeon()

        else:
            print("The roar of a magnificent beast shakes the slick stairs leading to the dungeon. You fall down the stairs straight into the sewer. Perhaps you should come back with some better footwork.")
            input()
            adventure()

    elif choice == '6':

        if player['item_level'] >= 70:
            king()

        else:
            print("You journey to the King's Palace, but you are laughed away by the King's men. They jeer, \"Look at this fool! Has he come to try out for the next jester?\" You walk home dejected.")
            input()
            adventure()

    else:
        print("I didn't quite get that.")
        adventure()

def fight(creature):
    global player

    if player['item_level'] >= creature['item_level'] and player['life_points'] >= creature['life_points']:
        damage = ceil((90/player['life_points'])*(creature['item_level']/player['item_level'])*creature['difficulty']/2)
        player['life_points'] -= damage
        print(f"Congratulations! You have beaten {creature['name']}, but have suffered {damage} damage.")
        input()
        return True

    else:
        lose(creature)

def beat(creature):
    global player
    print(f"You loot {creature['gold_loot']} gold.")
    input()
    player['gold'] += creature['gold_loot']

    if creature['loot']:
        for i in creature['loot']:
            loot(i)
            input()

def lose(creature):
    global player
    damage = ceil((90/player['life_points'])*(creature['item_level']/player['item_level'])*creature['difficulty'])
    print(f"You have lost to the {creature['name']} and have sustained {damage} damage.")
    input()
    player['life_points'] -= damage

    check_death(creature['death statement'])

def woods():
    global player
    global wolf_count
    print("As you wander through the dark woods, you hear a howl in the distance. Do you want to fight the wolf or scavenge around for supplies?")
    choice = input('> ')

    if 'fight' in choice or 'wolf' in choice:
        wolf = {'name': 'wolf', 'item_level': 7, 'life_points': 50, 'gold_loot': 25, 'loot': [], 'difficulty': 6.7, 'death statement': "The wolf overpowers you and rips off chunks of flesh. You succumb to your injuries."}
        if fight(wolf):
            beat(wolf)
            wolf_count += 1

            if wolf_count >= 3:
                if randint(0,4) == 0:
                    print("As you leave the woods to return home, a gang of bandits robs you and steals all of your gold!")
                    input()
                    player['gold'] = 0


    elif 'scav' in choice or 'supp' in choice:
        loot('stick')
        gold_loot = randint(0, 5)
        print(f"You have also found {gold_loot} gold in the woods!")
        input()
        player['gold'] += gold_loot

    else:
        print("I didn't quite get that.")
        woods()

def cave():
    global player
    print("As you creep into the cave, you feet begin to stick to the ground. Suddenly, a spider comes out of the darkness and stares at you. Do you want to fight or flee?")
    choice = input('> ')
    reset = player['life_points']

    if 'fight' in choice or 'spider' in choice:
        spider = {'name': 'spider', 'item_level': 15, 'life_points': 65, 'gold_loot': 10, 'loot': ['shovel'], 'difficulty': 18, 'death statement': "The spider injects its venom in you, and your heart stops."}
        if fight(spider):
            print("Would you like to loot the body of the spider and run or smash the spider's eggs?")
            choice = input('> ')

            if 'loot' in choice or 'body' in choice:
                beat(spider)

            elif 'smash' in choice or 'egg' in choice:
                husband()

            else:
                print("I did not understand what you typed, so this encounter has been reset.")
                player['life_points'] = reset
                input()

    elif 'flee' in choice:
        print("As you run away, you sustain 5 damage.")
        input()
        player['life_points'] -= 5

    else:
        print("I didn't quite get that.")
        cave()

def husband():
    global player
    print("The spider's husband starts running at you. While he is smaller than his mate, he is still a formidible foe. Do you want to flee or fight?")
    choice = input('> ')

    if 'fight' in choice:
        husband = {'name': 'male spider', 'item_level': 15, 'life_points': 59, 'gold_loot': 0, 'loot': ['shovel', 'silver'], 'difficulty': 37, 'death statement': "You were greedy."}
        if fight(husband):
            beat(husband)

    elif 'flee' in choice:
        print("As you run away, you sustain 5 damage.")
        input()
        player['life_points'] -= 5

    else:
        print("I didn't quite get that.")
        husband()

def prison():
    global player
    global gone_to_prision

    if gone_to_prision:
        print("There is nothing left to do at the prison.")
        input()
        return

    print("As you walk into the prison, a gang surrounds you. The alpha of the pack smiles reavling many missing teeth, and they all start attacking you at the alpha's whistle.")
    alpha = {'name': 'alpha prisoner', 'item_level': 30, 'life_points': 70, 'gold_loot': 30, 'loot': ['axe'], 'difficulty': 28, 'death statement': "The prisoners pull out their shanks and knife you to death. You don't even want to know what they do with your corpse after..."}
    input()
    reset = player['life_points']

    if fight(alpha):
        print("After beating the prisoners, you can either loot the alpha or have a look around.")
        choice = input('> ')

        if 'loot' in choice or 'alpha' in choice:
            beat(alpha)

        elif 'look' in choice or 'around' in choice:
            print("You see a prison guard assaulting of one of the prisoners. Do you report him or extort him?")
            choice = input('> ')

            if 'report' in choice:
                print("The officers of the prison thank you greatly for your service. They award you 200 gold and allow you to take the loot from the alpha prisoner.")
                input()
                player['gold'] += 200
                beat(alpha)

            elif 'extort' in choice:
                print("The guard gives you 20 gold and his silver armour to keep you quiet.")
                input()
                player['gold'] += 20
                loot('silver')

            else:
                print("I did not understand what you typed, so this encounter has been reset.")
                player['life_points'] = reset
                input()
                return

        else:
            print("I did not understand what you typed, so this encounter has been reset.")
            player['life_points'] = reset
            input()
            return

        gone_to_prision = True

def witch():
    global player
    global first_drink
    print("As you enter the witch's house, a beautiful lady with ruby red eyes greets you. She asks you to try out a special potion of hers. Do you want to drink the potion, fight the witch, or try to seduce her?")
    choice = input('> ')

    if 'seduce' in choice:
        print("The witch gives it a shot, but apparently, you were not good at all. She is very dissatisfied and curses you with a hex. This puts your life points at 1.")
        input()
        player['life_points'] = 1

    elif 'drink' in choice or 'potion' in choice:
        if first_drink:
            print("You hesitantly drink the potion, but nothing happens. Frustrated, the witch works on a new potion but pays you 700 gold for partaking in her clinical trial.")
            input()
            player['gold'] += 700
            first_drink = False

        else:
            player['life_points'] = -1000000000
            check_death("\"Ahh, I see you've come back for a second drink,\" the witch exclaims. She confidently pours the potion down your throat, and you begin hallucinating. When you come to, you are in the underworld. Apparetly, she fixed her potion.")

    elif 'fight' in choice:
        witch_2 = {'name': 'witch', 'item_level': 50, 'life_points': 70, 'gold_loot': 80, 'loot': ['gold', 'sword'], 'difficulty': 40, 'death statement': "The witch reaches her hand into your chest and pulls out your beating heart. Well, at least it WAS beating."}
        if fight(witch_2):
            beat(witch_2)

    else:
        print("I didn't quite get that.")
        witch()

def dungeon():
    global player
    print("As you creep into the dungeon, you get lost in its maze. Everntually, you wander into a room with an exit. As you go to leave, a dragon flies down from its nest and breathes fire around you. You begin to fight.")
    dragon = {'name': 'dragon', 'item_level': 70, 'life_points': 80, 'gold_loot': 50, 'loot': ['platinum'], 'difficulty': 54, 'death statement': "The dragon cooks you to a crisp and swallows you whole."}
    input()
    reset = player['life_points']

    if fight(dragon):
        print("After beating the dragon, you can either loot it or wipe off one of the nearby dusty eggs.")
        choice = input('> ')

        if 'loot' in choice or 'dragon' in choice:
            beat(dragon)

        elif 'wipe' in choice or 'egg' in choice:
            print("You choose an egg at random and after wiping off the dust, it shines like gold. It must be worth a hefty sum. Do you want to keep it or crack it open?")
            choice = input('> ')

            if 'crack' in choice or 'open' in choice:
                rand = randint(0, 3)
                if rand == 0:
                    print("You crack open the golden egg, and something mystical is inside...")
                    input()
                    loot('Ashbringer')
                    print("Ashbringer is the most powerful weapon to have even been created.\nThis sword was forged long ago by acient dwarfs deep in the heart of Ironforge Mountain.\nWield it with care, for none who face you truly stand a chance.")
                    input()

                else:
                    print('You crack the egg open, but nothing is inside! Better luck next time.')
                    input()

            elif 'keep' in choice:
                loot('golden egg')

            else:
                print("I did not understand what you typed, so this encounter has been reset.")
                player['life_points'] = reset
                input()

        else:
            print("I did not understand what you typed, so this encounter has been reset.")
            player['life_points'] = reset
            input()

def king():
    global player
    print("You have been summoned by King Varian Wrynn for a private audience. The King thanks you for your service to the land as you have quickly become his best champion.\nThe old man looks frail and weak, so you question why he should reign and not someone younger, someone more in touch with the people.\nWould you like to swear allegiance to King Varian, fight him, or return on your conquest?\nNOTE: the game will end one way or another if you do not return.")
    choice = input('> ')

    if 'swear' in choice or 'all' in choice:
        print("Becuase of your unwavering dedication to the throne, King Varian has decided to grant you Knighthood.")
        print(f"People from all over Azeroth gather in your honor as you are named Knight {player['name']}, Hero of the Land.")
        input()
        exit(0)

    elif 'fight' in choice:
        king = {'name': 'King Varian', 'item_level': 150, 'life_points': 100, 'gold_loot': 1000000, 'loot': ['diamond'], 'difficulty': 112, 'death statement': "The King is truly the greatest warrior in the land, even besting you. There is only one weapon capable of killing King Varian, but you either did not have it or were not at maximum health."}
        if fight(king):
            beat(king)
            print("You have won the game with highest honors. Congratulations!")
            input()
            report()
            exit(0)

    elif 'return' in choice:
        print("You have graciously declined his Majesty's offer and return to your home in Goldshire.")
        input()

    else:
        print("I didn't quite understand.")
        king()

def merchant():
    print("Do you want to buy or sell?")
    choice = input('> ')

    if choice == 'buy':
        buy()

    elif choice == 'sell':
        sell()

    else:
        print("I didn't quite get that.")
        merchant()

def buy():
    global player
    print(f"""
    What would you like to purchase? (type only one item; nevermind if you change your mind)
    WEAPONS
    \tstick\t\t{items['stick'][1]} gold\t\t{items['stick'][2]} IL
    \tshovel\t\t{items['shovel'][1]} gold\t{items['shovel'][2]} IL
    \taxe\t\t{items['axe'][1]} gold\t{items['axe'][2]} IL
    \tsword\t\t{items['sword'][1]} gold\t{items['sword'][2]} IL

    ARMOUR
    \tbronze\t\t{items['bronze'][1]} gold\t\t{items['bronze'][2]} IL
    \tsilver\t\t{items['silver'][1]} gold\t\t{items['silver'][2]} IL
    \tgold\t\t{items['gold'][1]} gold\t{items['gold'][2]} IL
    \tplatinum\t{items['platinum'][1]} gold\t{items['platinum'][2]} IL

    OTHER
    \tfood\t\t{items['food'][1]} gold\t\tRestores {items['food'][2]} HP


    You have {player['gold']} gold remaining.
    """)

    choice = input('> ')

    if choice in items:

        if choice == 'food':
            print("How many pieces of bread would you like to purchase?")
            choice = input('> ')

            choice = whole_number(choice)
            if player['gold'] >= items['food'][1] * choice:
                player['food'] += choice
                player['gold'] -= items['food'][1] * choice
                buy_else()

            else:
                print("You cannot afford that item.")
                input()
                buy_else()

        elif player['gold'] >= items[choice][1]:
            player['gold'] -= items[choice][1]
            loot(choice)
            input()
            buy_else()

        else:
            print("You cannot afford that item.")
            input()
            buy_else()

    elif 'never' in choice:
        return

    else:
        print("I didn't quite get that.")
        buy()

def buy_else():
    print("Do you want to buy something else?")
    choice = input("> ")

    if choice == 'yes':
        buy()

    else:
        return

def sell():
    global player

    if len(player['bag']) == 0:
        print("You don't have anything in your bags to sell.")
        input()

    elif len(player['bag']) == 1:
        print(f"I will give you {items[player['bag'][0]][0]} gold for {player['bag'][0]}. Do you want to sell?")
        choice = input("> ")

        if choice == 'yes':
            player['gold'] += items[player['bag'][0]][0]
            player['bag'].remove(player['bag'][0])

        elif choice == 'no':
            pass

        else:
            print("I don't follow.")
            sell()

    else:
        print(f"I will give you {items[player['bag'][0]][0]} gold for {player['bag'][0]} or {items[player['bag'][1]][0]} gold for {player['bag'][1]}. Tell me what you want to sell, say both, or say neither.")
        choice = input('> ')

        if choice == player['bag'][0]:
            player['gold'] += items[player['bag'][0]][0]
            player['bag'].remove(player['bag'][0])

        elif choice == player['bag'][1]:
            player['gold'] += items[player['bag'][1]][0]
            player['bag'].remove(player['bag'][1])

        elif 'both' in choice or 'and' in choice:
            player['gold'] += items[player['bag'][0]][0]
            player['bag'].remove(player['bag'][0])
            player['gold'] += items[player['bag'][0]][0]
            player['bag'].remove(player['bag'][0])

        elif choice == "neither":
            pass

        else:
            print("I don't follow.")
            sell()

def eat_food():
    global player

    if player['food'] == 0 or player['life_points'] == 100:
        print("You either have full health or no food!")
        input()

    else:
        print(f"""How many pieces of bread would you like to eat? \nRecall that one piece restores 10 life points, and you have {player['life_points']} life points and {player['food']} piece(s) of bread.""")
        choice = input('> ')

        choice = whole_number(choice)

        max_pieces = ceil((100 - player['life_points']) / 10)

        if choice < max_pieces and choice <= player['food']:
            player['life_points'] += 10 * choice
            player['food'] -= choice
            print(f"Success! You now have {player['life_points']} life points and {player['food']} piece(s) of food remaining.")
            input()

        elif choice >= max_pieces and choice <= player['food']:
            player['life_points'] = 100
            player['food'] -= max_pieces
            print(f"Success! You now have 100 life points and {player['food']} piece(s) of food remaining.")
            input()

        else:
            print("You don't have that much food! Try again!")
            eat_food()

def change_gear(item = None):
    global player

    if item:
        print(f"""
        Weapon: \t\t{player['weapon']}
        Armour: \t\t{player['armour']}
        Bag: \t\t{player['bag']}
        """)
        print("Would you like to change your gear around at all?")
        choice = input('> ')

        if choice == 'yes':
            pass

        elif choice == 'no':
            set_item_level()
            return

        else:
            print("I didn't quite get that.")
            change_gear(item)
            return



    if len(player['bag']) == 1:
        print(f"Would you like to equip {player['bag'][0]}?")
        choice = input('> ')

        if choice == 'yes':
            equip(0)

        elif choice == 'no':
            pass

        else:
            print("I didn't quite get that.")
            change_gear()

    elif len(player['bag']) == 2:
        print(f"Would you like to equip {player['bag'][0]} or {player['bag'][1]}?")
        choice = input('> ')

        if choice == player['bag'][0]:
            equip(0)

        elif choice == player['bag'][1]:
            equip(1)

        else:
            print("I didn't quite get that.")
            change_gear()

    elif len(player['bag']) == 3:
        print(f"Would you like to equip {player['bag'][0]}, {player['bag'][1]}, or {player['bag'][2]}?")
        choice = input('> ')

        if choice == player['bag'][0]:
            equip(0, item)

        elif choice == player['bag'][1]:
            equip(1, item)

        elif choice == player['bag'][2]:
            equip(2, item)

        else:
            print("I didn't quite get that.")
            change_gear()

    else:
        print("You have no gear in your bag to equip! **cough** ya broke **couch**")
        input()

    try:
        player['bag'].remove('fists')

    except:
        pass

    set_item_level()

def check_bag():
    if len(player['bag']) <= 2:
        return True
    else:
        return False

def equip(n, item = None):
    global player

    if player['bag'][n] in weapon_types:
        player['bag'].append(player['weapon'])
        player['weapon'] = player['bag'][n]
        player['bag'].remove(player['weapon'])

    elif player['bag'][n] in armour_types:
        player['bag'].append(player['armour'])
        player['armour'] = player['bag'][n]
        player['bag'].remove(player['armour'])

    else:
        print("This item in unequippable.")
        input()

        if item:
            player['bag'].remove(item)
            loot(item)

def check_death(statement):
    global player

    if player['life_points'] <= 0:
        print(statement)
        input()
        report()
        exit(0)

def loot(item):
    global player

    print(f"Congratulations! You have received {item}!")
    print("You can now change your gear around and throw things away until you only have two items in your backpack.")
    input()

    player['bag'].append(item)
    change_gear(item)


    while not check_bag():
        try:
            throw_away()

        except:
            pass

def throw_away():
    global player
    print(f"Would you rather throw {player['bag'][0]}, {player['bag'][1]}, or {player['bag'][2]} away?")
    choice = input('> ')

    try:
        player['bag'].remove(choice)

    except:
        print("I didn't quite get that. Please try again.")
        throw_away()

def whole_number(choice):
    try:
        choice_int = int(choice)
        choice_float = float(choice)

        if choice_int == choice_float and choice_int >= 0:
            return choice_int

        else:
            print("Enter a positive whole number, please.")
            input()
            play()

    except:
        print("Enter a whole number, please.")
        input()
        play()



print("Welcome to Azeroth, young warrior! What do they call you?")
player.update({'name': input('> ')})
print(f"""
Ahh, welcome, {player['name']}! Let me get you acclimated to your new surroundings.
You are in the village of Goldshire, where bad things have been happening.
We need you to help save our village and serve our king, but you must be careful.
You are rather inexperienced and poor. Complete conquests to earn gold, which you can
use to buy food and gear from the merchant. Protect your health, which can be regenerated with food.
NEVER let your health get to 0, or you die! I advise you to ALWAYS eat to 100 health!
Good luck, {player['name']}, and may the Light bless you!
""")

play()
