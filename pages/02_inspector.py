import ee
import geemap

import solara


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()
        self.add("layer_manager")
        self.add("inspector")

    def add_ee_data(self):
        # Add Earth Engine dataset
        dem = ee.Image("USGS/SRTMGL1_003")
        landsat7 = ee.Image("LANDSAT/LE7_TOA_5YEAR/1999_2003").select(
            ["B1", "B2", "B3", "B4", "B5", "B7"]
        )
        states = ee.FeatureCollection("TIGER/2018/States")

        # Set visualization parameters.
        vis_params = {
            "min": 0,
            "max": 4000,
            "palette": ["006633", "E5FFCC", "662A00", "D8D8D8", "F5F5F5"],
        }

        # Add Earth Engine layers to Map
        self.addLayer(
            landsat7,
            {"bands": ["B4", "B3", "B2"], "min": 20, "max": 200, "gamma": 2.0},
            "Landsat 7",
            True,
        )
        self.addLayer(dem, vis_params, "SRTM DEM", True, 1)
        self.addLayer(states, {}, "US States")


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(
            center=[40, -100],
            zoom=4,
            height="600px",
        )
