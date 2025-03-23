init -10 python:
    # Useful functions

    # Convert from hexcode to rgb tuples, "FFF" -> (1.0, 1.0, 1.0)
    def validate_gradient_colors(colors: list[str, tuple[float, float, float]]):
        """This functions takes a list of string or tuple colors and return their rgba values"""

        items = []

        if (type(colors) is not list) and (type(colors) is not tuple):
            raise TypeError(f"Invalid type passed to [colors] argument; {type(colors)} {colors}.")

        for i in colors:
            if type(i) is str:
                items.append(Color(i).rgba)

            elif type(i) is tuple or type(i) is str:
                items.append(tuple(i))

            else:
                raise TypeError(f"Invalid color argument: {type(i)} {i}")
        
        return items

    def validate_circle_color(color):
        """Function to check if a color is a valid value"""
        
        if type(color) is str:
            return Color(color).rgb

        elif type(color) is tuple or type(color) is list:
            if len(color) == 3:
                return tuple(color)

            else:
                raise ValueError(f"color argument expect at least 3 values but got {len(color)}.")

        else:
            raise TypeError(f"color argument must be of type string: \"#FFF\", tuple: (0.0, 0.0, 0.0) or list: [0.0, 1.0, 0.0].\n but got {type(color)} {color}.")

    def from_path(*args: tuple[str], base: str = config.gamedir) -> str:
        from os.path import join
        return join(base, *args)
    
    # TODO: refactor this, ai sheissu
    def image_to_bytes(filename: str):
        import zlib, struct
        
        with open(from_path(filename), 'rb') as f:
            if f.read(8) != b'\x89PNG\r\n\x1a\n':
                raise ValueError("Not a PNG file")
        
            # Read IHDR
            length = struct.unpack('>I', f.read(4))[0]
            if f.read(4) != b'IHDR':
                raise ValueError("Invalid PNG header")
                
            width = struct.unpack('>I', f.read(4))[0]
            height = struct.unpack('>I', f.read(4))[0]
            bit_depth = f.read(1)[0]
            color_type = f.read(1)[0]
            f.seek(length - 10 + 4, 1)  # Skip rest of IHDR + CRC
            
            # Read all IDAT chunks
            image_data = b''
            while True:
                length = struct.unpack('>I', f.read(4))[0]
                chunk_type = f.read(4)
                
                if chunk_type == b'IDAT':
                    image_data += f.read(length)
                    f.read(4)  # Skip CRC
                elif chunk_type == b'IEND':
                    break
                else:
                    f.seek(length + 4, 1)

            decompressed_data = zlib.decompress(image_data)
            
            # Handle different color types
            if color_type == 6:  # RGBA
                pixel_size = 4
            elif color_type == 2:  # RGB
                pixel_size = 3
            else:
                raise ValueError(f"Unsupported color type: {color_type}")

            stride = width * pixel_size + 1  # +1 for filter type
            
            # Process each scanline
            pixels = bytearray()
            previous_row = bytearray(width * pixel_size)
            
            for y in range(height):
                filter_type = decompressed_data[y * stride]
                current_row = bytearray(decompressed_data[y * stride + 1:(y + 1) * stride])
                
                # Apply reverse filtering
                for x in range(width * pixel_size):
                    if filter_type == 0:  # None
                        pass
                    elif filter_type == 1:  # Sub
                        if x >= pixel_size:
                            current_row[x] = (current_row[x] + current_row[x - pixel_size]) & 0xff
                    elif filter_type == 2:  # Up
                        current_row[x] = (current_row[x] + previous_row[x]) & 0xff
                    elif filter_type == 3:  # Average
                        a = current_row[x - pixel_size] if x >= pixel_size else 0
                        b = previous_row[x]
                        current_row[x] = (current_row[x] + ((a + b) // 2)) & 0xff
                    elif filter_type == 4:  # Paeth
                        a = current_row[x - pixel_size] if x >= pixel_size else 0
                        b = previous_row[x]
                        c = previous_row[x - pixel_size] if x >= pixel_size else 0
                        p = a + b - c
                        pa = abs(p - a)
                        pb = abs(p - b)
                        pc = abs(p - c)
                        if pa <= pb and pa <= pc:
                            current_row[x] = (current_row[x] + a) & 0xff
                        elif pb <= pc:
                            current_row[x] = (current_row[x] + b) & 0xff
                        else:
                            current_row[x] = (current_row[x] + c) & 0xff

                pixels.extend(current_row)
                previous_row = current_row[:]
                
            # If the surface expects RGBA but we have RGB, add alpha channel
            if color_type == 2:  # RGB to RGBA
                rgba_pixels = bytearray()
                for i in range(0, len(pixels), 3):
                    rgba_pixels.extend([pixels[i], pixels[i+1], pixels[i+2], 255])

                return rgba_pixels
            
        return pixels