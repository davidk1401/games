import random
import sys

# Dictionary containing all possible poker hands
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
             1:"Kings or Better"}

# Dictionary containing the paytable for each of the possible hands above
paytable = {11:"800",
            10:"200",
            9:"100",
            8:"50",
            7:"20",
            6:"8",
            5:"5",
            4:"4",
            3:"3",
            2:"1",
            1:"1"}

# Indicates the relative value of each card. Useful for detecting straights.
card_values = {2:"2", 3:"3", 4:"4", 5:"5", 6:"6",7:"7",8:"8",
               9:"9",10:"T",11:"J",12:"Q",13:"K",14:"A",15:"W"}

# Function for returning the corresponding key of a dictionary for one of the values above.
def findKey(input_dict, value):
    return next((k for k, v in input_dict.items() if v == value), None)

# Returns 10 cards which will be used for the game of Joker Poker. 
def getCards():
    deck = ['2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', 'T♥', 'J♥', 'Q♥', 'K♥', 'A♥',
        '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', 'T♦', 'J♦', 'Q♦', 'K♦', 'A♦',
        '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', 'T♣', 'J♣', 'Q♣', 'K♣', 'A♣',
        '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', 'T♠', 'J♠', 'Q♠', 'K♠', 'A♠',
        'W*']
    hand = []
    x = 0
    for i in range(0,10):
        x = random.randint(0,len(deck)-1)
        hand.append(deck[x])
        deck.remove(deck[x])
    return hand

def dealHand(hand):
    for i in range(0,5):
        print(hand[i],end = ' ')
    print()

# This function checks five cards to determine if something is a winning hand
# and, if so, returns the highest value winning hand. There are a couple hands
# it doesn't check for yet, notably straights, royal flushes, and two pair.
def checkHand(hand):
    dealHand(hand)
    value = []
    suit = []
    joker = 0
    checkValue = {}
    checkSuit = {}
    for i in range(0,5):
        if hand[i][0] == 'W':
            joker = 1
        value.append(findKey(card_values,hand[i][0]))
    for i in range(0,5):
        suit.append(hand[i][1])
    for i in value:
        if i in checkValue:
            checkValue[i] += 1
        else:
            checkValue[i] = 1
    value.sort()
    print(checkValue)
    print(value)
    print(suit)
    if max(checkValue.values()) + joker == 5:
        return print(hand_dict[10])
    if max(checkValue.values()) + joker == 4:
        return print(hand_dict[7])
    if max(checkValue.values()) == 3 and min(checkValue.values()) == 2:
        return print(hand_dict[6])
    if len(set(suit)) - joker == 1:
        return print(hand_dict[5])
    if max(checkValue.values()) + joker == 3:
        return print(hand_dict[3])
    if max(checkValue.values()) + joker == 2:
        return print(hand_dict[1])

# This is for testing out the system by going through multiple hands at once.
def testCheckHand():
    print('How many hands would you like?')
    times = int(input())
    for i in range(0,times):
        x = getCards()
        checkHand(x)

# I use this to test the getCards() function.
def testCardValues():
    print('How many hands would you like?')
    times = int(input())
    for i in range(0,times):
        x = getCards()
        print()
        print(x)
        for i in range(0,len(x)):
            print(findKey(card_values,x[i][0]),end=' ')

testCheckHand()

