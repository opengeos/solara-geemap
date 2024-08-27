import ee
import geemap
import ipywidgets as widgets
from IPython.display import display
import solara


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_basemap("Esri.WorldImagery")
        self.add_ee_data()
        self.add_buttons(add_header=True)

    def add_ee_data(self):

        dataset = ee.Image("JRC/GSW1_4/GlobalSurfaceWater")
        image = dataset.select(["occurrence"])
        vis_params = {
            "min": 0.0,
            "max": 100.0,
            "palette": ["ffffff", "ffbbbb", "0000ff"],
        }
        self.addLayer(image, vis_params, "Occurrence")
        self.add_colorbar(
            vis_params, label="Water occurrence (%)", layer_name="Occurrence"
        )

    def add_buttons(self, position="topright", **kwargs):
        padding = "0px 5px 0px 5px"
        widget = widgets.VBox(layout=widgets.Layout(padding=padding))
        layout = widgets.Layout(width="auto")
        style = {"description_width": "initial"}
        hist_btn = widgets.Button(description="Occurrence", layout=layout)
        bar_btn = widgets.Button(description="Monthly history", layout=layout)
        reset_btn = widgets.Button(description="Reset", layout=layout)
        scale = widgets.IntSlider(
            min=30, max=1000, value=90, description="Scale", layout=layout, style=style
        )
        month_slider = widgets.IntRangeSlider(
            description="Months",
            value=[5, 10],
            min=1,
            max=12,
            step=1,
            layout=layout,
            style=style,
        )
        widget.children = [
            widgets.HBox([hist_btn, bar_btn, reset_btn]),
            month_slider,
            scale,
        ]
        self.add_widget(widget, position=position, **kwargs)
        output = widgets.Output()
        self.add_widget(output, position="bottomleft", add_header=False)

        def hist_btn_click(b):
            region = self.user_roi
            if region is not None:
                output.clear_output()
                output.append_stdout("Computing histogram...")
                image = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select(["occurrence"])
                self.default_style = {"cursor": "wait"}
                hist = geemap.image_histogram(
                    image,
                    region,
                    scale=scale.value,
                    height=350,
                    width=550,
                    x_label="Water Occurrence (%)",
                    y_label="Pixel Count",
                    layout_args={
                        "title": dict(x=0.5),
                        "margin": dict(l=0, r=0, t=10, b=0),
                    },
                    return_df=False,
                )

                with output:
                    output.clear_output()
                    display(hist)
                self.default_style = {"cursor": "default"}
            else:
                output.clear_output()
                with output:
                    output.append_stdout("Please draw a region of interest first.")

        hist_btn.on_click(hist_btn_click)

        def bar_btn_click(b):
            region = self.user_roi
            if region is not None:
                self.default_style = {"cursor": "wait"}
                output.clear_output()
                output.append_stdout("Computing monthly history...")
                bar = geemap.jrc_hist_monthly_history(
                    region=region,
                    scale=scale.value,
                    height=350,
                    width=550,
                    layout_args={
                        "title": dict(x=0.5),
                        "margin": dict(l=0, r=0, t=10, b=0),
                    },
                    frequency="month",
                    start_month=month_slider.value[0],
                    end_month=month_slider.value[1],
                    denominator=1e4,
                    y_label="Area (ha)",
                )

                with output:
                    output.clear_output()
                    display(bar)
                self.default_style = {"cursor": "default"}
            else:
                output.clear_output()
                with output:
                    output.append_stdout("Please draw a region of interest first.")

        bar_btn.on_click(bar_btn_click)

        def reset_btn_click(b):
            self._draw_control.clear()
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
