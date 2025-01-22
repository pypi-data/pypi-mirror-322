"""
hurley-generic-plot: Just some generic functions to make plots
"""

__version__ = "0.1.6"

from .clinical import plot_CFB, plot_response
from .generic import plot_correlation, plot_bar_from_baseline

__all__ = ['clinical', 'generic'] 