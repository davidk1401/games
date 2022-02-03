# This is a functional version of Joker Poker. It uses a full deck of 52 cards
# along with one joker which can act as any card.
# If you want to keep all cards, type 12345. If you want to keep the
# pair of fives here [2♦ 5♥ T♥ 5♠ J♣] You would type in "24" as you want to
# keep the 2nd and 4th card. The number 0 discards everything.

card_deck = ['2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',
             '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',
             '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',
             '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠',
             'W*']

import random
import sys
import time
import colorama
from colorama import Fore, Back, Style
colorama.init()

money = 100
bet = 5
winnings = 0
total_winnings = 0
tries = 0
play = 'yes'
playAgain = 'y'
exit_prompt = "Bet again? Y / N (enter C for continuous mode)"

print("Welcome to Video Poker!")
print("Joker Wild")

# Dictionary containing all possible winning poker hands.
hand_dict = {11:"Natural Royal Flush",
             10:"Five of a Kind",
              9:"Royal Flush w/ Joker",
              8:"Straight Flush",
              7:"Four of a Kind",
              6:"Full House",
              5:"Flush",
              4:"Straight",
              3:"Three of a Kind",
              2:"Two Pair",
              1:"Kings or Better",
              0:"Nothing"}

# Dictionary containing the paytable which corresponds to the winning hands above.
paytable = {11:800,
            10:200,
             9:100,
             8:50,
             7:20,
             6:8,
             5:5,
             4:3,
             3:2,
             2:1,
             1:1,
             0:0}

# Indicates the relative value of each card. Used for determining straights and also if a
# pair is equal to Kings or Better.
card_values = {2:"2", 3:"3", 4:"4", 5:"5", 6:"6",7:"7",8:"8",
               9:"9",10:"1",11:"J",12:"Q",13:"K",14:"A",15:"W"}

# Returns the corresponding key of a dictionary for any of the values above.
def findKey(input_dict, value):
    return next((k for k, v in input_dict.items() if v == value), None)

# Returns 10 cards which will be used for a single game of Joker Poker. 
def getCards():
    deck = ['2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',
            '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',
            '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',
            '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠',
            'W*']
    hand = []
    x = 0
    for i in range(0,10):
        x = random.randint(0,len(deck)-1)
        hand.append(deck[x])
        deck.remove(deck[x])
    return hand

# Prints the current hand
def dealHand(hand):
    for i in range(0,5):
        if hand[i][-1] in ['♥','♦']:
            print(Fore.RED + Back.WHITE + hand[i] + Style.RESET_ALL,end = ' ')
        elif hand[i][-1] in ['♣','♠']:
            print(Fore.BLACK + Back.WHITE + hand[i] + Style.RESET_ALL,end = ' ')
        else:
            print(Fore.MAGENTA + Back.WHITE + hand[i] + Style.RESET_ALL,end = ' ')
    print()
    return hand


def checkHand(hand):
    value = []
    suit = []
    pair = 0
    joker = 0
    straight = 0
    sequential = 0
    checkValue = {}
    checkSuit = {}
    for i in range(0,5):
        value.append(findKey(card_values,hand[i][0]))
    for i in range(0,5):
        suit.append(hand[i][-1])
    for i in range(0,5):
        if hand[i][-1] == '*':
            joker = 1
    value.sort()
        

    # Counts how many cards with the same value are in your hand. 
    for i in value:
        if i in checkValue:
            checkValue[i] += 1
        else:
            checkValue[i] = 1
    
    # If two cards with the same value are present, that's one pair.
    for i in checkValue:
        if checkValue[i] == 2:
            pair += 1

    # If all cards in your hand have unique values, then it could be a straight. This checks if it is. 
    if max(checkValue.values()) == 1:
        straight = checkStraight(value)
        if value[4] == 15:
            for i in range(2,16):
                value.pop()
                value.append(i)
                if checkStraight(value) == 1:
                    straight = 1
                
                
            

    # Starting from a royal flush and working down, this will return the highest winning combination in your hand.
    if straight == 1 and len(set(suit)) == 1 and value[0] == 10:
        return hand_dict[11] # Natural Royal Flush
    if max(checkValue.values()) + joker == 5:
        return hand_dict[10] # Five of a Kind
    if straight == 1 and len(set(suit)) == 1 and (value[0] == 10 or value[0] == 11) and joker == 1:
        return hand_dict[9] # Wild Royal Flush
    if straight == 1 and len(set(suit)) - joker == 1:
        return hand_dict[8] # Straight Flush
    if max(checkValue.values()) + joker == 4:
        return hand_dict[7] # Four of a Kind
    if max(checkValue.values()) + joker == 3 and min(checkValue.values()) == 2:
        return hand_dict[6] # Full House
    if len(set(suit)) - joker == 1:
        return hand_dict[5] # Flush
    if straight == 1:
        return hand_dict[4] # Straight
    if max(checkValue.values()) + joker == 3:
        return hand_dict[3] # Three of a Kind
    if pair == 2:
        return hand_dict[2] # Two Pair
    if max(checkValue.values()) + joker == 2:
        for i in range(13,15):
            if checkValue.get(i) == 2 or checkValue.get(i) == 1 and joker == 1:
                return hand_dict[1] # Kings or Better
    return hand_dict[0] # Nothing
    
def selectCards(hand):
    newHand = []
    keep = input()
    if keep == "EXIT":
        sys.exit()
    for i in keep:
        newHand.append(hand[int(i) - 1])
    for i in range(5,10):
        newHand.append(hand[i])
    dealHand(newHand)
    return checkHand(newHand)

def checkStraight(originalHand):
    sequential = 0
    hand = originalHand.copy()
    hand.sort()
    if hand[4] == 14 or hand[4] == 15:
        if hand[0] == 2 and hand[1] == 3 and hand[2] == 4 and hand[3] == 5:
            return 1
    for i in range(0,5):
        if hand[i] == hand[i - 1] + 1:
            sequential += 1
    if sequential == 4:
        return 1
    return 0

def testCheckHand():
    print('How many hands would you like?')
    times = int(input())
    for i in range(0,times):
        x = getCards()
        for i in range(0,5):
            if x[i][-1] == ' ':
                print(dealHand(x))
                print(checkHand(x))
        if checkHand(x) == hand_dict[4]:
            for i in range(0,5):
                print(x[i],end = ' ')
            print(dealHand(x))
            print(checkHand(x))

while playAgain.lower() != 'n':
    time.sleep(0.25)
    money -= 5
    tries += 1
    newHand = []
    x = getCards()
    print("===================================")
    print("Money: $" + str(money) + "              # Bets: " + str(tries))
    print()
    dealHand(x)
    if checkHand(x) != hand_dict[0]:
        print(Fore.YELLOW + checkHand(x) + "!" + Style.RESET_ALL)
    print()
    if play.lower() == 'c':
        print("Which cards would you like to keep? (e to exit)")
    else: 
        print("Which cards would you like to keep?")

    # Ensures that the 
    while True:
        try:
            keep = input()
            if len(str(keep)) < 1:
                keep = '0'
                break
            break
            if len(str(keep)) <= 5:
                checkKeep = {}
                max = 0
                for i in keep:
                    if i in checkKeep:
                        checkKeep[i] += 1
                    else:
                        checkKeep[i] = 1
                    if i > max:
                        max = i
                if max(checkKeep.values()) == 1 and max <=5:
                    break
        except ValueError:
            print("Please enter a valid input")
        print("Please enter a valid input")
    keep = str(keep)
    print()
    if keep[0].lower() == "e":
        break
    for i in keep:
        newHand.append(x[int(i) - 1])
    for i in range(5,10):
        newHand.append(x[i])
    time.sleep(0.1)
    dealHand(newHand)
    time.sleep(0.1)
    if checkHand(newHand) == hand_dict[0]:
        print(checkHand(newHand))
    else:
        print(Fore.YELLOW + checkHand(newHand) + "!" + Style.RESET_ALL)
    time.sleep(0.1)
    winnings = paytable.get(findKey(hand_dict, checkHand(newHand))) * bet
    money += winnings
    total_winnings += winnings
    if winnings > 0:
        print("Won: $" + str(winnings) + "!")
    print()
    print("Money: $" + str(money))
    print("-----------------------------------")
    if money < 5:
        print("No money left. Game over!")
        break
    if play.lower() != 'c':
        play = ''
    while len(play) != 1:
        print(exit_prompt)
        play = input()
        if len(play) == 1:
            while play[0].lower() not in ['y','n','c']:
                print(exit_prompt)
                play = input()
    playAgain = play[0]

print()
print()
print("_______________________________________")
print()
print("Thank you for playing! Here are your stats: ")
print()
print("# of Bets:       " + str(tries))
print("Final Balance:  $" + str(money))
print("Profit/Loss:    $" + str(money - 100))
print("Total Winnings: $" + str(total_winnings))
input()
