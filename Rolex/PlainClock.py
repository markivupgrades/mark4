#!/usr/bin/env python

import tkinter as tk
import time
import math
import os

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack(fill='both', expand=True)

        # Load background image once
        image_path = os.path.join("/home/pi/Rolex/png", "CLOCK.png")
        self.background_image = tk.PhotoImage(file=image_path)

    def draw_static_layers(self):
        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')

    def draw_center_dot(self):
        """Draws the static center dot that stays on top of all hands."""
        x0 = 990
        y0 = 635
        self.canvas.create_oval(x0-44, y0-44, x0+44, y0+44, fill='white', tags='center_dot')
        self.canvas.create_oval(x0-38, y0-38, x0+38, y0+38, fill='black', tags='center_dot')
        self.canvas.create_oval(x0-34, y0-34, x0+34, y0+34, fill='white', tags='center_dot')

    def draw_hands(self, hour, minute, second):
        x0 = 990
        y0 = 635

        # Convert to radians
        hour_angle = (hour % 12 + minute / 60) * math.pi / 6
        minute_angle = minute * math.pi / 30
        second_angle = second * math.pi / 30

        # Main hand tips
        hour_x = x0 + 290 * math.sin(hour_angle)
        hour_y = y0 - 290 * math.cos(hour_angle)
        minute_x = x0 + 498 * math.sin(minute_angle)
        minute_y = y0 - 498 * math.cos(minute_angle)
        second_x = x0 + 517 * math.sin(second_angle)
        second_y = y0 - 517 * math.cos(second_angle)

        # Hand tails
        hour_tail_x = x0 - 100 * math.sin(hour_angle)
        hour_tail_y = y0 + 100 * math.cos(hour_angle)
        minute_tail_x = x0 - 130 * math.sin(minute_angle)
        minute_tail_y = y0 + 130 * math.cos(minute_angle)
        second_tail_x = x0 - 160 * math.sin(second_angle)
        second_tail_y = y0 + 160 * math.cos(second_angle)

        # Hour hand
        self.canvas.create_line(hour_tail_x, hour_tail_y, hour_x, hour_y, width=39, fill='black', tags='hands')

        # Minute hand
        self.canvas.create_line(minute_tail_x, minute_tail_y, minute_x, minute_y, width=25, fill='black', tags='hands')

        # Second hand
        self.canvas.create_line(second_tail_x, second_tail_y, second_x, second_y, width=8, fill='black', tags='hands')
        self.canvas.create_oval(second_x-2, second_y-2, second_x+2, second_y+2, fill='black', tags='hands')

    def update_hands(self):
        now = time.localtime()
        self.canvas.delete('hands')
        self.draw_hands(now.tm_hour, now.tm_min, now.tm_sec)

        # Keep center dot above all hands (cheap operation)
        self.canvas.tag_raise('center_dot')

        self.root.after(1000, self.update_hands)

    def run(self):
        self.draw_static_layers()
        self.draw_center_dot()
        self.update_hands()
        self.root.mainloop()

if __name__ == '__main__':
    clock = Clock()
    clock.run()