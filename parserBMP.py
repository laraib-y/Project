# Import necessary libraries 
import tkinter as tk 
import tkinter.filedialog as fd
import tkinter.font as font

def bmp_parser(self, file_path):
    # Read the BMP file into an array of bytes
    with open(file_path, "rb") as file:
        bmp = file.read()

    # Obtain metadata from the BMP file: 
    # 1.File signature to confirm the file selected is a BMP file 
    signature = bmp[:2].decode("utf-8")

    # 2. File size (4 bytes and in between 2-6 bytes)
    file_size = int.from_bytes(bmp[2:6], "little")
    
    # 3. Get width of the image (4 bytes and in between 18-22 bytes)
    width = int.from_bytes(bmp[18:22], "little")

    # 4. Get the height of the image (4 bytes and in between 22 - 26 bytes)
    height = int.from_bytes(bmp[22:26], "little")   

    # 5. Get the number of bits per pixel (2 bytes and in between 28-30 bytes)  
    bits_per_pixel = int.from_bytes(bmp[28:30], "little")

    # Create a dictionary for the meta data and return 
    return {
        "Signature": signature,
        "File Size": file_size,
        "Width": width,
        "Height": height,
        "Bits per Pixel": bits_per_pixel
    } 