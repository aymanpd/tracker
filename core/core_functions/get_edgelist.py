
import pandas as pd


def get_edgelist(self, *,
                 weight_col=None,
                 norm_type=None,
                 edge_attributes='edge_weight'):
    """
    Creates weighted table of the transitions between events.

    Parameters
    ----------
    weight_col: str (optional, default=None)
        Aggregation column for transitions weighting. To calculate weights
        as number of transion events use None. To calculate number
        of unique users passed through given transition 'user_id'.
         For any other aggreagtion, like number of sessions, pass the column name.

    norm_type: {None, 'full', 'node'} (optional, default=None)
        Type of normalization. If None return raw number of transtions
        or other selected aggregation column. 'full' - normalized over
        entire dataset. 'node' weight for edge A --> B normalized over
        user in A

    edge_attributes: str (optional, default 'edge_weight')
        Name for edge_weight columns

    Returns
    -------
    Dataframe with number of rows equal to all transitions with weight
    non-zero weight

    Return type
    -----------
    pd.DataFrame
    """
    if norm_type not in [None, 'full', 'node']:
        raise ValueError(f'unknown normalization type: {norm_type}')

    event_col = self.retention_config['event_col']
    time_col = self.retention_config['event_time_col']
    # print("event_col", event_col)
    cols = [event_col, 'next_' + str(event_col)]
    # print("cols", cols)
    data = self._get_shift().copy()
    # print("data", data)


    # get aggregation:
    # group by both columns (event, nextevent)
    if weight_col is None:
        agg = (data
               .groupby(cols)[time_col]
               .count()
               .reset_index())
        agg.rename(columns={time_col: edge_attributes}, inplace=True)
    else:
        agg = (data
               .groupby(cols)[weight_col]
               .nunique()
               .reset_index())
        agg.rename(columns={weight_col: edge_attributes}, inplace=True)

    # print("agg", agg)
    # apply normalization:
    if norm_type == 'full':
        if weight_col is None:
            agg[edge_attributes] /= agg[edge_attributes].sum()
        else:
            agg[edge_attributes] /= data[weight_col].nunique()
        agg[edge_attributes] = (round(agg[edge_attributes] * 100, 3))

    if norm_type == 'node':
        if weight_col is None:
            event_transitions_counter = data.groupby(event_col)[cols[1]].count().to_dict()
            agg[edge_attributes] /= agg[cols[0]].map(event_transitions_counter)
        else:
            user_counter = data.groupby(cols[0])[weight_col].nunique().to_dict()
            agg[edge_attributes] /= agg[cols[0]].map(user_counter)
        agg[edge_attributes] = (round(agg[edge_attributes] * 100, 3))
    return agg
