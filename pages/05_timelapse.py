import geemap
import solara


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_basemap("Esri.WorldImagery")
        self.add_gui("timelapse", basemap=None)


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px", "isolation": "isolate"}):
        Map.element(
            center=[20, -0],
            zoom=2,
            height="750px",
            zoom_ctrl=False,
            measure_ctrl=False,
        )
