import matplotlib.pyplot as plt
import networkx as nx
import os
from graphviz import Digraph


class TSPVisualizer:
    def visualize_graph(self, n, coords, matrix, folder_path):
        plt.figure(figsize=(10, 8))
        G = nx.Graph()
        for i in range(n):
            label = chr(65 + i)
            G.add_node(label, pos=(coords[i][0], coords[i][1]))

        pos = nx.get_node_attributes(G, 'pos')
        for i in range(n):
            for j in range(i + 1, n):
                G.add_edge(chr(65 + i), chr(65 + j))

        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray', style='dashed')

        plt.grid(True, linestyle='--', alpha=0.6)
        plot_file = os.path.join(folder_path, f"graph_connectivity_n{n}.png")
        plt.savefig(plot_file)
        plt.close()

    def visualize_tree(self, node_data, folder_path, n, best_cost_final, best_path_nodes):
        dot = Digraph(comment='TSP State Space Tree')
        dot.attr(rankdir='TB', size='20,20', dpi='300')
        dot.attr('node', shape='ellipse', style='filled', fontname='Arial')

        for p_id, c_id, edge_lab, cost, _, _ in node_data:
            node_label = f"ID: {c_id}\nLB: {cost:.2f}"
            is_best = c_id in best_path_nodes

            if is_best:
                dot.node(str(c_id), node_label, fillcolor='#98fb98', color='#2e8b57', penwidth='2')
            elif cost > best_cost_final:
                dot.node(str(c_id), node_label, fillcolor='#ffcccb', color='#ff0000')
            else:
                dot.node(str(c_id), node_label, fillcolor='#e1f5fe', color='#01579b')

            if p_id is not None:
                e_color = '#2e8b57' if is_best else '#555555'
                e_width = '2.5' if is_best else '1.0'
                dot.edge(str(p_id), str(c_id), label=edge_lab, color=e_color, penwidth=e_width)

        output_path = os.path.join(folder_path, f'tree_n{n}_final')
        dot.render(output_path, format='png', cleanup=True)