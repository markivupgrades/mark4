#!/usr/bin/env python

import tkinter as tk
import time
import math
import os  # ✅ Added for absolute path handling
from datetime import datetime

CENTER_X, CENTER_Y = 989, 632

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, width=2560, height=1440)
        self.canvas.pack(fill='both', expand=True)

        # 🔧 Use absolute paths for all images
        base_path = "/home/pi/Rolex/png"
        self.background_image = tk.PhotoImage(file=os.path.join(base_path, "RolexGOLD.png"))
        self.weekday_images = {
            "Mon": tk.PhotoImage(file=os.path.join(base_path, "Monday.png")),
            "Tue": tk.PhotoImage(file=os.path.join(base_path, "Tuesday.png")),
            "Wed": tk.PhotoImage(file=os.path.join(base_path, "Wednesday.png")),
            "Thu": tk.PhotoImage(file=os.path.join(base_path, "Thursday.png")),
            "Fri": tk.PhotoImage(file=os.path.join(base_path, "Friday.png")),
            "Sat": tk.PhotoImage(file=os.path.join(base_path, "Saturday.png")),
            "Sun": tk.PhotoImage(file=os.path.join(base_path, "Sunday.png"))
        }

    def draw_static_layers(self):
        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        now = datetime.now()
        self.draw_date(now.day, now.strftime("%a"))
        self.draw_center_ovals()

    def draw_date(self, day, weekday):
        self.canvas.create_image(980, 142, image=self.weekday_images[weekday], anchor='center')
        self.canvas.create_text(1399, 636, text=day, font=('Copperplate', 64), fill='black')
        self.canvas.create_text(1397, 634, text=day, font=('Copperplate', 64), fill='#FCF2E3', anchor='center')

    def draw_hands(self, hour, minute):
        x0 = 980
        y0 = 632
        hour_angle = (hour % 12 + minute / 60) * math.pi / 6
        minute_angle = minute * math.pi / 30

        hour_x = x0 + 310 * math.sin(hour_angle)
        hour_y = y0 - 310 * math.cos(hour_angle)
        minute_x = x0 + 520 * math.sin(minute_angle)
        minute_y = y0 - 520 * math.cos(minute_angle)

        self.canvas.create_line(x0, y0, hour_x, hour_y, width=42, fill='black', capstyle=tk.ROUND, tags='main_hands')
        self.canvas.create_line(
            x0 + (hour_x - x0) * ((310 - 60) / 310),
            y0 + (hour_y - y0) * ((310 - 60) / 310),
            x0 + (hour_x - x0) * ((310 - 15) / 310),
            y0 + (hour_y - y0) * ((310 - 15) / 310),
            fill='#FCF2E3', width=14, capstyle=tk.ROUND, tags='main_hands'
        )

        self.canvas.create_line(x0, y0, minute_x, minute_y, width=25, fill='black', capstyle=tk.ROUND, tags='main_hands')
        self.canvas.create_line(
            x0 + (minute_x - x0) * ((520 - 70) / 520),
            y0 + (minute_y - y0) * ((520 - 70) / 520),
            x0 + (minute_x - x0) * ((520 - 20) / 520),
            y0 + (minute_y - y0) * ((520 - 20) / 520),
            fill='#FCF2E3', width=12, capstyle=tk.ROUND, tags='main_hands'
        )

    def update_main_hands(self):
        self.canvas.delete('main_hands')
        now = datetime.now()
        self.draw_hands(now.hour, now.minute)
        self.root.after(1000, self.update_main_hands)

    def draw_center_ovals(self):
        x0 = 980
        y0 = 632
        self.canvas.create_oval(x0-44, y0-44, x0+44, y0+44, fill='#FCF2E3')
        self.canvas.create_oval(x0-38, y0-38, x0+38, y0+38, fill='black')
        self.canvas.create_oval(x0-34, y0-34, x0+34, y0+34, fill='black')

    def draw_second_hand(self):
        now = datetime.now()
        seconds = now.second + now.microsecond / 1_000_000
        angle = math.radians(seconds * 6)

        second_center_x = CENTER_X - 4
        second_center_y = CENTER_Y + 4
        second_x = second_center_x + 542 * math.sin(angle)
        second_y = second_center_y - 542 * math.cos(angle)

        self.canvas.delete('second_hand')
        self.canvas.create_line(second_center_x, second_center_y, second_x, second_y, width=8, fill='black', capstyle=tk.ROUND, tags='second_hand')

        marker_start_x = second_center_x + (second_x - second_center_x) * ((542 - 67) / 542)
        marker_start_y = second_center_y + (second_y - second_center_y) * ((542 - 67) / 542)
        marker_end_x = second_center_x + (second_x - second_center_x) * ((542 - 15) / 542)
        marker_end_y = second_center_y + (second_y - second_center_y) * ((542 - 15) / 542)

        self.canvas.create_line(marker_start_x, marker_start_y, marker_end_x, marker_end_y, fill='#fcf2e3', width=5, capstyle=tk.ROUND, tags='second_hand')

    def update_second_hand(self):
        self.draw_second_hand()
        self.root.after(50, self.update_second_hand)

    def exit_clock(self):
        self.root.destroy()

    def run(self):
        self.draw_static_layers()
        self.update_main_hands()
        self.update_second_hand()
        self.root.after(3600000, self.exit_clock)
        self.root.mainloop()

if __name__ == '__main__':
    Clock().run()