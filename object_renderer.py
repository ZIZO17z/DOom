import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_crosshair()

    def draw_crosshair(self):
        # Draw a modern crosshair at the center of the screen
        center_x, center_y = WIDTH // 2, HALF_HEIGHT
        color = (255, 255, 255)
        length = 18
        thickness = 3
        gap = 6
        # Horizontal line
        pg.draw.line(self.screen, color, (center_x - length, center_y), (center_x - gap, center_y), thickness)
        pg.draw.line(self.screen, color, (center_x + gap, center_y), (center_x + length, center_y), thickness)
        # Vertical line
        pg.draw.line(self.screen, color, (center_x, center_y - length), (center_x, center_y - gap), thickness)
        pg.draw.line(self.screen, color, (center_x, center_y + gap), (center_x, center_y + length), thickness)

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        # Modern health bar
        player = self.game.player
        bar_width = 320
        bar_height = 32
        x = 40
        y = HEIGHT - bar_height - 40
        # Background
        pg.draw.rect(self.screen, (40, 40, 40), (x-4, y-4, bar_width+8, bar_height+8), border_radius=12)
        # Health fill
        health_ratio = max(0, min(1, player.health / PLAYER_MAX_HEALTH))
        fill_width = int(bar_width * health_ratio)
        pg.draw.rect(self.screen, (200, 40, 40), (x, y, fill_width, bar_height), border_radius=10)
        # Border
        pg.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 3, border_radius=10)
        # Health text
        font = pg.font.SysFont('arial', 28, bold=True)
        text = font.render(f"{player.health} / {PLAYER_MAX_HEALTH}", True, (255,255,255))
        text_rect = text.get_rect(center=(x + bar_width//2, y + bar_height//2))
        self.screen.blit(text, text_rect)

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        # Use smoothscale for better quality
        return pg.transform.smoothscale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }