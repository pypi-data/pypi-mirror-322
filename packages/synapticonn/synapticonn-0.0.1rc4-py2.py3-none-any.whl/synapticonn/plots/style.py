""" Style and aesthetics definitions for plots. """

import pathlib
import pkg_resources

from functools import wraps

import matplotlib.pyplot as plt


###################################################################
###################################################################


def apply_plot_style(style_path=None):
    """Decorator to apply matplotlib style before a plotting function."""

    if style_path is None:
        style_path = pkg_resources.resource_filename('synapticonn.plots', 'settings.mplstyle')

    def decorator_plot_style(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            plt.style.use(style_path)
            return func(*args, **kwargs)
        return wrapper
    return decorator_plot_style