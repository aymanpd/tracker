

import json
from datetime import datetime
import matplotlib.pyplot as plt

import seaborn as sns
from functools import wraps
from IPython.display import IFrame, display, HTML


def __save_plot__(func):
    @wraps(func)
    def save_plot_wrapper(*args, **kwargs):
        sns.mpl.pyplot.show()
        sns.mpl.pyplot.close()
        res = func(*args, **kwargs)
        if len(res) == 2:
            (vis_object, name), res, cfg = res, None, None
        elif len(res) == 3:
            (vis_object, name, res), cfg = res, None
        else:
            vis_object, name, res, cfg = res
        idx = 'id: ' + str(int(datetime.now().timestamp()))
        coords = vis_object.axis()

        vis_object.get_figure().savefig(name, bbox_inches="tight", dpi=cfg.get('save_dpi') or 200)
        return res

    return save_plot_wrapper


class ___FigureWrapper__(object):
    def __init__(self, fig):
        self.fig = fig

    def get_figure(self):
        return self.fig

    def axis(self):
        if len(self.fig.axes) > 1:
            x = self.fig.axes[1].axis()
        else:
            x = self.fig.axes[0].axis()
        return (x[0] / 64, x[0] + (x[1] - x[0]) / 50, x[2] / 1.5, x[3] / 1.5)

    def text(self, *args, **kwargs):
        self.fig.text(*args, **kwargs)

