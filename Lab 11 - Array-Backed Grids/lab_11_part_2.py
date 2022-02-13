
import arcade
import numpy

WIDTH = 20
HEIGHT = 20
MARGIN = 5
ROW_COUNT = 10
COLUMN_COUNT = 10


SCREEN_WIDTH = ROW_COUNT * WIDTH + MARGIN * (ROW_COUNT + 1)
SCREEN_HEIGHT = COLUMN_COUNT * HEIGHT + MARGIN * (COLUMN_COUNT + 1)


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

        self.grid = numpy.zeros([ROW_COUNT, COLUMN_COUNT])


    def on_draw(self):
        """
        Render the screen.
        """

        self.clear()
        for row in range(0, ROW_COUNT):
            for column in range(0, COLUMN_COUNT):

                if self.grid[row][column] == 1:
                    color = arcade.color.GREEN

                else:
                    color = arcade.color.WHITE

                arcade.draw_rectangle_filled(WIDTH/2 * (column * 2) + WIDTH/2 + MARGIN * (1 + column),
                                             HEIGHT/2 * (row * 2) + HEIGHT/2 + MARGIN * (1 + row),
                                             WIDTH, HEIGHT, color)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        column = x//(WIDTH + MARGIN)
        row = y//(HEIGHT + MARGIN)
        print('')
        print(f"Click: {x, y}; Grid coords: {column, row}")
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.grid[row][column] == 0:
                self.grid[row][column] = 1
            else:
                self.grid[row][column] = 0

            if row + 1 < ROW_COUNT:
                if self.grid[row + 1][column] == 0:
                    self.grid[row + 1][column] = 1
                else:
                    self.grid[row + 1][column] = 0

            if row - 1 >= 0:
                if self.grid[row - 1][column] == 0:
                    self.grid[row - 1][column] = 1
                else:
                    self.grid[row - 1][column] = 0

            if column + 1 < COLUMN_COUNT:
                if self.grid[row][column + 1] == 0:
                    self.grid[row][column + 1] = 1
                else:
                    self.grid[row][column + 1] = 0

            if column - 1 >= 0:
                if self.grid[row][column - 1] == 0:
                    self.grid[row][column - 1] = 1
                else:
                    self.grid[row][column - 1] = 0

        print('')
        print(f'Total of {int(self.grid.sum())} cells are selected')
        for i in range(0, ROW_COUNT):
            if int(self.grid[i].sum()) > 0:
                print(f'Row {i}: total of {int(self.grid[i].sum())} cells are selected')

        for i in range(0, ROW_COUNT):
            if int(self.grid[:, i].sum()) > 0:
                print(f'Column {i}: total of {int(self.grid[:, i].sum())} cells are selected')


def main():

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
