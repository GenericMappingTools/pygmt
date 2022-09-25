import pygmt

fig = pygmt.Figure()

pygmt.makecpt(cmap="batlow", series=[0, 80, 10])

fig.ternary("@ternary.txt", 
            region = [0, 100, 0, 100, 0, 100], 
            width = "10c",
            style = "c0.1c",
            L = "Water/Air/Limestone",
            cmap = True,
            frame = ['aafg+l"Water component"+u" %"', 
                     'bafg+l"Air component"+u" %"', 
                     'cagf+l"Limestone component"+u" %"',
                     "+givory"])

fig.show()
