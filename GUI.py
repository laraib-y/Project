# import necessary libraries 
import tkinter as tk 
import tkinter.filedialog as fd
import tkinter.font as font
from  PIL import Image, ImageTk, ImageEnhance
import parserBMP as parser

# create a class BMP for all the required functions 
class BMP: 

    # crate a function called "browse_file" to open the file explorer and get the file path
    def browse_file(self):

        # restrict files to only .bmp (only bmp files will show in file explorer)
        file_path = fd.askopenfilename(filetypes=[("BMP files", "*.bmp")])

        # if a BMP file is selected, delete and existing characters into the file entry and inser the file path obtained
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
            
            # open the bmp image and convert to RGB format and create a copy of the original image (may be needed later)
            self.original_image = Image.open(file_path).convert("RGB")
            self.image = self.original_image.copy()

            # resize the image to 300 pixels and convert to tkinter format 
            self.image = self.image.resize((300, 300))  
            self.tk_image = ImageTk.PhotoImage(self.image)

            # update the image viewer to show the image 
            self.image_viewer.config(image=self.tk_image)

            # parse the BMP file to return the appropriate metadata
            self.metadata = parser.bmp_parser(file_path)
            
            # display the metadata in the GUI
            self.display_metadata()

    # create a function to display the metadata aquired in the GUI 
    def display_metadata(self):

        # use hasattr to check if the metadata exists. if it does, then display it in the GUI 
        if hasattr(self, 'metadata'):

            # for  each metadata key and value, display it in the GUI
            for key, value in self.metadata.items():
                if key in self.metadata_gui:
                    self.metadata_gui[key].config(text=f"{key}: {value}")

    # create a function to remove / add RGB values to the image when the button is toggled 
    def rgb_changer (self):

        # check to see if the image has been loaded, if not, return to exit the functioon
        if self.image is None: 
            return 
            
        # get the width and height of the original image 
        width, height = self.image.size

        # create a new image that has rgb format and the same width and height as the original image 
        new_image = Image.new("RGB", (width, height))

        # loop through all the pixels in the image and get their RGB 
        for y in range(height):
            for x in range(width):
                r, g, b = self.image.getpixel((x, y))

                # check to see if there is red in the pixel and if the red button is toggled
                # if toggled, set r = 0 (removes red)
                if not self.red_button.get():
                    r = 0 

                # check to see if there is green in the pixel and if the green button is toggled
                # if toggled, set g = 0 (removes green)
                if not self.green_button.get():
                    g = 0

                # check to see if there is blue in the pixel and if the blue button is toggled 
                # if toggled, set b = 0 (removes blue)
                if not self.blue_button.get():
                    b = 0

                # put the acrquired pixels in the new image 
                new_image.putpixel((x, y), (r, g, b))

        # convert the new image into tkinter fornat and update it to the GUI 
        self.tk_image = ImageTk.PhotoImage(new_image)
        self.image_viewer.config(image=self.tk_image)

        # update the GUI 
        self.root.update()

    # create a function to change the brightness of the image
    def change_brightness(self, value):

        # check to see if the image has been loaded, if not, return to exit the function
        if self.original_image is None:
            return  

        # convert brightness to a scaling factor between 0 and 1 (easier handling)
        brightness_factor = int(value) / 100

        # use ImageEhance.Brightness to change the brighness of the image
        enhance_image = ImageEnhance.Brightness(self.original_image)
        brightened_image = enhance_image.enhance(brightness_factor)

        # resize the image to match the size of the original image 
        brightened_image = brightened_image.resize(self.image.size)

        # update the GUI with the new image
        self.tk_image = ImageTk.PhotoImage(brightened_image)
        self.image_viewer.config(image=self.tk_image)

    # create a function to help scale the function 
    def scale_image(self, value):

        # check to see if the image has been loaded, if not, return to exit the function
        if self.original_image is None:
            return
        
        # convert the scale factor to a number between 0 and 1
        scaling = int(value) / 100
        if scaling == 0:
            return  
        
        # update the size (height and width) of the image to the new size 
        new_height = int(self.original_image.height * scaling)
        new_width = int(self.original_image.width * scaling)
        new_size = new_width, new_height

        # resize the image to the new size and update the GUI 
        scaled_image = self.original_image.resize(new_size)
        self.tk_image = ImageTk.PhotoImage(scaled_image)
        self.image_viewer.config(image=self.tk_image)
            

    # create a constructor, __init__
    def __init__(self, root):

        # create a window by initializing to root and create the title 
        self.root = root
        self.root.title("BMP Image Viewer and Editor")

        #define image and original image as None, will be defined later in functions
        self.image = None
        self.original_image = None

        # create a title for the GUI by createing a font for the title and adding it to the to center of the GUI 
        title_font = font.Font(family = "Times New Roman", size = 14, weight = "bold") 
        tk.Label(root, text = "BMP Image Viewer and Editor:", font = title_font).grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 5)

        # create a file entry so that the user can choose thier file or input it manually 
        # Use sticky = ew to expand the entry when the window is resized
        self.file_path_entry = tk.Entry(root, width = 50)
        self.file_path_entry.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "ew")

        # create a browse button so that the user can open file explorer on their computer 
        tk.Button(root, text = "Browse", command = self.browse_file).grid(row =1, column = 1, padx = 5, pady = 5, sticky = "ew")

        # create an image viewer so that the user can see the image they have selected
        self.image_viewer = tk.Label(root, text = "Image Viewer",bg = "lightgrey")
        self.image_viewer.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 5, sticky = "nsew")

        # create each value in the metadata dictionary into a label 
        self.metadata_gui = {
            "Signature": tk.Label(root, text = "Signature: "),
            "File Size": tk.Label(root, text = "File Size: "),
            "Width": tk.Label(root, text = "Width: "),
            "Height": tk.Label(root, text = "Height: "),
            "Bits per Pixel": tk.Label(root, text = "Bits Per Pixel: ")
        }

        # display each label and its corresponding value in the GUI
        row = 3
        for key, label in self.metadata_gui.items():
            label.grid(row = row, column = 0, sticky = "w", padx = 10)
            row = row + 1

       # create RGB toggle buttons and initialize to true. Once the button is pressed, the rgb_changer function will be called
        self.red_button = tk.BooleanVar(value=True)
        self.green_button = tk.BooleanVar(value=True)
        self.blue_button = tk.BooleanVar(value=True)

        # create a Checkbutton for each colour so that the image can revert to the original state if needed
        tk.Checkbutton(root, text="R", bg = "red", variable=self.red_button, command=self.rgb_changer).grid(row=3, column=1)
        tk.Checkbutton(root, text="G", bg = "green", variable=self.green_button, command=self.rgb_changer).grid(row=4, column=1)
        tk.Checkbutton(root, text="B", bg = "#1247D3", variable=self.blue_button, command=self.rgb_changer).grid(row=5, column=1)

        # create sliders for brightness 
        self.brightness = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Brightness", command=self.change_brightness)
        self.brightness.grid(row = 6, column = 1, columnspan = 2, pady = 5)

        # set the default brightness to 100
        self.brightness.set(100)

        # create sliders for scale 
        self.scale_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Scale (%)", command=self.scale_image)
        self.scale_slider.grid(row=7, column=1, columnspan=2, pady=5)

       # set default slider to 100 
        self.scale_slider.set(100)
