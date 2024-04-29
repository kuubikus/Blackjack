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
  
  def __repr__(self):
    return "{}'s budget is {}".format(self.name,self.budget)

  def bet(self):
    self.bet = int(input("How much do you want to bet? "))
    self.budget -= self.bet

  def begin_play(self):
    for x in range(2):
      card = self.dealer.manager.draw()
      if card.value == 11:
        ace = input("An Ace! Do you want a value of 1 or 11")
        card.value = ace
      self.cards.append(card)
      self.sum += card.value
      print("You drew a card of value {}". format(card.value))
    print("Your score is {}".format(self.sum))

  def play(self):
    yes = input("Draw one more card? Enter True if yes.")
    if yes:
      card = self.dealer.manager.draw()
      print("You drew a card of value {}". format(card.value))
      if card.value == 11:
        ace = input("An Ace! Do you want a value of 1 or 11")
        card.value = ace
      self.cards.append(card)
      self.sum += card.value
      print("Your points total to {}".format(self.sum))
    else:
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

  def ace_value(self,card):
    if self.sum > 16:
      self.sum -= card.value
      card.change_ace()
      
  def begin_play(self):
    for x in range(2):
      card = self.manager.draw()
      if self.manager.is_ace(card.value):
        self.ace_value(card)
      self.cards.append(card)
      self.sum += card.value
      if self.hide:
        print("The Dealer's card is hidden")
      else:
        print("Dealer drew a card of value {}". format(card.value))
        print("The Dealer's score is {}".format(self.sum))
        self.hide = True
  
  def play(self):
    # Dealer must take cards until his score is 17 or above
    while self.sum <= 16:
      card = self.manager.draw()
      if self.manager.is_ace(card.value):
        self.ace_value(card)
      self.cards.append(card)
      self.sum += card.value
    print("The Dealer's points total to {}".format(self.sum))

def winner(player, dealer):
  if player.sum <= 21 and player.sum > dealer.sum or dealer.sum > 21:
    print("{} won".format(player.name))
    player.budget += player.bet*2
    dealer.budget -= player.bet
  elif player.sum <= 21 and player.sum == dealer.sum:
    print("It's a draw")
  elif player.sum > 21 and dealer.sum > 21:
    print("Both bust. Draw!")
  else:
    print("The Dealer won")
    dealer.budget += player.bet

def __main__():
  # Start of the game
  dealer = Dealer()
  print("Welcome to a game of Blackjack!")
  player1 = Player(input("Enter your name "),int(input("Enter your budget ")), dealer)
  # Initial bets
  print("The player must make the initial bet")
  player1.bet()
  # First draw
  player1.begin_play()
  dealer.begin_play()
  # Main play
  while player1.keep_playing:
    player1.play()
  else:
    dealer.play()
  winner(player1, dealer)
__main__()
