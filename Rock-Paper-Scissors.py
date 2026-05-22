# rock paper scissors game 

import random, sys

SCORE = {
    'wins': 0, 
    'losses': 0, 
    'ties': 0
}
CHOICES = ['rock', 'paper', 'scissors']


def show_score():
    wins, losses, ties = SCORE.values()
    # wins =      SCORE['wins']
    # losses =    SCORE['losses']
    # ties =      SCORE['ties']
    print('Scoreboard: ')
    print(f'Wins: {wins}, Losses: {losses}, Ties: {ties}.')

def get_user_input():
    try: 
        possible_inputs = []
        possible_inputs.extend(CHOICES)
        possible_inputs.append('quit')
        # print(possible_inputs)

        to_print = [f'[{i[0]}]{i[1:]}' for i in possible_inputs]
        to_print = f'Enter {', '.join(to_print[0: -1])}, or {to_print[-1]}:'        

        # print('Enter [r]ock, [p]aper, [s]cissors, or [q]uit:')
        print(to_print)
        user_input = input('').lower().strip()[0]
        # print(user_input)

        if user_input == 'q': 
            print('Exiting.\n')
            sys.exit()

        if not user_input.isalpha() or user_input not in (i[0] for i in CHOICES): 
            # print(user_input.isalpha()) 
            raise Exception

        return user_input
    except Exception: 
        print('An error occured.\n')
        return 'error'
        # sys.exit()
    # print('')

def generate_computer_input():
    computer_input = CHOICES[random.randint(0, len(CHOICES) - 1)]
    print(f'The computer chose: {computer_input.title()}.')
    return computer_input[0] 

def update_score(user, comp):
    if user == comp: 
        SCORE['ties'] += 1
        SCORE['losses'] += 1
        print('It was a tie.\n')

    elif user == 'r' and comp == 'p': 
        SCORE['losses'] += 1
        print('You lost.\n')
    elif user == 'r' and comp == 's': 
        SCORE['wins'] += 1
        print('You won!\n')

    elif user == 'p' and comp == 'r': 
        SCORE['wins'] += 1
        print('You won!\n')
    elif user == 'p' and comp == 's': 
        SCORE['losses'] += 1
        print('You lost.\n')

    elif user == 's' and comp == 'r': 
        SCORE['losses'] += 1
        print('You lost.\n')
    elif user == 's' and comp == 'p': 
        SCORE['wins'] += 1
        print('You won!\n')

def main(): 
    show_score()
    user_input = get_user_input()
    if not (user_input == 'error'): 
        computer_input = generate_computer_input()
        update_score(user_input, computer_input)
    main()
    # sys.exit()

print('Welcome to this Rock-Paper-Scissors game!\n')
main()