# This is a fully functional version of 9/6 Jacks or Better. You can choose which cards to
# keep by assuming the first card is number 1, the last is number 5, and you type as one number
# Whatever cards you want to keep. So if you want to keep the pair of fives here: 2♦ 5♥ T♥ 5♠ J♣
# You would type in "24" as you want to keep the second and forth card. 

import random
import sys

money = 100
bet = 5
winnings = 0
total_winnings = 0
tries = 0
play = 'yes'
playAgain = 'y'
exit_prompt = "Bet again? Y / N"

print("Welcome to Video Poker!")

# Dictionary containing all possible winning poker hands.
hand_dict = {9:"Royal Flush",
             8:"Straight Flush",
             7:"Four of a Kind",
             6:"Full House",
             5:"Flush",
             4:"Straight",
             3:"Three of a Kind",
             2:"Two Pair",
             1:"Jacks or Better",
             0:"Nothing"}

# Dictionary containing the paytable which corresponds to the winning hands above.
paytable = {9:800,
            8:50,
            7:25,
            6:9,
            5:6,
            4:4,
            3:3,
            2:2,
            1:1,
            0:0}

# Indicates the relative value of each card. Used for determining straights and also if a
# pair is equal to Jacks or Better.
card_values = {2:"2", 3:"3", 4:"4", 5:"5", 6:"6",7:"7",8:"8",
               9:"9",10:"T",11:"J",12:"Q",13:"K",14:"A",15:"W"}

# Returns the corresponding key of a dictionary for any of the values above.
def findKey(input_dict, value):
    return next((k for k, v in input_dict.items() if v == value), None)

# Returns 10 cards which will be used for a single game of Video Poker. 
def getCards():
    deck = ['2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', 'T♥', 'J♥', 'Q♥', 'K♥', 'A♥',
            '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', 'T♦', 'J♦', 'Q♦', 'K♦', 'A♦',
            '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', 'T♣', 'J♣', 'Q♣', 'K♣', 'A♣',
            '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', 'T♠', 'J♠', 'Q♠', 'K♠', 'A♠']
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
        print(hand[i],end = ' ')
    print()
    return hand


def checkHand(hand):
    value = []
    suit = []
    pair = 0
    straight = 0
    sequential = 0
    checkValue = {}
    checkSuit = {}
    for i in range(0,5):
        value.append(findKey(card_values,hand[i][0]))
    for i in range(0,5):
        suit.append(hand[i][1])
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
        if value[4] == 14:
            if value[0] == 2 and value[1] == 3 and value[2] == 4 and value[3] == 5:
                straight = 1
        for i in range(0,5):
            if value[i] == value[i - 1] + 1:
                sequential += 1
        if sequential == 4:
            straight = 1

    # Starting from a royal flush and working down, this will return the highest winning combination in your hand.
    if straight == 1 and len(set(suit)) == 1 and value[0] == 10:
        return hand_dict[9] # Royal Flush
    if straight == 1 and len(set(suit)) == 1:
        return hand_dict[8] # Straight Flush
    if max(checkValue.values()) == 4:
        return hand_dict[7] # Four of a Kind
    if max(checkValue.values()) == 3 and min(checkValue.values()) == 2:
        return hand_dict[6] # Full House
    if len(set(suit)) == 1:
        return hand_dict[5] # Flush
    if straight == 1:
        return hand_dict[4] # Straight
    if max(checkValue.values()) == 3:
        return hand_dict[3] # Three of a Kind
    if pair == 2:
        return hand_dict[2] # Two Pair
    if max(checkValue.values()) == 2:
        for i in range(11,15):
            if checkValue.get(i) == 2:
                return hand_dict[1] # Jacks or Better
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


while playAgain == 'Y' or playAgain == 'y':
    newHand = []
    x = getCards()
    print("===================================")
    print("Money: $" + str(money) + "              # Bets: " + str(tries))
    print()
    dealHand(x)
    if checkHand(x) != hand_dict[0]:
        print(checkHand(x))
    print()
    print("Which cards would you like to keep?")
    keep = input()
    print()
    if keep[0].lower() == "e":
        break
    money -= 5
    tries += 1
    for i in keep:
        newHand.append(x[int(i) - 1])
    for i in range(5,10):
        newHand.append(x[i])
    dealHand(newHand)
    print(checkHand(newHand))
    winnings = paytable.get(findKey(hand_dict, checkHand(newHand))) * bet
    money += winnings
    total_winnings += winnings
    if winnings > 0:
        print("Won: $" + str(winnings) + "!")
    print()
    print("-----------------------------------")
    if money < 5:
        print("No money left. Game over!")
        break
    play = ''
    while len(play) != 1:
        print(exit_prompt)
        play = input()
        if len(play) == 1:
            while play[0].lower() not in ['y','n']:
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
