import tkinter as tk
from GUI import BMP  # Import the BMP class from GUI.py

if __name__ == "__main__":
    root = tk.Tk()
    app = BMP(root)
    root.mainloop()