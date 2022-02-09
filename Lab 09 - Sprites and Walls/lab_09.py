"""
Sprite Sample Program
"""

import arcade
import random

# --- Constants ---
SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING_PLAYER = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_WIDTH_MARGIN = SCREEN_WIDTH * 4
SCREEN_HEIGHT_MARGIN = SCREEN_HEIGHT * 4 - 32


PLAYER_MOVEMENT_SPEED = 2

CAMERA_SPEED = 0.2

# --- Variables ---


class MyGame(arcade.Window):
    """ This class represents the main window of the game. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprites With Walls Example")

        # Initiate sound

        self.bump_sound = arcade.load_sound(":resources:sounds/error4.wav")
        self.sound_player = None

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.grass_list = None
        self.ceiling_list = None
        self.platform_list = None

        # Set up the player
        self.player_sprite = None

        # This variable holds our simple "physics engine"
        self.physics_wall = None
        self.physics_ceiling = None
        self.physics_grass = None
        self.physics_platform = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.timer = 0
        self.time_passed_after_left_pressed = 0
        self.time_passed_after_right_pressed = 0
        self.time_passed_after_up_pressed = 0
        self.time_passed_after_down_pressed = 0

        self.left_t = 0
        self.right_t = 0
        self.top_t = 0
        self.bottom_t = 0

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_for_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_for_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Reset the score
        self.score = 0

        # FPS counter
        self.fps = 0

    def setup(self):

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.grass_list = arcade.SpriteList()
        self.ceiling_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Create the player
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # This identifies the player character
        # and a lists of sprites that the player character isn’t allowed to pass through.
        self.physics_wall = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.physics_ceiling = arcade.PhysicsEngineSimple(self.player_sprite, self.ceiling_list)
        self.physics_grass = arcade.PhysicsEngineSimple(self.player_sprite, self.grass_list)
        self.physics_platform = arcade.PhysicsEngineSimple(self.player_sprite, self.platform_list)

        # Place boxes inside a loop
        for y in range(32, SCREEN_HEIGHT_MARGIN, 64):
            for x in range(32, SCREEN_WIDTH_MARGIN, 64):
                grass = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING_BOX)
                wall = arcade.Sprite(":resources:images/tiles/stoneCenter_rounded.png", SPRITE_SCALING_BOX)
                ceiling = arcade.Sprite(":resources:images/tiles/bridgeB.png", SPRITE_SCALING_BOX)
                platform = arcade.Sprite(":resources:images/tiles/grassHalf_mid.png", SPRITE_SCALING_BOX)

                if y == 32 and 32 < x <= SCREEN_WIDTH_MARGIN - 64:
                    grass.center_x = x
                    grass.center_y = y
                    self.grass_list.append(grass)

                if 32 <= y < SCREEN_HEIGHT_MARGIN and x <= 32 or x >= SCREEN_WIDTH_MARGIN - 32:
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

                if y == SCREEN_HEIGHT_MARGIN - 32 and 32 < x <= SCREEN_WIDTH_MARGIN - 64:
                    ceiling.center_x = x
                    ceiling.center_y = y
                    self.ceiling_list.append(ceiling)

                if y % 64 == 0 and 32 < x <= SCREEN_WIDTH_MARGIN - 64:
                    if random.randrange(5) > 0:
                        platform.center_x = x
                        platform.center_y = y
                        self.platform_list.append(wall)




    def scroll_to_player(self):
        """Scroll the window to the player."""
        #
        # If CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        # Anything between 0 and 1 will have the camera move to the location with a smoother
        # pan.

        lower_left_corner = (self.player_sprite.center_x - self.width / 2,
                             self.player_sprite.center_y - self.height / 2)
        # noinspection PyTypeChecker
        self.camera_for_sprites.move_to(lower_left_corner, CAMERA_SPEED)

    def on_draw(self):
        self.clear()

        # Select the scrolled camera for our sprites
        self.camera_for_sprites.use()

        # Draw the sprites
        self.wall_list.draw()
        self.grass_list.draw()
        self.ceiling_list.draw()
        self.platform_list.draw()
        self.player_list.draw()
        arcade.draw_rectangle_outline(SCREEN_WIDTH_MARGIN / 2, SCREEN_HEIGHT_MARGIN / 2,
                                      SCREEN_WIDTH_MARGIN, SCREEN_HEIGHT_MARGIN, arcade.color.BLACK, 1)

        # Select the (unscrolled) camera for our GUI
        self.camera_for_gui.use()
        arcade.draw_text(f"Score: {self.score}", 10, 10, arcade.color.WHITE, 24)

        arcade.draw_text(f"FPS: {self.fps:.2f}", SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.9, arcade.color.WHITE, 24)

        arcade.draw_text(f"Coords: {self.player_sprite.center_x}, {self.player_sprite.center_y}",
                         SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.9, arcade.color.WHITE, 24)

    def update(self, delta_time):
        # calculating fps
        self.fps = 1 / delta_time

        # move character:
        self.control()

        # See if the player hit the edge of the screen
        flag = self.check_screen_collision()

        #  If there is no player, or the playing boolean is false, and the player hit the wall, we’ll play the sound.
        if (not self.sound_player or not self.sound_player.playing) and flag:
            self.sound_player = arcade.play_sound(self.bump_sound)

        # We used to update sprite lists like this:
        # self.player_list.update()
        # self.wall_list.update()

        # With the physics engine, we will instead update the sprites by using the physics engine’s update:
        # It is good to keep all the sprites updated AFTER the logics takes place, which is more logical
        self.physics_wall.update()
        self.physics_ceiling.update()
        self.physics_grass.update()
        self.physics_platform.update()
        # Scroll the screen to the player
        self.scroll_to_player()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.W:
            self.up_pressed = True

        elif key == arcade.key.S:
            self.down_pressed = True

        elif key == arcade.key.A:
            self.left_pressed = True

        elif key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W:
            self.up_pressed = False
            self.player_sprite.change_y = 0
            self.time_passed_after_up_pressed = 0
        elif key == arcade.key.S:
            self.down_pressed = False
            self.player_sprite.change_y = 0
            self.time_passed_after_down_pressed = 0
        elif key == arcade.key.A:
            self.left_pressed = False
            self.player_sprite.change_x = 0
            self.time_passed_after_left_pressed = 0
        elif key == arcade.key.D:
            self.right_pressed = False
            self.player_sprite.change_x = 0
            self.time_passed_after_right_pressed = 0

    def control(self):
        """Control your character"""

        if self.up_pressed or self.down_pressed or self.left_pressed or self.right_pressed:
            self.timer += 1 / self.fps
        else:
            self.timer = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            self.time_passed_after_up_pressed = self.timer

        if self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            self.time_passed_after_down_pressed = self.timer

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            self.time_passed_after_left_pressed = self.timer

        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.time_passed_after_right_pressed = self.timer

        if self.up_pressed and self.down_pressed \
                and self.time_passed_after_up_pressed < self.time_passed_after_down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED

        if self.down_pressed and self.up_pressed \
                and self.time_passed_after_up_pressed > self.time_passed_after_down_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        if self.left_pressed and self.right_pressed \
                and self.time_passed_after_left_pressed < self.time_passed_after_right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        if self.right_pressed and self.left_pressed \
                and self.time_passed_after_left_pressed > self.time_passed_after_right_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y

    def check_screen_collision(self):
        """
        See if the player hit the edge of the screen.

        :return: False by default; True, if character hits the borders
        """
        bump = False
        if self.player_sprite.left < 0:
            self.player_sprite.change_x = 0
            self.player_sprite.left = 0
            bump = True
            if self.player_sprite.left - self.left_t == 0:
                bump = False

        elif self.player_sprite.right > SCREEN_WIDTH_MARGIN:
            self.player_sprite.change_x = 0
            self.player_sprite.right = SCREEN_WIDTH_MARGIN
            bump = True
            if self.player_sprite.right - self.right_t == 0:
                bump = False

        if self.player_sprite.bottom < 0:
            self.player_sprite.change_y = 0
            self.player_sprite.bottom = 0
            bump = True
            if self.player_sprite.bottom - self.bottom_t == 0:
                bump = False

        elif self.player_sprite.top > SCREEN_HEIGHT_MARGIN:
            self.player_sprite.change_y = 0
            self.player_sprite.top = SCREEN_HEIGHT_MARGIN
            bump = True
            if self.player_sprite.top - self.top_t == 0:
                bump = False

        self.left_t = self.player_sprite.left
        self.right_t = self.player_sprite.right
        self.top_t = self.player_sprite.top
        self.bottom_t = self.player_sprite.bottom

        return bump


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
