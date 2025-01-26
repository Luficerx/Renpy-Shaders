init python:
    class Player():
        def __init__(self, name, money=0):
            self.name = name
            self.money = money

    RED_RGBA = Color("#F00").rgba
    GREEN_RGBA = Color("#0F0").rgba
    GRAPH_SEGMENT_HEIGHT = 100

    class GraphSegment(renpy.Displayable):
        def __init__(self, y, h, width, color="#0F0", *args, **kwargs):
            super(GraphSegment, self).__init__(*args, **kwargs)
            
            self.y = y
            self.h = h
            self.width = width
            self.height = GRAPH_SEGMENT_HEIGHT
            self.color = Color(color).rgba
            self.line_width = kwargs.get("line_width", 1.0)
            self.alpha = kwargs.get("alpha", 0.25)

        def render(self, w, h, st, at):
            
            rv = renpy.Render(self.width, self.height)
            shader_rv = renpy.Render(self.width, self.height)
            
            shader_rv.add_shader("2DVfx.graph_segment")
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            shader_rv.mesh = True
            
            shader_rv.add_uniform("u_line_width", self.line_width)
            shader_rv.add_uniform("u_alpha", self.alpha)
            shader_rv.add_uniform("u_color", self.color)
            shader_rv.add_uniform("u_y", self.y)
            shader_rv.add_uniform("u_h", self.h)

            rv.blit(shader_rv, (0, 0))
            return rv

    class Graph(renpy.Displayable):
        def __init__(self, width=None, height=None, *args, **kwargs):
            self.width = width
            self.height = height
            
            super(Graph, self).__init__(*args, **kwargs)

            self.childs = []

        def render(self, w, h, st, at):
            if self.width is not None and self.height is not None:
                self.size = (self.width, self.height)

            elif self.width is not None:
                self.size = (self.width, h)
                self.height = h

            elif self.height is not None:
                self.size = (w, self.height)
                self.width = w

            rv = renpy.Render(*self.size)
            
            for i, child in enumerate(self.childs[::-1], start=1):
                child_rv = child.render(w, h, st, at)
                x = self.size[0] - (child.width * i)
                rv.blit(child_rv, (x, 0))

            renpy.redraw(self, 0.0)
            return rv

        def visit(self):
            return self.childs

        def add_segment(self, seg):
            self.childs.append(seg)

        @property
        def len(self):
            return len(self.childs)
    
    def EvaluateGraph(graph, player):
        v = renpy.random.randint(25, 75)

        height = min((v / 200) * GRAPH_SEGMENT_HEIGHT, GRAPH_SEGMENT_HEIGHT)
        if not graph.childs:
            seg = GraphSegment(0, height, graph.width//10)

            graph.add_segment(seg)
        
        else:
            last = graph.childs[-1]

            seg = GraphSegment(last.h, v, graph.width//10)

            graph.add_segment(seg)

            if len(graph.childs) * graph.width/10 > graph.width:
                graph.childs.pop(0)
                
    class AnimatedGraphSegment(renpy.Displayable):
        def __init__(self, y, h, width, start_color="#0F0", end_color="#0F0", *args, **kwargs):
            super(AnimatedGraphSegment, self).__init__(*args, **kwargs)
            
            self.y = y
            self.h = h

            self.x = kwargs.get("x", 0)

            self.width = width
            self.height = GRAPH_SEGMENT_HEIGHT
            self.start_color = Color(start_color).rgba
            self.end_color = Color(end_color).rgba
            self.line_width = kwargs.get("line_width", 1.0)
            self.alpha = kwargs.get("alpha", 0.10)

        def render(self, w, h, st, at):
            
            rv = renpy.Render(self.width, self.height)
            shader_rv = renpy.Render(self.width, self.height)
            
            shader_rv.add_shader("2DVfx.anim_graph_segment")
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            shader_rv.mesh = True
            
            shader_rv.add_uniform("u_line_width", self.line_width)
            shader_rv.add_uniform("u_start_color", self.start_color)
            shader_rv.add_uniform("u_end_color", self.end_color)
            shader_rv.add_uniform("u_alpha", self.alpha)
            shader_rv.add_uniform("u_y", self.y)
            shader_rv.add_uniform("u_h", self.h)

            rv.blit(shader_rv, (0, 0))
            return rv
        
        def update_pos(self, new):
            if self.x > new:
                self.x = max(new, self.x-1.0)
                return False
            
            return True

    class AnimatedGraph(renpy.Displayable):
        def __init__(self, width=None, height=None, *args, **kwargs):
            self.width = width
            self.height = height
            
            super(AnimatedGraph, self).__init__(*args, **kwargs)

            self.childs = []
            self.add_segment()

        def render(self, w, h, st, at):
            self.handle_size(w, h)

            rv = renpy.Render(*self.size)

            for i, child in enumerate(self.childs[::-1], start=1):
                child.update_pos(self.width - child.width*i)
                    
                child_rv = child.render(w, h, st, at)
                rv.blit(child_rv, (child.x, 0))
            
            last = self.childs[-1]
            first = self.childs[0]
            if last.x <= self.width - last.width:
                self.add_segment()
            
            if first.x <= 0 - first.width:
                self.childs.pop(0)

            rv = rv.subsurface((0, 0, *self.size))
            
            renpy.redraw(self, 0.0)
            return rv

        def visit(self):
            return self.childs

        def add_segment(self):
            v = renpy.random.randint(25, 75)

            if not self.childs:
                seg = AnimatedGraphSegment(0, v, 100, x=self.width)
            
            else:
                last = self.childs[-1]
                seg = AnimatedGraphSegment(last.h, v, 100, x=self.width)

                if seg.h < last.h:
                    seg.start_color = last.end_color
                    seg.end_color = RED_RGBA

                else:
                    seg.start_color = last.end_color
                    seg.end_color = GREEN_RGBA

            self.childs.append(seg)

        def handle_size(self, w, h):
            if self.width is not None and self.height is not None:
                self.size = (self.width, self.height)

            elif self.width is not None:
                self.size = (self.width, h)
                self.height = h

            elif self.height is not None:
                self.size = (w, self.height)
                self.width = w

            else:
                self.width, self.height = (w, h)
                self.size = (self.width, self.height)

        @property
        def len(self):
            return len(self.childs)