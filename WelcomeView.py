#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   InstructionsView.py por:
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
from gi.repository import Gtk, Gdk, GObject, Pango, GdkPixbuf

from Globales import COLORES, is_xo


class WelcomeView(Gtk.EventBox):

    __gsignals__ = {
        "instructions": (GObject.SIGNAL_RUN_FIRST,
                         GObject.TYPE_NONE, ()),
        "credits": (GObject.SIGNAL_RUN_FIRST,
                    GObject.TYPE_NONE, ()),
        "start": (GObject.SIGNAL_RUN_FIRST,
                  GObject.TYPE_NONE, ())}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateFlags.NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.image = Gtk.Image()
        self.image.set_from_file("Imagenes/ple.png")

        tabla = Gtk.Table(rows=10, columns=2, homogeneous=False)
        tabla.set_border_width(16)
        tabla.attach(self.image, 0, 2, 0, 9)

        bb = Gtk.HButtonBox()
        bb.set_layout(Gtk.ButtonBoxStyle.SPREAD)

        b = Gtk.Button("")
        b.set_relief(Gtk.ReliefStyle.NONE)
        b.modify_bg(Gtk.StateFlags.NORMAL, COLORES["toolbar"])
        b.connect("enter-notify-event", self.__color, "manual")
        b.connect("leave-notify-event", self.__decolor, "manual")
        b.connect("clicked", self.__instructions)
        img = Gtk.Image()
        img.set_from_file("Imagenes/manual_disabled.png")
        b.set_image(img)
        bb.pack_start(b, True, True, 0)
        img.show()

        b = Gtk.Button("")
        b.set_relief(Gtk.ReliefStyle.NONE)
        b.modify_bg(Gtk.StateFlags.NORMAL, COLORES["toolbar"])
        b.connect("enter-notify-event", self.__color, "contributors")
        b.connect("leave-notify-event", self.__decolor, "contributors")
        b.connect("clicked", self.__credits)
        img = Gtk.Image()
        img.set_from_file("Imagenes/contributors_disabled.png")
        b.set_image(img)
        bb.pack_start(b, True, True, 0)
        img.show()
        bb.show_all()

        b = Gtk.Button("")
        b.set_relief(Gtk.ReliefStyle.NONE)
        b.modify_bg(Gtk.StateFlags.NORMAL, COLORES["toolbar"])
        b.connect("clicked", self.__start)
        img = Gtk.Image()
        img.set_from_file("Imagenes/start.png")
        b.set_image(img)
        bb.pack_start(b, True, True, 0)
        img.show()
        bb.show_all()

        tabla.attach(bb, 0, 2, 9, 10)

        self.add(tabla)
        self.show_all()

    def __decolor(self, widget, event, filestub):
        widget.get_image().set_from_file("Imagenes/%s_disabled.png" % filestub)

    def __color(self, widget, event, filestub):
        widget.get_image().set_from_file("Imagenes/%s.png" % filestub)

    def __instructions(self, widget):
        self.emit("instructions")

    def __credits(self, widget):
        self.emit("credits")

    def __start(self, widget):
        self.emit("start")

    def stop(self):
        self.hide()

    def fix_scale(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("Imagenes/welcome_slide.png")
        screen = self.get_parent().get_screen()
        offset = 220 if not is_xo() else 340
        desired_height = screen.get_height() - offset
        desired_width = pixbuf.get_height() / desired_height * pixbuf.get_width()
        pixbuf = pixbuf.scale_simple(desired_width, desired_height, 2)
        self.image.set_from_pixbuf(pixbuf)

    def run(self):
        self.fix_scale()
        self.show()
