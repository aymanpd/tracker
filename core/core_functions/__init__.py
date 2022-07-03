
from .base_dataset import BaseDataset

from .get_edgelist import get_edgelist
from .get_adjacency import get_adjacency
from .get_clusters import get_clusters, filter_cluster
from .plot_graph import plot_graph
from .extract_features import extract_features
from .funnel import funnel


BaseDataset.get_edgelist = get_edgelist
BaseDataset.get_adjacency = get_adjacency
BaseDataset.get_clusters = get_clusters
BaseDataset.filter_cluster = filter_cluster
BaseDataset.plot_graph = plot_graph
BaseDataset.extract_features = extract_features
BaseDataset.funnel = funnel
