MARGIN = 20

BORDER_STYLE = {"border": "2px white transparent",
                'margin': MARGIN, 'border-radius': 20, 'background': '#181240',
                'width': '95%',"padding":20}


def border_style(percent):
    return {"border": "2px white transparent",
            'margin': MARGIN, 'border-radius': 20, 'background': '#181240',
            'width': f'{percent}%'}

def padding_border_style(value):
    return {"border": "2px white transparent",
                'margin': MARGIN, 'border-radius': 20, 'background': '#181240',
                'width': '90%',"padding":value}

def width_style(width):
    return {"border": "2px white transparent",
                'margin': MARGIN, 'border-radius': 20, 'background': '#181240',
                'width': width,"padding":20}

BORDER_STYLE_NO_WIDTH = {"border": "2px white transparent",
                'margin': MARGIN, 'border-radius': 20, 'background': '#181240',"padding":20}

FIGURE_STYLE = {
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    "legend_font_color": "white",
    "title_font_color": "white"
}

