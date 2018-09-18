#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import game_functions as gf
import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button

def run_game():
    #初始化游戏并创建一个游戏对象
    pygame.init()

    #创建设置对象
    ai_settings=Settings()

    #创建屏幕对象
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建button按钮
    play_button=Button(ai_settings,screen,"Play")

    stats=GameStats(ai_settings)

    #创建一艘飞船
    ship=Ship(ai_settings,screen)

    #创建一个用于存储子弹的编组 当前所有子弹全在该分组中
    bullets=Group()

    #创建一个用于存储外星人的编组 当前所有外星人全在该分组中
    aliens=Group()

    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #创建一个外星人
    alien=Alien(ai_settings,screen)

    #开始游戏主循环
    while True:
        #监听键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)

        #更新屏幕图像
        gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button)

run_game()




