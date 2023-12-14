class Graph:
    def __init__(self, size: int):
        self.adjacency_list: dict[int, set[int]] = {}
        self.visited: dict[int, bool] = {}

        for i in range(size):
            self.adjacency_list[i] = set()
            self.visited[i] = False

    def add_edge(self, start_edge: int, end_edge: int):
        self.adjacency_list[start_edge].add(end_edge)

    def dfs_po(self, node: int, postorder):
        self.visited[node] = True
        unvisited_nodes = [item for item in self.adjacency_list[node] if not self.visited[item]]
        if len(unvisited_nodes) > 0:
            n_list = sorted(unvisited_nodes)
            for n in n_list:
                if not self.visited[n]:
                    self.dfs_po(n, postorder)
        postorder.append(node)

    def dfs_forest_po(self):
        postorder: list[int] = []
        for node in self.adjacency_list.keys():
            if not self.visited[node]:
                self.dfs_po(node, postorder)
        return postorder

    def dfs_scc(self, node: int, scc: set[int], postorder: list[int]):
        self.visited[node] = True
        unvisited_nodes = [item for item in self.adjacency_list[node] if not self.visited[item]]
        if len(unvisited_nodes) > 0:
            n_list = sorted(unvisited_nodes, key=lambda x: postorder.index(x))
            for n in n_list:
                if not self.visited[n]:
                    self.dfs_scc(n, scc, postorder)
        scc.add(node)

    def dfs_forest_scc(self, postorder: list[int]):
        for key in self.visited.keys():
            self.visited[key] = False
        scc_list: list[set[int]] = []
        for node in postorder:
            if not self.visited[node]:
                scc: set[int] = set()
                self.dfs_scc(node, scc, postorder)
                scc_list.append(scc)
        return scc_list

    def to_string(self):
        string = ''
        for k in self.adjacency_list.keys():
            string += 'R' + str(k) + ':'
            string += ','.join(['R' + str(num) for num in self.adjacency_list[k]])
            string += '\n'
        string += '\n'
        return string
