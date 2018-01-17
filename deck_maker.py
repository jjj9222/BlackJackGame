#Going to create a class for the cards
#to create deck going to call a function that takes a paramaters of how many decks are in game
import random
import time
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

#initalizes the large deck of cards
Total_Cards = []
#cards is a copy of total cards this is used for the blackjack game 
cards = []
#hand is the cards in you hand 
hand = []
#the dealerhand are the cards in dealers hand
dealerhand = []
#initalizes the amount of tokens user has
tokens = 1000
#initalizes the count of the blackjack game. To predict outcome of next game
gamecount = 0

class Cards:
    """The class is fairly simple
        Each card has a suit and a value attached to it"""
    def __init__(self,name, suit, value):
        self.s = suit
        self.v = value

class HitStand(GridLayout):
    """Going to lay out the buttons for hit or stand"""
    def __init__(self, **kwargs):
        super(HitStand, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.hit = Button(text='Hit')
        self.add_widget(self.hit)
        self.stand = Button(text='Stand')
        self.add_widget(self.stand)



class blackjack(Widget):
    pass

class blackjackApp(App):
    def build(self):
        parent = Widget()
        hitbtn = Button(text="hit", pos=(10, 10))
        standbtn = Button(text="stand", pos=(100, 100))
        parent.add_widget(hitbtn)
        parent.add_widget(standbtn)
        return parent

def Make_Deck(NumofDecks):
    while NumofDecks > 0:
        for Suit in ['Spades', 'Diamonds', 'Clubs', 'Hearts']:
            for Rank in ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
                     'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']:
                Total_Cards.append(Cards(Rank+Suit,Suit,Rank))
                #appending to the list the card class that will traverse through the different suits and ranks
        NumofDecks = NumofDecks - 1
    #out of the while loop here
    return Total_Cards

def find_count(list):
    count = 0
    for card in list:
        value = card.v
        if(value == 'Ace'):
            #special case
            count += 11
        elif(value == 'Two'):
            count += 2
        elif(value == "Three"):
            count += 3
        elif (value == "Four"):
            count += 4
        elif (value == "Five"):
            count += 5
        elif (value == "Six"):
            count += 6
        elif (value == "Seven"):
            count += 7
        elif (value == "Eight"):
            count += 8
        elif (value == "Nine"):
            count += 9
        else:
            count += 10
    if(count > 21):
        for x in list:
            if(x.v == "Ace"):
                count -= 10
            if(count <= 21):
                break
    return count

def rand_fourNums():
    intRand1 = random.randint(0, len(cards) - 1)
    intRand2 = random.randint(0, len(cards) - 2)
    intRand3 = random.randint(0, len(cards) - 3)
    intRand4 = random.randint(0, len(cards) - 4)
    return intRand1,intRand2,intRand3,intRand4

def update_gamecount(val, gamecount):
    if(val in ('Two','Three','Four','Five','Six')):
        total = (gamecount - 1)/int(len(cards)/56)
        return total
    if(val in ('Ace','King','Queen','Jack','Ten')):
        total = (gamecount + 1)/int(len(cards)/56)
        return total
    return gamecount




def main():
    numberdecks = 6
    while(1 != 0):
        global gamecount
        global cards
        global hand
        global dealerhand
        global tokens
        if (len(cards) <= 10):
            print("Shuffling")
            time.sleep(1)
            cards = Total_Cards
        print("")
        print("New Game")
        bet = 0
        while True:
            try:
                bet =  int(input("How many tokens would you like to wager? : "))
                while True:
                    if(tokens < bet):
                        #if your bet is greater your amount of tokens
                        print("You don't have enough tokens. You only have "+ str(tokens)+ " tokens")
                        bet = int(input("How many tokens would you like to wager? : "))
                    else:
                        break
            except ValueError:
                print("Thats not a valid bet")
                continue
            else:
                break
        intRand1, intRand2, intRand3, intRand4 = rand_fourNums()
        #gets the four random numbers for the players cards and the dealers cards
        uno = cards.pop(intRand1)
        dos = cards.pop(intRand2)
        #initalize the original two user cards
        dealer1 = cards.pop(intRand3)
        dealer2 = cards.pop(intRand4)
        #initalize the two dealers cards only going to see the first dealer card
        hand.append(uno)
        hand.append(dos)
        count = find_count(hand)
        print("DEALER" + " :" + dealer1.s +"," +dealer1.v)
        gamecount = update_gamecount(dealer1.v, gamecount)
        dealerhand.append(dealer1)
        dealcount = find_count(dealerhand)
        print("Dealer count: " + str(dealcount))
        print(uno.s + "," + uno.v)
        gamecount = update_gamecount(uno.v, gamecount)
        print(dos.s + "," + dos.v)
        gamecount = update_gamecount(dos.v, gamecount)
        print("Players's Count :" + str(count))
        userinput = input("These are your cards with the count. Would you like to hit(h) or stand(s)?")
        while(userinput.strip().lower()== 'h' or userinput.strip().lower() == 'hit'):
            drawRand = random.randint(0, len(cards) - 1)
            draw = cards.pop(drawRand)
            hand.append(draw)
            count = find_count(hand)
            print(draw.s + "," + draw.v)
            gamecount = update_gamecount(draw.v, gamecount)
            print("Players's Count :" + str(count))
            if(count > 21):
                break
            userinput = input("Would you like ot hit(h) or stand(s)")
        #player has completed their part of the game

        print("Dealers second card is :" + dealer2.s + "," + dealer2.v )
        update_gamecount(dealer2.v, gamecount)
        dealerhand.append(dealer2)
        dealcount = find_count(dealerhand)
        print("Dealer count: " + str(dealcount))
        #finish dealers hand He needs to hit if he is at 16 or below stand elsewise
        while(dealcount <= 16):
            #want to hit or add one more cards to dealer hand
            randnum = random.randint(0,len(cards)-1)
            hitcard = cards.pop(randnum)
            dealerhand.append(hitcard)
            dealcount = find_count(dealerhand)
            time.sleep(.5)
            print("Dealer's card is :" + hitcard.s + "," + hitcard.v)
            gamecount = update_gamecount(hitcard.v, gamecount)
            print("Dealer count: " + str(dealcount))

        #need to reset hands for next round
        if(count > 21):
            tokens -= bet
            print("LOSER over 21")
        elif(count == 21 and len(hand) == 2):
            tokens += (bet*1.5)
            print("BLACKJACK")
        elif(dealcount > 21 and count <= 21):
            tokens += bet
            print("WINNER")
        elif(count > dealcount):
            tokens += bet
            print("WINNER")
        elif(dealcount == count):
            print("PUSH")
        else:
            tokens -= bet
            print("LOSER")
        hand = []
        dealerhand = []
        print("Token Total= :" + str(tokens))
        print("Gamecount = " + str(int(gamecount)))
        time.sleep(3)




#blackjackApp().run()
main()
