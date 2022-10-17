import base64
from io import BytesIO as _BytesIO
from PIL import Image
import plotly.graph_objs as go

def b64_to_pil(string):
    decoded = base64.b64decode(string)
    buffer = _BytesIO(decoded)
    im = Image.open(buffer)

    return im


def show_histogram(image):
    def hg_trace(name, color, hg):
        line = go.Scatter(
            x=list(range(0, 256)),
            y=hg,
            name=name,
            line=dict(color=(color)),
            mode='lines',
            showlegend=False
        )
        fill = go.Scatter(
            x=list(range(0, 256)),
            y=hg,
            mode='fill',
            name=name,
            line=dict(color=(color)),
            fill='tozeroy',
            hoverinfo='none'
        )

        return line, fill

    hg = image.histogram()

    if image.mode == 'RGBA':
        rhg = hg[0:256]
        ghg = hg[256:512]
        bhg = hg[512:768]
        ahg = hg[768:]

        data = [
            *hg_trace('Red', '#FF4136', rhg),
            *hg_trace('Green', '#2ECC40', ghg),
            *hg_trace('Blue', '#0074D9', bhg),
            *hg_trace('Alpha', 'gray', ahg)
        ]

        title = 'RGBA Histogram'

    elif image.mode == 'RGB':
        # Returns a 768 member array with counts of R, G, B values
        rhg = hg[0:256]
        ghg = hg[256:512]
        bhg = hg[512:768]

        data = [
            *hg_trace('Red', '#FF4136', rhg),
            *hg_trace('Green', '#2ECC40', ghg),
            *hg_trace('Blue', '#0074D9', bhg),
        ]

        title = 'RGB Histogram'

    else:
        data = [*hg_trace('Gray', 'gray', hg)]

        title = 'Grayscale Histogram'

    layout = go.Layout(
        title=title,
        margin=go.Margin(l=35, r=35),
        legend=dict(x=0, y=1.15, orientation="h")
    )

    return go.Figure(data=data, layout=layout)


def update_histogram(figure):
    # Retrieve the image stored inside the figure
    enc_str = figure['layout']['images'][0]['source'].split(';base64,')[-1]
    # Creates the PIL Image object from the b64 png encoding
    im_pil = b64_to_pil(string=enc_str)

    return show_histogram(im_pil)