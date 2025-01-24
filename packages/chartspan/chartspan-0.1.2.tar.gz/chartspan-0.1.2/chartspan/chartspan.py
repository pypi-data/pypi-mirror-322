import json
from IPython.display import HTML, display

class ChartSpan:
    def __init__(self, width: int = 600, height: int = 400, text_color: str = "black"):
        """
        Initialize ChartSpan with custom dimensions and text color.

        Args:
            width (int): Desired chart width (default: 600)
            height (int): Desired chart height (default: 400)
            text_color (str): Color for text elements (default: "black")
        """
        self.width = width
        self.height = height
        self.text_color = text_color

    def render_inline(self, spec: dict, text_color: str = None) -> None:
        """
        Render a Vega-Lite JSON spec inline using Vega-Embed.

        Args:
            spec (dict): Vega-Lite specification dictionary
            text_color (str, optional): Override default text color
        """
        # Prioritize given over default
        color = text_color or self.text_color

        # Modify the spec for size
        spec["width"] = self.width
        spec["height"] = self.height

        # Set up config with text color and font
        spec.setdefault("config", {})
        spec["config"].setdefault("view", {})
        spec["config"]["view"]["continuousWidth"] = self.width
        spec["config"]["view"]["continuousHeight"] = self.height
        
        # Font family for all text elements
        default_font = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif'
        
        # Add text color and font configuration
        spec["config"]["text"] = {
            "color": color,
            "font": default_font,
            "fontSize": 11
        }
        spec["config"]["title"] = {
            "color": color,
            "font": default_font,
            "fontSize": 13
        }
        spec["config"]["axis"] = {
            "labelColor": color,
            "titleColor": color,
            "labelFont": default_font,
            "titleFont": default_font,
            "labelFontSize": 11,
            "titleFontSize": 13
        }
        spec["config"]["legend"] = {
            "labelColor": color,
            "titleColor": color,
            "labelFont": default_font,
            "titleFont": default_font,
            "labelFontSize": 11,
            "titleFontSize": 13
        }

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