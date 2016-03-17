#! /usr/bin/env python3
from __future__ import print_function

import os.path
from argparse import ArgumentParser

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def image_to_wiggle(filename, skip=1):
    image = Image.open(filename, 'r').convert(mode='L')
    shape = (image.height, image.width)
    pixels = np.asarray(image.getdata(), dtype=np.float64).reshape(shape)
    pixels = (pixels.T - 127.5) / 127.5 # -1 < pixel < 1

    fig, ax = plt.subplots()

    y = np.arange(image.height, 0, -1)

    for i, trace in enumerate(pixels[::skip, :]):
        offset = i * 2
        x = trace + offset

        ax.plot(x, y, 'k-')
        ax.fill_betweenx(y, offset, x, where=(x < offset), color='k')

    ax.set_xlim(0, image.width * 2 / skip)
    ax.set_ylim(0, image.height)

    fig.canvas.set_window_title("{} wiggle".format(*os.path.splitext(filename)))
    print("Supported output formats:", *sorted(fig.canvas.get_supported_filetypes().keys()))
    plt.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename', help="image path")
    parser.add_argument('--skip', type=int, default=1, help="trace increment")

    args = parser.parse_args()

    image_to_wiggle(args.filename, args.skip)
