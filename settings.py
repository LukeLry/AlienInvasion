#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

class Settings():
    #设置存储

    def __init__(self):
        #初始化游戏设置

        #屏幕设置
        self.screen_width=800
        self.screen_height=600
        self.bg_color=(230,230,230)

        self.ship_speed_factor=0.8

        #子弹设置
        self.bullet_speed_factor=3
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=60,60,60
        self.bullets_allowed=3

        #外星人设置
        self.alien_speed_factor=1
        self.fleet_drop_speed=10
        self.fleet_direction=1

        #飞船设置
        self.ship_limit=3


