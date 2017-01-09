from nltk.util import flatten

class DirectedGraph:
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj_mat = dict([(x, []) for x in range(self.V)])
        
    def adj(self, fro):
        return self.adj_mat[fro]
    
    def add_edges(self, tups):
        '''Hope this here code be giving you the creeps'''
        if (len(tups[0]) == 2):
            [self.add_edge(Edge(*v)) for v in tups]
        elif (len(tups[0]) == 3):
            [self.add_edge(WeightedEdge(*v)) for v in tups]
        elif (len(tups[0]) == 4):
            [self.add_edge(WeightedLabledEdge(*v)) for v in tups]
 
            
    def add_edge(self, edge):
        self.adj(edge.fro).append(edge)
        self.E += 1;
    
    def edges(self):
        all_edges = []
        for v in self.adj_mat.keys():
            adj = self.adj(v)
            if adj:
                all_edges += [edge for edge in adj]
        return all_edges
            
    def has_cycle(self):
        return CycleDetecter(self).cycle
            
        
    def reverse(self):
        Reversed = DirectedGraph(self.V)
        [Reversed.add_edge(edge.reverse()) for edge in self.edges()]
        return Reversed

    def prune(self):
        Reversed = self.reverse()
        Pruned = DirectedGraph(self.V)
        for m in range(self.V):
            parents = Reversed.adj(m)
            if parents:
                Pruned.add_edge(max(parents, key= lambda x: x.weight))
        return Pruned.reverse()
            
        

class Edge:
    def __init__(self, fro, to):
        self.fro = fro
        self.to = to
        
    def reverse(self):
        return Edge(self.to, self.fro)
        
    def __repr__(self):
        return '%s -> %s' % (self.fro, self.to)

class WeightedEdge(Edge):
    def __init__(self, fro, to, weight):
        Edge.__init__(self, fro, to)
        self.weight = weight

    def reverse(self):
        return WeightedEdge(self.to, self.fro, self.weight)

    def __repr__(self):
        return '%s -> %s # %s' % (self.fro, self.to, self.weight)

class LabeledEdge(Edge):
    def __init__(self, fro, to, label):
        Edge.__init__(self, fro, to)
        self.label = label
        
    def reverse(self):
        return LabeledEdge(self.to, self.fro, self.label)
    
    def __repr__(self):
        return "%s -> %s 'L' %s" % (self.fro, self.to, self.label)

class WeightedLabledEdge(WeightedEdge):
    def __init__(self, fro, to, label, weight):
        WeightedEdge.__init__(self, fro, to, weight)
        self.label = label
        
    def reverse(self):
        return WeightedLabledEdge(self.to, self.fro, self.label, self.weight)
    def __repr__(self):
        return "%s -> %s '#' %s 'L' %s" % (self.fro, self.to, self.weight, self.label)


class CycleDetecter:
    def __init__(self, graph):
        self.G = graph
        self.marked  = [False] * self.G.V
        self.edge_to = [-1] * self.G.V
        self.cycle = []
        self.has_cycle = lambda: bool(self.cycle)
        self.on_stack = [False] * self.G.V 
        self.is_cyclic()
        
    def dfs(self, v):
        self.on_stack[v] = True
        self.marked[v] = True
        for w in self.G.adj(v):
            if (self.has_cycle()):
                return
            elif not self.marked[w.to]:
                self.edge_to[w.to] = v
                self.dfs(w.to)
            elif(self.on_stack[w.to]):
                x = v
                while(x != w.to):
                    self.cycle.append(x)
                    x = self.edge_to[x]
                self.cycle.append(w.to)
                self.cycle.append(v)

        self.on_stack[v] = False
                

    def is_cyclic(self):
        for v in range(self.G.V):
            if not self.marked[v]:
                self.dfs(v)
    
        
    def __repr__(self):
        return " -> ".join([str(x) for x in self.cycle])
                    
        
class DFS:
    def __init__(self, graph):
        self.G = graph
        self.pathTo = [-1] * self.G.V
        self.marked = [False] * self.G.V
        self.count = 1
        
    
    def dfs(self, w):
        for edge in self.G.adj(w):
            if not self.marked[edge.to]:
                self.marked[edge.to] = True
                self.pathTo[edge.to] = w
                self.count  = self.count +1
                self.dfs(edge.to)
                
    def isTree(self, root=0):
        self.dfs(root)
        return bool(self.count/ self.G.V)
           
        
    
        
