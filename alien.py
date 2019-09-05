import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):#初始化
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image, and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')#引进外星人图像
        self.rect = self.image.get_rect()#获取外星人的rectangle属性

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width#把左边距设置为高度，
        self.rect.y = self.rect.height#把上边距设置为高度

        # Store the alien's exact position.
        self.x = float(self.rect.x)#使rect属性具有小数性质

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()#获取屏幕的rect属性
        if self.rect.right >= screen_rect.right#如果没有触碰到屏幕右边缘，就返回Tr
            return True
        elif self.rect.left <= 0:#如果没有触碰到屏幕左边缘，就返回True
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *#使外星人左右移动
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):#使每个外星人得以绘制
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
