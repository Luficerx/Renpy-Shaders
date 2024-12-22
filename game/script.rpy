label start:
    call screen projects()

label circle_examples:
    if not (persistent.circle_disclaimer):
        "[DISCLAIMER] For anyone reading this, the following examples are for study purposes."
        "I don't recommend an extensive use for perfomance issues, It could be quite expensive at rendering."
        "HollowArc is not optimized."
        $ persistent.circle_disclaimer = True

    call screen display_circles()