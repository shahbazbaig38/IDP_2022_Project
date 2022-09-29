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
# Functions to read spectral images from ENVI-files.
#
# Main functions:
#   read_envi           read an ENVI-file into a numpy ndarray
#   read_zipped_envi    read an ENVI-file into a numpy ndarray from a zip-file
#
# The other functions are intended as private functions to be used from the
# two main functions and should not be used outside this module.
#
# 2022-09-05 Prepare file for Industrial Project course
# 2022-05-20 Fix raw data suffix selection
#            Specim IQ does not terminate the last line
# 2022-01-31 Initial version

from __future__ import annotations

import decimal
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import dateutil.parser
import numpy as np


def normalize_envi_cube(header, cube):
    if cube.dtype == 'uint8':
        return cube.astype('float64') / (2**8 - 1)

    elif cube.dtype == 'uint16':
        # Specim IQ has a 12-bit sensor:
        if header.get('sensor type').lower() == 'specim iq':
            cube = cube << 4
        return cube.astype('float64') / (2**16 - 1)

    else:
        raise ValueError(f'Unhandled cube dtype: {cube.dtype}')


def read_envi(header_file: Path, normalize=True):
    header = parse_envi_header(header_file.read_text('utf-8'))

    cube = None
    for raw_data_suffix in ['.raw', '.dat', '.img']:
        if (raw_data_file := header_file.with_suffix(raw_data_suffix)).exists():
            cube = bytes_to_cube(header, raw_data_file.read_bytes())
            break

    if cube is None:
        raise FileNotFoundError(f'Could not find data file for header {header_file}')

    if normalize:
        cube = normalize_envi_cube(header, cube)

    return cube, np.array(header['wavelength'], 'float32'), header


def read_zipped_envi(zipfile: ZipFile, header_file: Path, normalize=True):
    with zipfile.open(header_file.as_posix()) as zip_header_file:
        header_bytes = zip_header_file.read()
    for raw_data_suffix in ['.raw', '.dat']:
        try:
            raw_info = zipfile.getinfo(header_file.with_suffix(raw_data_suffix).as_posix())
            break
        except KeyError:
            raw_info = None
    if raw_info is None:
        raise FileNotFoundError('Failed to determine raw data file.')
    with zipfile.open(raw_info) as zip_raw_file:
        raw_bytes = zip_raw_file.read()

    header = parse_envi_header(header_bytes.decode('utf-8'))
    cube = bytes_to_cube(header, raw_bytes)

    if normalize:
        cube = normalize_envi_cube(header, cube)

    return cube, np.array(header['wavelength']).astype('float32'), header


def parse_envi_header(to_be_parsed: str) -> dict:
    def fix_header_field_types(stringy_header: dict[str, str | list[str]]) -> dict[str, Any]:
        field_types = {
            'acquisition time': dateutil.parser.isoparse,
            'bands': int,
            'byte order': int,
            'data gain values': float,
            'data type': int,
            'fwhm': float,
            'lines': int,
            'samples': int,
            'wavelength': float,

            # Senop HSC-2
            'senop acquisition mode': int,
            'senop frame counter': int,
            'senop integration time': float,
            'senop order': int,
            'senop sequence order': int,
            'senop timestamp': int,
            'senop acceleration': lambda x: tuple(map(decimal.Decimal, x.split(','))),
            'senop gyroscope': lambda x: tuple(map(decimal.Decimal, x.split(','))),
        }
        for f, t in field_types.items():
            if f in stringy_header:
                if isinstance(stringy_header[f], list):
                    stringy_header[f] = list(map(t, stringy_header[f]))
                else:
                    stringy_header[f] = t(stringy_header[f])
        return stringy_header

    # assignment -> { " " | "\t" } "=" { " " | "\t" }
    def parse_assignment(s: str) -> tuple[str, str]:
        i = 0
        while s[i] in [' ', '\t']:
            i = i + 1
        if s[i] != '=':
            raise ValueError('Expected "="')
        i = i + 1
        while s[i] in [' ', '\t']:
            i = i + 1
        return s[i:], s[:i]

    # identifier -> { ^"=" }
    def parse_identifier(s: str) -> tuple[str, str]:
        i = 0
        while s[i] != '=':
            i = i + 1
        return s[i:], s[:i].strip()

    # value -> *\n | "{" ? "}"
    def parse_value(s: str) -> tuple[str, str | list[str]]:
        def parse_list(ls: str) -> tuple[str, list[str]]:
            values = []
            i = 1
            while ls[i] != '}':
                s = i
                e = 1
                while ls[i] != ',' and ls[i] != '}':
                    if ls[i] == '"':
                        i = i + 1
                        s = i
                        while ls[i] != '"':
                            i += 1
                        e = i
                        i += 1
                    else:
                        i += 1
                        e = i
                values.append(ls[s:e].strip())
                if ls[i] == ',':
                    i = i + 1
            if ls[i:i + 2] != '}\n':
                raise ValueError('Expected }')
            return ls[i + 2:], values

        if s[0] == '{':
            return parse_list(to_be_parsed)
        i = 0
        while s[i] != '\n':
            i = i + 1
        return s[i + 1:], s[:i]

    # Ditch DOS/Windows line ends for Unixy approach
    to_be_parsed = to_be_parsed.replace('\r\n', '\n')
    # Force new line character as a line terminator
    if to_be_parsed[-1] != '\n':
        to_be_parsed += '\n'

    if to_be_parsed[:5] != 'ENVI\n':
        raise ValueError('Expected ENVI.')
    to_be_parsed = to_be_parsed[5:]

    # header <- { identifier assignment value }
    header = {}
    while len(to_be_parsed) > 0:
        to_be_parsed, ident = parse_identifier(to_be_parsed)
        to_be_parsed, _ = parse_assignment(to_be_parsed)
        to_be_parsed, value = parse_value(to_be_parsed)
        header[ident] = value

    header = fix_header_field_types(header)

    return header


def bytes_to_cube(header: dict[str, Any], b: bytes) -> np.ndarray:
    if (header_byte_order := header['byte order']) == 0:
        byte_order = '<'
    elif header_byte_order == 1:
        byte_order = '>'
    else:
        raise ValueError(f'Unknown byte order {header_byte_order}')

    if (header_data_type := header['data type']) == 1:
        data_type = 'u1'
    elif header_data_type == 2:
        data_type = 's2'
    elif header_data_type == 3:
        data_type = 's4'
    elif header_data_type == 4:
        data_type = 'f4'
    elif header_data_type == 5:
        data_type = 'f8'
    elif header_data_type == 12:
        data_type = 'u2'
    else:
        raise ValueError(f'Unknown data type {header_data_type}.')

    dtype = np.dtype(f'{byte_order}{data_type}')
    rows = header['lines']
    cols = header['samples']
    bands = header['bands']

    data = np.frombuffer(b, dtype)

    if (header_interleave := header['interleave'].lower()) == 'bil':
        # BIL stack has the images laid out horizontally in a (rows, cols * bands) matrix
        data = data.reshape((rows, cols * bands))
        data = data.reshape(rows, cols, bands, order='F')

    elif header_interleave == 'bip':
        data = data.reshape((bands, rows * cols), order='F')
        data = data.reshape(bands, rows, cols, order='C')

    elif header_interleave == 'bsq':
        # BSQ stack has the band images layered sequentially (rows, cols, bands)
        data = data.reshape((bands, rows, cols))
        data = np.swapaxes(data, 0, 2)
        data = np.swapaxes(data, 0, 1)

    else:
        raise ValueError(f'Unknown interleave {header_interleave}.')

    return data
