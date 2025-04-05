from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import networkx as nx

def show_graph(sprite_dict : dict) -> None:
    """Creates a graphical output displaying sprites, events and messages.
    Each node represents either a sprite, an event, or a broadcast message:
      - Sprites are shown in sky blue.
      - Events are shown in gold.
      - Broadcast messages are shown in orange.

    Directed edges connect:
      - Events with Sprites (when an event triggers a sprite)
      - Sprites with Broadcast Messages (when a sprite sends a message)

    Args:
        sprite_dict (dict): A dictionary where each key is a sprite's name, and the value is another
                            dictionary with:
                                - 'events': A list of tuples representing events and their parameters.
                                - 'broadcasts_sent': A list of broadcast message names sent by the sprite.

    Returns:
        None
    """
    G = nx.DiGraph()

    for sprite_name, value in sprite_dict.items():
        # Draw sprite
        G.add_node(sprite_name, color="skyblue")

        # Draw events
        events = value["events"]
        for event in events:
            event_label = "\n".join(str(part) for part in event) 
            G.add_node(event_label, color="gold")
            G.add_edge(event_label, sprite_name, color="gold")

        # Draw broadcasts
        broadcasts_sent = value["broadcasts_sent"]
        for broadcast in broadcasts_sent:
            broadcast_name = broadcast[0]
            G.add_node(broadcast_name, color="orange")
            G.add_edge(sprite_name, broadcast_name, color="orange")

    pos = nx.spring_layout(G, k=2, scale=2.5)
    node_colors = [G.nodes[n]["color"] for n in G.nodes()]
    edge_colors = [G[u][v]["color"] for u, v in G.edges()]

    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=7000,
        font_weight='bold',
        arrows=True,
        arrowsize=30,
        width=2.5
    )

    # Add the legend to the plot
    legend_elements = [
        Patch(facecolor='skyblue', label='Sprite'),
        Patch(facecolor='gold', label='Event'),
        Patch(facecolor='orange', label='Broadcasted Message')
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    plt.show()