#!/usr/bin/env python

import tkinter as tk
import time
import math
import os
from datetime import datetime

CENTER_X, CENTER_Y = 989, 632

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, width=2560, height=1440)
        self.canvas.pack(fill='both', expand=True)

        base_path = "/home/pi/Rolex/png"
        self.background_image = tk.PhotoImage(file=os.path.join(base_path, "RolexBLUE.png"))

        # Weekday images (commented out)
        # self.weekday_images = {
        #     "Mon": os.path.join(base_path, "Monday.png"),
        #     "Tue": os.path.join(base_path, "Tuesday.png"),
        #     "Wed": os.path.join(base_path, "Wednesday.png"),
        #     "Thu": os.path.join(base_path, "Thursday.png"),
        #     "Fri": os.path.join(base_path, "Friday.png"),
        #     "Sat": os.path.join(base_path, "Saturday.png"),
        #     "Sun": os.path.join(base_path, "Sunday.png")
        # }

    def draw_static_layers(self):
        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        now = datetime.now()
        self.draw_date(now.day)
       

    def draw_date(self, day):
        # Weekday image logic removed
        # self.load_weekday_image()
        # self.canvas.create_image(985, 130, image=self.weekday_image, anchor='center')
        self.canvas.create_text(1394, 637, text=day, font=('Copperplate', 64), fill='black')
        self.canvas.create_text(1392, 635, text=day, font=('Copperplate', 64), fill='white', anchor='center')

    def draw_hands(self, hour, minute):
        x0 = CENTER_X
        y0 = CENTER_Y
        hour_angle = (hour % 12 + minute / 60) * math.pi / 6
        minute_angle = minute * math.pi / 30

        hour_x = x0 + 310 * math.sin(hour_angle)
        hour_y = y0 - 310 * math.cos(hour_angle)
        minute_x = x0 + 520 * math.sin(minute_angle)
        minute_y = y0 - 520 * math.cos(minute_angle)

        self.canvas.create_line(x0, y0, hour_x, hour_y, width=42, fill='white', capstyle=tk.ROUND, tags='hands')
        self.canvas.create_line(
            x0 + (hour_x - x0) * ((310 - 60) / 310),
            y0 + (hour_y - y0) * ((310 - 60) / 310),
            x0 + (hour_x - x0) * ((310 - 15) / 310),
            y0 + (hour_y - y0) * ((310 - 15) / 310),
            fill='gray30', width=10, capstyle=tk.ROUND, tags='hands'
        )

        self.canvas.create_line(x0, y0, minute_x, minute_y, width=25, fill='white', capstyle=tk.ROUND, tags='hands')
        self.canvas.create_line(
            x0 + (minute_x - x0) * ((520 - 70) / 520),
            y0 + (minute_y - y0) * ((520 - 70) / 520),
            x0 + (minute_x - x0) * ((520 - 20) / 520),
            y0 + (minute_y - y0) * ((520 - 20) / 520),
            fill='gray30', width=9, capstyle=tk.ROUND, tags='hands'
        )

        self.canvas.create_oval(x0-44, y0-44, x0+44, y0+44, fill='#FCF2E3', tags='hands')
        self.canvas.create_oval(x0-38, y0-38, x0+38, y0+38, fill='black', tags='hands')
        self.canvas.create_oval(x0-34, y0-34, x0+34, y0+34, fill='white', tags='hands')

    def draw_second_hand(self, second):
        angle = math.radians(second * 6)
        x0 = CENTER_X - 4
        y0 = CENTER_Y + 4
        x = x0 + 542 * math.sin(angle)
        y = y0 - 542 * math.cos(angle)

        self.canvas.create_line(x0, y0, x, y, width=8, fill='white', capstyle=tk.ROUND, tags='second_hand')

        marker_start_x = x0 + (x - x0) * ((542 - 67) / 542)
        marker_start_y = y0 + (y - y0) * ((542 - 67) / 542)
        marker_end_x = x0 + (x - x0) * ((542 - 15) / 542)
        marker_end_y = y0 + (y - y0) * ((542 - 15) / 542)

        self.canvas.create_line(marker_start_x, marker_start_y, marker_end_x, marker_end_y, fill='gray30', width=5, capstyle=tk.ROUND, tags='second_hand')

    def update_clock(self):
        now = datetime.now()
        self.canvas.delete('hands')
        self.canvas.delete('second_hand')
        self.draw_hands(now.hour, now.minute)
        self.draw_second_hand(now.second + now.microsecond / 1_000_000)
        self.root.after(20, self.update_clock)

    def exit_clock(self):
        self.root.destroy()

    def run(self):
        self.draw_static_layers()
        self.update_clock()
        self.root.after(3600000, self.exit_clock)
        self.root.mainloop()

if __name__ == '__main__':
    Clock().run()
