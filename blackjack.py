# Mini-project #6 - Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        s = ''
        for x in self.hand:
            s += str(x)+' '
        return s

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        val = 0
        contains_ace = False
        for x in self.hand:
            val += VALUES[x.get_rank()]
            if x.get_rank() == 'A':
                contains_ace = True
        if contains_ace and val+10<=21:
            val += 10
        return val
   
    def draw(self, canvas, pos):
        for i in range(len(self.hand)):
            self.hand[i].draw(canvas, (pos[0]+CARD_SIZE[0]*i, pos[1]))
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = list()
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        s = ''
        for x in self.deck:
            s += str(x)+' '
        return s       



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, score
    deck = Deck()
    dealer_hand = Hand()
    player_hand = Hand()
    deck.shuffle()
    for _ in range(2):
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
    if in_play:
        score -= 1
        outcome = 'Player lost. Hit or Stand?!'
    else:
        outcome = 'Hit or Stand?!'
    in_play = True

def hit():
    global outcome
    if in_play:
        if player_hand.get_value()>21:
            return
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value()>21:
            outcome = 'You have BUSTED! New Deal?'
            return
       
def stand():
    global outcome, in_play, score
    if in_play:
        while dealer_hand.get_value()<17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value()>21:
            outcome = 'Dealer has BUSTED! New Deal?'
            score += 1
        else:
            if dealer_hand.get_value()>=player_hand.get_value():
                outcome = 'Dealer Won! New Deal?'
                score -= 1
            else:
                outcome = 'Player Won! New Deal?'
                score += 1
        in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('BLACKJACK', (60, 80), 36, 'black', 'serif')
    canvas.draw_text('Score: '+str(score), (450, 80), 22, '#002915', 'serif')
    canvas.draw_text('Dealer\'s Hand', (60, 150), 28, '#002915', 'serif')
    canvas.draw_text('Player\'s Hand', (60, 400), 28, '#002915', 'serif')
    dealer_hand.draw(canvas, (80, 180))
    player_hand.draw(canvas, (80, 430))
    canvas.draw_text(outcome, (100, 340), 32, 'white', 'serif')
    if in_play:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, (116, 228), CARD_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
