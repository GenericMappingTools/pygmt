"""
Functions to display NASA WorldWind Web in the Jupyter notebook.
"""
import base64

import numpy as np

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

        var wwd = new WorldWind.WorldWindow("{canvas}");

        // Add an image source as layer
        var image = new Image()
        image.src = "{image}"
        var surfaceImage = new WorldWind.SurfaceImage(
            new WorldWind.Sector({region[2]}, {region[3]},
                                 {region[0]}, {region[1]}),
            new WorldWind.ImageSource(image)
        );
        var surfaceImageLayer = new WorldWind.RenderableLayer();
        surfaceImageLayer.addRenderable(surfaceImage);

        // Add the imagery and display layers
        var layers = [
            new WorldWind.BMNGLayer(),
            new WorldWind.CompassLayer(),
            new WorldWind.CoordinatesDisplayLayer(wwd),
            new WorldWind.ViewControlsLayer(wwd),
            surfaceImageLayer,
        ];
        for (var l = 0; l < layers.length; l++) {{
            wwd.addLayer(layers[l]);
        }}

        // Set the view point
        wwd.goTo(new WorldWind.Position({center[1]}, {center[0]},
                                        {center[2]})
        );

        wwd.redraw();
    }});
</script>
"""


def worldwind_show(image, width, region, canvas_id, globe_center):
    """
    Create the HTML and Javascript to view an image in WorldWind Web

    WorldWind Web is a Javascript library for viewing a 3D globe, like Google
    Earth. This function creates the HTML and Javascript code to display a
    given image in the Jupyter notebook.

    Parameters
    ----------
    image : bytes
        An image loaded as a bytes string (use ``'rb'`` in the ``open``
        function).
    width : int
        The width of the HTML canvas element.
    region : list = [W, E, S, N]
        Boundaries of the image in geographical latitude and longitude degrees.
    canvas_id : str
        A unique id for the HTML canvas tag that will house the globe. A good
        choice would be the unique figure name.
    globe_center : tuple = (lon, lat, height[m])
        The coordinates used to set the view point. If None, will be chosen
        automatically based on the region argument.

    Returns
    -------
    IPython.display.HTML
        The IPython object with the HTML and Javascript inserted.

    """
    if globe_center is None:
        height = 200000 * max(region[1] - region[0], region[3] - region[2])
        # Cap the height at 9000km so the earth doesn't look so tiny on global maps
        if height > 9000e3:
            height = 9000e3
        lon = np.mean(region[:2])
        lat = np.mean(region[2:])
        globe_center = (lon, lat, height)
    # Need to escape the newlines so that they can be inserted in the
    # Javascript
    data = base64.encodebytes(image).decode("utf-8").encode("unicode_escape")
    b64image = "data:image/png;base64,{}".format(data.decode("utf-8"))
    worldwind = TEMPLATE.format(
        url=URL,
        canvas=canvas_id,
        width=width,
        height=width,
        region=region,
        image=b64image,
        center=globe_center,
    )
    return HTML(data=worldwind)
