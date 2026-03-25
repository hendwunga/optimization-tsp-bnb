class Node:
    def __init__(self, matrix, cost, path, level, current_city):
        self.matrix = matrix        # Matriks tereduksi simpul ini
        self.cost = cost            # Lower Bound (LB)
        self.path = path            # Jalur yang sudah dilalui
        self.level = level          # Kedalaman pohon
        self.current_city = current_city

    # Agar PriorityQueue mengurutkan berdasarkan cost (LB) terkecil
    def __lt__(self, other):
        return self.cost < other.cost