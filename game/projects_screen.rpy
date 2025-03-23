screen projects():
    add Solid("#181818")

    style_prefix "default"

    frame:
        background None align (0.5, 0.5) xysize (800, 500)
        has vbox spacing 10 xalign 0.5
        
        label "PROJECTS" xalign 0.5

        textbutton "Tree Canvas Displayable" action Jump("tree_canvas_examples") xalign 0.5
        textbutton "Gradient Displayables" action Jump("gradient_examples") xalign 0.5
        textbutton "Circle Displayables" action Jump("circle_examples") xalign 0.5
        textbutton "Color Picker" action Jump("color_picker_examples") xalign 0.5
        textbutton "[[WIP] Painter Displayables" action Jump("painter_examples") xalign 0.5
        textbutton "[[WIP] Extended Transitions" action Jump("transitions_examples") xalign 0.5
        textbutton "[[WIP] Graph Displayables" action Jump("graph_examples") xalign 0.5
        textbutton "[[WIP] OS Window" action Jump("oswindow_examples") xalign 0.5