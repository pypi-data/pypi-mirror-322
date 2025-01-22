import json
from IPython.display import HTML, display

class ChartSpan:
    def __init__(self, width: int = 600, height: int = 400):
        """
        Initialize ChartSpan with custom dimensions.

        Args:
            width (int): Desired chart width (default: 600)
            height (int): Desired chart height (default: 400)
        """
        self.width = width
        self.height = height

    def render_inline(self, spec: dict) -> None:
        """
        Render a Vega-Lite JSON spec inline using Vega-Embed.

        Args:
            spec (dict): Vega-Lite specification dictionary
        """
        # Modify the spec for size
        spec["width"] = self.width
        spec["height"] = self.height

        # Or embed config for repeated/layered specs
        spec.setdefault("config", {})
        spec["config"].setdefault("view", {})
        spec["config"]["view"]["continuousWidth"] = self.width
        spec["config"]["view"]["continuousHeight"] = self.height

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
            <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
            <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
        </head>
        <body>
            <div id="vis"></div>
            <script type="text/javascript">
                const spec = {json.dumps(spec)};
                vegaEmbed('#vis', spec, {{
                  "renderer": "svg",
                  "width": {self.width},
                  "height": {self.height}
                }}).catch(console.error);
            </script>
        </body>
        </html>
        """
        display(HTML(html_template))
