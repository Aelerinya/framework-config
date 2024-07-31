#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cairo
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constant for counter duration (in seconds)
COUNTER_DURATION = 10

class OverlayWindow(Gtk.Window):
    def __init__(self):
        logging.debug("Initializing OverlayWindow")
        Gtk.Window.__init__(self, title="Morning Reminder")
        self.set_default_size(800, 600)
        self.connect("destroy", Gtk.main_quit)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.fullscreen()
        logging.debug("Window set to fullscreen")

        overlay = Gtk.Overlay()
        self.add(overlay)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_draw)
        overlay.add(self.drawing_area)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_valign(Gtk.Align.CENTER)
        overlay.add_overlay(main_box)

        label = Gtk.Label()
        label.set_markup("""
            <span font='DejaVu Sans 36' color='white'>Use the</span>\n
            <span font='DejaVu Sans Bold 48' color='white'>Theme System</span>\n
            <span font='DejaVu Sans 36' color='white'>before engaging with your laptop</span>
        """)
        label.set_justify(Gtk.Justification.CENTER)
        main_box.pack_start(label, True, True, 0)

        countdown_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        countdown_box.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(countdown_box, False, False, 0)

        self.countdown_label = Gtk.Label()
        self.countdown_label.set_markup(f"<span font='DejaVu Sans Bold 72' color='white'>{COUNTER_DURATION}</span>")
        countdown_box.pack_start(self.countdown_label, False, False, 0)

        self.screenshots = []
        self.countdown = COUNTER_DURATION
        GLib.idle_add(self.take_screenshots)
        GLib.timeout_add(1000, self.update_countdown)

        logging.debug("OverlayWindow initialized")

    def take_screenshots(self):
        logging.debug("Taking screenshots")
        display = Gdk.Display.get_default()
        n_monitors = display.get_n_monitors()
        logging.debug(f"Number of monitors detected: {n_monitors}")
        
        for i in range(n_monitors):
            monitor = display.get_monitor(i)
            geometry = monitor.get_geometry()
            scale_factor = monitor.get_scale_factor()
            
            logging.debug(f"Monitor {i}: Geometry: {geometry.x},{geometry.y} {geometry.width}x{geometry.height}, Scale: {scale_factor}")
            
            root_window = Gdk.get_default_root_window()
            pb = Gdk.pixbuf_get_from_window(root_window, 
                                            geometry.x * scale_factor, 
                                            geometry.y * scale_factor, 
                                            geometry.width * scale_factor, 
                                            geometry.height * scale_factor)
            
            if pb is None:
                logging.error(f"Failed to capture screenshot for monitor {i}")
                continue

            # Scale down the screenshot if it was taken with a scale factor
            if scale_factor != 1:
                pb = pb.scale_simple(geometry.width, geometry.height, GdkPixbuf.InterpType.BILINEAR)
            
            self.screenshots.append((pb, geometry))
            logging.debug(f"Screenshot captured for monitor {i}")
        
        self.drawing_area.queue_draw()
        logging.debug(f"Screenshots taken: {len(self.screenshots)}")
        return False

    def on_draw(self, widget, cr):
        logging.debug("Drawing started")
        if not self.screenshots:
            logging.warning("No screenshots to draw")
            return

        for i, (screenshot, geometry) in enumerate(self.screenshots):
            logging.debug(f"Drawing screenshot {i}: pos({geometry.x},{geometry.y}) size({geometry.width}x{geometry.height})")
            Gdk.cairo_set_source_pixbuf(cr, screenshot, geometry.x, geometry.y)
            cr.paint()
        
        cr.set_source_rgba(0, 0, 0, 0.7)  # Semi-transparent black
        cr.paint()
        logging.debug("Drawing complete")

    def update_countdown(self):
        self.countdown -= 1
        self.countdown_label.set_markup(f"<span font='DejaVu Sans Bold 72' color='white'>{self.countdown}</span>")
        if self.countdown <= 0:
            logging.debug("Countdown finished, quitting main loop")
            Gtk.main_quit()
            return False
        return True

def show_reminder():
    logging.debug("Showing reminder")
    win = OverlayWindow()
    win.show_all()
    Gtk.main()
    logging.debug("Reminder shown")

if __name__ == "__main__":
    show_reminder()