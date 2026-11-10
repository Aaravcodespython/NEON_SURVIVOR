# survivor_main.py
import arcade
import random
from entities import SurvivorPlayer, ChaserEnemy, Projectile, ExperienceGem, ExplosionParticle

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Neon Survivor - Lesson 9 (Upgrades & Juice FX)"

STATE_PLAYING = "PLAYING"
STATE_LEVEL_UP = "LEVEL_UP"
STATE_GAME_OVER = "GAME_OVER"

class SurvivorGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.DARK_SLATE_GRAY

        # Entity collections
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.gem_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()

        self.player = SurvivorPlayer(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player_list.append(self.player)

        # Game state tracking
        self.current_state = STATE_PLAYING
        self.score = 0
        self.spawn_timer = 0.0
        self.fire_cooldown = 0.0
        self.damage_cooldown = 0.0

        # Persistent GPU-cached text (using modern x, y coordinates)
        self.stats_text = arcade.Text(
            f"LVL {self.player.level}  |  HP: {self.player.health}/{self.player.max_health}  |  SCORE: {self.score}",
            x=20, y=565, color=arcade.color.WHITE, font_size=12, bold=True
        )
        self.xp_text = arcade.Text(
            f"XP: {self.player.xp} / {self.player.xp_to_level}",
            x=20, y=542, color=arcade.color.CYAN, font_size=11, bold=True
        )

        # Level-Up UI Text
        self.upgrade_title = arcade.Text(
            "⚡ LEVEL UP! SELECT UPGRADE ⚡",
            x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2 + 80, color=arcade.color.GREEN, font_size=18, bold=True, anchor_x="center"
        )
        self.option1 = arcade.Text(
            "[1] Quick Draw (+25% Fire Rate)",
            x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 25, color=arcade.color.WHITE, font_size=13, anchor_x="center"
        )
        self.option2 = arcade.Text(
            "[2] Agility Boots (+20% Move Speed)",
            x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 - 15, color=arcade.color.WHITE, font_size=13, anchor_x="center"
        )
        self.option3 = arcade.Text(
            "[3] Magnetic Surge (+50% Gem Magnet and +30 Health)",
            x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 - 55, color=arcade.color.WHITE, font_size=13, anchor_x="center"
        )

        # Game Over UI Text
        self.game_over_title = arcade.Text(
            "SURVIVOR DOWN, GAME OVER",
            x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 20, color=arcade.color.RED, font_size=40, anchor_x="center"
        )
        self.game_over_subtitle = arcade.Text(
            "Press R to restart game",
            x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 - 20, color=arcade.color.RED, font_size=15, anchor_x="center"
        )
                
        

    def on_draw(self):
        self.clear()

        # 1. Render gameplay layers
        self.gem_list.draw()
        self.particle_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

        # 2. Render HUD & XP Bar
        self.stats_text.text = f"LVL {self.player.level}  |  HP: {self.player.health}/{self.player.max_health}  |  SCORE: {self.score}"
        self.xp_text.text = f"XP: {self.player.xp} / {self.player.xp_to_level}"
        self.stats_text.draw()
        self.xp_text.draw()

        # XP progress bar background & fill using modern draw_lbwh_rectangle_filled
        arcade.draw_lbwh_rectangle_filled(20, 525, 200, 10, arcade.color.DARK_GRAY)
        xp_ratio = min(self.player.xp / self.player.xp_to_level, 1.0)
        arcade.draw_lbwh_rectangle_filled(20, 525, int(200 * xp_ratio), 10, arcade.color.ELECTRIC_CYAN)

        # 3. Level-Up Modal
        

    def on_update(self, delta_time):
        # Only simulate game action when actively playing
        if self.current_state != STATE_PLAYING:
            return

        self.player_list.update()
        self.enemy_list.update(delta_time)
        self.bullet_list.update()
        self.particle_list.update(delta_time)

        # Gems magnetize toward player
       
        # Collect Gems
        

        # Check for Level-Up condition
        

        # Cooldown ticks
       

        # Wave Spawner: 1 enemy every 1.4 seconds
        

        # Bullet-Enemy collisions
        
        # Enemy-Player collisions
        

    def spawn_enemy(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 30
        elif side == "bottom":
            x, y = random.randint(0, SCREEN_WIDTH), -30
        elif side == "left":
            x, y = -30, random.randint(0, SCREEN_HEIGHT)
        else:
            x, y = SCREEN_WIDTH + 30, random.randint(0, SCREEN_HEIGHT)

        new_enemy = ChaserEnemy(x, y, self.player, speed=random.uniform(1.8, 2.7))
        self.enemy_list.append(new_enemy)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        # Level-Up Selection Handling
        if self.current_state == STATE_LEVEL_UP:
            if key == arcade.key.KEY_1:
                self.player.fire_rate_multiplier += 0.25
                self.current_state = STATE_PLAYING
            elif key == arcade.key.KEY_2:
                self.player.movement_speed += 1.0
                self.current_state = STATE_PLAYING
            elif key == arcade.key.KEY_3:
                self.player.magnet_radius += 60.0
                self.player.health = min(self.player.health + 30, self.player.max_health)
                self.current_state = STATE_PLAYING
            return

        # Game Over Restart
        if self.current_state == STATE_GAME_OVER and key == arcade.key.R:
            self.reset_game()
            return

        # Normal Movement Controls
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -self.player.movement_speed
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = self.player.movement_speed
        elif key in (arcade.key.UP, arcade.key.W):
            self.player.change_y = self.player.movement_speed
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.change_y = -self.player.movement_speed

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0
        elif key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.player.change_y = 0

    def reset_game(self):
        """Resets all player progression and clean state."""
        pass

def main():
    window = SurvivorGame()
    arcade.run()

if __name__ == "__main__":
    main()