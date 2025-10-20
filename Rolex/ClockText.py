#!/usr/bin/env python

import tkinter as tk
import time
import math
import sys
import os

class Clock:
    def __init__(self, message="Default Message"):
        self.message = message
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack(fill='both', expand=True)

        # 🔧 Absolute path for background
        image_path = os.path.join("/home/pi/Rolex/png", "Plain.png")
        self.background_image = tk.PhotoImage(file=image_path)

        self.draw_static_layers()

    def draw_static_layers(self):
        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        self.display_message()

    def update_main_hands(self):
        now = time.localtime()
        self.canvas.delete('main_hands')
        self.draw_hands(now.tm_hour, now.tm_min, now.tm_sec)
        self.root.after(1000, self.update_main_hands)

    def update_second_hand(self):
        now = time.localtime()
        self.canvas.delete('second_hand')
        self.draw_second_hand(now.tm_sec)
        self.root.after(50, self.update_second_hand)

    def draw_hands(self, hour, minute, second):
        x0 = 992
        y0 = 635
        hour_angle = (hour % 12 + minute / 60) * math.pi / 6
        minute_angle = minute * math.pi / 30

        hour_x = x0 + 290 * math.sin(hour_angle)
        hour_y = y0 - 290 * math.cos(hour_angle)
        minute_x = x0 + 498 * math.sin(minute_angle)
        minute_y = y0 - 498 * math.cos(minute_angle)

        hour_tail_x = x0 - 100 * math.sin(hour_angle)
        hour_tail_y = y0 + 100 * math.cos(hour_angle)
        minute_tail_x = x0 - 130 * math.sin(minute_angle)
        minute_tail_y = y0 + 130 * math.cos(minute_angle)

        self.canvas.create_line(hour_tail_x, hour_tail_y, hour_x, hour_y, width=39, fill='black', tags='main_hands')
        self.canvas.create_oval(x0-44, y0-44, x0+44, y0+44, fill='white', tags='main_hands')

        self.canvas.create_line(minute_tail_x, minute_tail_y, minute_x, minute_y, width=25, fill='black', tags='main_hands')
        self.canvas.create_oval(minute_x-5, minute_y-5, minute_x+5, minute_y+5, fill='black', tags='main_hands')
        self.canvas.create_oval(x0-38, y0-38, x0+38, y0+38, fill='black', tags='main_hands')

    def draw_second_hand(self, second):
        x0 = 992
        y0 = 635
        second_angle = second * math.pi / 30

        second_x = x0 + 517 * math.sin(second_angle)
        second_y = y0 - 517 * math.cos(second_angle)
        second_tail_x = x0 - 160 * math.sin(second_angle)
        second_tail_y = y0 + 160 * math.cos(second_angle)

        self.canvas.create_line(second_tail_x, second_tail_y, second_x, second_y, width=8, fill='black', tags='second_hand')
        self.canvas.create_oval(second_x-2, second_y-2, second_x+2, second_y+2, fill='black', tags='second_hand')
        self.canvas.create_oval(x0-34, y0-34, x0+34, y0+34, fill='white', tags='second_hand')

    def display_message(self):
        x = 998
        y = 805
        self.canvas.create_text(x, y, text=self.message, font=('Optima', 26, 'bold italic'), fill='black', justify='center')

    def run(self):
        self.update_main_hands()
        self.update_second_hand()
        self.root.mainloop()

if __name__ == '__main__':
    message = sys.argv[1] if len(sys.argv) > 1 else "Default Message"
    clock = Clock(message=message)
    clock.run()