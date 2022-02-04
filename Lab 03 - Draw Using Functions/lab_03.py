# Import the "arcade" library
import arcade
import random as rand

# Setting variables for dimensions (width and height)
window_width = 1920
window_height = 1080


# Draw the snowman function
def snowman(x, y, scale,  snow_color):
    """
    :param x: x coord
    :param y: y coord
    :param scale: scaling a snowman. Only >=1!
    :param snow_color: snowman's color
    """

    # Lower ball outlined
    arcade.draw_circle_filled(x, y, int(90/100*scale), arcade.color.WHITE)
    arcade.draw_circle_outline(x, y, int(90/100*scale), arcade.color.BLACK, int(5/100*scale))

    # Arms
    arcade.draw_line(x + int(150/100*scale), y + int(50/100*scale),
                     x - int(150/100*scale), y + int(170/100*scale), arcade.color.DEEP_COFFEE, int(10/100*scale))

    # Middle ball outline
    arcade.draw_circle_filled(x, y + int(100/100*scale), int(70/100*scale), arcade.color.WHITE)
    arcade.draw_circle_outline(x, y + int(100/100*scale), int(70/100*scale), arcade.color.BLACK, int(5/100*scale))

    # Upper ball outlined
    arcade.draw_circle_filled(x, y + int(170/100*scale), int(50/100*scale), arcade.color.WHITE)
    arcade.draw_circle_outline(x, y + int(170/100*scale), int(50/100*scale),
                               arcade.color.BLACK, int(5/100*scale))

    # Bucket
    arcade.draw_polygon_filled([[x - int(30/100*scale), y + int(210/100*scale)],
                                [x + int(45/100*scale), y + int(190/100*scale)],
                                [x + int(45/100*scale), y + int(270/100*scale)],
                                [x, y + int(280/100*scale)]],
                               arcade.color.GRAY)
    arcade.draw_polygon_outline([[x - int(30 / 100 * scale), y + int(210 / 100 * scale)],
                                [x + int(45 / 100 * scale), y + int(190 / 100 * scale)],
                                [x + int(45 / 100 * scale), y + int(270 / 100 * scale)],
                                [x, y + int(280 / 100 * scale)]],
                                arcade.color.BLACK, int(4 / 100 * scale))

    # Eyes
    arcade.draw_circle_filled(x - int(20/100*scale), y + int(190/100*scale), int(5/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x + int(20/100*scale), y + int(190/100*scale), int(5/100*scale), arcade.color.BLACK)

    # Nose
    arcade.draw_triangle_filled(x, y + int(160/100*scale),
                                x, y + int(180/100*scale),
                                x - int(80/100*scale), y + int(170/100*scale), arcade.color.ORANGE)

    # Mouth
    arcade.draw_circle_filled(x, y + int(140/100*scale), int(5/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x - int(15/100*scale), y + int(145/100*scale), int(5/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x + int(15/100*scale), y + int(145/100*scale), int(5/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x - int(25/100*scale), y + int(157/100*scale), int(5/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x + int(25/100*scale), y + int(157/100*scale), int(5/100*scale), arcade.color.BLACK)

    # Buttons
    arcade.draw_circle_filled(x, y + int(105/100*scale), int(8/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x, y + int(75/100*scale), int(8/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x, y + int(45/100*scale), int(8/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x, y + int(15/100*scale), int(8/100*scale), arcade.color.BLACK)
    arcade.draw_circle_filled(x, y - int(15/100*scale), int(8/100*scale), arcade.color.BLACK)

    # Legs
    arcade.draw_circle_filled(x - int(70/100*scale), y - int(90/100*scale), int(40/100*scale), arcade.color.WHITE,
                              int(5/100*scale))

    arcade.draw_circle_filled(x + int(70/100*scale), y - int(90/100*scale), int(40/100*scale), arcade.color.WHITE,
                              int(5100*scale))

    arcade.draw_circle_outline(x - int(70/100*scale), y - int(90/100*scale), int(40/100*scale), arcade.color.BLACK,
                               int(5/100*scale))

    arcade.draw_circle_outline(x + int(70/100*scale), y - int(90/100*scale), int(40/100*scale), arcade.color.BLACK,
                               int(5/100*scale))

    arcade.draw_line(x - int(110/100*scale), y - int(90/100*scale), x - int(30/100*scale), y - int(90/100*scale),
                     arcade.color.BLACK, int(10/100*scale))

    arcade.draw_line(x + int(30/100*scale), y - int(90/100*scale), x + int(110/100*scale), y - int(90/100*scale),
                     arcade.color.BLACK, int(10/100*scale))

    arcade.draw_rectangle_filled(x, y - int(110/100*scale), int(240/100*scale), int(40/100*scale), snow_color)


# Defining a function that creates an array of non-intersecting coordinates for multiple objects
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


# Draw the moon function
def moon(x, y, size, craters, size_min, size_max):

    # defining the moon disk
    arcade.draw_circle_filled(x, y, size, arcade.color.GRAY)

    crater_coords = []
    while len(crater_coords) <= craters:  # пока кратеров менее craters
        if len(crater_coords) == craters:
            break

        if len(crater_coords) < 1:  # первый кратер
            crater_coords.append([rand.randint(-int(size * 0.6), int(size * 0.6)),
                                  rand.randint(-int(size * 0.6), int(size * 0.6)),
                                  rand.randint(size_min, size_max)])

        x_t = rand.randint(-int(size * 0.6), int(size * 0.6))  # случайные координаты след кратера
        y_t = rand.randint(-int(size * 0.6), int(size * 0.6))
        s_t = rand.randint(size_min, size_max)  # случайный размер след кратера

        cond = True  # есть ли место для кратера?
        for c_x, c_y, c_size in crater_coords:
            a = int((((c_x-x_t)**2) + ((c_y-y_t)**2))**0.5)  # расстояние между ц. старого и нового кратеров
            b = int(c_size/2 + s_t/2 + rand.randint(15, 30))  # минимальное расстояние между ц. кратеров
            if a <= b and a != 0:  # если негде делать новый кратер и он не совпадает со старым центрами
                cond = False  # мест нет
                break
        if [x_t, y_t, s_t] not in crater_coords \
                and cond is True:  # если этих координат в списке нет и есть место
            crater_coords.append([x_t, y_t, s_t])  # добавить кратер

    for crater in crater_coords:
        arcade.draw_circle_filled(x + crater[0], y + crater[1], crater[2], arcade.color.DIM_GRAY)


# Draw the stars function
def stars(star_num):

    stars_coords = no_intersect(star_num, 1, window_width, int(window_height / 3), window_height, 10, 30)

    for star in stars_coords:
        arcade.draw_ellipse_filled(star[0], star[1], 10, 2, arcade.color.DUTCH_WHITE)
        arcade.draw_ellipse_filled(star[0], star[1], 2, 10, arcade.color.DUTCH_WHITE)


# main window
def main():

    # Open up a window.
    # Set the window title to "The snowmen"

    arcade.open_window(window_width, window_height, "The snowmen")
    arcade.set_background_color(arcade.color.DARK_BLUE)

    # --- Start drawing ---
    arcade.start_render()

    # set stars
    stars(750)

    # Set the background color
    arcade.draw_lrtb_rectangle_filled(0, window_width, window_height / 3, 0, arcade.color.WHITE)

    # placing moon
    moon(int(window_width * 0.8), int(window_height * 0.8), 100, 15, 7, 20)

    # Multiplying snowmen
    snowmen = no_intersect(30, 20, window_width - 30, 50, window_height / 3, 30, 50)
    for x, y in snowmen:
        snowman(x, y, 21,  arcade.color.WHITE)

    # --- Finish drawing ---
    arcade.finish_render()

    # Keep the window up until someone closes it.
    arcade.run()


main()
