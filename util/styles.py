BORDER_STYLE = {"border": "2px white transparent",
                'margin': 20, 'border-radius': 20, 'background': '#181240',
                'width': '90%',"padding":30}


def border_style(percent):
    return {"border": "2px white transparent",
            'margin': 20, 'border-radius': 10, 'background': '#181240',
            'width': f'{percent}%'}

def padding_border_style(value):
    return {"border": "2px white transparent",
                'margin': 20, 'border-radius': 20, 'background': '#181240',
                'width': '90%',"padding":value}


FIGURE_STYLE = {
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    "legend_font_color": "white",
    "title_font_color": "white"
}
