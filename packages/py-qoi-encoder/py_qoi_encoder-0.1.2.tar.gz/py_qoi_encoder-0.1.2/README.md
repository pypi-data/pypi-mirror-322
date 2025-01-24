# QOI Library
A Python library for encoding and decoding QOI (Quite OK Image) files.
QOI is a lossless image compression format known for its simplicity and speed.

## Features
Encode: Convert pixel data (RGB or RGBA) to .qoi format.
Decode: Convert .qoi files back to raw pixel data.
Convenient load/save functions for file I/O.
Pure Python implementation—easy to read or modify.

## What is QOI?
QOI (Quite OK Image) is a fast, lossless image format originally developed by Dominic Szablewski (phoboslab). It uses a simple run-length and index-based compression method and requires no external dependencies to encode/decode. Despite being relatively new, QOI has gained popularity due to its ease of implementation and often excellent speed.

Learn more about QOI in the official QOI repository.

## Installation
You can install this library from PyPI:

pip install py-qoi-encoder

## Quick Usage
Below is a minimal example using Pillow to handle PNG images and converting them to .qoi:

    from PIL import Image
    import py-qoi-encoder

    # Load an image (PNG, JPG, etc.) via Pillow
    img = Image.open("example.png").convert("RGBA")
    width, height = img.size
    pixels = list(img.getdata())  # RGBA tuples

    # Encode pixel data to QOI bytes, then write to file
    qoi_data = my_qoi_lib.encode(pixels, width, height, channels=4, colorspace=0)
    with open("output.qoi", "wb") as f:
        f.write(qoi_data)

    # Decode the QOI file back to raw pixel data
    w, h, c, decoded_pixels = my_qoi_lib.load_qoi("output.qoi")

    # Convert the decoded pixels back to a Pillow image and save
    decoded_img = Image.new("RGBA", (w, h))
    decoded_img.putdata(decoded_pixels)
    decoded_img.save("decoded.png")

## Example
For more example check out the examples folder

## Requirements
Python 3.7+
(Optional) Pillow for loading/saving PNG images in the examples.