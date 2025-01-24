import pytest
from chartspan import ChartSpan
import json

def test_render_inline():
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": "point",
        "data": {"values": [{"x": 1, "y": 2}, {"x": 2, "y": 3}]},
        "encoding": {"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}}
    }
    chart = ChartSpan(width=800, height=600)
    chart.render_inline(spec)