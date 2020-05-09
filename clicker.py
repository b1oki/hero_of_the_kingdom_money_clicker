#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import time
from pynput.mouse import Button, Controller
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ClickerExecutor(object):
    def __init__(self, cash_value: int) -> None:
        self.log = logging.getLogger('clicker')
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(logging.StreamHandler())
        self.cash_value = cash_value
        self.is_fullscreen = False
        self.mouse = Controller()

    def get_mouse_position(self):
        position = self.mouse.position
        self.log.debug('The current pointer position is {0}'.format(position))
        return position

    def mouse_click(self, x, y, x_offset=0, y_offset=0, delay=0.0):
        need_position = (x + x_offset, y + y_offset)
        self.log.debug('Move mouse to {} before click'.format(need_position))
        self.mouse.position = need_position
        self.get_mouse_position()
        self.log.debug('Mouse click')
        time.sleep(0.1)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)
        time.sleep(delay)
        self.log.debug('Verify mouse after click')
        if self.get_mouse_position() != need_position:
            raise SystemExit('Exit because mouse moved')

    def clicker_process(self):
        self.log.debug('Clicker start')
        x_offset = 0  # 1920x1080
        # x_offset = 1920  # 3840x1080
        clean_position = (215, 150)
        if self.is_fullscreen:
            clean_position = (23, 23)
        self.log.debug('Activate game')
        bottle_buy_price = 85
        bottle_sell_price = 90
        sell_profit = bottle_sell_price - bottle_buy_price
        cash_value = self.cash_value
        self.log.debug('Initial cash value {}'.format(cash_value))
        if cash_value < bottle_buy_price:
            raise SystemExit(
                'Cash value less than poision bottle price {}'.format(bottle_buy_price))
        self.mouse_click(*clean_position, delay=0.7, x_offset=x_offset)
        while True:
            if self.get_mouse_position() == (0, 0):
                raise SystemExit('Exit because mouse position (0, 0)')
            bottle_number = cash_value // bottle_buy_price
            self.log.debug('Poision bottles number {}'.format(bottle_number))
            cash_value += bottle_number * sell_profit
            self.log.debug('New cash value {}'.format(cash_value))
            self.hero_of_the_kingdom_trade_iteration(bottle_number)
        self.log.debug('Clicker finish')

    def hero_of_the_kingdom_trade_iteration(self, bottle_number):
        self.log.debug('Trade iteration start')
        x_offset = 0  # 1920x1080
        # x_offset = 1920  # 3840x1080
        if self.is_fullscreen:
            map_position = (75, 75)
            map_city_position = (410, 450)
            map_secret_glade_position = (1310, 145)
            bootlegger_position = (1595, 220)
            bootlegger_buy_bottle_position = (1535, 340)
            bootlegger_trade_confirm_position = (1550, 600)
            hunter_position = (485, 495)
            hunter_sell_bottle_position = (675, 465)
            hunter_trade_confirm_position = (430, 735)
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
        self.log.debug('Open map')
        self.mouse_click(*map_position, delay=2, x_offset=x_offset)
        self.log.debug('Travel to city')
        self.mouse_click(*map_city_position, delay=1.7, x_offset=x_offset)
        self.log.debug('Trade with bootlegger')
        self.mouse_click(*bootlegger_position, delay=1.7, x_offset=x_offset)
        self.log.debug('Buy {} poision bottles'.format(bottle_number))
        for i in range(bottle_number):
            self.mouse_click(*bootlegger_buy_bottle_position,
                             delay=0.5, x_offset=x_offset)
        self.log.debug('Confirm trade')
        self.mouse_click(*bootlegger_trade_confirm_position,
                         delay=0.7, x_offset=x_offset)
        self.log.debug('Open map')
        self.mouse_click(*map_position, delay=2, x_offset=x_offset)
        self.log.debug('Travel to glade')
        self.mouse_click(*map_secret_glade_position,
                         delay=1.7, x_offset=x_offset)
        self.log.debug('Trade with hunter')
        self.mouse_click(*hunter_position, delay=1.7, x_offset=x_offset)
        self.log.debug('Sell {} poision bottles'.format(bottle_number))
        for i in range(bottle_number):
            self.mouse_click(*hunter_sell_bottle_position,
                             delay=0.5, x_offset=x_offset)
        self.log.debug('Confirm trade')
        self.mouse_click(*hunter_trade_confirm_position,
                         delay=0.7, x_offset=x_offset)
        self.log.debug('Trade iteration finish')


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

        adjustment = Gtk.Adjustment(value=0, lower=0, upper=999999,
                                    step_increment=1, page_increment=10, page_size=0)
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
        cash_value = int(self.money.get_text())
        clicker_exec = ClickerExecutor(cash_value=cash_value)
        clicker_exec.clicker_process()


win = ClickerWindow()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()
