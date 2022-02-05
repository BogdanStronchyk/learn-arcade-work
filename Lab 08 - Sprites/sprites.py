"""
Sprite Collect Coins

Simple program to show basic sprite usage.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_collect_coins
"""

import random
import arcade
import time

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
SPRITE_SCALING_STONE = .25
SPRITE_SCALING_HEART = 0.25
COIN_COUNT = 50
STONE_COUNT = 20
HEART_COUNT = 1
MOVEMENT_SPEED = 3
FPS = 0
LIVES = 3
LUCK = 0
trig = False
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Coins Example"


class Stone(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        if self.top < 0:
            self.reset_pos()
        self.center_y -= 4


class Coin(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

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

        # Move the coin
        self.center_x += self.change_x
        self.center_y += self.change_y


class Heart(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def repos(self):
        global trig
        self.center_x = random.randrange(20, SCREEN_WIDTH - 20)
        self.center_y = random.randrange(20, SCREEN_HEIGHT - 20)
        self.change_x = 5
        self.change_y = 5
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
        self.hit_sound = arcade.load_sound(":resources:sounds/error1.wav")
        self.coin_sound = arcade.load_sound(":resources:sounds/coin2.wav")
        self.heart_taken_sound = arcade.load_sound(":resources:sounds/upgrade3.wav")
        self.heart_appeared_sound = arcade.load_sound(":resources:sounds/upgrade5.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover4.wav")
        self.sound_player = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.stone_list = None
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
        self.luck = LUCK
        self.lock_heart = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.stone_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        img = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(20, SCREEN_WIDTH - 20)
            coin.center_y = random.randrange(20, SCREEN_HEIGHT - 20)
            coin.change_x = random.randrange(-3, 4)
            coin.change_y = random.randrange(-3, 4)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Create the stones
        for i in range(STONE_COUNT):
            # Create the stone instance
            # Stone image from kenney.nl
            stone = Stone(":resources:images/space_shooter/meteorGrey_big4.png", SPRITE_SCALING_STONE)

            # Position the coin
            stone.center_x = random.randrange(20, SCREEN_WIDTH - 20)
            stone.center_y = random.randrange(20, SCREEN_HEIGHT - 20)

            # Add the stones to the list
            self.stone_list.append(stone)

        # Create the heart
        for i in range(HEART_COUNT):
            # Create the heart instance
            # Heart image from kenney.nl
            heart = Heart(":resources:images/items/gemBlue.png", SPRITE_SCALING_HEART)

            # Position the heart
            heart.repos()

            # Add the coin to the lists
            self.heart_list.append(heart)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.coin_list.draw()
        self.stone_list.draw()
        self.player_list.draw()
        self.heart_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=SCREEN_WIDTH * 0.01, start_y=SCREEN_HEIGHT*0.02,
                         color=arcade.color.WHITE, font_size=14)

        output = f"FPS: {self.fps:.2f}"
        arcade.draw_text(text=output, start_x=SCREEN_WIDTH*0.8, start_y=SCREEN_HEIGHT*0.9,
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
        global trig
        # FPS counter
        self.fps = 1 / delta_time

        # Chance to spawn a heart (1/3600)
        self.luck = random.randint(1, int(self.fps) * 20)
        if self.luck == 1:
            trig = True

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

        self.coin_list.update()
        self.stone_list.update()
        self.heart_list.update()
        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        stone_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.stone_list)
        heart_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.heart_list)

        # Loop through each colliding sprite, replace it, and add to the score.
        for coin in coins_hit_list:

            # Reset the coin to a random spot above the screen
            coin.center_y = random.randint(30, SCREEN_WIDTH - 30)
            coin.center_x = random.randint(30, SCREEN_HEIGHT - 30)

            coin.update()

            arcade.play_sound(self.coin_sound)
            self.score += 1

        for stone in stone_hit_list:
            stone.reset_pos()
            arcade.play_sound(self.hit_sound)
            self.lives -= 1
            self.score -= 5

        for heart in heart_hit_list:

            # Reset the coin to a random spot above the screen
            heart.remove()

            arcade.play_sound(self.heart_taken_sound)
            self.lives += 1

        if self.lives < 1:
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
