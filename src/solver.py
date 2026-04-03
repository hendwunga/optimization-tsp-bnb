import numpy as np
import heapq
from utils import reduce_matrix, calculate_cost
from node import Node
from scipy.spatial.distance import cdist

class TSPSolver:
    def generate_matrix(self, n, seed=42):
        np.random.seed(seed)
        coords = np.random.randint(1, 101, size=(n, 2))
        matrix = cdist(coords, coords, metric='euclidean')
        np.fill_diagonal(matrix, float('inf'))
        return matrix, coords

    def solve_tsp(self, adj_matrix):
        nodes_explored = 0
        n = len(adj_matrix)
        adj_matrix = np.array(adj_matrix, dtype=float)
        original_matrix = adj_matrix.copy()

        tree_data = []
        node_counter = 1

        root_matrix, initial_reduction = reduce_matrix(adj_matrix.copy())
        root = Node(root_matrix, initial_reduction, [0], 0, 0)
        root.id = node_counter

        pq = []
        heapq.heappush(pq, root)
        tree_data.append((None, root.id, "Start: A", root.cost, False, False))

        best_solution = float('inf')
        best_path = []

        while pq:
            current_node = heapq.heappop(pq)
            nodes_explored += 1

            if current_node.cost >= best_solution:
                continue

            if current_node.level == n - 1:
                last_city = current_node.current_city
                return_dist = original_matrix[last_city, 0]
                final_cost = current_node.cost + return_dist

                if final_cost < best_solution:
                    best_solution = final_cost
                    best_path = current_node.path + [0]
                continue

            for next_city in range(n):
                if next_city not in current_node.path:
                    node_counter += 1
                    child_cost, child_matrix = calculate_cost(
                        current_node.matrix,
                        current_node.current_city,
                        next_city,
                        current_node.cost
                    )

                    child_node = Node(child_matrix, child_cost, current_node.path + [next_city], current_node.level + 1, next_city)
                    child_node.id = node_counter
                    child_node.parent_id = current_node.id
                    heapq.heappush(pq, child_node)

                    edge_label = f"X{child_node.level}={chr(65 + next_city)}"
                    tree_data.append((current_node.id, child_node.id, edge_label, round(child_cost, 2), False, False))

        return best_path, best_solution, nodes_explored, tree_data