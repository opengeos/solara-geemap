import ee
import geemap
import ipywidgets as widgets
import solara
from datetime import date


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_basemap("Esri.WorldImagery")
        self.add_gui_widget(add_header=True)

    def clean_up(self):

        layers = [
            "Pre-event Image",
            "Post-event Image",
            "Pre-event NDWI",
            "Post-event NDWI",
            "Pre-event Water",
            "Post-event Water",
            "Disappeared Water",
            "New Water",
        ]
        for layer_name in layers:
            layer = self.find_layer(layer_name)
            if layer is not None:
                self.remove(layer)

    def add_gui_widget(self, position="topright", **kwargs):

        widget = widgets.VBox(layout=widgets.Layout(padding="0px 5px 0px 5px"))
        pre_widget = widgets.HBox()
        post_widget = widgets.HBox()
        layout = widgets.Layout(width="auto")
        style = {"description_width": "initial"}
        padding = "0px 5px 0px 5px"
        pre_start_date = widgets.DatePicker(
            description="Start",
            value=date(2014, 1, 1),
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )
        pre_end_date = widgets.DatePicker(
            description="End",
            value=date(2014, 12, 31),
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )
        pre_cloud_cover = widgets.IntSlider(
            description="Cloud",
            min=0,
            max=100,
            value=25,
            step=1,
            readout=False,
            style=style,
            layout=widgets.Layout(padding=padding, width="130px"),
        )
        pre_cloud_label = widgets.Label(value=str(pre_cloud_cover.value))
        geemap.jslink_slider_label(pre_cloud_cover, pre_cloud_label)
        pre_widget.children = [
            pre_start_date,
            pre_end_date,
            pre_cloud_cover,
            pre_cloud_label,
        ]
        post_start_date = widgets.DatePicker(
            description="Start",
            value=date(2024, 1, 1),
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )
        post_end_date = widgets.DatePicker(
            description="End",
            value=date(2024, 12, 31),
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )
        post_cloud_cover = widgets.IntSlider(
            description="Cloud",
            min=0,
            max=100,
            value=30,
            step=1,
            readout=False,
            style=style,
            layout=widgets.Layout(padding=padding, width="130px"),
        )
        post_cloud_label = widgets.Label(value=str(post_cloud_cover.value))
        geemap.jslink_slider_label(post_cloud_cover, post_cloud_label)
        post_widget.children = [
            post_start_date,
            post_end_date,
            post_cloud_cover,
            post_cloud_label,
        ]

        apply_btn = widgets.Button(description="Apply", layout=layout)
        reset_btn = widgets.Button(description="Reset", layout=layout)
        buttons = widgets.HBox([apply_btn, reset_btn])
        output = widgets.Output()

        use_split = widgets.Checkbox(
            value=False,
            description="Split map",
            style=style,
            layout=widgets.Layout(padding=padding, width="100px"),
        )

        use_ndwi = widgets.Checkbox(
            value=False,
            description="Compute NDWI",
            style=style,
            layout=widgets.Layout(padding=padding, width="160px"),
        )

        ndwi_threhold = widgets.FloatSlider(
            description="Threshold",
            min=-1,
            max=1,
            value=0,
            step=0.05,
            readout=True,
            style=style,
            layout=widgets.Layout(padding=padding, width="230px"),
        )

        options = widgets.HBox(
            [
                use_split,
                use_ndwi,
                ndwi_threhold,
            ]
        )

        widget.children = [pre_widget, post_widget, options, buttons, output]
        self.add_widget(widget, position=position, **kwargs)

        def apply_btn_click(b):

            marker_layer = self.find_layer("Search location")
            if marker_layer is not None:
                self.remove(marker_layer)
            self.clean_up()

            if self.user_roi is None:
                output.clear_output()
                output.append_stdout("Please draw a ROI first.")
            elif (
                pre_start_date.value is None
                or pre_end_date.value is None
                or post_start_date.value is None
                or post_end_date.value is None
            ):
                output.clear_output()
                output.append_stdout("Please select start and end dates.")

            elif self.user_roi is not None:
                output.clear_output()
                output.append_stdout("Computing... Please wait.")
                roi = ee.FeatureCollection(self.user_roi)
                vis_params = {"bands": ["B6", "B5", "B4"], "min": 0, "max": 0.4}
                if pre_start_date.value.strftime("%Y-%m-%d") < "2013-04-11":
                    pre_col = geemap.landsat_timeseries(
                        roi,
                        start_year=pre_start_date.value.year,
                        end_year=pre_end_date.value.year,
                    ).select(["SWIR1", "NIR", "Red", "Green"], ["B6", "B5", "B4", "B3"])
                else:
                    pre_col = (
                        ee.ImageCollection("NASA/HLS/HLSL30/v002")
                        .filterBounds(roi)
                        .filterDate(
                            pre_start_date.value.strftime("%Y-%m-%d"),
                            pre_end_date.value.strftime("%Y-%m-%d"),
                        )
                        .filter(ee.Filter.lt("CLOUD_COVERAGE", pre_cloud_cover.value))
                    )

                if post_start_date.value.strftime("%Y-%m-%d") < "2013-04-11":
                    post_col = geemap.landsat_timeseries(
                        roi,
                        start_year=post_start_date.value.year,
                        end_year=post_end_date.value.year,
                    ).select(["SWIR1", "NIR", "Red", "Green"], ["B6", "B5", "B4", "B3"])
                else:
                    post_col = (
                        ee.ImageCollection("NASA/HLS/HLSL30/v002")
                        .filterBounds(roi)
                        .filterDate(
                            post_start_date.value.strftime("%Y-%m-%d"),
                            post_end_date.value.strftime("%Y-%m-%d"),
                        )
                        .filter(ee.Filter.lt("CLOUD_COVERAGE", post_cloud_cover.value))
                    )

                pre_img = pre_col.median().clip(roi)
                post_img = post_col.median().clip(roi)

                if use_split.value:
                    left_layer = geemap.ee_tile_layer(
                        pre_img, vis_params, "Pre-event Image"
                    )
                    right_layer = geemap.ee_tile_layer(
                        post_img, vis_params, "Post-event Image"
                    )
                    self.split_map(
                        left_layer,
                        right_layer,
                        add_close_button=True,
                        left_label="Pre-event",
                        right_label="Post-event",
                    )
                else:
                    pre_img = pre_col.median().clip(roi)
                    post_img = post_col.median().clip(roi)
                    self.add_layer(pre_img, vis_params, "Pre-event Image")
                    self.add_layer(post_img, vis_params, "Post-event Image")

                if use_ndwi.value and (not use_split.value):
                    pre_ndwi = pre_img.normalizedDifference(["B3", "B6"]).rename("NDWI")
                    post_ndwi = post_img.normalizedDifference(["B3", "B6"]).rename(
                        "NDWI"
                    )
                    ndwi_vis = {"min": -1, "max": 1, "palette": "ndwi"}
                    self.add_layer(pre_ndwi, ndwi_vis, "Pre-event NDWI", False)
                    self.add_layer(post_ndwi, ndwi_vis, "Post-event NDWI", False)

                    pre_water = pre_ndwi.gt(ndwi_threhold.value)
                    post_water = post_ndwi.gt(ndwi_threhold.value)
                    self.add_layer(
                        pre_water.selfMask(), {"palette": "blue"}, "Pre-event Water"
                    )
                    self.add_layer(
                        post_water.selfMask(), {"palette": "red"}, "Post-event Water"
                    )
                    new_water = post_water.subtract(pre_water).gt(0)
                    disappear_water = pre_water.subtract(post_water).gt(0)
                    self.add_layer(
                        disappear_water.selfMask(),
                        {"palette": "brown"},
                        "Disappeared Water",
                    )
                    self.add_layer(
                        new_water.selfMask(), {"palette": "cyan"}, "New Water"
                    )

                    with output:
                        output.clear_output()

                output.clear_output()

        apply_btn.on_click(apply_btn_click)

        def reset_btn_click(b):
            self.clean_up()
            self._draw_control.clear()
            draw_layer = self.find_layer("Drawn Features")
            if draw_layer is not None:
                self.remove(draw_layer)
            output.clear_output()

        reset_btn.on_click(reset_btn_click)


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(
            center=[20, -0],
            zoom=2,
            height="750px",
            zoom_ctrl=False,
            measure_ctrl=False,
        )
