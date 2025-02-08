# Import necessary libraries 
import tkinter as tk 
import tkinter.filedialog as fd
import tkinter.font as font
from  PIL import Image, ImageTk, ImageEnhance
import parserBMP as parser

# Create a class BMP 
class BMP: 

    # Create a function to browse the file 
    def browse_file(self):

        # Open the file explorer and get the file path, restrict it so that only BMP files are selected 
        file_path = fd.askopenfilename(filetypes=[("BMP files", "*.bmp")])

        # If a BMP file is selected, delete and existing characters into the file entry and inser the file path obtained
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
            
            # Keep an original copy of the image and load the image 
            self.original_image = Image.open(file_path).convert("RGB")
            self.image = self.original_image.copy()

            self.image = self.image.resize((300, 300))  
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.image_viewer.config(image=self.tk_image)

            # Parse the BMP file 
            self.metadata = parser.bmp_parser(file_path)
            
            # Display the metadata as a GUI 
            self.display_metadata()

    # Create a function to help load and display the image
    def load_image( self,file_path):

        # Open the image via the file path and resize to 300x300 pixels
        self.image = Image.open(file_path)
        self.image = self.image.resize((300, 300)).convert("RGB")  
        
        # Convert for tkinter and update the label to show the image
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_viewer.config(image=self.tk_image)  

    # Create a function to help display the metadata in the GUI 
    def display_metadata(self):

        # Use hasattr toq check if the metadata exists and if it does, display it in the GUI
        if hasattr(self, 'metadata'):

            # For each metadata key and value, display it in the GUI
            for key, value in self.metadata.items():
                if key in self.metadata_gui:
                    self.metadata_gui[key].config(text=f"{key}: {value}")

    # Create a function to toggle the RGB values 
    def rgb_changer (self):

        # Check to see if the image has loaded. 
        if self.image is None: 
            return 
            
        # Get the width and height of the original image
        width, height = self.image.size

        # Create a new image with the same width and height as the original image
        new_image = Image.new("RGB", (width, height))

        # Loop through all the pixels in the original image
        for y in range(height):
            for x in range(width):
                r, g, b = self.image.getpixel((x, y))

                # Check to see if there is red in the pixel and if the red button is toggled
                if not self.red_button.get():
                    r = 0

                # Check to see if there is green in the pixel and if the green button is toggled
                if not self.green_button.get():
                    g = 0

                # Check to see if there is blue in the pixel and if the blue button is toggled 
                if not self.blue_button.get():
                    b = 0

                # Put the acquired pixels in the new image 
                new_image.putpixel((x, y), (r, g, b))

        # Conver the new image into tkinter fornat and update it to the GUI 
        self.tk_image = ImageTk.PhotoImage(new_image)
        self.image_viewer.config(image=self.tk_image)

        self.root.update()

    def change_brightness(self, value):
        if self.original_image is None:
            return  

        brightness_factor = int(value) / 100  # Convert slider value (0-100) to a multiplier
        enhancer = ImageEnhance.Brightness(self.original_image)  # Create a brightness enhancer
        brightened_image = enhancer.enhance(brightness_factor)  # Adjust brightness

        # Ensure the image maintains the correct size
        brightened_image = brightened_image.resize(self.image.size)

        # Update the GUI image
        self.tk_image = ImageTk.PhotoImage(brightened_image)
        self.image_viewer.config(image=self.tk_image)

    # Create a constructor, __init__
    def __init__(self, root):

        # Create a window by initializing to root and create the title 
        self.root = root
        self.root.title("BMP Image Viewer and Editor")

        self.image = None
        self.original_image = None

        # Create a title for the GUI by createing a font for the title and adding it to the to center of the GUI 
        title_font = font.Font(family = "Times New Roman", size = 14, weight = "bold") 
        tk.Label(root, text = "BMP Image Viewer and Editor:", font = title_font).grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 5)

        # Create a file entry so that the user can choose thier file or input it manually 
        # Use sticky = ew to expand the entry when the window is resized
        self.file_path_entry = tk.Entry(root, width = 50)
        self.file_path_entry.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "ew")

        # Create a browse button so that the user can open file explorer on their computer 
        tk.Button(root, text = "Browse", command = self.browse_file).grid(row =1, column = 1, padx = 5, pady = 5)

        # Create an image viewer so that the user can see the image they have selected
        self.image_viewer = tk.Label(root, text = "Image Viewer",bg = "lightgrey")
        self.image_viewer.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 5)

        # Create each value in the metadata dictionary into a label 
        self.metadata_gui = {
            "Signature": tk.Label(root, text = "Signature: "),
            "File Size": tk.Label(root, text = "File Size: "),
            "Width": tk.Label(root, text = "Width: "),
            "Height": tk.Label(root, text = "Height: "),
            "Bits per Pixel": tk.Label(root, text = "Bits per Pixel: ")
        }

        # Display each label and its corresponding value in the GUI
        row = 3
        for key, label in self.metadata_gui.items():
            label.grid(row = row, column = 0, sticky = "w", padx = 10)
            row = row + 1

       # Create RGB toggle buttons and initialize to true. Once the button is pressed, the rgb_changer function will be called
        self.red_button = tk.BooleanVar(value=True)
        self.green_button = tk.BooleanVar(value=True)
        self.blue_button = tk.BooleanVar(value=True)

        # Create a Checkbutton for each colour so that the image can revert to the original state if needed
        tk.Checkbutton(root, text="R", bg = "red", variable=self.red_button, command=self.rgb_changer).grid(row=3, column=1)
        tk.Checkbutton(root, text="G", bg = "green", variable=self.green_button, command=self.rgb_changer).grid(row=4, column=1)
        tk.Checkbutton(root, text="B", bg = "#1247D3", variable=self.blue_button, command=self.rgb_changer).grid(row=5, column=1)

        # Create sliders for brightness 
        self.brightness = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Brightness", command=self.change_brightness)
        self.brightness.grid(row = 6, column = 1, columnspan = 2, pady = 5)

        # Set the default brightness to 100
        self.brightness.set(100)

        # Create sliders for scale 
    
if __name__ == "__main__":
    root = tk.Tk()
    app = BMP(root)
    root.mainloop()