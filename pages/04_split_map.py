import ee
import geemap

import solara


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()

    def add_ee_data(self):
        # Select the eight NLCD epochs after 2000.
        years = ["2001", "2004", "2006", "2008", "2011", "2013", "2016", "2019"]

        # Get an NLCD image by year.
        def getNLCD(year):
            # Import the NLCD collection.
            dataset = ee.ImageCollection("USGS/NLCD_RELEASES/2019_REL/NLCD")

            # Filter the collection by year.
            nlcd = dataset.filter(ee.Filter.eq("system:index", year)).first()

            # Select the land cover band.
            landcover = nlcd.select("landcover")
            return landcover

        ## Create an NLCD image collection for the selected years.
        collection = ee.ImageCollection(ee.List(years).map(lambda year: getNLCD(year)))

        # Create a list of labels to populate the dropdown list.
        labels = [f"NLCD {year}" for year in years]

        # Add a split-panel map for visualizing NLCD land cover change.
        self.ts_inspector(
            left_ts=collection,
            right_ts=collection,
            left_names=labels,
            right_names=labels,
        )

        # Add the NLCD legend to the map.
        self.add_legend(
            title="NLCD Land Cover Type",
            builtin_legend="NLCD",
            height="460px",
            add_header=False,
        )


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(
            center=[40, -100],
            zoom=4,
            height="600px",
        )
