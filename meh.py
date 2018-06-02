import gmt

gmt.print_libgmt_info()
topo = gmt.datasets.load_earth_relief()
print(gmt.grdinfo(topo, L=0, C='n'))
print(gmt.grdinfo(topo, V='d'))

fig = gmt.Figure()
fig.grdimage(topo, cmap='ocean', region='g', projection='W0/10i')
fig.savefig('meh.png', show=True)
