# Dungeon adventure


class Room:
    description = ''
    west = 0
    north = 0
    east = 0
    south = 0

    def __init__(self, description,  west, north, east, south):
        self.description = description
        self.west = west
        self.north = north
        self.east = east
        self.south = south


def main():
    room_list = []
    room = Room('You are in the dusty stone corridor, leading south.', None, None, None, 1)
    room_list.append(room)
    room = Room('You are in the dusty stone corridor, leading north and south.', None, 0, None, 2)
    room_list.append(room)
    room = Room('You are in the dusty stone corridor, leading west, north and south.', 3, 1, None, 5)
    room_list.append(room)
    room = Room('You are in the armory. '
                'Rusty spears, swords and breastplates are covered in web. '
                'There are doors to the north and east', None, 4, 2, None)
    room_list.append(room)
    room = Room('You are in the barracks. '
                'Some beds are broken, other have a thick layer of dust on them. '
                'There is a door to the south', None, None, None, 3)
    room_list.append(room)
    room = Room('You are in the dusty stone corridor, leading north, east and south.', None, 2, 6, 8)
    room_list.append(room)
    room = Room('You are in the supplies room. Some wooden crates and barrels stink... '
                'There are doors to the west and north', 5, 7, None, None)
    room_list.append(room)
    room = Room('You are in the kitchen. Everything is rotten and stinks even more. '
                'There is a door to the south', None, None, None, 6)
    room_list.append(room)
    room = Room('You are in the dusty stone corridor, leading west and north.', 9, 5, None, None)
    room_list.append(room)
    room = Room('You are in the dusty stone corridor, leading west and east.', 10, None, 8, None)
    room_list.append(room)
    room = Room('You are in the officer\'s canteen. Rotten dishes lying on the table.'
                'There is a door to the east', None, None, 9, None)
    room_list.append(room)

    done = False
    current_room = 0
    while not done:
        print('')
        print(room_list[current_room].description)
        print('W: go west')
        print('N: go north')
        print('E: go east')
        print('S: go south')
        print('Q: quit')
        player_input = input('Actions: ')

        if current_room == 0 and player_input.upper() == 'N':
            print('You left the dungeon')
            break

        if player_input.upper() == 'W':
            next_room = room_list[current_room].west

            if next_room is None:
                print('There is nothing on this direction')
            else:
                current_room = next_room

        elif player_input.upper() == 'N':
            next_room = room_list[current_room].north

            if next_room is None:
                print('There is nothing on this direction')
            else:
                current_room = next_room

        elif player_input.upper() == 'E':
            next_room = room_list[current_room].east

            if next_room is None:
                print('There is nothing on this direction')
            else:
                current_room = next_room

        elif player_input.upper() == 'S':
            next_room = room_list[current_room].south

            if next_room is None:
                print('There is nothing on this direction')
            else:
                current_room = next_room

        elif player_input.upper() == 'Q':
            print('You left the dungeon')
            break

        else:
            print('Select the direction')


main()
