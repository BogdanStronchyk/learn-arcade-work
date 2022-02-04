# starting...
# A Camel game
import random as r


def main():

    print('Welcome to Camel!')
    print('You have stolen a camel to make your way across the great Mobi desert.')
    print('The natives want their camel back and are chasing you down!')
    print('Survive your desert trek and out run the natives.')

    done = False
    miles = 0
    thirst = 0
    drinks = 3
    camel_tiredness = 0
    natives_distance = -20

    def oasis(chance, water):

        if chance == 20 and water < 3:
            print('You have found an oasis and refilled your canteen!')
            water = 3

        elif chance == 20 and water == 3:
            print('You have found an oasis!')
            print('But you still have a full canteen of water')
            print('and you decided to move on...')

        return water

    while not done:
        print('')
        print('A. Drink from your canteen.')
        print('B. Ahead moderate speed.')
        print('C. Ahead full speed.')
        print('D. Stop for the night.')
        print('E. Status check.')
        print('Q. Quit.')
        print('')

        user_choice = input('Your choice: ')

        luck = r.randint(1, 20)

        if user_choice.upper() == 'A':
            if drinks > 1 and thirst > 1:
                print('You decided to drink some water.')
                drinks -= 1
                thirst = 0

            elif drinks > 1 and thirst == 0:
                print('You are not thirsty! Don\'t waste the water!')

            else:
                print('Your ran out of water! Now the real challenge begins...')

        elif user_choice.upper() == 'B':
            print('You decided to ride without a hurry.')
            miles_t = r.randint(5, 12)
            print(f'You travelled {miles_t} miles')
            miles += miles_t
            thirst += 1
            camel_tiredness += 1
            natives_distance += r.randint(7, 14)
            drinks = oasis(luck, drinks)

        elif user_choice.upper() == 'C':
            print('You decided to run for your life!')
            miles_t = r.randint(10, 20)
            print(f'You travelled {miles_t} miles')
            miles += miles_t
            thirst += 1
            camel_tiredness += r.randint(1, 3)
            natives_distance += r.randint(7, 14)
            drinks = oasis(luck, drinks)

        elif user_choice.upper() == 'D':
            print('You decided to stop for the night.')
            print('Your camel feels fresh and rested!')
            camel_tiredness = 0
            natives_distance += r.randint(7, 14)

        elif user_choice.upper() == 'E':
            print(f'Miles travelled: {miles}')
            print(f'Drinks in canteen: {drinks}')
            print(f'The natives are {abs(miles - natives_distance)} miles behind you')

        elif user_choice.upper() == 'Q':
            print('You have decided to abandon this poor man...')
            user_choice = input('Are you sure you want to hand his soul to the chance himself? Y/N ')
            if user_choice.upper() == 'Y':
                done = True
            elif user_choice.upper() == 'N':
                continue

        # The ending scenarios
        if 4 < thirst <= 6 and not done:
            print('You are thirsty!')
        elif thirst > 6 and not done:
            print('You died of thirst!')
            done = True

        if 5 < camel_tiredness <= 8 and not done:
            print('Your camel is tired.')
        elif camel_tiredness > 8 and not done:
            print('Your camel is dead.')
            done = True

        if abs(natives_distance - miles) <= 15 and not done:
            print('The natives are getting closer!')
        elif natives_distance >= miles and not done:
            print('The natives ran over you and lynched on the spot!')
            done = True

        if miles >= 200 and not done:
            print('You made it across the desert! You won!')
            done = True


main()
