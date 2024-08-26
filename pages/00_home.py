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

        1. Go to <https://huggingface.co/spaces/giswqs/solara-geemap/tree/main> and duplicate the space to your own space.

            ![](https://i.imgur.com/gTg4V2x.png)

        2. You need to set `EARTHENGINE_TOKEN` in order to use Earth Engine. The token value should be copied from the following file depending on your operating system:

            ```text
            Windows: C:\\Users\\USERNAME\\.config\\earthengine\\credentials
            Linux: /home/USERNAME/.config/earthengine/credentials
            MacOS: /Users/USERNAME/.config/earthengine/credentials
            ```

            Simply open the file and copy **ALL** the content to the `EARTHENGINE_TOKEN` environment variable.

            ![](https://i.imgur.com/i04gzyH.png)

            ![](https://i.imgur.com/Ex37Ut7.png)


            ```python
            import geemap
            geemap.get_ee_token()
            ```

            Copy all the content of the printed token and set it as the `EARTHENGINE_TOKEN` environment variable.

        3. After the space is built successfully, click the `Embed this Space` menu and find the `Direct URL` for the app, such as <https://giswqs-solara-geemap.hf.space>.

            ![](https://i.imgur.com/DNM36sk.png)

            ![](https://i.imgur.com/KX82lSf.png)

        4. Add your own apps (*.py) to the `pages` folder.

        5. Commit and push your changes to the repository. Wait for the space to be built successfully.

        """

        solara.Markdown(markdown)
