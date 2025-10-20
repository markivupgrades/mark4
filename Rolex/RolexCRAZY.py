#!/usr/bin/env python

import tkinter as tk
import time
import math
import os  # ✅ Added for absolute path handling

CENTER_X, CENTER_Y = 984, 635

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack(fill='both', expand=True)

        # 🔧 Use absolute path for background image
        image_path = os.path.join("/home/pi/Rolex/png", "RolexCRAZY.png")
        self.background_image = tk.PhotoImage(file=image_path)

    def draw_static_layers(self):
        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        self.draw_center_ovals()

    def draw_hands(self, hour, minute):
        x0 = CENTER_X
        y0 = CENTER_Y
        hour_angle = (hour % 12 + minute / 60) * math.pi / 6
        minute_angle = minute * math.pi / 30

        hour_x = x0 + 290 * math.sin(hour_angle)
        hour_y = y0 - 290 * math.cos(hour_angle)
        minute_x = x0 + 550 * math.sin(minute_angle)
        minute_y = y0 - 550 * math.cos(minute_angle)

        self.canvas.create_line(x0, y0, hour_x, hour_y, width=54, fill='black', capstyle=tk.ROUND, tags='main_hands')
        self.canvas.create_line(x0, y0, hour_x, hour_y, width=50, fill='white', capstyle=tk.ROUND, tags='main_hands')
        self.canvas.create_oval(hour_x-10, hour_y-10, hour_x+10, hour_y+10, fill='gray', tags='main_hands')

        self.canvas.create_line(x0, y0, minute_x, minute_y, width=29, fill='black', capstyle=tk.ROUND, tags='main_hands')
        self.canvas.create_line(x0, y0, minute_x, minute_y, width=25, fill='white', capstyle=tk.ROUND, tags='main_hands')

        minute_oval_x = minute_x - 10 * math.sin(minute_angle)
        minute_oval_y = minute_y + 10 * math.cos(minute_angle)
        self.canvas.create_oval(minute_oval_x-5, minute_oval_y-5, minute_oval_x+5, minute_oval_y+5, fill='gray', tags='main_hands')

    def update_main_hands(self):
        self.canvas.delete('main_hands')
        now = time.localtime()
        self.draw_hands(now.tm_hour, now.tm_min)
        self.root.after(1000, self.update_main_hands)

    def draw_center_ovals(self):
        x0 = CENTER_X
        y0 = CENTER_Y
        self.canvas.create_oval(x0-44, y0-44, x0+44, y0+44, fill='white')
        self.canvas.create_oval(x0-38, y0-38, x0+38, y0+38, fill='black')
        self.canvas.create_oval(x0-34, y0-34, x0+34, y0+34, fill='white')

    def draw_second_hand(self):
        now = time.localtime()
        second_angle = now.tm_sec * math.pi / 30

        x0 = CENTER_X
        y0 = CENTER_Y
        second_x = x0 + 560 * math.sin(second_angle)
        second_y = y0 - 560 * math.cos(second_angle)

        self.canvas.create_line(x0, y0, second_x, second_y, width=10, fill='black', capstyle=tk.ROUND, tags='second_hand')
        self.canvas.create_line(x0, y0, second_x, second_y, width=8, fill='white', capstyle=tk.ROUND, tags='second_hand')

        second_oval_x = second_x - 10 * math.sin(second_angle)
        second_oval_y = second_y + 10 * math.cos(second_angle)
        self.canvas.create_oval(second_oval_x-2, second_oval_y-2, second_oval_x+2, second_oval_y+2, fill='gray', tags='second_hand')

    def update_second_hand(self):
        self.canvas.delete('second_hand')
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