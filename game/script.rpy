label start:
    if not persistent.warning:
        """
        [DISCLAIMER] Some of the displayables in this project uses displayables from different files,
        In case you extract specific files, make sure to either; include all dependent files or adapt
        the source code to not depend on them."""
        $ persistent.warning = True
        
    call screen projects()

label circle_examples:
    if not (persistent.circle_disclaimer):
        "[DISCLAIMER] For anyone reading this, the following examples are for study purposes."
        "I don't recommend an extensive use for perfomance issues, It could be quite expensive at rendering."
        "HollowArc is not optimized."
        $ persistent.circle_disclaimer = True

    call screen display_circles()

label color_picker_examples:
    if not persistent.color_picker_disclaimer:
        "[DISCLAIMER] For anyone reading this, the following examples are for study purposes."
        "If you modify the default color of ColorGradient, you won't be able to use with the SpectrumGradient."
        $ persistent.color_picker_disclaimer = True

    call screen color_picker()

label gradient_examples:
    if not persistent.gradient_disclaimer:
        "[DISCLAIMER] For anyone reading this, the following examples are for study purposes."
        "This contains a simple gradient that mixes four colors in between in each corner."
        "[[NEW GRADIENT'S PLANNED.]"
        $ persistent.gradient_disclaimer = True

    call screen display_gradients()

label tree_canvas_examples:
    if not persistent.tree_canvas_disclaimer:
        "[DISCLAIMER] For anyone reading this, the following examples are for study purposes."
        "This contains an displayable that draws line across the children of the tree."
        $ persistent.tree_canvas_disclaimer = True

    python:
        tree = TreeCanvas()
        
        branches = [
            TreeBranch(
                ImageButton(
                    idle_image="placeholder.png",
                    action=(Notify("Unknown")),
                    focus_mask=True),

                color="#00ff73", 
                id="branch1",
                target=("branch2", "branch3"),
                xpos=100,
                ypos=0,
                ),

            TreeBranch(
                ImageButton(
                    idle_image="melissa.png",
                    action=(Notify("Girl 1")),
                    focus_mask=True),
                
                color="#fffb00",
                id="branch2",
                target=("branch4",),
                xpos=200,
                ypos=300,
                ),

            TreeBranch(
                ImageButton(
                    idle_image="lynn.png",
                    action=(Notify("Girl 2")),
                    focus_mask=True),
                
                color="#d400ff",
                id="branch3",
                xpos=400,
                ypos=300,
                ),

            TreeBranch(
                "placeholder.png",
                color="#ff7700", 
                id="branch4",
                xpos=400,
                ypos=600,
                ),

            TreeBranch(
                "placeholder.png",
                color="#006aff", 
                id="branch5",
                target=("branch3", "branch4"),
                xpos=100,
                ypos=800,
                ),
            ]

        tree.add_branches(*branches)

    call screen display_tree_canvas(tree)

label transitions_examples:
    "[[NOT DONE]"
    
    jump start

    call screen display_transitions()

label graph_examples:
    "[[NOT DONE]"
    
    # jump start

    call screen display_graph()

default data = None

label painter_examples:
    call screen display_painter()

label oswindow_examples:
    call screen display_oswindow()