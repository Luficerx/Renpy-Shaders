init python:
    class Gradient(renpy.Displayable):
        def __init__(self, size: tuple[int, int], colors: tuple[str, str, str, str] = ("#282828", "#282828", "#0e0e0e", "#0e0e0e"), *args, **kwargs):
            """
            This creates a gradient with four colors;

            `size`: tuple[int, int] - width and height of this displayable.
            
            `colors`: tuple[str, str, str, str] - optional, this set's the default color of this gradient;.
            """
            super(Gradient, self).__init__(*args, **kwargs)

            self.size = size
            self.top_left, self.top_right, self.bottom_left, self.bottom_right = validate_gradient_colors(colors)

        def render(self, w, h, st, at):
            rv = renpy.Render(*self.size)
            shader_rv = renpy.Render(*self.size)
            
            shader_rv.add_shader("2DVfx.simple_gradient")
            shader_rv.mesh = True
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            
            shader_rv.add_uniform("u_bottom_right", self.bottom_right)
            shader_rv.add_uniform("u_bottom_left", self.bottom_left)
            shader_rv.add_uniform("u_top_right", self.top_right)
            shader_rv.add_uniform("u_top_left", self.top_left)

            rv.blit(shader_rv, (0, 0))

            return rv
    
    # [NOTE] Uncomment this in case you're using the gradient alone. [NOTE]

    # def validate_gradient_colors(colors: list[str, tuple[float, float, float]]):
    #     """This functions takes a list of string or tuple colors and return their rgba values"""

    #     items = []

    #     if (type(colors) is not list) and (type(colors) is not tuple):
    #         raise TypeError(f"Invalid type passed to [colors] argument; {type(colors)} {colors}.")

    #     for i in colors:
    #         if type(i) is str:
    #             items.append(Color(i).rgba)

    #         elif type(i) is tuple or type(i) is str:
    #             items.append(tuple(i))

    #         else:
    #             raise TypeError(f"Invalid color argument: {type(i)} {i}")
        
    #     return items