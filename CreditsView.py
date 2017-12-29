#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   CreditsView.py por:
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
from gi.repository import Gtk, GObject
import cairo
import os

from Globales import COLORES

BASE_PATH = os.path.dirname(__file__)


class CreditsView(Gtk.EventBox):

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateFlags.NORMAL, COLORES["window"])
        self.set_border_width(10)

        self.visor = Visor()

        self.add(self.visor)
        self.show_all()

    def stop(self):
        self.visor.new_handle(False)
        self.hide()

    def run(self):
        self.show()
        self.visor.new_handle(True)


class Visor(Gtk.DrawingArea):

    def __init__(self):

        Gtk.DrawingArea.__init__(self)

        self.modify_bg(Gtk.StateFlags.NORMAL, COLORES["text"])

        self.posy = 300
        self.update = False
        self.imagen = False

        self.connect("draw", self.__expose)
        self.connect("realize", self.__realize)
        self.show_all()

    def __expose(self, widget, event):
        self.new_handle(True)

    def __realize(self, widget):
        cr = self.get_window().cairo_create()
        self.imagen = cairo.ImageSurface.create_from_png(os.path.join(
            BASE_PATH, "Iconos", "creditos_ple.png"))

    def __handle(self):
        cr = self.get_window().cairo_create()
        alloc = self.get_allocation()
        x, y, w, h = alloc.x, alloc.y, alloc.width, alloc.height
        cr.rectangle(x, y, w, h)
        ww = self.imagen.get_width()
        hh = self.imagen.get_height()
        x = w / 2 - ww / 2
        cr.set_source_surface(self.imagen, x, self.posy)
        cr.fill()
        self.posy -= 2
        if self.posy < -hh:
            self.posy = h
        return True

    def new_handle(self, reset):
        if self.update:
            GObject.source_remove(self.update)
            self.update = False
        if reset:
            self.posy = 300
            self.update = GObject.timeout_add(50, self.__handle)
