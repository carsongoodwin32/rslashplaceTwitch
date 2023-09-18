from PIL import Image, ImageDraw
import random
import time
import csv

# Initialize the image as a white canvas
width, height = 100, 100
background_color = (255, 255, 255)  # White
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

# Initialize the pixel data array
pixel_data = []

def update_image_with_pixel(x, y, r, g, b):
    # Update the specified pixel with the RGB values
    draw.point((x, y), fill=(r, g, b))

def load_csv_data():
    # Load pixel data from the CSV file
    with open("commandstream.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            x, y, r, g, b = map(int, row)
            pixel_data.append((x, y, r, g, b))
            update_image_with_pixel(x, y, r, g, b)

# Load initial pixel data from the CSV file
load_csv_data()

while True:
    # Check for new data in the CSV file
    image.save("your_image.png")
    with open("commandstream.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        new_rows = list(csv_reader)

    # Append new data to the pixel_data array
    if len(new_rows) > len(pixel_data):
        for row in new_rows[len(pixel_data):]:
            x, y, r, g, b = map(int, row)
            pixel_data.append((x, y, r, g, b))
            update_image_with_pixel(x, y, r, g, b)
            image.save("your_image.png")
            time.sleep(1)
            #time.sleep(1 / 10)
            # Save the updated image to your_image.png
    time.sleep(1/20)
    # Wait for a moment to control the update rate # Adjust as needed for your desired frame rate
