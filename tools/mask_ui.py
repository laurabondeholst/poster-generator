"""
Creates GUI for drawing mask, which is what determines what part of the image should be inpainted
"""


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageOps
import matplotlib.pyplot as plt

class MaskUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Click and drag the area inpaiting algorithm should focus on")

        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.update()

        # Load the image
        # self.save_path = path
        self.image = None
        self.photo = None  # Store the PhotoImage object
        self.mask = None
        # self.load_image_button = tk.Button(root, text="Load Image", command=self.load_image)
        # self.load_image_button.pack()

        # Store the cropping coordinates
        self.start_x = None
        self.start_y = None
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

        self.canvas.config(width=self.img_width, height=self.img_height)
        

        # Create a PhotoImage object from the resized image
        self.photo = ImageTk.PhotoImage(self.image)

        # Display the resized image on the canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        self.canvas.update()

    def on_mouse_press(self, event):
        self.start_x = event.x  # Store the canvas x-coordinate directly
        self.start_y = event.y  # Store the canvas y-coordinate directly
        # Start drawing when the mouse is pressed
        self.drawing = True
        self.draw = ImageDraw.Draw(self.image)
        self.line_coords = []  # Reset the list of line coordinates

    def on_mouse_drag(self, event):
        if self.drawing:
            cur_x = event.x  # Store the canvas x-coordinate directly
            cur_y = event.y  # Store the canvas y-coordinate directly
            # Draw a line from the previous point to the current point
            self.draw.line([self.start_x, self.start_y, cur_x, cur_y], fill="white", width=1)
            self.start_x = cur_x
            self.start_y = cur_y

            # Append the current coordinates to the list of line coordinates
            self.line_coords.append((cur_x, cur_y))

    def on_mouse_release(self, event):
        if self.drawing:
            # Stop drawing when the mouse is released
            self.drawing = False

            # Create a black background image
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            black_bg = Image.new("RGB", (canvas_width, canvas_height), "white")

            # Calculate the coordinates of the ROI within the canvas
            x, y, width, height = self.canvas.bbox("all")

            # Create a mask for the region of interest based on the drawn line
            mask = Image.new("L", black_bg.size, 0)
            draw = ImageDraw.Draw(mask)
            # Adjust the line coordinates based on the image's position within the canvas
            adjusted_line_coords = [(x0 - x, y0 - y) for x0, y0 in self.line_coords]
            draw.polygon(adjusted_line_coords, outline=255, fill=255)

            # Resize the mask to match the size of the image
            mask = mask.resize((self.img_width, self.img_height), Image.LANCZOS)
            black_bg = black_bg.resize((self.img_width, self.img_height), Image.LANCZOS)

            # Paste the cropped region onto the black background at the correct position
            # black_bg.paste(self.image, (x, y), mask=mask) # copy image to mask
            black_bg.paste(0, (x, y), mask=mask) # set values to 0 in mask


            # Display the modified image with the freehand-drawn ROI
            self.mask = ImageOps.invert(black_bg)
            self.root.destroy()


    def update_display(self):
        if self.image:
            # Display the modified image
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

if __name__ == "__main__":
    root = tk.Tk()
    app = MaskUI(root)
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
