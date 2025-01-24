# ChartSpan

ChartSpan is a Python library designed for rendering Vega-Lite JSON specifications directly within Jupyter Notebook or Google Colab. It simplifies the visualization of interactive charts and supports customization for chart dimensions.

## Features

- **Inline Rendering**: Renders Vega-Lite JSON specifications directly within Jupyter/Colab notebooks.
- **Interactive Charts**: Maintains full Vega-Lite interactivity (e.g., zoom, pan, tooltips).
- **Custom Dimensions**: Easily adjust chart width and height for different use cases.
- **Lightweight and Easy-to-Use**: Minimal setup and dependencies.

## Installation

To install ChartSpan, use pip:

```bash
pip install chartspan
```

## Usage

### Rendering Vega-Lite JSON Charts

Here is an example of how to use ChartSpan to render a Vega-Lite JSON chart:

```python
from chartspan import ChartSpan
import json

# Load Vega-Lite JSON specification
with open("example.json", "r") as f:
    spec = json.load(f)

# Render chart inline
chart = ChartSpan(width=800, height=600)
chart.render_inline(spec)
```

### Customization

You can specify custom dimensions for the chart:

```python
chart = ChartSpan(width=1000, height=800)
chart.render_inline(spec)
```

This modifies the chart's width and height, ensuring it fits your specific needs.

## Example

Save the following Vega-Lite JSON to a file named `example.json`:

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "mark": "point",
  "data": {
    "values": [
      {"x": 1, "y": 2},
      {"x": 2, "y": 3}
    ]
  },
  "encoding": {
    "x": {"field": "x", "type": "quantitative"},
    "y": {"field": "y", "type": "quantitative"}
  }
}
```

Run the following Python code:

```python
from chartspan import ChartSpan
import json

with open("example.json", "r") as f:
    spec = json.load(f)

chart = ChartSpan(width=800, height=600)
chart.render_inline(spec)
```

This will display an interactive scatter plot in your Jupyter Notebook or Colab environment.

## Dependencies

- `IPython`

Install dependencies using:

```bash
pip install IPython
```

## License

ChartSpan is licensed under the MIT License.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## Acknowledgments

ChartSpan uses the Vega-Lite and Vega-Embed libraries for rendering charts. Special thanks to the developers of these powerful visualization tools.