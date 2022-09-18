from constants import *


class Bird:
    IMGS = BIRD_IMG
    MAX_ROT = 25
    ROT_VEL = 20
    ANIM_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_idx = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = (
            self.vel * self.tick_count + 1.5 * self.tick_count**2
        )  # d = vt + (gravity black magic)

        if d >= 16:
            d = 16  # Speed Limiter

        if d < 0:
            d -= 2  # Momentum

        self.y = self.y + d  # Displace by d units

        if d < 0 or self.y < self.height + 50:  # Decides tilt of the bird
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_idx += 1

        if self.img_idx < self.ANIM_TIME:  # Worst way to animate anything
            self.img = self.IMGS[0]
        elif self.img_idx < self.ANIM_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_idx < self.ANIM_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_idx < self.ANIM_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_idx == self.ANIM_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_idx = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_idx = self.ANIM_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(  # Adjust center of rotated image
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
