screen display_circles():
    add Solid("#181818")

    frame:
        background None align (0.5, 0.5)
        has vbox spacing 25

        style_prefix "circle_style"

        frame:
            background None xsize 310
            has vbox spacing 20
            label "RawCircle" xalign 0.5

            hbox:
                xalign 0.5 spacing 5
                add RawCircle("#F00", 50.0)
                add RawCircle("#0F0", 50.0)
                add RawCircle("#00F", 50.0)

        frame:
            background None xsize 310
            has vbox spacing 20
            label "Circle" xalign 0.5

            hbox:
                xalign 0.5 spacing 5
                add Circle("#F00", 50.0, 0.0)
                add Circle("#0F0", 50.0, 1.0)
                add Circle("#00F", 50.0, 1.5)

        frame:
            background None xsize 310
            has vbox spacing 20
            label "HollowCircle" xalign 0.5
            hbox:
                xalign 0.5 spacing 5
                add HollowCircle("#F00", 50.0, 0.0, 5.0)
                add HollowCircle("#0F0", 50.0, 1.0, 15.0)
                add HollowCircle("#00F", 50.0, 2.0, 30.0)

        frame:
            background None xsize 310
            has vbox spacing 20
            label "HollowArc" xalign 0.5

            hbox:
                xalign 0.5 spacing 5
                add HollowArc("#F00", 50.0, 0.0, 15.0, 0.95, 0.25)
                add HollowArc("#0F0", 50.0, 1.0, 20.0, 0.95, 0.50)
                add HollowArc("#00F", 50.0, 2.0, 15.0, 0.95, 0.75)
    
    textbutton "Return (x)" action Jump("start") keysym "K_x" align (0.0, 1.0) offset (10, -10) text_style "return_button_style"