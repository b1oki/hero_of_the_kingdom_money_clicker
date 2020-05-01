#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import time
from pynput.mouse import Button, Controller
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def get_mouse_position(output=False):
    mouse = Controller()
    position = mouse.position
    if output:
        print('The current pointer position is {0}'.format(position))
    return position


def mouse_click(x, y, x_offset=0, y_offset=0, delay=0.0):
    mouse = Controller()
    mouse.position = (x + x_offset, y + y_offset)
    print('click', mouse.position)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(delay)
    if get_mouse_position() != (x + x_offset, y + y_offset):
        print('Exit because mouse moved')
        exit(1)


def clicker():
    print('clicker start')
    x_offset = 0  # 1920x1080
    # x_offset = 1920  # 3840x1080
    # clean_position = (23, 23)  # fullscreen
    clean_position = (215, 150)
    print('Activate game')
    mouse_click(*clean_position, delay=0.7, x_offset=x_offset)
    bottle_buy_price = 85
    bottle_sell_price = 90
    cash_value = 5085
    print('initial cash value', cash_value)
    while True:
        if get_mouse_position() == (0, 0):
            print('Exit because mouse position (0, 0)')
            break
        bottle_number = cash_value // bottle_buy_price
        print('bottle_number', bottle_number)
        cash_value = cash_value + bottle_number * \
            (bottle_sell_price - bottle_buy_price)
        print('new cash value', cash_value)
        hero_of_the_kingdom_trade_iteration(bottle_number)
    print('clicker finish')


def hero_of_the_kingdom_trade_iteration(bottle_number):
    print('Trade iteration start')
    x_offset = 0  # 1920x1080
    # x_offset = 1920  # 3840x1080
    if False:
        map_position = (75, 75)  # fullscreen
        map_city_position = (410, 450)  # fullscreen
        map_secret_glade_position = (1310, 145)  # fullscreen
        bootlegger_position = (1595, 220)  # fullscreen
        bootlegger_buy_bottle_position = (1535, 340)  # fullscreen
        bootlegger_trade_confirm_position = (1550, 600)  # fullscreen
        hunter_position = (485, 495)  # fullscreen
        hunter_sell_bottle_position = (675, 465)  # fullscreen
        hunter_trade_confirm_position = (430, 735)  # fullscreen
    else:
        map_position = (250, 195)
        map_city_position = (525, 490)
        map_secret_glade_position = (1240, 255)
        bootlegger_position = (1470, 305)
        bootlegger_buy_bottle_position = (1415, 400)
        bootlegger_trade_confirm_position = (1430, 620)
        hunter_position = (580, 525)
        hunter_sell_bottle_position = (735, 505)
        hunter_trade_confirm_position = (535, 720)
    print('Open map')
    mouse_click(*map_position, delay=2, x_offset=x_offset)
    print('Travel to city')
    mouse_click(*map_city_position, delay=1.7, x_offset=x_offset)
    print('Trade with bootlegger')
    mouse_click(*bootlegger_position, delay=1.7, x_offset=x_offset)
    print('Buy {} poision bottles'.format(bottle_number))
    for i in range(bottle_number):
        mouse_click(*bootlegger_buy_bottle_position, delay=0.5, x_offset=x_offset)
    print('Confirm trade')
    mouse_click(*bootlegger_trade_confirm_position, delay=0.7, x_offset=x_offset)
    print('Open map')
    mouse_click(*map_position, delay=2, x_offset=x_offset)
    print('Travel to glade')
    mouse_click(*map_secret_glade_position, delay=1.7, x_offset=x_offset)
    print('Trade with hunter')
    mouse_click(*hunter_position, delay=1.7, x_offset=x_offset)
    print('Sell {} poision bottles'.format(bottle_number))
    for i in range(bottle_number):
        mouse_click(*hunter_sell_bottle_position, delay=0.5, x_offset=x_offset)
    print('Confirm trade')
    mouse_click(*hunter_trade_confirm_position, delay=0.7, x_offset=x_offset)
    print('Trade iteration finish')


class ClickerWindow(Gtk.Window):

    def progressbar_value(self, move=0.1, value=None):
        if value is not None:
            self.progressbar.set_fraction(value)
            return
        value = self.progressbar.get_fraction() + move
        if value > 1:
            value = 0
        self.progressbar.set_fraction(value)

    def __init__(self):
        Gtk.Window.__init__(self, title='Hero of the Kingdom Money')
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        adjustment = Gtk.Adjustment(0, 0, 999999, 1, 10, 0)
        self.money = Gtk.SpinButton()
        self.money.set_adjustment(adjustment)
        self.money.set_numeric(True)
        self.money.set_tooltip_text('Money in pocket')
        self.money.set_max_length(6)

        self.button = Gtk.Button(label='Start money mining')
        self.button.connect('clicked', self.on_button_clicked)

        self.progressbar = Gtk.ProgressBar()

        self.add(vbox)
        vbox.pack_start(self.money, expand=True, fill=True, padding=0)
        vbox.pack_start(self.button, expand=True, fill=True, padding=0)
        vbox.pack_start(self.progressbar, expand=True, fill=True, padding=0)

    def on_button_clicked(self, widget):
        self.money.set_sensitive(False)
        self.button.set_sensitive(False)
        self.progressbar_value(value=0)
        self.progressbar.set_text('Money mining')
        self.progressbar.set_show_text(True)
        get_mouse_position(output=True)


win = ClickerWindow()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()
