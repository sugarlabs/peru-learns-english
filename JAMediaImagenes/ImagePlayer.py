#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ImagePlayer.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
Descripción:
    Visor de Imágenes en base a gstreamer.

    Recibe un widget gtk para dibujar sobre él.

    Utilice la función: load(file_path)
        para cargar el archivo a dibujar.

    Utilice la función: stop()
        para detener la reproducción

    Utilice la función: rotar("Derecha") o rotar("Izquierda")
        para rotar la imágen
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf

import os
import cairo


class ImagePlayer(GObject.GObject):

    def __init__(self, ventana, uri):

        GObject.GObject.__init__(self)

        self.ventana = ventana
        self.src_path = uri
        self.image_surface = False

        self.ventana.connect("draw", self.__draw_cb)

    def __draw_cb(self, widget, cr):
        rect = self.ventana.get_allocation()
        area = widget.get_allocation()
        cr.rectangle(area.x, area.y, area.width, area.height)
        cr.clip()

        if not self.image_surface:
            if os.path.exists(self.src_path):
                self.image_surface = cairo.ImageSurface.create_from_png(
                    self.src_path)
                self.ventana.queue_draw()
            cr.set_source_surface(self.image_surface, area.x, area.y)
            cr.paint()

            self.image_surface = False

        return True

    def stop(self):
        try:
            self.ventana.disconnect_by_func(self.__set_size)
        except:
            pass
