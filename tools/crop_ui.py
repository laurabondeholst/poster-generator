"""
Creates GUI which allows the user to crop the correct person
Not used in main script anymore, but might be useful if you wish to use UI instead of face rec

"""


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageOps
import matplotlib.pyplot as plt
import numpy as np

class CropUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Click and drag the bounding box surrounding the person in focus")

        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.update()

        # Load the image
        # self.save_path = path
        self.image = None
        self.photo = None  # Store the PhotoImage object
        self.cropped_image = None

        # Store the cropping coordinates
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.line_coords = []  # List to store the coordinates of the drawn line

        # Create a drawing object for freehand drawing
        self.drawing = False
        self.draw = None

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)



    def load_image(self, img):
        self.image = img
        self.img_width, self.img_height = self.image.size
        # if self.img_height > 1000 or self.img_width > 1000:
        #     self.scaling = 1000/self.img_height
        #     self.canvas.config(width=int(self.scaling*self.img_width), height=1000)
        #     s
        # else:     
        #     self.scaling = 1
        self.canvas.config(width=self.img_width, height=self.img_height)
        
        

        # Create a PhotoImage object from the resized image
        self.photo = ImageTk.PhotoImage(self.image)

        # Display the resized image on the canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        self.canvas.update()

    def on_mouse_press(self, event):
        self.min_x = event.x  
        self.max_x = event.x
        self.min_y = event.y  
        self.max_y = event.y  
        # Start drawing when the mouse is pressed
        self.drawing = True
        self.draw = ImageDraw.Draw(self.image)
        self.line_coords = []  # Reset the list of line coordinates

    def on_mouse_drag(self, event):
        if self.drawing:
            cur_x = event.x  # Store the canvas x-coordinate directly
            cur_y = event.y  # Store the canvas y-coordinate directly

            if cur_x < self.min_x:
                self.min_x = cur_x
            elif cur_x > self.max_x: 
                self.max_x = cur_x

            if cur_y < self.min_y:
                self.min_y = cur_y
            elif cur_y > self.max_y: 
                self.max_y = cur_y


            # Draw a line from the previous point to the current point
            # self.draw.line([self.start_x, self.start_y, cur_x, cur_y], fill="white", width=1)
            # self.start_x = cur_x
            # self.start_y = cur_y

            # # Append the current coordinates to the list of line coordinates
            # self.line_coords.append((cur_x, cur_y))

    def on_mouse_release(self, event):
        if self.drawing:
            # Stop drawing when the mouse is released
            self.drawing = False

            if self.min_x < 0: 
                self.min_x
            if self.min_y < 0: 
                self.min_y = 0
            if self.max_x > self.img_width:  
                self.max_x = self.img_width
            if self.max_y > self.img_height: 
                self.max_y = self.img_height

            box = (self.min_x, self.min_y, self.max_x, self.max_y)
            self.cropped_image = self.image.crop(box)
            self.root.destroy()


    def update_display(self):
        if self.image:
            # Display the modified image
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

if __name__ == "__main__":
    root = tk.Tk()
    app = CropUI(root)
    root.mainloop()

    #add image directory
    image = "final_image.png"
    output_path = 'output.png' # output image path

    if image is None:
        print("Error: Could not load the image.")
    else:

        output = Image.open(image) # load image


        # output = remove(input) # remove background
        
        # Crop the image to remove transparent space
        # bbox = output.getbbox()
        # cropped_output = output.crop(bbox)

        output.save(output_path) # save image

        plt.figure(figsize=(8,4))
        plt.imshow(output)
        plt.axis('off')
