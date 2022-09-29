# -*- coding: utf-8 -*-
# Copyright © 2020, 2021, 2022 Joni Hyttinen, University of Eastern Finland
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the “Software”),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Functions to parse and render the annotation CSV-files.
#
# Main functions:
#   parse               Parse an annotation CSV-file content into a list of ParsedLabels
#   create_masks        Render ParsedLabels as bitmaps
#                       the return value is a dictionary with annotation label as key,
#                       the value behind the key in the dictionary is a list of bitmaps.
#                       Each bitmap matches a single ParsedLabel.
#   flatten_masks       Combine the individual bitmaps in a dictionary returned by 
#                       create_masks into a single bitmap per label. The return value
#                       is thus a dictionary of form {'annotation label': mask image}.
#   overlay_rgb_mask    Overlay masks on an RGB color image with an optional legend on
#                       the right side of the image.

from typing import Union

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy as np

ParsedLabel = tuple[str, str, dict[str, Union[int, str]], list[int], list[tuple[int, int]]]


def parse(input_string: str) -> list[ParsedLabel]:
    labels = []
    input_lines = input_string.splitlines()
    for input_line in input_lines:
        input_items = input_line.strip(';').split(';')
        # Segmentation label...
        label_name = input_items.pop(0).strip()
        # ... maybe followed by a type and parameters
        # f.ex. 'type', 'type: param=value', 'type: param=value: param=value...'
        # if not, assume polygon without parameters
        maybe_type = input_items[0].partition(':')[0].strip().lower()
        label_type = 'polygon'
        label_type_params = {}
        if maybe_type in ['polygon', 'line']:
            type_and_parameters = [x.strip() for x in input_items.pop(0).strip().lower().partition(':')]
            label_type = type_and_parameters[0]
            if type_and_parameters[2]:
                for parameter_and_value in type_and_parameters[2].split(':'):
                    parameter, useless, value = parameter_and_value.partition('=')
                    try:
                        label_type_params[parameter] = int(value)
                    except ValueError:
                        label_type_params[parameter] = value
        # label color up next...
        label_color = list(map(int, input_items.pop(0).split(',')))
        # ... followed by points
        label_points = []
        for point in input_items:
            x, y = list(map(float, point.split(',')))
            label_points.append((round(x), round(y)))

        labels.append((label_name, label_type, label_type_params, label_color, label_points))

    return labels


def create_masks(parsed_labels: list[ParsedLabel], image_width: int, image_height: int) -> dict[str: list[np.ndarray]]:
    masks = {parsed_label[0]: [] for parsed_label in parsed_labels}

    for label_name, label_type, label_type_params, label_color, label_points in parsed_labels:
        img = PIL.Image.new('L', (image_width, image_height), 0)

        if label_type == 'polygon':
            PIL.ImageDraw.Draw(img).polygon(label_points, outline=1, fill=1)
        elif label_type == 'line':
            width = t if (t := label_type_params.get('width')) else 1
            PIL.ImageDraw.Draw(img).line(label_points, fill=1, width=width)
        else:
            raise ValueError(f'Unknown label type "{label_type}".')

        img = np.array(img)
        masks[label_name].append(img)

    return masks


def flatten_masks(input_masks: dict[str: list[np.ndarray]]) -> dict[str: np.ndarray]:
    flattened_masks = {}
    for label, masks in input_masks.items():
        flattened_masks[label] = np.sum(np.dstack(masks), axis=2)

    for label, mask in flattened_masks.items():
        flattened_masks[label] = mask > 0

    return flattened_masks


def overlay_rgb_mask(rgb: np.ndarray, masks: dict[str, np.ndarray], label_colors: dict[str, tuple[int, int, int]],
                     mask_opacity: float = 0.75, legend: bool = False, legend_title: str = 'Masked RGB'):
    """
    Overlay mask on an RGB image.
    """

    def create_alpha_mask(mask: np.ndarray, fill: tuple[int, int, int] = (255, 0, 0), alpha: float = 0.50):
        """
        Create a mask image with an alpha channel. The stupid way.
        """
        import numpy as np

        mask_alpha = np.zeros((mask.shape[0], mask.shape[1], 4), 'uint8')
        mask_alpha[:, :, 0] = mask * fill[0]
        mask_alpha[:, :, 1] = mask * fill[1]
        mask_alpha[:, :, 2] = mask * fill[2]
        mask_alpha[mask, 3] = round(255 * alpha)

        return mask_alpha

    def generate_label_legend(variables: list[str], labeled_image: np.ndarray,
                              legend_footer: str = 'unnamed classifier',
                              font_name: str = 'calibri.ttf', font_size_label: int = 24, font_size_tag: int = 16):
        font = PIL.ImageFont.truetype(font_name, font_size_label)
        image = PIL.Image.new('RGB', (250, labeled_image.shape[0]), (255, 255, 255))
        draw = PIL.ImageDraw.Draw(image)
        for i, e in enumerate(sorted(variables)):
            draw.rectangle((10, 25 + 32 * i, 55, 20 + 32 * i + 32), label_colors[e], (0, 0, 0))
            draw.text((60, 27 + 32 * i), e, (0, 0, 0), font)

        if legend_footer is not None:
            font_tag = PIL.ImageFont.truetype(font_name, font_size_tag)
            size = draw.textsize(legend_footer, font_tag)
            draw.text((image.size[0] - size[0] - 10, image.size[1] - size[1] - 10),
                      legend_footer, (0, 0, 0), font_tag)

        return np.asarray(image)

    alpha_masks = []
    labels = []

    for mask_class in masks.keys():
        alpha_masks.append(create_alpha_mask(masks[mask_class], label_colors[mask_class]))
        labels = list(masks.keys())

    if rgb.dtype != 'uint8':
        print('RGB: {}, {}'.format(rgb.shape, rgb.dtype))
    if rgb.dtype == 'float64':
        rgb = rgb * (2 ** 8 - 1)
        rgb = rgb.astype('uint8')

    if legend:
        legend_image = generate_label_legend(labels, np.zeros_like(rgb[:, :, 0]), legend_title)
        rgb = np.hstack((rgb, legend_image))
        dummy_image = np.zeros((legend_image.shape[0], legend_image.shape[1], 4), 'uint8')
        dummy_image[:, :, 3] = 255
        old_alpha_masks = alpha_masks
        alpha_masks = []
        for alpha_mask in old_alpha_masks:
            alpha_masks.append(np.hstack((alpha_mask, dummy_image)))

    composite = PIL.Image.fromarray(rgb, 'RGB')
    composite.putalpha(255)
    for alpha_mask in alpha_masks:
        mask_image = PIL.Image.fromarray(alpha_mask)
        mask_image.putalpha(mask_image.convert('L'))
        composite = PIL.Image.alpha_composite(composite, mask_image)
    return np.asarray(composite)
