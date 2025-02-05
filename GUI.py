# Import necessary libraries 
import tkinter as tk 
import tkinter.filedialog as fd

# Create a browse file function to open the files
def browse_file():
    file_path = fd.askopenfilename()
    file_path_entry.delete(0, tk.END) # delete any current text in Entry
    file_path_entry.insert(0, file_path) # insert the path to the file in Entry 
    
root = tk.Tk()

# Create a label for the GUI to show the user what this program is for 
tk.Label(root, text="BMP Image Viewer and Editor:").grid()

# Create a file entry 
file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row = 0, column = 1)

# Create a browse button to find the desired file 
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2)

root.mainloop()
