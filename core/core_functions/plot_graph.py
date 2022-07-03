
import networkx as nx
import netgraph
import matplotlib.pyplot as plt

def plot_graph(self, *,
               weight_col=None,
               norm_type='full',
               layout_dump=None,
               width=800,
               height=500,
               thresh=0):
    """
    Create interactive graph visualization. Each node is a unique event_col
    value, edges are transitions between events and edge weights are calculated
    metrics. By default, it is a percentage of unique users that have passed
    though a particular edge visualized with the edge thickness. Node sizes are
    Graph loop is a transition to the same node, which may happen if users
    encountered multiple errors or made any action at least twice. Graph nodes
    are movable on canvas which helps to visualize user trajectories but is also
    a cumbersome process to place all the nodes so it forms a story.

    That is why IFrame object also has a download button. By pressing it, a JSON
    configuration file with all the node parameters is downloaded. It contains
    node names, their positions, relative sizes and types. It it used as
    layout_dump parameter for layout configuration. Finally, show weights
    toggle shows and hides edge weights.

    Parameters
    ----------
    norm_type: str (optional, default 'full')
        Type of normalization used to calculate weights for graph edges. Possible
        values are:
            * None
            * 'full'
            * 'node'

    weight_col: str (optional, default None)
        Aggregation column for edge weighting. If None, number of events will be
        calculated. For example, can be specified as `client_id` or `session_id`
        if dataframe has such columns.

    thresh: float (optional, default 0.01)
        Minimal edge weight value to be rendered on a graph. If a node has no
        edges of the weight >= thresh, then it is not shown on a graph. It
        is used to filter out rare event and not to clutter visualization. Nodes
        specified in targets parameter will be always shown regardless selected
        threshold.

    layout_dump: str (optional, default None)
        Path to layout configuration file relative to current directory. If
        defined, uses configuration file as a graph layout.

    width: int (optional, default 800)
        Width of plot in pixels.

    height: int (optional, default 500)
        Height of plot in pixels.
    """

    event_col = self.retention_config['event_col']

    # TODO: change downstream processing

    node_weights = self._obj[event_col].value_counts().to_dict() # count of events {event: count}
    # print("node_weights", node_weights)

    data = self.get_edgelist(weight_col=weight_col,   #df [event nextevent edgeweight]
                             norm_type=norm_type)

    G = nx.from_pandas_edgelist(data[:20], "event", "next_event", ["event", "next_event", "edge_weight"], create_using=nx.DiGraph())
    labels = nx.get_edge_attributes(G, "edge_weight")

    plt.figure(figsize=(15,15), dpi=60) 
    
    plot_instance = netgraph.InteractiveGraph(
        G, node_size=8,
        node_labels=True, arrows=True, edge_layout="curved", edge_labels=labels, origin=(0, 0))
    plt.show()
    return plot_instance