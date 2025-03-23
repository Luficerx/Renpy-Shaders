init python in painter:
    from store import from_path, image_to_bytes, Color, Solid, HollowCircle
    _saving_image = False

    def empty_image_data(width, height):
        image_data = bytearray([0]*width*height*4)
        return image_data
            
    class Canvas(renpy.Displayable):
        def __init__(self, width, height, *args, **kwargs):
            super(Canvas, self).__init__(**kwargs)
            self.width = width
            self.height = height
            self.background = Solid("#18181880")
            self.layers = []
            self.layer = None
            self.layer_index = 0
            self.mode = "paint"
            self.pencil = 5
            self.color = [1.0, 1.0, 1.0, 1.0]

            self.add_layer()

        def render(self, w, h, st, at):
            rv = renpy.Render(self.width, self.height)
            if not _saving_image:
                bg_rv = renpy.render(self.background, self.width, self.height, st, at)
                rv.blit(bg_rv, (0, 0))

            for layer in self.layers:
                self.layer.radius = self.pencil
                layer_rv = layer.render(self.width, self.height, st, at)
                rv.blit(layer_rv, (0, 0))
            
            sub_rv = rv.subsurface((0, 0, self.width, self.height))
            renpy.redraw(self, 0.0)
            return sub_rv
                
        def visit(self):
            if self.layer is not None:
                return [self.layer]
            return []
        
        def event(self, ev, x, y, st):
            if self.layer is None:
                return
            
            if renpy.map_event(ev, "alt_K_k"):
                global _saving_image
                _saving_image = True
                rv = renpy.render(self, self.width, self.height, 0, 0)
                renpy.render_to_file(rv, "Canvas.png", resize=True)
                renpy.notify("Image saved.")
                
                _saving_image = False

            self.layer.mode = self.mode
            self.layer.color = self.color
            self.layer.pencil = self.pencil
            return self.layer.event(ev, x, y, st)

        def per_interact(self):
            renpy.redraw(self, 0.0)

        def add_layer(self, file=None):
            leng = len(self.layers) - 1
            leng += 1

            if file is None:
                layer = Layer(id=leng, width=self.width, height=self.height)
            else:
                layer = Layer(file, id=leng)
            
            layer.color = self.color
            layer.mode = self.mode

            self.layer_index = layer.id
            self.layers.append(layer)
            self.layer = self.layers[-1]
            renpy.restart_interaction()

        def undo_layer(self):
            if self.layer is not None:
                self.layer.undo()

        def clear_layer(self):
            if self.layer is not None:
                self.layer.clear_array()
        
        def fill_layer(self):
            if self.layer is not None:
                self.layer.fill_array()

        def set_layer(self, index):
            self.layer_index = index
            self.layer = self.layers[self.layer_index]

        def remove_layer(self, index):
            self.layers.pop(index)
            self.layer_index = len(self.layers) - 1
            
            if self.layers:
                self.layer = self.layers[self.layer_index]
            else:
                self.layer = None

        def list_layers(self):
            return [LayerPreview(layer) for layer in self.layers]

        @property
        def ffffff(self):
            return Color(rgb=self.color[:3], alpha=self.color[3]).hexcode
        

    class LayerPreview(renpy.Displayable):
        def __init__(self, layer, *args, **kwargs):
            super(LayerPreview, self).__init__(**kwargs)
            self.width, self.height = layer.size
            self.image_data = layer.image_data
            self.id = layer.id
        
        def render(self, w, h, st, at):
            rv = renpy.Render(100, 100)
            image = renpy.load_rgba(self.image_data, (self.width, self.height))

            rv.blit(image, (0, 0))
            return rv

    class Layer(renpy.Displayable):
        def __init__(self, image: str = None, id=None, *args, **kwargs):
            super(Layer, self).__init__(**kwargs)
            self.focus = False
            self.mode = "paint"
            
            self.color = None
            self.opacity = 1.0
            self.id = id
            
            self.pencil = 5.0
            self.mouse_x = 0
            self.mouse_y = 0

            if image is not None:
                self.image_data = image_to_bytes(image)
                self.size = renpy.image_size(image)
                self.image = image
            else:
                width, height = kwargs['width'], kwargs['height']
                self.image_data = empty_image_data(width, height)
                self.size = (width, height)

            self.previous = []
            self.bytes_steps = range(0, len(self.image_data), 4)

        @property
        def hexcode(self):
            return [*Color(rgb=self.color[:3], alpha=self.color[3])]

        @property
        def rgba(self):
            return Color(rgb=self.color[:3], alpha=self.color[3]).rgba

        def undo(self):
            if len(self.previous) > 0:
                self.image_data = self.previous.pop()

        def render(self, w, h, st, at):
            image = renpy.load_rgba(self.image_data, self.size)
            rv = renpy.Render(*self.size)
            if not _saving_image:
                self.outline = HollowCircle(self.color[:3], self.pencil+3.0, 0.75, 2.0)
                outline_rv = self.outline.render(w, h, st, at)

            rv.blit(image, (0, 0))

            if not _saving_image:
                x, y = int(self.mouse_x-self.outline.radius), int(self.mouse_y-self.outline.radius)
                rv.blit(outline_rv, (x, y))

            return rv
        
        def event(self, ev, x, y, st):
            self.mouse_x = x
            self.mouse_y = y

            if (x >= 0 and x <= self.size[0]) and (y >= 0 and y <= self.size[1]) and renpy.map_event(ev, "mousedown_1") and not self.focus:
                self.focus = True
                self.previous.append(self.image_data.copy())

            if renpy.map_event(ev, "mouseup_1") and self.focus:
                self.focus = False

            if (x <= self.size[0] and x >= 0) and (y <= self.size[1] and y >= 0):
                if self.focus:
                    self.tint_pixel(x, y, self.pencil, self.hexcode)
        
        def clear_array(self):
            self.previous.append(self.image_data.copy())
            for i in self.bytes_steps:
                self.image_data[i+3] = 0
            renpy.restart_interaction()
    
        def fill_array(self):
            self.previous.append(self.image_data.copy())
            for i in self.bytes_steps:
                self.image_data[i]   = self.hexcode[0]
                self.image_data[i+1] = self.hexcode[1]
                self.image_data[i+2] = self.hexcode[2]
                self.image_data[i+3] = self.hexcode[3]
            renpy.restart_interaction()

        def tint_pixel(self, center_x, center_y, radius, color):
            center_x, center_y, radius = int(center_x), int(center_y), int(radius)
            width, height = self.size
    
            def blend_pixel(x, y, alpha):
                if 0 <= x < width and 0 <= y < height:
                    index = (y * width + x) * 4
                    pixel_alpha = self.image_data[index+3]

                    if self.mode == "paint":
                        for i in range(3):
                            self.image_data[index+i] = int(self.hexcode[i] * alpha + self.image_data[index+i] * (1 - alpha)) # R

                        self.image_data[index+3] = min(255, int(pixel_alpha + (alpha * color[3]))) # A

                    if self.mode == "erase":
                        self.image_data[index+3] = max(0, self.image_data[index+3] - color[3]) # A

            for y in range(center_y - radius - 1, center_y + radius + 2):
                for x in range(center_x - radius - 1, center_x + radius + 2):
                    dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    if dist <= radius:
                        blend_pixel(x, y, 1.0)
                    
                    elif dist <= radius + 1:
                        alpha = 1.0 - (dist - radius)
                        blend_pixel(x, y, alpha)
            
            renpy.restart_interaction()