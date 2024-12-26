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
        "[[NEW GRADIENT'S PLANNEN.]"
        $ persistent.gradient_disclaimer = True

    call screen display_gradients()