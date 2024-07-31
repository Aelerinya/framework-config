#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
from gi.repository import GLib
from pydbus import SessionBus

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REMINDER_SCRIPT_PATH = os.path.join(SCRIPT_DIR, "fullscreen_blur_reminder.py")
LAST_RUN_FILE = os.path.expanduser("~/.last_reminder_run")

def get_last_run_date():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as f:
            return f.read().strip()
    return None

def set_last_run_date():
    with open(LAST_RUN_FILE, 'w') as f:
        f.write(datetime.now().strftime("%Y-%m-%d"))

def on_active_changed(active):
    if not active:  # Screen was unlocked
        last_run = get_last_run_date()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if last_run != today:
            print("Screen unlocked. Running reminder script...")
            subprocess.run(["python3", REMINDER_SCRIPT_PATH])
            set_last_run_date()
        else:
            print("Screen unlocked, but reminder already run today. Skipping.")

def main():
    bus = SessionBus()
    screensaver = bus.get('org.gnome.ScreenSaver')
    screensaver.onActiveChanged = on_active_changed
    
    print("D-Bus monitor started. Waiting for screen unlock events...")
    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()