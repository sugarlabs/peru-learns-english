#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2008-2011 Zuza Software Foundation
#
# This file is part of Virtaal.
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
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Positioning constants below:
# POS_CENTER_BELOW: Centers the pop-up window below the button (default).
# POS_CENTER_ABOVE: Centers the pop-up window above the button.
# POS_NW_SW: Positions the pop-up window so that its North West (top left)
#            corner is on the South West corner of the button.
# POS_NE_SE: Positions the pop-up window so that its North East (top right)
#            corner is on the South East corner of the button. RTL of POS_NW_SW
# POS_NW_NE: Positions the pop-up window so that its North West (top left)
#            corner is on the North East corner of the button.
# POS_SW_NW: Positions the pop-up window so that its South West (bottom left)
#            corner is on the North West corner of the button.
# POS_SE_NE: Positions the pop-up window so that its South East (bottom right)
#            corner is on the North East corner of the button. RTL of POS_SW_NW
POS_CENTER_BELOW, POS_CENTER_ABOVE, POS_NW_SW, POS_NE_SE, POS_NW_NE, POS_SW_NW, POS_SE_NE = range(7)
# XXX: Add position symbols above as needed and implementation in
#      _update_popup_geometry()

_rtl_pos_map = {
        POS_CENTER_BELOW: POS_CENTER_BELOW,
        POS_CENTER_ABOVE: POS_CENTER_ABOVE,
        POS_SW_NW: POS_SE_NE,
        POS_NW_SW: POS_NE_SE,
}

class PopupMenuButton(Gtk.ToggleButton):
    """A toggle button that displays a pop-up menu when clicked."""

    # INITIALIZERS #
    def __init__(self, label=None, menu_pos=POS_NW_SW):
        Gtk.ToggleButton.__init__(self, label=label)
        self.set_relief(Gtk.ReliefStyle.NONE)
        self.set_menu(Gtk.Menu())

        if self.get_direction() == Gtk.StateFlags.DIR_LTR:
            self.menu_pos = menu_pos
        else:
            self.menu_pos = _rtl_pos_map.get(menu_pos, POS_SE_NE)

        self.connect('toggled', self._on_toggled)


    # ACCESSORS #
    def set_menu(self, menu):
        if getattr(self, '_menu_selection_done_id', None):
            self.menu.disconnect(self._menu_selection_done_id)
        self.menu = menu
        self._menu_selection_done_id = self.menu.connect('selection-done', self._on_menu_selection_done)

    def get_label_widget(self):
        return self.get_child()

    def _get_text(self):
        return unicode(self.get_label())
    def _set_text(self, value):
        self.set_label(value)
    text = property(_get_text, _set_text)

    def popdown(self):
        self.menu.popdown()
        return True

    def popup(self):
        self.menu.popup_at_widget(self, POS_NW_SW, self.menu_pos, None)


    # EVENT HANDLERS #
    def _on_menu_selection_done(self, menu):
        self.set_active(False)

    def _on_toggled(self, togglebutton):
        assert self is togglebutton

        if self.get_active():
            self.popup()
        else:
            self.popdown()