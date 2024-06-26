import random

class Card:
  def __init__(self,value):
    self.value = value

  def change_ace(self):
    if self.value == 11:
      self.value = 1
    elif self.value == 1:
      self.value = 11
    else:
      # redundant
      print("Only Aces can have 2 different values!")


class Card_manager:
    def __init__(self):
        self.available_values = 4*[11] + 4*[10] +4*[2,3,4,5,6,7,8,9]

    def reshuffle(self):
        self.available_values = 4*[11] + 4*[10] +4*[2,3,4,5,6,7,8,9]

    def draw(self):
        draw = Card(random.choice(self.available_values))
        self.available_values.pop(draw.value)
        return draw
  
    def is_ace(self, value):
        if value == 11 or value == 1:
            return True
        else:
            return False

class Player: 
    def __init__(self, name, budget, dealer):
        self.name = name
        self.budget = budget
        self.dealer = dealer
        self.cards = []
        self.sum = 0
        self.keep_playing = True
        self.bust = False
        self.aces = []
  
    def __repr__(self):
        return "{}'s budget is {}".format(self.name,self.budget)

    def bet(self):
        self.bet = int(input("How much do you want to bet? "))
        self.budget -= self.bet

    def check_bust(self):
      if self.sum > 21:
         self.bust = True
         print("BUST")

    def check_ace(self):
       if len(self.aces) > 0:
            for i in range(len(self.aces)):
                if i == 0:
                    ace = input("Do you want to change the value of your ace? Current value is {} \n".format(self.aces[i].value))
                    if ace == 'y':
                       self.aces[i].change_ace()
                else:
                    ace = input("Do you want to change the value of your next ace? Current value is {} \n".format(self.aces[i].value))
                    if ace == 'y':
                       self.aces[i].change_ace()

    def begin_play(self):
        for x in range(2):
            card = self.dealer.manager.draw()
            print("You drew a card of value {}". format(card.value))
            if card.value == 11:
                self.aces.append(card)

            self.check_ace()
            self.cards.append(card)
            self.sum += card.value
        print("Your score is {}".format(self.sum))
        self.check_bust()


    def play(self):
        yes = input("Draw one more card? Enter y if yes. ")
        if yes == 'y':
            card = self.dealer.manager.draw()
            print("You drew a card of value {}". format(card.value))
            if card.value == 11:
                self.aces.append(card)

            self.check_ace()
            self.cards.append(card)
            self.sum += card.value
            print("Your points total to {}".format(self.sum))
            self.check_bust()
        if yes != 'y':
            print("Your points total to {}".format(self.sum))
            self.keep_playing = False

class Dealer(Player):
    def __init__(self, name='Dealer', budget=1000):
        self.name = name
        self.budget = budget
        self.manager = Card_manager()
        self.cards = []
        self.sum = 0
        self.hide = False
        self.aces = []
        self.bust = False
        self.keep_playing = True 
        

    def check_ace(self):
       # plays ace as 11 and only changes if it is about to go bust
       if len(self.aces) > 0:
            for ace in self.aces:
                if self.sum + ace.value > 21 and ace.value == 11:
                    ace.change_ace()
      
    def begin_play(self):
        for x in range(2):
            card = self.manager.draw()
            if self.manager.is_ace(card.value):
                self.ace_value(card)
            self.check_ace()
            self.cards.append(card)
            self.sum += card.value
            if self.hide:
                print("The Dealer's card is hidden")
            else:
                print("Dealer drew a card of value {}". format(card.value))
                self.hide = True
        self.check_bust()
  
    def play(self):
        # Dealer must take cards until his score is 17 or above
        if self.sum <= 16:
            card = self.manager.draw()
            if self.manager.is_ace(card.value):
                self.aces.append(card)
            self.cards.append(card)
            self.sum += card.value
            print("The Dealer drew a card")
            self.check_bust()
        else:
            self.keep_playing = False

def winner(player, dealer):
    if player.bust is True:
        print("Dealer won. Player {} went bust".format(player.name))
        dealer.budget += player.bet
    elif dealer.bust is True:
        print("The dealer went bust. Player {} won".format(player.name))
        player.budget += 2*player.bet
        dealer.budget -= player.bet

    else:
        if player.sum == dealer.sum:
            print("DRAW")
        elif player.sum > dealer.sum:
            print("Player {} won".format(player.name))
            player.budget += 2*player.bet
            dealer.budget -= player.bet
        else:
            print("The Dealer won")
            dealer.budget += player.bet

def __main__():
    game_on = True
    # Start of the game
    dealer = Dealer()
    print("Welcome to a game of Blackjack!")
    player1 = Player(input("Enter your name "),int(input("Enter your budget ")), dealer)
    # Initial bets
    print("The player must make the initial bet")
    player1.bet()
    if game_on is True:
        print("Player's budget is {}".format(player1.budget))
        print("The Dealer's budget is {}".format(dealer.budget))
        # First draw
        player1.begin_play()
        dealer.begin_play()
        # Main play
        while player1.keep_playing is True and player1.bust is False and dealer.bust is False:
            player1.play()
            if player1.bust is False:
                dealer.play()
        if player1.keep_playing is False and dealer.bust is False and player1.bust is False:
            # player decided to stop playing but dealer hasn't drawn enough cards yet
            while dealer.keep_playing is True:
                dealer.play()
        winner(player1, dealer)
        play_on = input("Do you want to play another round? ")
        if play_on != 'y':
            game_on = False
            print("End of game")
            print("Player's budget is {}".format(player1.budget))
            print("The Dealer's budget is {}".format(dealer.budget))
        else:
            print("Another round of fun!")
__main__()
