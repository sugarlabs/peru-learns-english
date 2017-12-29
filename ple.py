#!/bin/env python2
# -*- coding: utf-8 -*-

#   Main.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

import os
import sys

installed_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(installed_dir)

from Toolbar import Toolbar
from Globales import COLORES
from VideoView import VideoView
from FlashCardView import FlashCardView
from GameView import GameMenu
from GameView import GameView
from InstructionsView import InstructionsView
from WelcomeView import WelcomeView
from CreditsView import CreditsView

BASE_PATH = os.path.dirname(__file__)

def ocultar(widget):
    widget.stop()

class App(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("Peru Learns English")
        self.set_icon_from_file(os.path.join(
            BASE_PATH , "Iconos", "icono.svg"))

        self.modify_bg(Gtk.StateFlags.NORMAL, COLORES["window"])
        self.set_border_width(2)

        # FIXME: No funciona en la XO con fedora 11
        #self.set_resizable(False)

        main = Main()
        self.add(main)

        GObject.idle_add(self.show)

class Main(Gtk.EventBox):

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.vbox = Gtk.VBox()
        self.toolbar = Toolbar()
        self.vbox.pack_start(self.toolbar, False, False, 0)

        self.videoview = VideoView()
        self.vbox.pack_start(self.videoview, True, True, 0)

        self.flashcards = FlashCardView()
        self.vbox.pack_start(self.flashcards, True, True, 0)

        self.gamemenu = GameMenu()
        self.vbox.pack_start(self.gamemenu, True, True, 0)

        self.instructionsview = InstructionsView()
        self.vbox.pack_start(self.instructionsview, True, True, 0)

        self.welcomeview = WelcomeView()
        self.vbox.pack_start(self.welcomeview, True, True, 0)

        self.creditsview = CreditsView()
        self.vbox.pack_start(self.creditsview, True, True, 0)

        self.add(self.vbox)
        self.show_all()

        self.toolbar.connect("activar", self.__switch)
        self.toolbar.connect("video", self.__play_video)
        self.gamemenu.gameview.connect("video", self.__game_return_to_video)
        self.gamemenu.connect("video", self.__game_return_to_video)
        self.videoview.connect("flashcards", self.__play_flashcards)
        self.videoview.connect("game", self.__play_game)
        self.flashcards.connect("video", self.__game_return_to_video)
        self.welcomeview.connect("instructions", self.__play_instructions)
        self.welcomeview.connect("credits", self.__play_credits)
        self.welcomeview.connect("start", self.__show_menu)
        self.connect("delete-event", self.__salir)
        self.toolbar.menubutton.connect("toggled", self.__stop_credits)

        self.toolbar.homebutton.set_active(True)

        self.__switch(False, "Home", None)

    def __stop_credits(self, widget):
        if self.creditsview.props.visible:
            run = not bool(self.creditsview.visor.update)
            if run:
                self.creditsview.visor.modify_bg(
                    Gtk.StateFlags.NORMAL, COLORES["text"])
            self.creditsview.visor.new_handle(run)

    def __game_return_to_video(self, widget, topic):
        self.__play_video(widget, topic)
        #self.videoview.videoplayer.stop()

    def __play_game(self, widget, topic):
        self.__switch(False, "game", topic)

    def __play_flashcards(self, widget, data):
        self.__switch(False, "flashcards", data)

    def __play_video(self, widget, topic):
        self.toolbar.homebutton.set_active(False)
        self.__switch(False, "Topics", topic)
        self.videoview.set_full(False)
        #self.videoview.videoplayer.pause()

    def __play_instructions(self, widget):
        self.__switch(False, "Instructions")
        self.toolbar.homebutton.set_active(False)

    def __play_credits(self, widget):
        self.__switch(False, "Credits")
        self.toolbar.homebutton.set_active(False)

    def __show_menu(self, widget):
        self.toolbar.menubutton.popup()
        self.toolbar.menubutton.set_active(True)
        self.toolbar.instructionsbutton.set_active(False)

    def __switch(self, widget, label, data=False):
        map(ocultar, self.vbox.get_children()[1:])
        if label == "Home":
            self.welcomeview.run()
        elif label == "Instructions":
            self.instructionsview.run()
        elif label == "Credits":
            self.creditsview.run()
        elif label == "Topics":
            self.videoview.run(data)
        elif label == "flashcards":
            self.flashcards.run(data)
        elif label == "game":
            self.gamemenu.run(data)
        return False

    def __salir(self, widget=None, senial=None):
        self.videoview.stop()
        Gtk.main_quit()
        sys.exit(0)


if __name__ == '__main__':
    App()
    Gtk.main()
