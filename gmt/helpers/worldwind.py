"""
Functions to display a KML file in NASA WorldWind Web edition.
"""
import os

try:
    from IPython.display import HTML
except ImportError:
    HTML = None


VERSION = "0.9.0"
URL = "//files.worldwind.arc.nasa.gov/artifactory/web/{}".format(VERSION)
TEMPLATE = """
<canvas id="{canvas}" width="{width}" height="{height}">
    Your browser does not support HTML5 Canvas.
</canvas>

<script type="text/javascript">
    require.config({{
        paths: {{
            'WorldWind': ['{url}/worldwind.min'],
        }},
    }});
    require(['WorldWind'],
    function (WorldWind) {{

        // Create the WorldWindow.
        var wwd = new WorldWind.WorldWindow("{canvas}");

        // Add imagery layers.
        var layers = [
            {{layer: new WorldWind.BMNGLayer(), enabled: true}},
            {{layer: new WorldWind.CompassLayer(), enabled: true}},
            {{layer: new WorldWind.CoordinatesDisplayLayer(wwd),
              enabled: true}},
            {{layer: new WorldWind.ViewControlsLayer(wwd), enabled: true}}
        ];

        for (var l = 0; l < layers.length; l++) {{
            layers[l].layer.enabled = layers[l].enabled;
            wwd.addLayer(layers[l].layer);
        }}

        var kmlFilePromise = new WorldWind.KmlFile('{fname}');
        kmlFilePromise.then(function (kmlFile) {{
            var renderableLayer = new WorldWind.RenderableLayer("GMT Preview");
            renderableLayer.addRenderable(kmlFile);
            wwd.addLayer(renderableLayer);
            wwd.goTo(new WorldWind.Position({center[1]}, {center[0]},
                                            {center[2]}));
            wwd.redraw();
        }});
    }});
</script>
"""


def worldwind_show_kml(fname, width, globe_view):
    """
    Create an HTML canvas and JS to view a KML in WorldWind Web on the notebook

    WorldWind Web is a Javascript library for viewing a 3D globe, like Google
    Earth. This function creates the HTML and Javascript code to display a
    given KML file.

    Parameters
    ----------
    fname : str
        The path to the KML file.
    width ; int
        The width of the HTML canvas element.
    globe_center : tuple = (lon, lat, height[m])
        The coordinates used to set the view point.

    Returns
    -------
    IPython.display.HTML
        The IPython object with the HTML inserted.

    """
    if not os.path.exists(fname):
        raise FileNotFoundError("Couldn't find KML file '{}'.".format(fname))
    # Need the relative path so that WorldWind can find the files
    relfname = os.path.relpath(fname)
    basedir = os.path.dirname(relfname)
    canvas = os.path.splitext(os.path.basename(fname))[0]
    worldwind = TEMPLATE.format(basedir=basedir, url=URL, canvas=canvas,
                                width=width, height=width, fname=relfname,
                                center=globe_view)
    return HTML(data=worldwind)
