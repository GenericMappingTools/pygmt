import pygmt

# Define region of interest around Caucasus 
region = [39, 50, 40, 45]

# Load sample grid (3 arc-seconds global relief) in target area
grid = pygmt.datasets.load_earth_relief(resolution="03s", region=region)

cmap = pygmt.makecpt(cmap='terra', series=[-5000, 5000])
fig = pygmt.Figure()
with fig.subplot(nrows=3, ncols=3, figsize=("20c", "20c")):
    for i, rad in enumerate(['210/0','210/45', '210/90']):#, 0.5, 1]:
        for j, nor in enumerate([1, 10, 20]):
            index = i * 3 + j
            dgrid = pygmt.grdgradient(grid=grid, radiance=rad, normalize=nor)

            with fig.set_panel(panel=index):
                fig.grdimage(
                grid=grid,
                projection="M5c",
                frame=["WSrt", "a2f1"],
                cmap=cmap
                )
        
fig.show()
