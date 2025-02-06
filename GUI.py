# Import necessary libraries 
import tkinter as tk 
import tkinter.filedialog as fd
import tkinter.font as font

# Create a class BMP 
class BMP: 

    # Create a constructor, __init__
    def __init__(self, file_path):

        # Create a window by initializing to root and create the title 
        self.root = root
        self.root.title("BMP Image Viewer and Editor")

"""""
# Create a browse file function to open the files
def browse_file():
    file_path = fd.askopenfilename()
    file_path_entry.delete(0, tk.END) # delete any current text in Entry
    file_path_entry.insert(0, file_path) # insert the path to the file in Entry 
    
root = tk.Tk() # Create a root window
root.title("BMP Image Viewer and Editor") # Title of the GUI

# Add padding to the grid
root.columnconfigure(0, weight=3)  # Entry takes more space
root.columnconfigure(1, weight=1)  # Button takes less space
root.rowconfigure(1, weight=1)  # Row expands when resized

title_font = font.Font(family = "Times New Roman", size = 14, weight = "bold") # Set the font size of the GUI

# Create a label for the GUI to show the user what this program is for 
tk.Label(root, text="BMP Image Viewer and Editor:", font = title_font).grid(row = 0, column = 0, columnspan=2, pady = 10)    

# Create a file entry 
file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "ew")

# Create a browse button to find the desired file 
tk.Button(root, text="Browse", command=browse_file).grid(row=1, column=1, padx = 5, pady = 5)

"""
if __name__ == "__main__":
    root = tk.Tk()
    app = BMP(root)
    root.mainloop()