import sys
from time import sleep#调用了函数sleep，来使函数暂停

import pygame

from bullet import Bullet#导入BUllet类
from alien import Alien#导入Alien类

def check_keydown_events(event, ai_settings, screen, ship, bullets):#对用户得按键做出反应
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:#如果是按得右键
        ship.moving_right = True#就返回True
    elif event.key == pygame.K_LEFT:#如果按得是左键·
        ship.moving_left = True#就返回Tr
    elif event.key == pygame.K_SPACE:#如果是按得空格键
        fire_bullet(ai_settings, screen, ship, bullets)#就调用子弹函数
    elif event.key == pygame.K_q:#如果是按得q
        sys.exit()#就退出游戏

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:#如果是松右键
        ship.moving_right = False#返回FAlse
    elif event.key == pygame.K_LEFT:#如果松左键
        ship.moving_left = False#返回

def check_events(ai_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#如果是按得quit
            sys.exit()#退出游戏
        elif event.type == pygame.KEYDOWN:#如果按键
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:#如果是松键
            check_keyup_events(event, ship)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:#如果子弹在允许发射的范围内
        new_bullet = Bullet(ai_settings, screen, ship)#就创造新的子弹
        bullets.add(new_bullet)#并把子弹加入编组

def update_screen(ai_settings, screen, ship, aliens, bullets):#更新屏幕
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)#更新背景色

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():#使每一个子弹得以绘制
        bullet.draw_bullet()
    ship.blitme()#使飞船得以绘制
    aliens.draw(screen)#使外星人得以绘制

    # Make the most recently drawn screen visible.
    pygame.display.flip()#使新绘制的屏幕可见

def update_bullets(ai_settings, screen, ship, aliens, bullets):#检查是否有子弹击中了外星人，若击中了，就删除对应的子弹与外星人
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()#更新子弹的位置
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():#如果子弹超出屏幕返回
        if bullet.rect.bottom <= 0:#就删除这个子弹
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)#调用函数

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):#检测子弹与外星人的碰撞情况
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)#运用这个函数检查

    if len(aliens) == 0:#如果外星人的数量清空
        # Destroy existing bullets, and create new fleet.
        bullets.empty()#我们清空子弹
        create_fleet(ai_settings, screen, ship, aliens)#创造新的外星人

def check_fleet_edges(ai_settings, aliens):#检查是否有外星人撞到了屏幕边缘
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():#我们遍历外星人，
        if alien.check_edges():#调用函数，对外星人的位置做出判断
            change_fleet_direction(ai_settings, aliens)#如果有外星人在屏幕的边缘，我们调用新的函数，并且退出循环
            break

def change_fleet_direction(ai_settings, aliens):#将所有的外星人下移，并改变它们的方向
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():#将所有的外星人下移
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1#并且修改速度的值，使外星人改变左右方向

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:#判断余下飞船数
        # Decrement ships_left.
        stats.ships_left -= 1#将余下的飞船数减一
    else:
        stats.game_active = False#如果少于0就结束游戏

    # Empty the list of aliens and bullets.
    aliens.empty()#清空外星人编组
    bullets.empty()#清空子弹编组

    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)#创造新的外星人
    ship.center_ship()#使飞船置于中央

    # Pause.
    sleep(0.5)#使游戏暂停

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):#检查是否有外星人到达底部

    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()#获取屏幕的rect属性
    for alien in aliens.sprites():#检查是否有到达底部的外星人
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)#像飞船被撞到那样处理
            break#结束循环

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):#更新外星人的位置
    """
    Check if the fleet is at an edge,
      then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)#检查外星人的位置
    aliens.update()#更新外星人的位置

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):#判断外星人与飞船是否相撞
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)#检查是否有外星人到达底部

def get_number_aliens_x(ai_settings, alien_width):#计算每一行可以容纳多少人
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width#计算可以容纳的宽度
    number_aliens_x = int(available_space_x / (2 * alien_width))#计算可以荣纳多少人
    return number_aliens_x#返回人数

def get_number_rows(ai_settings, ship_height, alien_height):#计算可容纳多少行外星人
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -#计算可以容纳多少行外星人
                            (3 * alien_height) - ship_height)#为遵循每行不超过79字符的建议，我们把它分成两行
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows#返回行数

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen)#创建一个外星人
    alien_width = alien.rect.width#获取外星人的宽度
    alien.x = alien_width + 2 * alien_width * alien_number#计算每个外星人的x坐标
    alien.rect.x = alien.x#将横坐标的值赋给x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)#将外星人添加进编组

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)#创建一个外星人
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)#获取行数

    # Create the fleet of aliens.
    for row_number in range(number_rows):#使用嵌套循环，创建多行外星人
        for alien_number in range(number_aliens_x):#创建row_number行数的外星人
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)
