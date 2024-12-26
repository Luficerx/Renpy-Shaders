screen color_picker():
    add Solid("#181818")

    default CanvasOne = ColorGradient((250, 250), outline="#000")
    default SpectrumOne = SpectrumGradient(CanvasOne, (250, 30), direction="horizontal", outline="#000")

    frame:
        background "#000" xysize (264, 354) align (0.5, 0.5)
        add Gradient((260, 350)) align (0.5, 0.5)

        vbox:
            fit_first "height" xsize 250 spacing 5 align (0.5, 0.5)
            add SpectrumOne align (0.0, 0.0)
            add CanvasOne align (0.0, 0.0)
            
            fixed:
                fit_first True
                add CanvasOne.solid(250, 50)
                textbutton "[CanvasOne.hexcode!u]":
                    action [Notify(f"Copied {CanvasOne.hexcode}"), CopyToClipboard(CanvasOne.hexcode)]
                    align (0.5, 1.0)
                    text_style "color_picker_button_style" text_size 24
                    
    textbutton "Return (x)" action Jump("start") keysym "K_x" align (0.0, 1.0) offset (10, -10) text_style "return_button_style"