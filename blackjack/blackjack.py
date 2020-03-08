import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
player_turn = True
dealer_turn = False

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                card = Card(suit,rank)
                self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)        

    def deal(self):
        return self.deck.pop(0)

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)

        if card.rank == "Ace":
            self.adjust_for_ace()
        else:
            self.value += values.get(card.rank) 

        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def adjust_for_ace(self):
        
        if self.value + 11 > 21:
            self.value += 1
        else:
            self.value += 11
            self.aces += 1

    def __str__(self):
        returnable = ""

        returnable = str(self.cards[0])
        i = 1
        while i < len(self.cards):
            returnable += '\n'
            returnable += str(self.cards[i])
            i += 1
        return returnable 

class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += (self.bet * 2)  
        print(f"You won {self.bet} chips!")

    def push(self):
        self.total += self.bet

def take_bet():

    while True:
        
        try:
            bet = int(input("How much would you like to bet? "))
            
            if bet < 1 :
                print("Invalid number!")
                continue
            player_chips.bet = bet
        except:
            print("Invalid number!")
            continue
        else:
            if bet > player_chips.total:
                print("Not enough chips!")
                continue
            else:
                player_chips.total -= bet
                break

def hit(deck,hand):

    hand.add_card(deck.deal())

def hit_or_stand(deck,hand):

    while True:
        inpt = str(input("Hit or stand? (h/s): "))

        if inpt == "h":
            hit(deck,hand)
            break
        elif inpt == "s":
            global player_turn
            global dealer_turn
            player_turn = False
            dealer_turn = True
            break
        else:
            print("Choose hit (h) or stand (s)")
            continue

def show_hand(hand):
    print(hand)
    print(f"Sum: {hand.value}")
    print("")

def show_some(player,dealer):
    print("")
    print("Dealer cards: ")
    second_card = dealer.cards[1]
    print("[FACE DOWN CARD]")
    print(second_card)
    second_card_value = values[str(second_card).split(" ")[0]]
    print(f"Sum: ? + {second_card_value}")
    print("")
    print("Player cards: ")
    print(player)
    print(f"Sum: {player.value}")
    print("")

def show_all(player,dealer):
    print("")
    print("Dealer cards: ")
    print(dealer)
    print(f"Sum: {dealer.value}")
    print("")
    print("Player cards: ")
    print(player)
    print(f"Sum: {player.value}")
    print("")

def player_bust_check(hand):

    if hand.value > 21:
        print("You bust!")
        global player_turn
        player_turn = False
        global dealer_turn
        dealer_turn = False 
    else:
        pass 

def dealer_bust_check(hand):

    if hand.value > 21:
        print("Dealer busts!")
        global dealer_turn 
        dealer_turn = False
    else:
        pass 

def win_check(player,dealer):
    
    if player.value > 21:
        pass
    elif dealer.value > 21:
        player_chips.win_bet()
    elif player.value > dealer.value:
        player_chips.win_bet()
    elif dealer.value > player.value:
        print("Dealer wins!")
    elif dealer.value == player.value:
        print("A push! Bet is returned!")
        player_chips.push()

def game_over():

    if player_chips.total == 0:
        print("You ran out of chips! Game over!")
        return True
    
    while True:
        inpt = input("Would you like to play again? (y/n): ")
        if inpt == "y":
            return False
        elif inpt == "n":
            return True
        else:
            print("Choose (y) or (n)")
            continue

player_chips = Chips()
print("Welcome to Blackjack!")
print(f"You have {player_chips.total} chips left.")
while True:

    playing_deck = Deck()
    playing_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    take_bet()
    player_hand.add_card(playing_deck.deal())
    player_hand.add_card(playing_deck.deal())
    dealer_hand.add_card(playing_deck.deal()) 
    dealer_hand.add_card(playing_deck.deal())
    show_some(player_hand,dealer_hand)

    while player_turn:
        
        hit_or_stand(playing_deck,player_hand)

        if player_turn:
            show_hand(player_hand)

        player_bust_check(player_hand)

    if dealer_turn:
        print("Dealer turn!")
        print("Dealer cards: ")
        show_hand(dealer_hand)

    while dealer_turn and dealer_hand.value < player_hand.value and dealer_hand.value < 21:
        
        input("Dealer hits! Press Enter to continue... ")
        hit(playing_deck,dealer_hand)
        show_hand(dealer_hand)
        dealer_bust_check(dealer_hand)

    win_check(player_hand,dealer_hand)
    print(f"Chips remaining: {player_chips.total}")

    if game_over():
        break
    else:
        player_turn = True
        dealer_turn = False
        continue

print("Thanks for playing!")
