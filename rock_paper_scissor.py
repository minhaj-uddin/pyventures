import random

ROCK = 'r'
SCISSORS = 's'
PAPER = 'p'
emojis = { ROCK: '🪨', SCISSORS: '✂️', PAPER: '📃' }
choices = tuple(emojis.keys())

# Score counters
user_win = 0
user_loss = 0
user_tie = 0

def get_user_choice():
  while True:
    user_choice = input('Rock, paper, or scissors? (r/p/s): ').lower()
    print(choices)
    
    if user_choice in choices:
      return user_choice      
    else:
      print('Invalid choice!')


def display_choices(user_choice, computer_choice):
  print(f'You chose {emojis[user_choice]}')
  print(f'Computer chose {emojis[computer_choice]}')


def determine_winner(user_choice, computer_choice):
  global user_win, user_loss, user_tie
  
  if user_choice == computer_choice:
    user_tie += 1
    print('Tie!')
  elif (
    (user_choice == ROCK and computer_choice == SCISSORS) or 
    (user_choice == SCISSORS and computer_choice == PAPER) or 
    (user_choice == PAPER and computer_choice == ROCK)):
    user_win += 1
    print('You win')
  else:
    user_loss += 1
    print('You lose')  


def play_game():
  while True:
    user_choice = get_user_choice()

    computer_choice = random.choice(choices)

    display_choices(user_choice, computer_choice)

    determine_winner(user_choice, computer_choice)

    should_continue = input('Continue? (y/n): ').lower()
    if should_continue == 'n':
      print(f"Win: {user_win}, Loss: {user_loss}, Tie: {user_tie}")
      break


play_game()
