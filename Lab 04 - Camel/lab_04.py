# starting...
# A Camel game
import random as r


def main():

    print('Welcome to Camel!')
    print('You have stolen a camel to make your way across the great Mobi desert.')
    print('The natives want their camel back and are chasing you down!')
    print('Survive your desert trek and out run the natives.')

    done = False
    user_choice = ''
    miles = 0
    thirst = 0
    drinks = 3
    camel_tiredness = 0
    natives_distance = -20
    while not done:
        print('A. Drink from your canteen.')
        print('B. Ahead moderate speed.')
        print('C. Ahead full speed.')
        print('D. Stop for the night.')
        print('E. Status check.')
        print('Q. Quit.')

        user_choice = input('Your choice: ')

        if user_choice.upper() == 'A':
            pass

        elif user_choice.upper() == 'B':
            pass

        elif user_choice.upper() == 'C':
            pass

        elif user_choice.upper() == 'D':
            print('You decided to stop for the night.')
            print('Your camel feels fresh and rested!')
            camel_tiredness = 0
            natives_distance = r.randint(7, 14)

        elif user_choice.upper() == 'E':
            print(f'Miles travelled: {miles}')
            print(f'Drinks in canteen: {drinks}')
            print(f'The natives are {miles} miles behind you')

        elif user_choice.upper() == 'Q':
            print('You have decided to abandon this poor man...')
            user_choice = input('Are you sure you want to hand his soul to the chance himself? Y/N ')
            if user_choice.upper() == 'Y':
                done = True
            elif user_choice.upper() == 'N':
                continue


main()
