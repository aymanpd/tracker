

import os
import pandas as pd
from .core_functions.base_dataset import BaseDataset

config = {'experiments_folder': 'experiments'}

if not os.path.exists(config['experiments_folder']):
    os.mkdir(config['experiments_folder'])


try:
    #delete the accessor to avoid warning 
    del pd.DataFrame.rete
except AttributeError:
    pass


@pd.api.extensions.register_dataframe_accessor("rete")
class TrackerDataset(BaseDataset):

    def __init__(self, pandas_obj):
        super(TrackerDataset, self).__init__(pandas_obj)
        self.retention_config = config



