#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button
from game_stats import GameStats

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:  # 右移开始
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:  # 左移开始
        ship.moving_left = True
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key==pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    #如果还没达到限制，就发射一颗子弹
    # 创建一颗子弹，并将它加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:  # 右移结束
        ship.moving_right = False

    if event.key == pygame.K_LEFT:  # 左移结束
        ship.moving_left = False


def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
         if event.type==pygame.QUIT:
                sys.exit()
         elif event.type==pygame.KEYDOWN:
             check_keydown_events(event,ai_settings,screen,ship,bullets)

         elif event.type==pygame.KEYUP:
             check_keyup_events(event,ship)
         elif event.type==pygame.MOUSEBUTTONDOWN:
             mouse_x,mouse_y=pygame.mouse.get_pos()
             check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color) # 每次循环重绘屏幕
    ship.blitme()                     # 绘制飞船

    aliens.draw(screen)               # 一次性将编组中的所有外星人全部绘制在屏幕上

    for bullet in bullets.sprites():  #在飞船和外星人后面重绘所有子弹 bullets.sprite()返回所有精灵的列表
        bullet.draw_bullet()

    #如果游戏处于非活跃状态,就会绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()             # 让最近绘制的屏幕可见

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if (len(aliens)) == 0:
        bullets.empty()  # 清空子弹
        create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings,screen,ship,aliens,bullets):
    """更新子弹位置，并删除已经消失的子弹"""
    #更新子弹的位置 将对编组中的所有子弹实例调用update()函数
    bullets.update()

    #删除已经消失的子弹
    for bullet in bullets.copy():  # 屏幕上最多出现3颗子弹 bullets.copy()返回子弹精灵列表副本
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)

def get_number_aliens_x(ai_settings,alien_width):
    """每行中外星人的个数"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows



def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少外星人
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #创建外星人群

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def change_fleet_direction(ai_settings,aliens):
    """将外星人整体下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left>0:
        #将ships_left减一
        stats.ships_left-=1

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True) #显现光标

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    """更新外星人中所有的外星人"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            #像飞船被撞到一样处理 ???
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """在玩家单机play时候开始新游戏"""
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.game_active=True
        stats.game_active=True

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()





