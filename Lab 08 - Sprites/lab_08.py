"""
Sprite Collect gears

Simple program to show basic sprite usage.

Artwork from https://kenney.nl

***********************
Необходимо исправить столкновения шестерёнок.
Проблема в их генерации (99%). Они генерируются
слишком близко друг к другу и "залипают" друг в друге.
Необходимо генерировать их в пустом месте.
Флаг "feature" активирует столкновения.
***********************


***********************
Замечен баг с генерацией шестеренок за границей экрана.
Причина неизвестна.
***********************
"""

import random
import arcade
import time

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_GEAR = .2
SPRITE_SCALING_LASER = 1
SPRITE_SCALING_HEART = 0.25
GEAR_COUNT = 50
LASER_COUNT = 20
LASER_SPEED = 8
HEART_COUNT = 1
MOVEMENT_SPEED = 3
FPS = 0
LIVES = 3
CHANCE = 1  # amount of seconds between the appearance of the heart
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Gears"

# Flags
trig = True
feature = False


class Laser(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0
        self.angle = 180

    def reset_pos(self):
        self.center_y = random.randint(SCREEN_HEIGHT + 20, SCREEN_HEIGHT * 2)
        self.center_x = random.randint(20, SCREEN_WIDTH)

    def update(self):
        if self.top < 0:
            self.reset_pos()
        self.center_y -= LASER_SPEED


class Gear(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0
        self.center_x_t = None
        self.center_y_t = None

    def repos(self, *gears):
        # Position the gear
        self.center_x = random.randint(20, SCREEN_WIDTH - 20)
        self.center_y = random.randint(20, SCREEN_HEIGHT - 20)
        self.change_x = random.randint(-3, 4)
        self.change_y = random.randint(-3, 4)

        # fix the static gears
        while self.change_x == 0 or self.change_y == 0:
            self.change_x = random.randint(-3, 4)
            self.change_y = random.randint(-3, 4)

        # fix sticking groups of gears
        # print(gears)

    def update(self):

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1

        # Move the gear
        self.center_x += self.change_x
        self.center_y += self.change_y


class Heart(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0
        self.heart_appeared_sound = arcade.load_sound(":resources:sounds/upgrade5.wav")

    def repos(self):
        global trig
        self.center_x = random.randint(60, SCREEN_WIDTH - 60)
        self.center_y = random.randint(60, SCREEN_HEIGHT - 60)
        self.change_x = 5
        self.change_y = 5
        arcade.play_sound(self.heart_appeared_sound)
        trig = False

    def remove(self):
        global trig
        self.remove_from_sprite_lists()
        if trig:
            self.repos()

    def update(self):

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1

        # Move the heart
        self.center_x += self.change_x
        self.center_y += self.change_y


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Initialize sounds
        self.bump_sound = arcade.load_sound(":resources:sounds/error4.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.coin_sound = arcade.load_sound(":resources:sounds/coin2.wav")
        self.heart_taken_sound = arcade.load_sound(":resources:sounds/upgrade3.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover4.wav")
        self.sound_player = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.gear_list = None
        self.laser_list = None
        self.heart_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Count fps
        self.fps = FPS

        # Count lives
        self.lives = LIVES

        # Count luck
        self.luck = None
        self.background = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Background
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.gear_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()
        # Score
        self.score = 0

        # Set up the player character
        # Character image from kenney.nl
        img = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.player_list.append(self.player_sprite)

        # Create the gears
        for i in range(GEAR_COUNT):
            # Create the laser instance
            # Gear image from kenney.nl
            gear = Gear(":resources:images/enemies/saw.png", SPRITE_SCALING_GEAR)

            # Position the laser
            gear.repos()

            # Add the gear to the lists
            self.gear_list.append(gear)

        # Create the lasers
        for i in range(LASER_COUNT):
            # Create the laser instance
            # Laser image from kenney.nl
            laser = Laser(":resources:images/space_shooter/laserRed01.png", SPRITE_SCALING_LASER)

            # Position the laser
            laser.reset_pos()

            # Add the gears to the list
            self.laser_list.append(laser)

    def setup_heart(self):

        global trig
        # Create the heart
        for i in range(HEART_COUNT):
            # Create the heart instance
            # Heart image from kenney.nl
            heart = Heart(":resources:images/items/gemYellow.png", SPRITE_SCALING_HEART)

            # Position the heart
            if trig:
                heart.repos()
                trig = False

            # Add the coin to the lists
            self.heart_list.append(heart)

    def on_draw(self):
        """ Draw everything """
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw texture lists
        self.gear_list.draw()
        self.laser_list.draw()
        self.player_list.draw()
        self.heart_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=SCREEN_WIDTH * 0.01, start_y=SCREEN_HEIGHT * 0.02,
                         color=arcade.color.WHITE, font_size=14)

        output = f"FPS: {self.fps:.2f}"
        arcade.draw_text(text=output, start_x=SCREEN_WIDTH * 0.8, start_y=SCREEN_HEIGHT * 0.9,
                         color=arcade.color.WHITE, font_size=14)

        output = f"Lives: {self.lives}"
        arcade.draw_text(text=output, start_x=SCREEN_WIDTH * 0.01, start_y=SCREEN_HEIGHT * 0.9,
                         color=arcade.color.WHITE, font_size=14)

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

        # print(f'Position: {self.player_sprite.center_x}, {int(self.player_sprite.center_y)}')

    def on_update(self, delta_time):
        """ Movement and game logic """
        global trig, CHANCE
        # FPS counter
        self.fps = 1 / delta_time

        # Chance to spawn a heart (1/3600)
        self.luck = random.randint(1, int(self.fps) * CHANCE * 60)
        if self.luck == 1:
            print('Heart!')
            self.setup_heart()

        # keyboard movement
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y

        # See if the player hit the edge of the screen. If so, play sound
        bump = False
        if self.player_sprite.left < 0:
            self.player_sprite.change_x = 0
            self.player_sprite.left = 0
            bump = True

        elif self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.change_x = 0
            self.player_sprite.right = SCREEN_WIDTH
            bump = True

        elif self.player_sprite.bottom < 0:
            self.player_sprite.change_y = 0
            self.player_sprite.bottom = 0
            bump = True

        elif self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.change_y = 0
            self.player_sprite.top = SCREEN_HEIGHT
            bump = True

        #  If there is no player, or the playing boolean is false, and the player has bumped, we’ll play the sound.
        if (not self.sound_player or not self.sound_player.playing) and bump:
            self.sound_player = arcade.play_sound(self.bump_sound)

        self.gear_list.update()
        self.laser_list.update()
        self.heart_list.update()
        # Generate a list of all sprites that collided with the player.
        gears_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.gear_list)
        lasers_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.laser_list)
        hearts_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.heart_list)

        # if the gear hits another gear
        if feature:
            for gear_hit in self.gear_list:
                gears_to_gears_hit_list = arcade.check_for_collision_with_list(gear_hit, self.gear_list)
                for gears in gears_to_gears_hit_list:
                    gears.change_x *= -1
                    gears.change_y *= -1

        # Loop through each colliding sprite, replace it, and add to the score.
        for gear in gears_hit_list:
            # Reset the gear to a random spot above the screen
            gear.repos()

            gear.update()

            arcade.play_sound(self.coin_sound)
            self.score += 1

        for laser in lasers_hit_list:
            laser.reset_pos()
            arcade.play_sound(self.hit_sound)
            self.lives -= 1
            self.score -= 5

        for heart in hearts_hit_list:
            # Reset the gear to a random spot above the screen

            heart.remove()
            trig = True

            arcade.play_sound(self.heart_taken_sound)
            self.lives += 1
            self.score += 20

        if self.lives == 0:
            time.sleep(1)
            arcade.play_sound(self.game_over)
            time.sleep(2)
            arcade.close_window()


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
