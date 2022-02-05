""" Lab 7 - User Control """

import arcade
import random as rand

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
coords_empty = []
moon_size = int(100/(SCREEN_WIDTH/SCREEN_HEIGHT))


def no_intersect(num, x_coord_min, x_coord_max, y_coord_min, y_coord_max, dist_min, dist_max):

    set_coords = []
    while len(set_coords) <= num:
        if len(set_coords) == num:
            break

        if len(set_coords) < 1:
            set_coords.append([rand.randint(x_coord_min, x_coord_max), rand.randint(y_coord_min, y_coord_max)])

        x_t = rand.randint(x_coord_min, x_coord_max)
        y_t = rand.randint(y_coord_min, y_coord_max)

        cond = True
        for c_x, c_y in set_coords:
            a = int((((c_x - x_t) ** 2) + ((c_y - y_t) ** 2)) ** 0.5)
            b = rand.randint(dist_min, dist_max)
            if a <= b and a != 0:
                cond = False
                break
        if [x_t, y_t] not in set_coords and cond is True:

            set_coords.append([x_t, y_t])
    return set_coords


stars_coords = no_intersect(200, 1, SCREEN_WIDTH, int(SCREEN_HEIGHT / 3), SCREEN_HEIGHT, 10, 30)


def place_craters(crater_coordinates, craters, size, size_min, size_max):
    while len(crater_coordinates) <= craters:  # пока кратеров менее craters
        if len(crater_coordinates) == craters:
            break

        if len(crater_coordinates) < 1:  # первый кратер
            crater_coordinates.append([rand.randint(-int(size * 0.6), int(size * 0.6)),
                                       rand.randint(-int(size * 0.6), int(size * 0.6)),
                                       rand.randint(size_min, size_max)])

        x_t = rand.randint(-int(size * 0.6), int(size * 0.6))  # случайные координаты след кратера
        y_t = rand.randint(-int(size * 0.6), int(size * 0.6))
        s_t = rand.randint(size_min, size_max)  # случайный размер след кратера

        cond = True  # есть ли место для кратера?
        for c_x, c_y, c_size in crater_coordinates:
            a = int((((c_x-x_t)**2) + ((c_y-y_t)**2))**0.5)  # расстояние между ц. старого и нового кратеров
            b = int(c_size/2 + s_t/2 + rand.randint(15, 30))  # минимальное расстояние между ц. кратеров
            if a <= b and a != 0:  # если негде делать новый кратер и он не совпадает со старым центрами
                cond = False  # мест нет
                break
        if [x_t, y_t, s_t] not in crater_coordinates \
                and cond is True:  # если этих координат в списке нет и есть место
            crater_coordinates.append([x_t, y_t, s_t])  # добавить кратер
    return crater_coordinates


crater_coords = place_craters(coords_empty, 15, moon_size, 7, 15)


class Stars:
    def __init__(self, num):
        self.num = int(num * (SCREEN_WIDTH / SCREEN_HEIGHT))
        self.stars_coords = stars_coords

    def draw(self):
        for star in self.stars_coords:
            arcade.draw_ellipse_filled(star[0], star[1], 10, 2, arcade.color.DUTCH_WHITE)
            arcade.draw_ellipse_filled(star[0], star[1], 2, 10, arcade.color.DUTCH_WHITE)


class Moon:
    def __init__(self, x, y, size, craters):
        self.x = x
        self.y = y
        self.size = size
        self.crater_coords = craters

    def draw(self):
        # defining the moon disk
        arcade.draw_circle_filled(self.x, self.y, self.size, arcade.color.GRAY)

        for crater in self.crater_coords:
            arcade.draw_circle_filled(self.x + crater[0], self.y + crater[1], crater[2], arcade.color.DIM_GRAY)


class Snowman:

    def __init__(self, position_x, position_y, change_x, change_y, scale, snow_color, movement_speed):
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.scale = scale
        self.snow_color = snow_color
        self.movement_speed = movement_speed
        self.laser_sound = arcade.load_sound("laser.wav")
        self.laser_sound_player = None

    def draw(self):
        """
        draw a snowman
        """

        # Lower ball outlined
        arcade.draw_circle_filled(self.position_x, self.position_y, int(90 / 100 * self.scale), arcade.color.WHITE)
        arcade.draw_circle_outline(self.position_x, self.position_y, int(90 / 100 * self.scale), arcade.color.BLACK,
                                   int(5 / 100 * self.scale))

        # Arms
        arcade.draw_line(self.position_x + int(150 / 100 * self.scale), self.position_y + int(50 / 100 * self.scale),
                         self.position_x - int(150 / 100 * self.scale), self.position_y + int(170 / 100 * self.scale),
                         arcade.color.DEEP_COFFEE,
                         int(10 / 100 * self.scale))

        # Middle ball outline
        arcade.draw_circle_filled(self.position_x, self.position_y + int(100 / 100 * self.scale),
                                  int(70 / 100 * self.scale), arcade.color.WHITE)
        arcade.draw_circle_outline(self.position_x, self.position_y + int(100 / 100 * self.scale),
                                   int(70 / 100 * self.scale), arcade.color.BLACK,
                                   int(5 / 100 * self.scale))

        # Upper ball outlined
        arcade.draw_circle_filled(self.position_x, self.position_y + int(170 / 100 * self.scale),
                                  int(50 / 100 * self.scale), arcade.color.WHITE)
        arcade.draw_circle_outline(self.position_x, self.position_y + int(170 / 100 * self.scale),
                                   int(50 / 100 * self.scale),
                                   arcade.color.BLACK, int(5 / 100 * self.scale))

        # Bucket
        arcade.draw_polygon_filled([[self.position_x - int(30 / 100 * self.scale),
                                     self.position_y + int(210 / 100 * self.scale)],
                                    [self.position_x + int(45 / 100 * self.scale),
                                     self.position_y + int(190 / 100 * self.scale)],
                                    [self.position_x + int(45 / 100 * self.scale),
                                     self.position_y + int(270 / 100 * self.scale)],
                                    [self.position_x, self.position_y + int(280 / 100 * self.scale)]],
                                   arcade.color.GRAY)

        arcade.draw_polygon_outline([[self.position_x - int(30 / 100 * self.scale),
                                      self.position_y + int(210 / 100 * self.scale)],
                                     [self.position_x + int(45 / 100 * self.scale),
                                      self.position_y + int(190 / 100 * self.scale)],
                                     [self.position_x + int(45 / 100 * self.scale),
                                      self.position_y + int(270 / 100 * self.scale)],
                                     [self.position_x, self.position_y + int(280 / 100 * self.scale)]],
                                    arcade.color.BLACK, int(4 / 100 * self.scale))

        # Eyes
        arcade.draw_circle_filled(self.position_x - int(20 / 100 * self.scale),
                                  self.position_y + int(190 / 100 * self.scale), int(5 / 100 * self.scale),
                                  arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x + int(20 / 100 * self.scale),
                                  self.position_y + int(190 / 100 * self.scale), int(5 / 100 * self.scale),
                                  arcade.color.BLACK)

        # Nose
        arcade.draw_triangle_filled(self.position_x, self.position_y + int(160 / 100 * self.scale),
                                    self.position_x, self.position_y + int(180 / 100 * self.scale),
                                    self.position_x - int(80 / 100 * self.scale),
                                    self.position_y + int(170 / 100 * self.scale), arcade.color.ORANGE)

        # Mouth
        arcade.draw_circle_filled(self.position_x, self.position_y + int(140 / 100 * self.scale),
                                  int(5 / 100 * self.scale), arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x - int(15 / 100 * self.scale),
                                  self.position_y + int(145 / 100 * self.scale), int(5 / 100 * self.scale),
                                  arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x + int(15 / 100 * self.scale),
                                  self.position_y + int(145 / 100 * self.scale), int(5 / 100 * self.scale),
                                  arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x - int(25 / 100 * self.scale),
                                  self.position_y + int(157 / 100 * self.scale), int(5 / 100 * self.scale),
                                  arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x + int(25 / 100 * self.scale),
                                  self.position_y + int(157 / 100 * self.scale), int(5 / 100 * self.scale),
                                  arcade.color.BLACK)

        # Buttons
        arcade.draw_circle_filled(self.position_x, self.position_y + int(105 / 100 * self.scale),
                                  int(8 / 100 * self.scale), arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x, self.position_y + int(75 / 100 * self.scale),
                                  int(8 / 100 * self.scale), arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x, self.position_y + int(45 / 100 * self.scale),
                                  int(8 / 100 * self.scale), arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x, self.position_y + int(15 / 100 * self.scale),
                                  int(8 / 100 * self.scale), arcade.color.BLACK)
        arcade.draw_circle_filled(self.position_x, self.position_y - int(15 / 100 * self.scale),
                                  int(8 / 100 * self.scale), arcade.color.BLACK)

        # Legs
        arcade.draw_circle_filled(self.position_x - int(70 / 100 * self.scale),
                                  self.position_y - int(90 / 100 * self.scale), int(40 / 100 * self.scale),
                                  arcade.color.WHITE,
                                  int(5 / 100 * self.scale))

        arcade.draw_circle_filled(self.position_x + int(70 / 100 * self.scale),
                                  self.position_y - int(90 / 100 * self.scale), int(40 / 100 * self.scale),
                                  arcade.color.WHITE,
                                  int(5100 * self.scale))

        arcade.draw_circle_outline(self.position_x - int(70 / 100 * self.scale),
                                   self.position_y - int(90 / 100 * self.scale), int(40 / 100 * self.scale),
                                   arcade.color.BLACK,
                                   int(5 / 100 * self.scale))

        arcade.draw_circle_outline(self.position_x + int(70 / 100 * self.scale),
                                   self.position_y - int(90 / 100 * self.scale), int(40 / 100 * self.scale),
                                   arcade.color.BLACK,
                                   int(5 / 100 * self.scale))

        arcade.draw_line(self.position_x - int(110 / 100 * self.scale), self.position_y - int(90 / 100 * self.scale),
                         self.position_x - int(30 / 100 * self.scale),
                         self.position_y - int(90 / 100 * self.scale),
                         arcade.color.BLACK, int(10 / 100 * self.scale))

        arcade.draw_line(self.position_x + int(30 / 100 * self.scale), self.position_y - int(90 / 100 * self.scale),
                         self.position_x + int(110 / 100 * self.scale),
                         self.position_y - int(90 / 100 * self.scale),
                         arcade.color.BLACK, int(10 / 100 * self.scale))

        arcade.draw_rectangle_filled(self.position_x, self.position_y - int(110 / 100 * self.scale),
                                     int(240 / 100 * self.scale), int(40 / 100 * self.scale),
                                     self.snow_color)

    def update(self):
        # Move the snowman
        self.position_y += self.change_y
        self.position_x += self.change_x

        # See if the snowman hit the edge of the screen. If so, change direction
        if self.position_x < int(150 / 100 * self.scale):
            self.position_x = int(150 / 100 * self.scale)
            arcade.play_sound(self.laser_sound)

        if self.position_x > SCREEN_WIDTH - int(150 / 100 * self.scale):
            self.position_x = SCREEN_WIDTH - int(150 / 100 * self.scale)
            arcade.play_sound(self.laser_sound)

        if self.position_y < (int(90 / 100 * self.scale)):
            self.position_y = (int(90 / 100 * self.scale))
            arcade.play_sound(self.laser_sound)

        if self.position_y > (SCREEN_HEIGHT / 3) + (int(90 / 100 * self.scale)):
            self.position_y = (SCREEN_HEIGHT / 3) + (int(90 / 100 * self.scale))
            arcade.play_sound(self.laser_sound)


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(width, height, title)
        self.stars = Stars(338)
        self.moon = Moon(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.8), moon_size, crater_coords)
        self.snowman = Snowman(50, 50, 0, 0, 40, arcade.color.WHITE, 3)

    def on_draw(self):
        """Draw a background."""
        arcade.set_background_color(arcade.color.DARK_BLUE)
        arcade.start_render()
        self.stars.draw()
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT / 3, 0, arcade.color.WHITE)
        self.moon.draw()
        self.snowman.draw()

    def on_update(self, delta_time):
        self.snowman.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.A:
            self.snowman.change_x = -self.snowman.movement_speed
        elif key == arcade.key.D:
            self.snowman.change_x = self.snowman.movement_speed
        elif key == arcade.key.W:
            self.snowman.change_y = self.snowman.movement_speed
        elif key == arcade.key.S:
            self.snowman.change_y = -self.snowman.movement_speed

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.A or key == arcade.key.D:
            self.snowman.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.snowman.change_y = 0

        print(f'Position: {self.snowman.position_x}, {int(self.snowman.position_y)}')


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'lab 7 - user control')
    arcade.run()


main()
