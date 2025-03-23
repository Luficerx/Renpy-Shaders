screen display_tree_canvas(tree):
    add "#181818"

    frame:
        align (0.5, 0.5)

        viewport:
            xysize (400, 1000) mousewheel True
            scrollbars "vertical"

            fixed:
                xfill True
                ysize 3000

                add tree