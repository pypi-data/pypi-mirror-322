import struct

QOI_MAGIC = b'qoif'

QOI_OP_INDEX = 0x00
QOI_OP_DIFF  = 0x40
QOI_OP_LUMA  = 0x80
QOI_OP_RUN   = 0xC0
QOI_OP_RGB   = 0xFE
QOI_OP_RGBA  = 0xFF

END_MARKER = b'\x00\x00\x00\x00\x00\x00\x00\x01'
INDEX_SIZE = 64

def _pixel_hash(r, g, b, a):
    
    return (r * 3 + g * 5 + b * 7 + a * 11) % INDEX_SIZE

def encode(pixels, width, height, channel=4, colorspace=0):

    if channel not in (3,4):
        raise ValueError("channels must be 3 (RGB) or 4 (RGBA)")
    
    header = (
        QOI_MAGIC +
        struct.pack(">I", width) +
        struct.pack(">I", height) +
        struct.pack("B", channel) +
        struct.pack("B", colorspace) 
    )

    # Starting index for previosly seen pixels
    index = [(0, 0, 0, 255)] * INDEX_SIZE
    index = list(index)

    # Start encoding
    encoded_bytes = bytearray()
    run = 0
    prev_pixel = (0, 0, 0, 255) # The default starting pixel

    for i, pix in enumerate(pixels):
        if channel == 3:
            r, g, b = pix
            a = 255
        else:
            r, g, b, a = pix

        if pix == prev_pixel:
            run += 1
            if run == 62 or i == len(pixels) - 1:
                encoded_bytes.append(QOI_OP_RUN | (run - 1))
                run = 0
        else:
            if run > 0:
                encoded_bytes.append(QOI_OP_RUN | (run - 1))
                run = 0
            idx = _pixel_hash(r, g, b, a)
            index[idx] = prev_pixel

            idx_new = _pixel_hash(r, g, b, a)
            if index[idx_new] == (r, g, b, a):
                encoded_bytes.append(idx_new)
            else:
                dr = (r - prev_pixel[0]) & 0xFF
                dg = (g - prev_pixel[1]) & 0xFF
                db = (b - prev_pixel[2]) & 0xFF

                dr_signed = ((dr + 128) & 0xFF) - 128
                dg_signed = ((dg + 128) & 0xFF) - 128
                db_signed = ((db + 128) & 0xFF) - 128

                if (a == prev_pixel[3] and -2 <= dr_signed <= 1 and -2 <= dg_signed <= 1 and -2 <= db_signed <= 1):
                    encoded_bytes.append(
                        QOI_OP_DIFF
                        | ((dr_signed + 2) << 4)
                        | ((dg_signed + 2) << 2)
                        | (db_signed + 2)
                    )
                elif (a == prev_pixel[3] and -32 <= dg_signed <= 31 and -8 <= (dr_signed - dg_signed) <= 7 and -8 <= (db_signed - dg_signed) <= 7):
                    vg = dg_signed + 32
                    vr = (dr_signed - dg_signed) + 8
                    vb = (db_signed - dg_signed) + 8
                    encoded_bytes.append(QOI_OP_LUMA | vg)
                    encoded_bytes.append((vr << 4) | vb)
                else:
                    if channel == 3 or a == prev_pixel[3]:
                        encoded_bytes.append(QOI_OP_RGB)
                        encoded_bytes.extend([r, g, b])
                    else:
                        encoded_bytes.append(QOI_OP_RGBA)
                        encoded_bytes.extend([r, g, b, a])
            index[idx_new] = (r, g, b, a)

        prev_pixel = (r, g, b, a)
    
    if run > 0:
        encoded_bytes.append(QOI_OP_RUN | (run - 1))

    encoded_bytes.extend(END_MARKER)

    return header + encoded_bytes


def decode(qoi_bytes):

    if qoi_bytes[:4] != QOI_MAGIC:
        raise ValueError("Not a valid QOI file (missing magic) !!")
    
    width = struct.unpack_from(">I", qoi_bytes, 4)[0]
    height = struct.unpack_from(">I", qoi_bytes, 8)[0]
    channels = qoi_bytes[12]
    colorspace = qoi_bytes[13]

    data = qoi_bytes[14:]

    index = [(0, 0, 0, 255) for _ in range(INDEX_SIZE)]
    pixels = []
    px = (0, 0, 0, 255)
    idx = 0

    num_pixels = width * height

    while len(pixels) < num_pixels:
        if data[idx:idx+8] == END_MARKER:
            break

        b1 = data[idx]
        idx += 1

        if b1 == QOI_OP_RGB:
            r = data[idx]; g = data[idx + 1]; b = data[idx + 2]
            idx += 3
            px = (r, g, b, px[3])
        elif b1 == QOI_OP_RGBA:
            r = data[idx]; g = data[idx+1]; b = data[idx+2]; a = data[idx+3]
            idx += 4
            px = (r, g, b, a)
        elif (b1 & 0xC0) == QOI_OP_INDEX:
            i_pos = b1 & 0x3F
            px = index[i_pos]
        elif (b1 & 0xC0) == QOI_OP_DIFF:
            dr = ((b1 >> 4) & 0x03) - 2
            dg = ((b1 >> 2) & 0x03) - 2
            db = (b1 & 0x03) - 2
            px = ((px[0] + dr) & 0xFF,
                  (px[1] + dg) & 0xFF,
                  (px[2] + db) & 0xFF,
                  px[3])
        elif (b1 & 0xC0) == QOI_OP_LUMA:
            b2 = data[idx]
            idx += 1
            dg = (b1 & 0x3F) - 32
            dr_dg = (b2 >> 4) & 0x0F
            db_dg = b2 & 0x0F
            dr = dr_dg - 8 + dg
            db = db_dg - 8 + dg
            px = (((px[0] + dr) & 0xFF),
                  ((px[1] + dg) & 0xFF),
                  ((px[2] + db) & 0xFF),
                  px[3])
        elif (b1 & 0xC0) == QOI_OP_RUN:
            run = (b1 & 0x3F) + 1
            for _ in range(run):
                pixels.append(px)
            i_pos = _pixel_hash(*px)
            index[i_pos] = px
            continue  # skip the below index update and re-check loop

        i_pos = _pixel_hash(*px)
        index[i_pos] = px

        pixels.append(px)

    return width, height, channels, pixels

def load_qoi(filepath):
    with open(filepath, "rb") as file:
        data = file.read()
    return decode(data)

def save_qoi(filepath, pixels, width, height, channel = 4, colorspace = 0):
    qoi_data = encode(pixels, width, height, channel, colorspace)
    with open(filepath, "wb") as file:
        file.write(qoi_data)