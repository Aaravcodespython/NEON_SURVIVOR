# entities.py
import arcade
import math
import random

class SurvivorPlayer(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.load_texture(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.center_x = x
        self.center_y = y
        self.movement_speed = 5.0
        self.health = 100
        self.max_health = 100
        
        # Progression & Stats
        self.level = 1
        self.xp = 0
        self.xp_to_level = 50
        self.magnet_radius = 120.0
        self.fire_rate_multiplier = 1.0

    def update(self, delta_time=None):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Screen boundaries (800x600 arena)
        if self.left < 0:
            self.left = 0
        elif self.right > 800:
            self.right = 800
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > 600:
            self.top = 600


class ChaserEnemy(arcade.Sprite):
    def __init__(self, x, y, target_player, speed=2.0):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.target = target_player
        self.speed = speed

        # 1. Walk animation frame sets (Frames 1-7)
        self.walk_textures_right = [
            arcade.load_texture(f":resources:images/animated_characters/zombie/zombie_walk{i}.png")
            for i in range(1, 8)
        ]
        # Texture mirroring using .flip_left_right()
        self.walk_textures_left = [
            tex.flip_left_right() for tex in self.walk_textures_right
        ]

        # 2. Animation state tracking
        self.current_frame = 0
        self.animation_timer = 0.0
        self.frame_duration = 0.1
        self.texture = self.walk_textures_right[0]

    def update(self, delta_time=1/60):
        dx = self.target.center_x - self.center_x
        dy = self.target.center_y - self.center_y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.change_x = (dx / distance) * self.speed
            self.change_y = (dy / distance) * self.speed
        else:
            self.change_x = 0
            self.change_y = 0

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.animation_timer += delta_time
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.walk_textures_right)

            if self.change_x < 0:
                self.texture = self.walk_textures_left[self.current_frame]
            else:
                self.texture = self.walk_textures_right[self.current_frame]


class Projectile(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, speed=12):
        super().__init__()
        self.texture = arcade.load_texture(":resources:images/space_shooter/laserBlue01.png")
        self.center_x = start_x
        self.center_y = start_y

        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.hypot(dx, dy)

        if distance == 0:
            dx, dy = 1, 0
            distance = 1

        self.change_x = (dx / distance) * speed
        self.change_y = (dy / distance) * speed

        angle_rad = math.atan2(dy, dx)
        self.angle = math.degrees(angle_rad) - 90

    def update(self, delta_time=None):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right < 0 or self.left > 800 or self.bottom < 0 or self.top > 600:
            self.remove_from_sprite_lists()


class ExperienceGem(arcade.Sprite):
    """Collectible XP dropped by defeated enemies."""
    def __init__(self, x, y, value=15):
        super().__init__()
        self.texture = arcade.load_texture(":resources:images/items/gemBlue.png")
        self.scale = 0.7
        self.center_x = x
        self.center_y = y
        self.value = value
        self.speed = 0.0

    def update_magnet(self, target_player):
        dx = target_player.center_x - self.center_x
        dy = target_player.center_y - self.center_y
        dist = math.hypot(dx, dy)

        # Attract toward player when within magnet radius
        if dist < target_player.magnet_radius and dist > 0:
            self.speed = min(self.speed + 0.5, 9.0)
            self.center_x += (dx / dist) * self.speed
            self.center_y += (dy / dist) * self.speed


class ExplosionParticle(arcade.SpriteCircle):
    """Juice FX: Spawns and fades away on zombie kill."""
    def __init__(self, x, y):
        # Pick vibrant neon colors
        color = random.choice([arcade.color.NEON_GREEN, arcade.color.ELECTRIC_CYAN, arcade.color.YELLOW])
        radius = random.randint(3, 6)
        super().__init__(radius, color)
        
        self.center_x = x
        self.center_y = y

        # Random explosion direction and velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2.0, 6.0)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed

        self.life = 0.4  # Lifespan in seconds
        self.max_life = self.life

    def update(self, delta_time=1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_x *= 0.92  # Friction deceleration
        self.change_y *= 0.92

        self.life -= delta_time
        if self.life <= 0:
            self.remove_from_sprite_lists()
        else:
            # Fade alpha
            self.alpha = int(255 * (self.life / self.max_life))