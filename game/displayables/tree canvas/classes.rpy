init python:
    class TreeBranch(renpy.Displayable):
        focusable = True

        def __init__(self, child, color: str, id: str, target: tuple[str] = None, **properties):

            self.start_xpos = properties.pop("xpos", 0)
            self.start_ypos = properties.pop("ypos", 0)

            self.x = 0
            self.y = 0

            super(TreeBranch, self).__init__(**properties)

            self.id = id

            self.child = renpy.displayable(child)

            self.target = target
            self.color = color

            self.tree_group = None
            self.draggable = True

            self.pos_set = False
            self.dragging = False

            self.zorder = 0

            self.last_x = 0
            self.last_y = 0

            self.offset_x = 0
            self.offset_y = 0
        
        def __eq__(self, other):
            if type(other) is TreeBranch:
                return self.id == other.id

        @property
        def pos(self):
            return (self.x, self.y)

        @property
        def pos_to_center(self):
            width, heigth = self.size

            return (self.x + (width//2), self.y + (heigth//2))
            
        @property
        def size(self) -> tuple[int, int]:
            rv = renpy.render(self.child, 0, 0, 0, 0)
            size = rv.get_size()
            return size
        
        def update_pos(self):
            if type(self.start_xpos) is float:
                self.x = int((self.tree_group.size[0] - self.size[0]) * self.start_xpos)

            else:
                self.x = self.start_xpos if self.start_xpos < self.tree_group.size[0] else 0

            if type(self.start_ypos) is float:
                self.y = int((self.tree_group.size[1] - self.size[1]) * self.start_ypos)

            else:
                self.y = self.start_ypos if self.start_ypos < self.tree_group.size[1] else 0

        def raise_self(self):
            self.tree_group.raise_branch([self])

        def render(self, w, h, st, at):
            child_rv = self.child.render(w, h, st, at)

            cw, ch = child_rv.get_size()

            self.w = cw
            self.h = ch

            fx, fy, fw, fh = (0.0, 0.0, 1.0, 1.0)

            fx = int(absolute.compute_raw(fx, cw))
            fy = int(absolute.compute_raw(fy, ch))

            fw = int(absolute.compute_raw(fw, cw))
            fh = int(absolute.compute_raw(fh, ch))
            
            if self.dragging:
                child_rv.add_focus(self, None, fx, fy, fw, fh)

            if renpy.display.focus.get_grab() != self:
                self.last_x = self.x
                self.last_y = self.y

            return child_rv

        def event(self, ev, x, y, st):

            grabbed = (renpy.display.focus.get_grab() == self)

            px = int(self.last_x + x)
            py = int(self.last_y + y)

            if self.draggable and renpy.map_event(ev, "drag_activate"):
                if (x > self.x and x < self.x+self.w) and (y > self.y and y < self.y+self.h):
                    renpy.display.focus.set_grab(self)
                    
                    self.offset_x = px - self.x
                    self.offset_y = py - self.y

                    self.dragging = True
                    grabbed = True

                    self.raise_self()
                    
            if renpy.map_event(ev, "drag_deactivate"):
                renpy.display.focus.set_grab(None)
                self.dragging = False

                if self.x == self.last_x and self.y == self.last_y:
                    rv = self.child.event(ev, x, y, st)

                    if rv is not None:
                        return rv

            if grabbed:
                self.x = max(0, min(self.tree_group.size[0] - self.size[0], px - self.offset_x))
                self.y = max(0, min(self.tree_group.size[1] - self.size[1], py - self.offset_y))

        def visit(self):
            return [ self.child ]

    class TreeCanvas(renpy.Displayable):
        zorder = 0

        def __init__(self, **properties):
            self.children = []
            self.sorted = False
            self.focus = None

            super(TreeCanvas, self).__init__(**properties)

        def render(self, w, h, st, at):
            rv = renpy.Render(w, h)
            
            self.size = rv.get_size()

            canvas = rv.canvas()
            surf = canvas.get_surface()
            
            if not self.sorted:
                self.children.sort(key = lambda ch: ch.zorder)
                self.sorted = True

            for child in self.children:
                child_rv = child.render(w, h, st, at)
                if not child.pos_set:
                    child.update_pos()
                    child.pos_set = True

                if child.target is not None:
                    for other_child in [ch for ch in self.children if ch != child]:
                        cx, cy = child.pos_to_center
                        ocx, ocy = other_child.pos_to_center

                        if other_child.id in child.target:
                            canvas.line(child.color, child.pos_to_center, other_child.pos_to_center, 3)

                rv.blit(child_rv, child.pos)

            return rv
        
        def event(self, ev, x, y, st):
            for child in sorted(self.children, key=lambda k: k.zorder):
                
                rv = child.event(ev, x, y, st)
                if rv is not None:
                    return rv

            renpy.redraw(self, 0.0)

        def visit(self) -> list:
            return self.children
        
        def add_branches(self, *args):
            for branch in args:
                self.add_branch(branch)

        def add_branch(self, branch):
            if type(branch) is not TreeBranch:
                raise TypeError(f"Only 'TreeBranch' objects can be added to 'TreeCanvas'.")

            branch.tree_group = self

            self.children.append(branch)
            self.sorted = False

            branch.raise_self()

        def raise_branch(self, branches):
            self.sorted = False

            for branch in branches:
                self.zorder += 1
                branch.zorder = self.zorder