"""
This is a sample program to show how to draw using the Python programming
language and the Arcade library.
"""

# Import the "arcade" library
import arcade

# Open up a window.
# From the "arcade" library, use a function called "open_window"
# Set the window title to "Drawing Example"
# Set the and dimensions (width and height)
window_width = 800
window_height = 800
arcade.open_window(window_width, window_height, "The snowman")

# Set the background color
arcade.set_background_color(arcade.color.DIAMOND)

# Get ready to draw
arcade.start_render()

# Draw the snow
arcade.draw_lrtb_rectangle_filled(0, window_width, window_height / 3, 0, arcade.color.WHITE)

# --- Draw the snowman ---
# Lower ball outlined
arcade.draw_circle_filled(400, 250, 90, arcade.color.WHITE)
arcade.draw_circle_outline(400, 250, 90, arcade.color.BLACK, 5)

# Arms
arcade.draw_line(550, 300, 250, 420, arcade.color.DEEP_COFFEE, 10)

# Middle ball outlined
arcade.draw_circle_filled(400, 350, 70, arcade.color.WHITE)
arcade.draw_circle_outline(400, 350, 70, arcade.color.BLACK, 5)

# Upper ball outlined
arcade.draw_circle_filled(400, 420, 50, arcade.color.WHITE)
arcade.draw_circle_outline(400, 420, 50, arcade.color.BLACK, 5)

# Bucket
arcade.draw_polygon_filled([[370, 460], [445, 440], [445, 520], [400, 530]], arcade.color.GRAY)

# Eyes
arcade.draw_circle_filled(380, 440, 5, arcade.color.BLACK)
arcade.draw_circle_filled(420, 440, 5, arcade.color.BLACK)

# Nose
arcade.draw_triangle_filled(400, 410, 400, 430, 320, 420, arcade.color.ORANGE)

# Mouth
arcade.draw_circle_filled(400, 390, 5, arcade.color.BLACK)
arcade.draw_circle_filled(385, 395, 5, arcade.color.BLACK)
arcade.draw_circle_filled(415, 395, 5, arcade.color.BLACK)
arcade.draw_circle_filled(375, 407, 5, arcade.color.BLACK)
arcade.draw_circle_filled(425, 407, 5, arcade.color.BLACK)

# Buttons
arcade.draw_circle_filled(400, 355, 8, arcade.color.BLACK)
arcade.draw_circle_filled(400, 325, 8, arcade.color.BLACK)
arcade.draw_circle_filled(400, 295, 8, arcade.color.BLACK)
arcade.draw_circle_filled(400, 265, 8, arcade.color.BLACK)
arcade.draw_circle_filled(400, 235, 8, arcade.color.BLACK)

# Legs
arcade.draw_circle_filled(330, 160, 40, arcade.color.WHITE, 5)
arcade.draw_circle_filled(470, 160, 40, arcade.color.WHITE, 5)
arcade.draw_circle_outline(330, 160, 40, arcade.color.BLACK, 5)
arcade.draw_circle_outline(470, 160, 40, arcade.color.BLACK, 5)
arcade.draw_line(290, 160, 370, 160, arcade.color.BLACK, 10)
arcade.draw_line(430, 160, 510, 160, arcade.color.BLACK, 10)
arcade.draw_rectangle_filled(400, 140, 520-280, 40, arcade.color.WHITE)


# --- Finish drawing ---
arcade.finish_render()

# Keep the window up until someone closes it.
arcade.run()