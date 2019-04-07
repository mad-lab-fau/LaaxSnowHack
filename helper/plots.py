from bokeh.io import show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
import numpy as np


def plot_ski_slopes(slopes, color_map=None, show_altitude=True):
    COLOR_MAP = {
        'intermediate': 'red',
        'easy': 'blue',
        'freeride': 'yellow',
        'advanced': 'black'
    }
    color_map = color_map or COLOR_MAP

    c_data = dict()
    c_data['id'] = list(slopes.keys())
    c_data['y'] = list(g['geo'].T[0] for g in slopes.values())
    c_data['x'] = list(g['geo'].T[1] for g in slopes.values())
    c_data['distance'] = list(g['distance'] for g in slopes.values())
    c_data['difficulty'] = list(g['difficulty'] for g in slopes.values())
    c_data['height'] = list(g['elevation'] for g in slopes.values())
    c_data['rel_height'] = list(np.array(g['elevation']) - g['elevation'][0] for g in slopes.values())
    c_data['pos'] = list(g['pos'] for g in slopes.values())
    c_data['name'] = list(g['name'] for g in slopes.values())
    c_data['color'] = list(color_map[g['difficulty']] for g in slopes.values())
    c_data = ColumnDataSource(c_data)


    TOOLTIPS = [
        ("id", "@id"),
        ("name", "@name"),
        ("distance", "@distance"),
        ("(x,y)", "($x, $y)"),
    ]

    TOOLS = "box_zoom,tap,reset"

    p = figure(plot_width=800, plot_height=800, tooltips=TOOLTIPS, tools=TOOLS)
    p.multi_line('x', 'y', source=c_data, color='color', line_width=3)
    if show_altitude is True:
        p1 = figure(plot_width=800, plot_height=800, tooltips=TOOLTIPS, tools=TOOLS)
        p1.multi_line('pos', 'rel_height', source=c_data, color='color', line_width=3)
        return gridplot([[p, p1]])
    else:
        return p


def plot_gps_track(source, color=None, overlay_onto=None):
    color = color or 'red'
    if not overlay_onto:
        p = figure(plot_width=800, plot_height=800)
    else:
        p = overlay_onto
    p.line('lo', 'la', source=source, line_width=3, color=color)
    return p


def plot_gps_altitude(source, color=None):
    p = figure(plot_width=800, plot_height=800)
    p.line('t', 'el', source=source, line_width=3, color=color)
    return p


