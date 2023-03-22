import datetime
import pytz
from tkinter import *
from PIL import ImageTk, ImageDraw, ImageFont, Image
import subprocess

# Set timezone
tz = pytz.timezone('Asia/Taipei')

# Sync time with NTP server
subprocess.call(['sudo', 'systemctl', 'stop', 'ntp.service'])
subprocess.call(['sudo', 'ntpd', '-gq'])
subprocess.call(['sudo', 'systemctl', 'start', 'ntp.service'])

# Set up the GUI
root = Tk()
root.title("My Clock")
root.geometry('1000x150')
root.resizable(False, False)

# Set font
font = ('FreeSansBold', 80)

# Set background color
background = 'black'

# Set font color
font_color = 'gray'

# Create the time label
time_label = Label(root, font=font, bg=background, fg=font_color, width=10)
time_label.pack(fill=BOTH, expand=1)

# Create a list to store PhotoImage objects
images = []

# Initialize a variable to store the previous timestamp
previous_timestamp = datetime.datetime.now(tz)

# Create a function to update the clock
def update_clock():
    global previous_timestamp

    # Get current time in GMT+8
    now = datetime.datetime.now(tz)
    elapsed_time = now - previous_timestamp
    formatted_now = now.strftime('%H:%M:%S:%f')[:-3]
    elapsed_microseconds = elapsed_time.microseconds

    # Update the previous timestamp
    previous_timestamp = now

    # Combine the current time and elapsed microseconds
    time_string = f"{formatted_now}.{elapsed_microseconds:06d}"

    # Create an image of the time label
    width, height = time_label.winfo_width(), time_label.winfo_height()
    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("FreeSansBold.ttf", 80)
    text_width, text_height = draw.textsize(time_string, font=font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), time_string, font=font, fill=font_color)
    photo = ImageTk.PhotoImage(image)
    time_label.config(image=photo, text="")
    time_label.image = photo

    # Add the image to the list
    images.append(photo)

    # Remove old images from the list
    if len(images) > 10:
        old_photo = images.pop(0)
        old_photo.__del__()

    # Schedule the next update
    root.after(1, update_clock)

# Schedule the first update
root.after(1, update_clock)

# Start the main event loop
root.mainloop()
