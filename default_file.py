""" Sprite Sample Program """

import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_NAME = "Sprites With Walls Example"


# --- Variables ---


# Classes
class MyClass1:
    pass


class MyClass2:
    pass


class MyClass3:
    pass


# Main window class
class MyGame(arcade.Window):
    """ This class represents the main window of the game. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME)

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
