
import pandas as pd


class BaseDataset(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self.retention_config = {}
        self.segments = {}
        

    def _get_shift(self, *,
                   index_col=None,
                   event_col=None):
        index_col = index_col or self.retention_config['user_col']
        event_col = event_col or self.retention_config['event_col']
        time_col = self.retention_config['event_time_col']

        data = self._obj.copy()
        data.sort_values([index_col, time_col], inplace=True)
        shift = data.shift(-1)
        # print("data", data)
        # print("shift", shift)
        data['next_'+event_col] = shift[event_col]
        data['next_'+str(time_col)] = shift[time_col]

        return data

