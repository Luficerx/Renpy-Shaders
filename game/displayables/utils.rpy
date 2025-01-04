init -10 python:
    # Useful functions to convert from hexcode 
    # To rgb tuples, "FFF" -> (1.0, 1.0, 1.0)

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