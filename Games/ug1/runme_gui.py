#!/bin/env python2
import sys
sys.path.insert(1, "../../Lib/")


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk

import sugargame2
import sugargame2.canvas
import spyral
import pygame
from runme import Escena


class GameWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(700, 700)

        self.pygamecanvas = sugargame2.canvas.PygameCanvas(self)
        self.pygamecanvas.set_flags(Gtk.EXPAND)
        self.pygamecanvas.set_flags(Gtk.FILL)

        self.connect("visibility-notify-event", self.redraw)
        self.pygamecanvas.set_events(Gdk.BUTTON_PRESS_MASK)
        self.pygamecanvas.connect(
            "button-press-event", self.pygamecanvas.grab_focus)

        self.add(self.pygamecanvas)
        GObject.timeout_add(300, self.pump)

        self.pygamecanvas.run_pygame(self.run_game)

    def redraw(self, *args, **kwargs):
        scene = spyral.director.get_scene()
        if scene:
            scene.redraw()

    def pump(self):
        # Esto es necesario porque sino pygame acumula demasiados eventos.
        pygame.event.pump()

    def run_game(self):
        spyral.director.init((700, 700), fullscreen=False, max_fps=30)
        self.game = Escena(self)  # JUEGO.Juego(self, callback=self.game_ready)
        spyral.director.push(self.game)
        self.start()

    def start(self):
        spyral.director.run(sugar=True)


if __name__ == "__main__":
    w = GameWindow()
    w.show_all()
    Gtk.main()
