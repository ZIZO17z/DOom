from sprite_object import *


class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.base_weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.weapon_pos = self.base_weapon_pos
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50
        self.bob_phase = 0

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        # Weapon bobbing effect
        player = self.game.player
        moving = any(pg.key.get_pressed()[k] for k in (pg.K_w, pg.K_a, pg.K_s, pg.K_d))
        if moving and player.on_ground:
            self.bob_phase += 0.18 * (2.2 if (pg.key.get_pressed()[pg.K_LSHIFT] or pg.key.get_pressed()[pg.K_RSHIFT]) else 1)
        else:
            self.bob_phase = 0
        bob_offset = int(8 * math.sin(self.bob_phase)) if player.on_ground else int(-18 * player.z * 30)
        x, y = self.base_weapon_pos
        self.weapon_pos = (x, y + bob_offset)
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()