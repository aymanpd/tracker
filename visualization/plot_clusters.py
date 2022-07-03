

from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import seaborn as sns

from .plot_utils import __save_plot__, ___FigureWrapper__


@__save_plot__
def cluster_bar(data, *,
                clusters,
                target,
                target_names,
                plot_name=None,
                **kwargs):
    """
    Plots bar charts with cluster sizes and average target conversion rate.
    Parameters
    ----------
    data : pd.DataFrame
        Feature matrix.
    clusters : np.array
        Array of cluster IDs.
    target: np.array
        Boolean vector, if ``True``, then user has `positive_target_event` in trajectory.

    target: list of np.arrays
        Boolean vector, if ``True``, then user has `positive_target_event` in trajectory.


    plot_name : str, optional
        Name of plot to save. Default: ``'clusters_bar_{timestamp}.svg'``
    kwargs: optional
        Width and height of plot.
    Returns
    -------
    Saves plot to ``retention_config.experiments_folder``
    Return type
    -------
    PNG
    """
    cl = pd.DataFrame([clusters, *target], index=['clusters', *target_names]).T
    cl['cluster size'] = 1
    for t_n in target_names:
        cl[t_n] = cl[t_n].astype(int)

    bars = cl.groupby('clusters').agg({
        'cluster size': 'sum',
        **{t_n: 'mean' for t_n in target_names}
    }).reset_index()
    bars['cluster size'] /= bars['cluster size'].sum()

    bars = bars.melt('clusters', var_name='type', value_name='value')
    bars = bars[bars['type'] != ' '].copy()

    fig_x_size = round((1 + bars['clusters'].nunique()**0.7 * bars['type'].nunique()**0.7))
    rcParams['figure.figsize'] = fig_x_size, 6

    bar = sns.barplot(x='clusters', y='value', hue='type', data=bars)

    # move legend outside the box
    bar.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    y_value = ['{:,.2f}'.format(x * 100) + '%' for x in bar.get_yticks()]

    bar.set_yticks(bar.get_yticks().tolist())
    bar.set_yticklabels(y_value)
    bar.set(ylabel=None)

    # adjust the limits
    ymin, ymax = bar.get_ylim()
    if ymax > 1:
        bar.set_ylim(ymin, 1.05)

    plot_name = plot_name or 'cluster_bar_{}'.format(datetime.now()).replace(':', '_').replace('.', '_') + '.svg'
    plot_name = data.rete.retention_config['experiments_folder'] + '/' + plot_name
    return bar, plot_name, None, data.rete.retention_config












