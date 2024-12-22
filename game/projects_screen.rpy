screen projects():
    add Solid("#181818")

    style_prefix "default"

    frame:
        background None align (0.5, 0.5) xysize (800, 500)
        has vbox spacing 10 xalign 0.5
        
        label "PROJECTS" xalign 0.5

        textbutton "Circle Displayables" action Jump("circle_examples") xalign 0.5