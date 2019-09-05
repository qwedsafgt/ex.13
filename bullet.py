import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):#对子弹进行编组并创造一个子弹
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object, at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen

        # Create bullet rect at (0, 0), then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)#设置一颗（0，0）起的子弹
        self.rect.centerx = ship.rect.centerx#使子弹从飞船上部发出
        self.rect.top = ship.rect.top

        # Store a decimal value for the bullet's position.
        self.y = float(self.rect.y)#使子弹的y坐标有小数的属性

        self.color = ai_settings.bullet_color#设置子弹的颜色
        self.speed_factor = ai_settings.bullet_speed_factor#设置子弹的·速度

    def update(self):#更新子弹的位置
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor#修改子弹得纵坐标
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):#使更新得子弹位置得以绘制
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
