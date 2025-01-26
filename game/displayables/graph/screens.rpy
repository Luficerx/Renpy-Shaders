default Mc = Player("Kars")

screen display_graph():
    default StaticGraph = Graph(600, 100)
    default AnimGraph = AnimatedGraph(600, 100)

    vbox:
        textbutton "Next" action Function(EvaluateGraph, StaticGraph, Mc)
        text "[AnimGraph.len]"

    vbox:
        align (0.5, 0.5) spacing 5
        frame:
            padding(5, 5, 5, 5)
            add StaticGraph

        frame:
            padding(5, 5, 5, 5)
            add AnimGraph