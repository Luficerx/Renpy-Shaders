init python in MouseState:
    from pygame import mouse
    
    def x():
        return (renpy.get_mouse_pos()[0])

    def y():
        return (renpy.get_mouse_pos()[1])
    
    def left():
        return (mouse.get_pressed()[0])

    def middle():
        return (mouse.get_pressed()[1])
    
    def right():
        return (mouse.get_pressed()[2])