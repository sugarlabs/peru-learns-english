#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Toolbar.py por:
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
from gi.repository import Gtk, GObject, Pango

import os

from popupmenubutton import PopupMenuButton

from ConfigParser import SafeConfigParser

from Globales import COLORES

BASE_PATH = os.path.dirname(__file__)


class Toolbar(Gtk.EventBox):

    __gsignals__ = {
        "activar": (GObject.SIGNAL_RUN_FIRST,
                    GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
        "video": (GObject.SIGNAL_RUN_FIRST,
                  GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = Gtk.Toolbar()

        self.modify_bg(Gtk.StateFlags.NORMAL, COLORES["toolbar"])
        toolbar.modify_bg(Gtk.StateFlags.NORMAL, COLORES["toolbar"])
        toolbar.modify_fg(Gtk.StateFlags.NORMAL, COLORES["text"])

        item = Gtk.ToolItem()
        item.set_expand(True)
        imagen = Gtk.Image()
        imagen.set_from_file("Imagenes/ple.png")

        self.homebutton = Gtk.ToggleToolButton()
        self.homebutton.set_label_widget(imagen)
        self.homebutton.connect("toggled", self.__go_home)
        item.add(self.homebutton)
        toolbar.insert(item, -1)

        separador = Gtk.SeparatorToolItem()
        separador.props.draw = True
        toolbar.insert(separador, -1)

        item = Gtk.ToolItem()
        item.set_expand(True)
        label = Gtk.Label("Instructions")
        label.modify_font(Pango.FontDescription("DejaVu Sans Bold 16"))
        label.modify_fg(Gtk.StateFlags.NORMAL, COLORES["text"])
        self.instructionsbutton = Gtk.ToggleToolButton()
        self.instructionsbutton.set_label_widget(label)
        self.instructionsbutton.connect("toggled", self.__go_instructions)
        item.add(self.instructionsbutton)
        toolbar.insert(item, -1)
        separador = Gtk.SeparatorToolItem()
        separador.props.draw = True
        toolbar.insert(separador, -1)

        self.menu = Menu()

        self.menubutton = PopupMenuButton("Topics")
        self.menubutton.get_child().modify_font(
            Pango.FontDescription("DejaVu Sans Bold 16"))
        self.menubutton.get_child().modify_fg(
            Gtk.StateFlags.NORMAL, COLORES["text"])
        self.menubutton.get_child().modify_bg(
            Gtk.StateFlags.NORMAL, COLORES["toolbar"])
        self.menubutton.set_menu(self.menu)

        item = Gtk.ToolItem()
        item.set_expand(True)
        item.add(self.menubutton)
        toolbar.insert(item, -1)

        self.add(toolbar)
        self.show_all()

        self.menu.connect("activar", self.__emit_accion_menu)

    def __emit_accion_menu(self, widget, topic):
        self.instructionsbutton.set_active(False)
        self.homebutton.set_active(False)
        self.emit("video", topic)

    def __go_home(self, widget):
        activo = widget.get_active()
        if activo:
            self.instructionsbutton.set_active(False)
            self.menubutton.set_active(False)
            self.emit("activar", "Home")
        else:
            self.homebutton.set_active(False)

    def __go_instructions(self, widget):
        activo = widget.get_active()
        if activo:
            self.emit("activar", "Instructions")
            self.menubutton.set_active(False)
            self.homebutton.set_active(False)
        else:
            self.instructionsbutton.set_active(False)


class Menu(Gtk.Menu):

    __gsignals__ = {
        "activar": (GObject.SIGNAL_RUN_FIRST,
                    GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):
        Gtk.Menu.__init__(self)

        self.modify_bg(Gtk.StateFlags.NORMAL, COLORES["menu"])

        topics = os.path.join(BASE_PATH, "Topics")
        for arch in sorted(os.listdir(topics)):
            item = Gtk.MenuItem()

            parser = SafeConfigParser()
            metadata = os.path.join(topics, arch, "topic.ini")
            parser.read(metadata)

            title = parser.get('topic', 'title')

            boton = Gtk.Label(title)
            boton.modify_font(Pango.FontDescription("DejaVu Sans Bold 16"))
            boton.modify_fg(Gtk.StateFlags.NORMAL, COLORES["window"])
            boton.set_padding(xpad=5, ypad=20)
            item.add(boton)
            item.connect("activate", self.__emit_accion_menu, arch)
            item.show()
            boton.show()
            self.append(item)

    def __emit_accion_menu(self, widget, arch):
        label = arch
        self.emit("activar", os.path.join(BASE_PATH, "Topics", label))
