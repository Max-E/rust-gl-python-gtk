#! /usr/bin/env python2

# Copyright (C) 2018 Max Eliaser

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from cffi import FFI
ffi = FFI ()
ffi.cdef ("""
    void init (void);
    void create_tab (size_t tabID);
    void set_tab_seed (size_t tabID, size_t seed);
    void close_tab (size_t tabID);
    void switch_to_tab (size_t tabID);
    void render (void);
""")

rust_component = ffi.dlopen ("target/debug/librust_component.so")

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import gi
gi.require_version ('Gtk', '3.0')
from gi.repository import Gtk

win = Gtk.Window ()
win.connect ("delete-event", Gtk.main_quit)

tabbar = Gtk.HBox ()

addbutton = Gtk.Button (image = Gtk.Image (stock = Gtk.STOCK_ADD))
addbutton.connect ("clicked", lambda *args: add_tab ())
tabbar.pack_end (addbutton, False, False, 0)

book = Gtk.Notebook ()
book.set_scrollable (True)
tabbar.pack_start (book, True, True, 0)

def switch_to_tab (notebook, page, page_idx):
    area.queue_render ()
    return True
book.connect ("switch-page", switch_to_tab)

def change_seed (entry, tablabel):
    n = int (entry.get_text ())
    tablabel.set_text (str (n))
    rust_component.set_tab_seed (book.get_current_page (), n)
    area.queue_render ()

def add_tab ():
    n = book.get_n_pages ()
    rust_component.create_tab (n)
    rust_component.set_tab_seed (n, 0)
    hbox = Gtk.HBox ()
    entry = Gtk.Entry ()
    entry.set_text ("0")
    hbox.pack_start (Gtk.Label ("Seed:"), False, False, 0)
    hbox.pack_start (entry, True, True, 0)
    tablabel = Gtk.Label ("0")
    entry.connect ("activate", change_seed, tablabel)
    book.append_page (hbox, tablabel)
    book.show_all ()
    return True

area = Gtk.GLArea ()
area.set_size_request (600, 400)

def render (area, ctx):
    ctx.make_current ()
    rust_component.switch_to_tab (book.get_current_page ())
    rust_component.render ()
    return True
area.connect ("render", render)

vbox = Gtk.VBox ()
vbox.pack_start (tabbar, False, False, 0)
vbox.pack_start (area, True, True, 0)

win.add (vbox)

win.show_all ()

area.get_context ().make_current ()
rust_component.init ()

add_tab ()

win.show_all ()

Gtk.main ()
