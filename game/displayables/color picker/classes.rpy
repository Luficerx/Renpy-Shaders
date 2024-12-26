# [ IMPORTANT NOTES ]
# This project is linked with different project, You can modify the code;
# But that will require changing different parts of the Picker and Spectrum class.

# This project also uses a simple store object. If you don't want to use the store
# you can `from pygame import mouse` and use mouse.get_pressed()[0] instead of MouseState.left()

init python:
    focus_taken = False # This blocks other displayables from getting focus
                        # when you're dragging something else

    class SpectrumGradient(renpy.Displayable):
        def __init__(self, gradient, size: tuple[int, int] = (25, 200), direction: str = "vertical", outline: str = "#FFF", *args, **kwargs):
            """
            `gradient`: ColorGradient - The gradient displayable which the slider will change the color.

            `size`: tuple[int, int] - The width and height of this displayable.

            `direction`: str - The direction which the hls gradient will be drawn; Only `'vertical'` and `'horizontal'` are allowed.
            
            `outline`: str - string hexcode passed to the Thumb displayable, this sets the "outline" color.
            """
            
            super(SpectrumGradient, self).__init__(*args, **kwargs)

            if direction not in ("vertical", "horizontal"):
                raise ValueError(f"direction argument accepts only ('vertical', 'horizontal') but got {direction}")

            self.direction = direction
            self.thumb = Thumb(size, direction, outline=outline)
            self.gradient = gradient
            self.focus = False
            self.size = size

        def render(self, w, h, st, at):
            rv = renpy.Render(*self.size)

            shader_rv = renpy.Render(*self.size)
            shader_rv.add_shader("2DVfx.spectrum_gradient")
            shader_rv.add_uniform("u_angle", (1.0 if self.direction == "vertical" else 0.0))
            shader_rv.mesh = True
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))

            thumb_rv = renpy.render(self.thumb, 0, 0, st=st, at=at)
            rv.blit(shader_rv, (0, 0))
            rv.blit(thumb_rv, (min(self.size[0]-self.thumb.xsize, self.thumb.x), min(self.size[1]-self.thumb.ysize, self.thumb.y)))

            return rv

        def event(self, ev, x, y, st):
            global focus_taken

            if MouseState.left() and (x > 0 and x < self.size[0] and y > 0 and y < self.size[1]) and (not self.focus and not focus_taken):
                self.focus = True
                focus_taken = True

            if not MouseState.left():
                self.focus = False
                focus_taken = False

            if self.focus:
                if self.direction == "horizontal":
                    self.thumb.x = int(min(self.size[0], max(0, ((x-config.screen_height)+config.screen_height))))
                    self.thumb.color[0] = (self.thumb.x / self.size[0]) / 1.0

                else:
                    self.thumb.y = int(min(self.size[1], max(0, ((y-config.screen_height)+config.screen_height))))
                    self.thumb.color[0] = (self.thumb.y / self.size[1]) / 1.0

                color = Color(hls=self.thumb.color).rgba
                self.gradient.top_right = color
                self.gradient.update_color()

    class ColorGradient(renpy.Displayable):
        def __init__(self, size: tuple[int, int], colors: tuple[str, str, str, str] = ("#FFF", "#F00", "#000", "#000"), outline: str = "#004cff", *args, **kwargs):
            """
            This creates a gradient with four colors;

            `size`: tuple[int, int] - width and height of this displayable.
            
            `colors`: tuple[str, str, str, str] - optional, this set's the default color of this gradient; you can use this to create a gradient with different colors but it won't work with the slider.
            
            `outline`: str - string hexcode passed to the Picker displayable, this sets the "outline" color.
            """

            super(ColorGradient, self).__init__(*args, **kwargs)

            self.size = size
            self.focus = False
            
            # These two are the default colors when you create the ColorGradient
            self.color = "ffffff"
            self.hexcode = "ffffff"

            self.picker = Picker(size[0], outline)
            self.top_left, self.top_right, self.bottom_left, self.bottom_right = validate_gradient_colors(colors)

        def render(self, w, h, st, at):
            rv = renpy.Render(*self.size)
            shader_rv = renpy.Render(*self.size)
            
            shader_rv.add_shader("2DVfx.square_gradient")
            shader_rv.mesh = True
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            
            shader_rv.add_uniform("u_bottom_right", self.bottom_right)
            shader_rv.add_uniform("u_bottom_left", self.bottom_left)
            shader_rv.add_uniform("u_top_right", self.top_right)
            shader_rv.add_uniform("u_top_left", self.top_left)
            
            picker_rv = renpy.render(self.picker, 0, 0, st, at)

            rv.blit(shader_rv, (0, 0))
            rv.blit(picker_rv, (self.picker.x, self.picker.y))

            return rv
        
        def solid(self, xsize=75, ysize=75):
            """Returns a solid displayable with the current color."""
            return Solid(self.color, xysize=(xsize, ysize))

        def event(self, ev, x, y, st):
            global focus_taken
            if (MouseState.left() and (x > 0 and x < self.size[0] and y > 0 and y < self.size[1])) and not self.focus and not focus_taken:
                self.focus = True
                focus_taken = True

            if not MouseState.left():
                self.focus = False
                focus_taken = False

            if self.focus:
                self.picker.x = int(min(self.size[0], max(0, ((x-config.screen_width)+config.screen_width))))
                self.picker.y = int(min(self.size[1], max(0, ((y-config.screen_height)+config.screen_height))))
                self.picker.update_color(self.size, self.top_left, self.top_right, self.bottom_left, self.bottom_right)
                self.update_color()

        def update_color(self):
            self.picker.update_color(self.size, self.top_left, self.top_right, self.bottom_left, self.bottom_right)
            self.color = Color(rgb=self.picker.color).hexcode
            self.hexcode = self.color
            renpy.restart_interaction()

    class Picker(renpy.Displayable):
        def __init__(self, size: int, outline: str = "#004cff", *args, **kwargs):
            """
            `size`: int - given from ColorGradient displayable, this is the width used as interpolator to set a minimum & maximum size of the color picker.

            `outline`: str - given from ColorGradient, the "outline" color of this displayable
            """

            super(Picker, self).__init__(*args, **kwargs)

            self.color = [1.0, 1.0, 1.0]
            self.x, self.y = (0, 0)
            self.outline = outline
            self.size = size

        def render(self, w, h, st, at):
            max_size = 15
            min_size = 7

            inner_size = min(10, max(7, (5*(self.size//200))))
            outer_size = min(12, max(9, (6*(self.size//200))))

            color = Color(rgb=self.color).hexcode
            
            self.inner = Circle(color, inner_size)
            self.outer = Circle(self.outline, outer_size)

            rv = renpy.render(Fixed(Transform(self.outer, align=(0.5, 0.5)), Transform(self.inner, align=(0.5, 0.5))), w, h, st, at)

            return rv
        
        def update_color(self, canvas: tuple[float], top_left, top_right, bottom_left, bottom_right):
            
            x = self.x / canvas[0]
            y = self.y / canvas[1]

            r = (1 - x) * (1 - y) * top_left[0] + x * (1 - y) * top_right[0] + (1 - x) * y * bottom_left[0] + x * y * bottom_right[0]
            g = (1 - x) * (1 - y) * top_left[1] + x * (1 - y) * top_right[1] + (1 - x) * y * bottom_left[1] + x * y * bottom_right[1]
            b = (1 - x) * (1 - y) * top_left[2] + x * (1 - y) * top_right[2] + (1 - x) * y * bottom_left[2] + x * y * bottom_right[2]

            self.color = [r, g, b]
        
    class Thumb(renpy.Displayable):
        def __init__(self, size: tuple[int, int], direction: str, outline: str = "#FFF", *args, **kwargs):
            """
            The thumb displayable used by the SpectrumGradient.

            `size`: tuple[int, int] - given by SpectrumGradient

            `direction`: str - given from SpectrumGradient, tell which direction the hls gradient is rendered horizontally or vertically.
            
            `outline`: str - string hexcode given from SpectrumGradient, the "outline" color of this displayable.
            """

            super(Thumb, self).__init__(*args, **kwargs)

            self.color = [0.0, 0.5, 1.0]
            self.direction = direction
            self.outline = outline
            self.x, self.y = (0, 0)

            self.size = size
            self.ysize = 6
            self.xsize = self.size[0]

            if self.direction == "horizontal":
                self.ysize = self.size[1]
                self.xsize = 6

        def render(self, w, h, st, at):
            thumb = Fixed(
                Solid(self.outline, xysize=(self.xsize, self.ysize)),
                Solid(Color(hls=self.color).hexcode, xysize=(self.xsize-4, self.ysize-4), align=(0.5, 0.5)), xysize=(self.xsize, self.ysize))

            rv = renpy.render(thumb, self.size[0], 10, st, at)
            renpy.redraw(self, 0.0)
            return rv

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