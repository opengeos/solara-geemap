import geemap
import solara

zoom = solara.reactive(4)
center = solara.reactive((40, -100))
bounds = solara.reactive(None)


@solara.component
def Page():
    # Isolation is required to prevent the map from overlapping navigation (when screen width < 960px)
    with solara.Column(
        style={"min-width": "500px", "height": "780px", "isolation": "isolate"}
    ):
        # solara components support reactive variables
        solara.SliderInt(label="Zoom level", value=zoom, min=1, max=20)
        # using 3rd party widget library require wiring up the events manually
        # using zoom.value and zoom.set
        geemap.Map.element(  # type: ignore
            zoom=zoom.value,
            on_zoom=zoom.set,
            center=center.value,
            on_center=center.set,
            on_bounds=bounds.set,
            scroll_wheel_zoom=True,
            height="600px",
        )
        solara.Text(f"Zoom: {zoom.value}")
        solara.Text(f"Center: {center.value}")
        solara.Text(f"Bounds: {bounds.value}")
