#!/usr/bin/env python

import tkinter as tk
import time
import math
import os  # ✅ For path handling

CENTER_X, CENTER_Y = 989, 632

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, width=3840, height=2160)
        self.canvas.pack(fill='both', expand=True)

        image_path = os.path.join("/home/pi/Rolex/png", "Rolex1908.png")
        self.background_image = tk.PhotoImage(file=image_path)
        self.second_angle = 0

    def draw_static_layers(self):
        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')

    def draw_hands(self, hour, minute):
        hour_angle = (hour % 12 + minute / 60) * math.pi / 6
        minute_angle = minute * math.pi / 30

        hour_x = CENTER_X + 350 * math.sin(hour_angle)
        hour_y = CENTER_Y - 350 * math.cos(hour_angle)
        minute_x = CENTER_X + 470 * math.sin(minute_angle)
        minute_y = CENTER_Y - 470 * math.cos(minute_angle)

        self.canvas.create_line(CENTER_X, CENTER_Y, hour_x, hour_y, width=47, fill='black', capstyle=tk.ROUND, tags='main_hands')
        self.canvas.create_oval(hour_x-7, hour_y-7, hour_x+7, hour_y+7, fill='gray', tags='main_hands')

        self.canvas.create_line(CENTER_X, CENTER_Y, minute_x, minute_y, width=25, fill='black', capstyle=tk.ROUND, tags='main_hands')
        self.canvas.create_oval(minute_x-5, minute_y-5, minute_x+5, minute_y+5, fill='gray', tags='main_hands')

    def update_main_hands(self):
        self.canvas.delete('main_hands')
        now = time.localtime()
        self.draw_hands(now.tm_hour, now.tm_min)
        self.draw_center_ovals()  # Draw on top of hands

        # Sync with the start of the next second
        current_time = time.time()
        delay = 1000 - int((current_time % 1) * 1000)
        self.root.after(delay, self.update_main_hands)

    def draw_center_ovals(self):
        self.canvas.create_oval(CENTER_X-44, CENTER_Y-44, CENTER_X+44, CENTER_Y+44, fill='white', tags='center_ovals')
        self.canvas.create_oval(CENTER_X-38, CENTER_Y-38, CENTER_X+38, CENTER_Y+38, fill='black', tags='center_ovals')
        self.canvas.create_oval(CENTER_X-34, CENTER_Y-34, CENTER_X+34, CENTER_Y+34, fill='white', tags='center_ovals')

    def draw_second_hand(self):
        second_center_x = CENTER_X - 4
        second_center_y = CENTER_Y + 342
        second_x = second_center_x + 200 * math.sin(math.radians(self.second_angle))
        second_y = second_center_y - 200 * math.cos(math.radians(self.second_angle))

        self.canvas.delete('second_hand')
        self.canvas.create_line(second_center_x, second_center_y, second_x, second_y, width=8, fill='black', capstyle=tk.ROUND, tags='second_hand')
        self.canvas.create_oval(second_x-2, second_y-2, second_x+2, second_y+2, fill='gray', tags='second_hand')

    def update_second_hand(self):
        now = time.time()
        seconds = now % 60
        self.second_angle = (seconds / 60.0) * 360
        self.draw_second_hand()
        self.draw_center_ovals()  # Ensure center ovals are always on top
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