import pytest
import py_qoi as qoi

def test_encode_decode_small_image():
    # Create a small 2x2 RGBA image in memory
    width, height = 2, 2
    pixels = [
        (255, 0,   0,   255),  # Red
        (0,   255, 0,   255),  # Green
        (0,   0,   255, 255),  # Blue
        (255, 255, 255, 255)   # White
    ]

    # Encode
    encoded_data = qoi.encode(pixels, width, height, channels=4, colorspace=0)
    
    # Decode
    w, h, c, decoded_pixels = qoi.decode(encoded_data)
    
    assert w == width
    assert h == height
    assert c == 4
    assert decoded_pixels == pixels

def test_encode_decode_rgb():
    # Similar test but for 3-channel (RGB) data
    width, height = 2, 1
    pixels = [
        (10, 20, 30),  # single row
        (40, 50, 60)
    ]

    encoded_data = qoi.encode(pixels, width, height, channels=3, colorspace=0)
    w, h, c, decoded_pixels = qoi.decode(encoded_data)

    # Rebuild 3->4 channel expansions by decode => RGBA
    # We'll assume decode always returns RGBA or you can interpret c as 3
    # if you want to handle that in your library.
    assert w == width
    assert h == height
    assert c == 3 or c == 4  # depends on how you handle it
    # If the decode returns RGBA, check only the RGB portion:
    decoded_rgb = [(px[0], px[1], px[2]) for px in decoded_pixels]
    assert decoded_rgb == pixels