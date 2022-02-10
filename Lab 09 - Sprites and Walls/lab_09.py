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

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

# How fast to move, and how fast to run the animation
PLAYER_MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

CAMERA_SPEED = 0.2
# --- Variables ---


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = SPRITE_SCALING_PLAYER

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        # main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]


class MyGame(arcade.Window):
    """ This class represents the main window of the game. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprites With Walls Example")

        # Initiate sound

        self.bump_sound = arcade.load_sound(":resources:sounds/error4.wav")
        self.sound_player = None
        self.gem_collected = arcade.load_sound(":resources:sounds/coin5.wav")
        self.stone_hit = arcade.load_sound(":resources:sounds/rockHit2.wav")

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.gem_list = None

        # Background image
        self.background_image = None

        # Set up the player
        self.player_sprite = None

        # This variable holds our simple "physics engine"
        self.physics_engine = None

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
        self.background_image = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.gem_list = arcade.SpriteList()

        # Create the player
        self.player_sprite = Player()
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # This identifies the player character
        # and a lists of sprites that the player character isn’t allowed to pass through.
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Place all sprite generation inside a loop
        for y in range(32, SCREEN_HEIGHT_MARGIN, 64):
            count_gap = 0
            for x in range(32, SCREEN_WIDTH_MARGIN, 64):

                # generate grass floor
                if y == 32 and 32 < x <= SCREEN_WIDTH_MARGIN - 64:
                    grass = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING_BOX)
                    grass.center_x = x
                    grass.center_y = y
                    self.wall_list.append(grass)

                # generate walls
                if 32 <= y < SCREEN_HEIGHT_MARGIN and x <= 32 or x >= SCREEN_WIDTH_MARGIN - 32:
                    wall = arcade.Sprite(":resources:images/tiles/stoneCenter_rounded.png", SPRITE_SCALING_BOX)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

                # generate ceiling tile
                if y == SCREEN_HEIGHT_MARGIN - 32 and 32 < x <= SCREEN_WIDTH_MARGIN - 64:
                    ceiling = arcade.Sprite(":resources:images/tiles/bridgeB.png", SPRITE_SCALING_BOX)
                    ceiling.center_x = x
                    ceiling.center_y = y
                    self.wall_list.append(ceiling)

                # Generate gems
                if y % 64 == 32 and not y % 128 == 32 and 32 < y < SCREEN_HEIGHT_MARGIN - 32 \
                        and 32 < x <= SCREEN_WIDTH_MARGIN - 64:
                    if random.randint(1, 100) < 5:
                        gem = arcade.Sprite(":resources:images/items/gemRed.png", SPRITE_SCALING_BOX)
                        gem.center_x = x
                        gem.center_y = y
                        self.gem_list.append(gem)

                # generate platforms
                if y % 128 == 32 and 32 < y < SCREEN_HEIGHT_MARGIN - 32 and 32 < x <= SCREEN_WIDTH_MARGIN - 64:
                    if random.randint(1, 5) > 2:
                        count_gap = 0
                        platform = arcade.Sprite(":resources:images/tiles/grassHalf_mid.png", SPRITE_SCALING_BOX)
                        platform.center_x = x
                        platform.center_y = y
                        self.wall_list.append(platform)

                    # if the gap is 2 or more tiles wide, generate bridges to connect separate platforms
                    else:
                        count_gap += 1
                        if count_gap == 2:
                            for i in range(count_gap):
                                bridge = arcade.Sprite(":resources:images/tiles/bridgeA.png", SPRITE_SCALING_BOX)
                                bridge.center_x = x - 64 * i
                                bridge.center_y = y
                                self.wall_list.append(bridge)

                        elif count_gap > 2:
                            bridge = arcade.Sprite(":resources:images/tiles/bridgeA.png", SPRITE_SCALING_BOX)
                            bridge.center_x = x
                            bridge.center_y = y
                            self.wall_list.append(bridge)

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

        # Set background image
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)

        # Select the scrolled camera for our sprites
        self.camera_for_sprites.use()

        # Draw the sprites
        self.wall_list.draw()
        self.player_list.draw()
        self.gem_list.draw()

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
        self.player_list.update_animation()

        # See if the player hit the edge of the screen
        flag = self.check_screen_collision()

        #  If there is no player, or the playing boolean is false, and the player hit the wall, we’ll play the sound.
        if (not self.sound_player or not self.sound_player.playing) and flag:
            self.sound_player = arcade.play_sound(self.bump_sound)

        # Update physical objects:
        self.physics_engine.update()

        # Update gems
        self.gem_list.update()

        gem_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.gem_list)

        for gem in gem_hit_list:
            arcade.play_sound(self.gem_collected)
            gem.remove_from_sprite_lists()
            self.score += 1

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
            self.player_sprite.center_x += self.player_sprite.change_y

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
