# Import necessary libraries 
import tkinter as tk 
import tkinter.filedialog as fd
import tkinter.font as font
from  PIL import Image, ImageTk
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
            
            # load the image
            self.load_image(file_path)

            # Parse the BMP file 
            self.metadata = parser.bmp_parser(file_path)
            
            # Display the metadata as a GUI 
            # self.display_metadata()


    # Create a function to help load and display the image
    def load_image( self,file_path):

        # Open the image via the file path and resize to 300x300 pixels
        self.image = Image.open(file_path)
        self.image = self.image.resize((300, 300))  
        
        # Convert for tkinter and update the label to show the image
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_viewer.config(image=self.tk_image, text="")  

    # Create a constructor, __init__
    def __init__(self, root):

        # Create a window by initializing to root and create the title 
        self.root = root
        self.root.title("BMP Image Viewer and Editor")

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

        # Create RGB buttons

        # Create sliders for brightness 

        # Create sliders for scale 
    
if __name__ == "__main__":
    root = tk.Tk()
    app = BMP(root)
    root.mainloop()