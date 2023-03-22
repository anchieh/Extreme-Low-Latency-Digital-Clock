import os
import time
import datetime
import tkinter as tk
from PIL import ImageTk, Image

class DigitalClock:
    def __init__(self, master):
        self.master = master
        self.time_images = []
        self.canvas = tk.Canvas(self.master, width=900, height=150, bg="black")
        self.canvas.pack()

        # 載入數字和符號的圖片
        for i in range(10):
            img = Image.open(str(i) + ".jpg")
            if max(img.size) > 50:
                img.thumbnail((50, 50), Image.ANTIALIAS)
            self.time_images.append(ImageTk.PhotoImage(img))

        comma_img = Image.open("comma.jpg")
        if max(comma_img.size) > 50:
            comma_img.thumbnail((50, 50), Image.ANTIALIAS)
        self.time_images.append(ImageTk.PhotoImage(comma_img))

        semicolon_img = Image.open("semicolon.jpg")
        if max(semicolon_img.size) > 50:
            semicolon_img.thumbnail((50, 50), Image.ANTIALIAS)
        self.time_images.append(ImageTk.PhotoImage(semicolon_img))

        self.update_clock()

    def update_clock(self):
        start_time = time.perf_counter()
        current_time = datetime.datetime.now().strftime('%H:%M:%S.%f')#[:-3]

        # 在畫布上顯示時間
        self.canvas.delete("all")
        x = (900 - 55*len(current_time)) // 2
        y = 10
        for i, ch in enumerate(current_time):
            if ch == ":":
                img = self.time_images[10]
            elif ch == ".":
                img = self.time_images[11]
            else:
                img = self.time_images[int(ch)]
            self.canvas.create_image(x, y, anchor=tk.NW, image=img)
            x += img.width() + 5

        end_time = time.perf_counter()
        update_time = round((end_time - start_time) * 1000000)
        update_time_str = f"{update_time:06}"
        img_list = []
        for i, ch in enumerate(update_time_str):
            img = self.time_images[int(ch)]
            img_list.append(img)

        x = (800 - 55*len(update_time_str)) // 2
        y = 80
        for i, img in enumerate(img_list):
            self.canvas.create_image(x, y, anchor=tk.NW, image=img)
            x += img.width() + 5

        self.master.after(1, self.update_clock)

def main():
    root = tk.Tk()
    clock = DigitalClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()
