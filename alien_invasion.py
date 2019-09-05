import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats#引入Gamestats
from ship import Ship
import game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()#建立设置的实例
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))#建立背景
    pygame.display.set_caption("Alien Invasion")#为背景添加名字

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)#创建一个用于存储信息的实例

    # Set the background color.
    bg_color = (230, 230, 230)#设置背景色

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)#创造飞船实例
    bullets = Group()#创造子弹的编组
    aliens = Group()#创造外星人的编组

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)#创建一群外星人

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)#对用户的按键做出反应

        if stats.game_active:#判断游戏是否可以运行
            ship.update()#使飞船图像得到更新
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)#更新子弹的位置
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)#更新外星人的位置，追踪还有多少艘飞船，并且创造一群新的外星人

        gf.update_screen(ai_settings, screen, ship, aliens, bullets)#更新屏幕

run_game()#调用函数
