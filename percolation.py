from collections import deque
import enum
import queue
import random

# Percolation idea explanation by James Riely: https://youtu.be/KNgfOmlLgh8
# Union-Find data structure concept explanation: https://en.wikipedia.org/wiki/Disjoint-set_data_structure


class VisitStatus(enum.Enum):
    closed = "C"
    open = ' '
    visited = 'V'


class Square:
    def __init__(self):
        self.status = VisitStatus.closed
        self.parent = None
        self.size = 0
        self.number = 0

    def get_status(self): return self.status.value
    def set_status(self, status): self.status = status
    def get_parent(self): return self.parent
    def set_parent(self, parent_square): self.parent = parent_square
    def get_size(self) -> int: return self.size
    def set_size(self, size): self.size = size
    def get_number(self): return self.number
    def set_number(self, number): self.number = number


class Grid:
    def __init__(self, n):
        self.n = n
        self.board = []
        self.adj_list = {}
        # self.sets holds the root nodes of all of the sets logic for who belongs to what set is determined by Find
        self.sets = []
        for i in range(n):
            row = []
            for j in range(n):
                new_square = Square()
                row.append(new_square)
                self.adj_list[new_square] = []
            self.board.append(row)

    def get_board(self) -> list: return self.board

    def get_square(self, i, j) -> Square: return self.board[i][j]

    def get_square_status(self, i, j): return self.board[i][j].get_status()

    # if necessary, could make this return a map of directions to squares
    def get_open_neighbors(self, row, column) -> list:
        neighbors = []
        if row > 0:
            # Check up
            neigh = self.get_square(row-1, column)
            if neigh.get_status() == ' ':
                neighbors.append(neigh)
        if row < (self.n - 1):
            # Check down
            neigh = self.get_square(row + 1, column)
            if neigh.get_status() == ' ':
                neighbors.append(neigh)
        if column > 0:
            # Check left
            neigh = self.get_square(row, column - 1)
            if neigh.get_status() == ' ':
                neighbors.append(neigh)
        if column < (self.n -1):
            # Check right
            neigh = self.get_square(row, column + 1)
            if neigh.get_status() == ' ':
                neighbors.append(neigh)
        return neighbors

    def visualize_board(self):
        visual = []
        for i in range(self.n):
            x = []
            for j in range(self.n):
                x.append(self.board[i][j].get_status())
            visual.append(x)
        for row in visual:
            print(*row)
        print("- " * self.n)

    def write_board(self, c: int, n: int):
        outfile = open("percolation_sample", "w")
        visual = []
        for i in range(self.n):
            x = []
            for j in range(self.n):
                x.append(self.board[i][j].get_status())
            visual.append(x)
        for row in visual:
            for square in row:
                outfile.write(str(square))
            outfile.write("\n")
        outfile.write(f"Percolation achieved in {n} x {n} graph after {c} iterations" + "\n")
        outfile.write(f"{c/(n**2)}% of graph opened")

    def make_set(self, node: Square):
        # parent is itself
        node.set_parent(node)
        node.set_size(1)
        self.sets.append(node)

    def union(self, x: Square, neighbor: Square):
        x_root = find(x)
        n_root = find(neighbor)
        # If x is not in the same set as neighbor
        if x_root is not n_root:
            if n_root.get_size() > x_root.get_size():
                x_root.set_parent(n_root)
                n_root.set_size(n_root.get_size() + x_root.get_size())
                self.sets.remove(x_root)
            else:
                n_root.set_parent(x_root)
                x_root.set_size(n_root.get_size() + x_root.get_size())
                self.sets.remove(n_root)

    def percolation_check(self):
        # n^2 bottleneck, could be optimized
        for top_row_node in self.board[0]:
            for bot_row_node in self.board[self.n-1]:
                if same_set(top_row_node, bot_row_node):
                    return True
        return False


def same_set(x: Square, y: Square) -> bool:
    x_find = find(x)
    y_find = find(y)
    if x_find is not None and y_find is not None:
        if x_find == y_find:
            return True
    return False


def find(node: Square):
    current_node = node
    if current_node.get_status() != "C":
        while current_node.get_parent() != current_node:
            current_node = current_node.get_parent()
        return current_node
    return None


def bfs(source: Square, grid: Grid):
    visited = []
    parent_map = {}
    top_node = None
    bot_node = None
    visited.append(source)
    queue_list = [source]
    d = deque(queue_list)
    while top_node is None or bot_node is None:
        current = d.popleft()
        visited.append(current)
        for neighbor in grid.adj_list[current]:
            if neighbor not in visited:
                d.append(neighbor)
                parent_map[neighbor] = current
        if current in grid.board[0]:
            top_node = current
        if current in grid.board[grid.n-1]:
            bot_node = current
    return parent_map, top_node, bot_node









def main(n: int):
    percolated = False
    grid = Grid(n)
    c = 0
    while not percolated:
        row = random.randint(0, n-1)
        column = random.randint(0, n-1)
        node = grid.get_square(row, column)
        if node.get_status() == "C":
            node.set_status(VisitStatus.open)
            grid.make_set(node)
            node_neighbors = grid.get_open_neighbors(row, column)
            for neighbor in node_neighbors:
                # node just opened. Thus, it will NOT be in any adj_list of any neighbors. Shouldn't need check
                # if node is already in the adj_list for neighbors
                grid.adj_list[neighbor].append(node)
                if neighbor not in grid.adj_list[node]:
                    grid.adj_list[node].append(neighbor)
                grid.union(node, neighbor)
            if grid.percolation_check():
                # node is the source node for BFS
                percolated = True
            c += 1
    node.set_status(VisitStatus.visited)
    path_info = bfs(node, grid)
    parent_map = path_info[0]
    top_current = path_info[1]
    bot_current = path_info[2]
    while top_current is not node:
        top_current.set_status(VisitStatus.visited)
        top_current = parent_map[top_current]
    while bot_current is not node:
        bot_current.set_status(VisitStatus.visited)
        bot_current = parent_map[bot_current]
    grid.write_board(c, n)
    grid.visualize_board()
    print(f"Percolation achieved in {c} iterations")
    print(f"{c/(n**2)}% of graph opened")

main(25)