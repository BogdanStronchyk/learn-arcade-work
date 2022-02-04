import arcade

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MOVEMENT_SPEED = 3


class Ball:
    def __init__(self, position_x, position_y, change_x, change_y, radius, color):

        # Take the parameters of the init function above,
        # and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_circle_filled(self.position_x,
                                  self.position_y,
                                  self.radius,
                                  self.color)

    def update(self):
        # Move the ball
        self.position_y += self.change_y
        self.position_x += self.change_x
        # See if the ball hit the edge of the screen. If so, change direction
        if self.position_x < self.radius:
            self.position_x = self.radius

        if self.position_x > SCREEN_WIDTH - self.radius:
            self.position_x = SCREEN_WIDTH - self.radius

        if self.position_y < self.radius:
            self.position_y = self.radius

        if self.position_y > SCREEN_HEIGHT - self.radius:
            self.position_y = SCREEN_HEIGHT - self.radius


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.ASH_GREY)

        # Create our ball
        self.ball = Ball(50, 50, 0, 0, 15, arcade.color.AUBURN)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        self.ball.draw()

    # def on_mouse_motion(self, x, y, dx, dy):
    #     self.ball.position_x = x
    #     self.ball.position_y = y
    #
    # def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
    #     if button == arcade.MOUSE_BUTTON_LEFT:
    #         print("Left mouse button pressed at", x, y)
    #     elif button == arcade.MOUSE_BUTTON_RIGHT:
    #         print("Right mouse button pressed at", x, y)

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.A:
            self.ball.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.ball.change_x = MOVEMENT_SPEED
        elif key == arcade.key.W:
            self.ball.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.ball.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.A or key == arcade.key.D:
            self.ball.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.ball.change_y = 0


def main():
    window = MyGame(640, 480, "Drawing Example")
    arcade.run()


main()
