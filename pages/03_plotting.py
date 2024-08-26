import ee
import geemap

import solara


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()
        self.add_plot_gui()

    def add_ee_data(self):
        landsat7 = ee.Image("LANDSAT/LE7_TOA_5YEAR/1999_2003").select(
            ["B1", "B2", "B3", "B4", "B5", "B7"]
        )

        landsat_vis = {"bands": ["B4", "B3", "B2"], "gamma": 1.4}
        self.addLayer(landsat7, landsat_vis, "Landsat")

        hyperion = ee.ImageCollection("EO1/HYPERION").filter(
            ee.Filter.date("2016-01-01", "2017-03-01")
        )

        hyperion_vis = {
            "min": 1000.0,
            "max": 14000.0,
            "gamma": 2.5,
        }
        self.addLayer(hyperion, hyperion_vis, "Hyperion")


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(
            center=[40, -100],
            zoom=4,
            height="600px",
        )
