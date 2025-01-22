import numpy
import math

TWO_PI = 2 * numpy.pi
SQRT_2 = math.sqrt(2)


def wrapTo2pi(x):
    """
    Python implementation of Matlab method `wrapTo2pi`.
    Wraps angles in x, in radians, to the interval [0, 2*pi] such that 0 maps
    to 0 and 2*pi maps to 2*pi. In general, positive multiples of 2*pi map to
    2*pi and negative multiples of 2*pi map to 0.
    """
    xwrap = numpy.remainder(x - numpy.pi, TWO_PI)
    mask = numpy.abs(xwrap) > numpy.pi
    xwrap[mask] -= TWO_PI * numpy.sign(xwrap[mask])
    return xwrap + numpy.pi


def compute_hsv(dim1_data: numpy.ndarray, dim2_data: numpy.ndarray):
    data = numpy.arctan2(-dim1_data, -dim2_data)

    hue = wrapTo2pi(data) / TWO_PI
    saturation = (
        numpy.sqrt(numpy.power(dim1_data, 2) + numpy.power(dim2_data, 2)) / SQRT_2
    )
    value = numpy.ones_like(dim1_data)

    return numpy.stack(
        (
            hue,
            saturation,
            value,
        ),
        axis=2,
    )
