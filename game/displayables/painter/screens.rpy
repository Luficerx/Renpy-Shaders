screen display_painter():
    default canvas = painter.Canvas(100, 100)
    add "#ACACAC80"

    hbox:
        offset (100, 100) spacing 5

        frame:
            background "#18181830"
            vbox:
                xsize 100 spacing 5

                text "Layers" xalign 0.5
                textbutton "+Layer" action canvas.add_layer xalign 0.5
                viewport:
                    ymaximum 600 xsize 150 mousewheel True draggable True #xalign 0.5
                    vbox:
                        spacing 5
                        for i, layer in enumerate(canvas.list_layers()):
                            button:
                                background "#181818" hover_background "#393939" selected_background "#393939" xysize (150, 40)
                                add Transform(layer, xzoom=30/layer.width, yzoom=30/layer.height) #yalign 0.5
                                text "[layer.id]" align (1.0, 0.5)
                                action Function(canvas.set_layer, i)
                                alternate Function(canvas.remove_layer, i)
                                selected i == canvas.layer_index

        frame:
            background "#18181830"
            vbox:
                xsize 110 spacing 5

                grid 3 3:
                    spacing 5 xalign 0.5
                    imagebutton idle Solid("#FFF", xysize=(25, 25)) action SetField(canvas, "color", Color("FFF").rgba)
                    imagebutton idle Solid("#000", xysize=(25, 25)) action SetField(canvas, "color", Color("000").rgba)
                    imagebutton idle Solid("#F00", xysize=(25, 25)) action SetField(canvas, "color", Color("F00").rgba)
                    imagebutton idle Solid("#0F0", xysize=(25, 25)) action SetField(canvas, "color", Color("0F0").rgba)
                    imagebutton idle Solid("#00F", xysize=(25, 25)) action SetField(canvas, "color", Color("00F").rgba)
                    imagebutton idle Solid("#FF0", xysize=(25, 25)) action SetField(canvas, "color", Color("FF0").rgba)
                    imagebutton idle Solid("#0FF", xysize=(25, 25)) action SetField(canvas, "color", Color("0FF").rgba)
                    imagebutton idle Solid("#F0F", xysize=(25, 25)) action SetField(canvas, "color", Color("F0F").rgba)
                    imagebutton idle Solid("#F55", xysize=(25, 25)) action SetField(canvas, "color", Color("F55").rgba)

                textbutton "[canvas.mode!c]" action CycleField(canvas, "mode", ("paint", "erase")) xalign 0.5
                textbutton "Clear" action canvas.clear_layer xalign 0.5
                textbutton "Undo" action canvas.undo_layer xalign 0.5
                textbutton "Fill" action canvas.fill_layer xalign 0.5

        frame:
            background "#18181830"
            vbox:
                xsize 140
                text "Pencil: [canvas.pencil]" xalign 0.5
                bar value FieldValue(canvas, "pencil", min=1.0, max=100.0) xysize (120, 7) xalign 0.5

    fixed:
        fit_first True align (0.5, 0.5)
        add canvas
        text "[canvas.width]" anchor (0.0, 1.0) size 15
        text "[canvas.height]" anchor (1.0, 0.0) size 15