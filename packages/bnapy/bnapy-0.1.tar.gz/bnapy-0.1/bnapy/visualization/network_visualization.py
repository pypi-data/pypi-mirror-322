def plot_group_network(df,groups,col1,col2,pruned=None,node_colors=None,\
                       edge_widths=lambda x: 1,plot_weights=None):
    """
    plots group-level bipartite networks projected w.r.t. col1 and col2
    inputs:
        df is student dataset
        groups is list of group names (strings) for which we want to plot networks
        col1, col2 are strings specifying bipartite projection of interest
        pruned specifies whether or not we want to prune the network first by keeping 
            only significant edges
            if not None, takes dict of kwargs from prune_edges function 
        node_colors is dict of form {node name:color}
        edge_widths is function that takes edge weight to edge width
        plot_weights will add task weights if tasks are plotted as a node set
    returns:
        plot of bipartite networks across specified groups
    """
    ########################################
    ###use package for this (maybe networkx)
    ########################################
    return 1