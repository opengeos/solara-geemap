import solara


@solara.component
def Page():
    with solara.Column(align="center"):
        markdown = """
        ## Earth Engine Web Apps
        
        ### Introduction

        **A collection of Earth Engine web apps developed using [Solara](https://github.com/widgetti/solara) and geemap**

        - Web App: <https://giswqs-solara-geemap.hf.space>
        - GitHub: <https://github.com/opengeos/solara-geemap>
        - Hugging Face: <https://huggingface.co/spaces/giswqs/solara-geemap>

        
        ### How to deploy this app on Hugging Face Spaces

        1. Go to <https://huggingface.co/spaces/giswqs/voila-geospatial/tree/main> and duplicate the space to your own space.

        ![](https://i.imgur.com/4ib5BzB.png)

        2. Set environment variables as needed. For example, if you use Google Earth Engine, you need to set `EARTHENGINE_TOKEN` to your Earth Engine token. The token value should be copied from the following file depending on your operating system:

        ```text
        Windows: C:\\Users\\USERNAME\\.config\\earthengine\\credentials
        Linux: /home/USERNAME/.config/earthengine/credentials
        MacOS: /Users/USERNAME/.config/earthengine/credentials
        ```

        Simply open the file and copy **ALL** the content to the `EARTHENGINE_TOKEN` environment variable.

        ![](https://i.imgur.com/i04gzyH.png)

        ![](https://i.imgur.com/Ex37Ut7.png)

        3. After the space is built successfully, click the `Embed this Space` menu and find the `Direct URL` for the app, such as <https://giswqs-voila-geospatial.hf.space>.

        ![](https://i.imgur.com/V2Lp0dP.png)

        ![](https://i.imgur.com/klhR5FL.png)

        4. Add your own notebooks to the `notebooks` folder and wait for the app to be rebuilt.

        5. To hide the source code from the notebook, modify `run.sh` and set `--strip_sources=True`.


        """

        solara.Markdown(markdown)
