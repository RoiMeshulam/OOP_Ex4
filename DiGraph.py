from GraphInterface import *
from Node import *
from Edge import *

class DiGraph(GraphInterface):
    def __init__(self):
        self._nodes = {}
        self._edges = {}
        self._revedges = {}
        self._degree = {}
        self._nodeSize = 0
        self._edgeSize = 0
        self._MCsize = 0
        self._isConnected = False

    def isOnEdge(self, e: Edge, pos: tuple):
        xy1: Node = self._nodes[e.get_src()]
        xy2: Node = self._nodes[e.get_dest()]
        m = (xy2.get_pos()[1] - xy1.get_pos()[1]) / (xy2.get_pos()[0] - xy1.get_pos()[0])
        n = xy2.get_pos()[1] - (m * xy2.get_pos()[0])
        linearEquation = pos[1] - (m * pos[0]) - n
        if (linearEquation < 0.0000001 and linearEquation > -0.0000001):
            return True
        else:
            return False


    def setconnectivity(self):
        self._isConnected = True
        return

    def connectivity(self):
        return self._isConnected

    def v_size(self) -> int:
        return self._nodeSize

    def e_size(self) -> int:
        return self._edgeSize

    def get_mc(self) -> int:
        return self._MCsize

    def get_all_v(self) -> dict:
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        ans ={}
        for e in self._degree[id1]:
            if(e.get_src() != id1):
                ans[e.get_src()] = e.get_weight()
        return ans


    def all_out_edges_of_node(self, id1: int) -> dict:
        ans ={}
        for e in self._edges[id1]:
            ans[e.get_dest()] = e.get_weight()
        return ans

    def all_out_rev_edges_of_node(self, id1: int) -> dict:
        ans ={}
        for e in self._revedges[id1]:
            ans[e.get_dest()] = e.get_weight()
        return ans


    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self._nodes.keys():
            return False
        if id2 not in self._nodes.keys():
            return False
        for e in self._edges[id1]:
            if (e.get_dest == id2):
                return False

        curr = Edge(id1,id2,weight)
        revcurr = Edge(id2,id1,weight)
        self._edges[id1].append(curr)
        self._revedges[id2].append(revcurr)
        self._degree[id1].append(curr)
        self._degree[id2].append(curr)
        self._edgeSize=self._edgeSize+1
        self._MCsize = self._MCsize+1


    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        curr = Node(node_id,pos)
        if node_id in self._nodes.keys():
            return False
        self._nodes[node_id] = curr
        self._edges[node_id] = []
        self._revedges[node_id] = []
        self._degree[node_id] = []
        self._nodeSize = self._nodeSize+1
        self._MCsize = self._MCsize + 1
        self.isConnected = False
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self._nodes.keys():
            return False
        removeList = self._degree[node_id]
        while(len(removeList)>0):
            e = removeList.pop(0)
            self.remove_edge(e.get_src(),e.get_dest())
        self._nodes.pop(node_id)
        self._edges.pop(node_id)
        self._nodeSize = self._nodeSize - 1
        self._MCsize = self._MCsize + 1
        self.isConnected = False
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        for e in self._degree[node_id1]:
            if(e.get_dest() == node_id2):
                self._degree[node_id1].remove(e)
                break
        for e in self._degree[node_id2]:
            if(e.get_src() == node_id1):
                self._degree[node_id2].remove(e)
                break

        for e in self._revedges[node_id2]:
            if(e.get_dest() == node_id1):
                self._revedges[node_id2].remove(e)
                break

        for e in self._edges[node_id1]:
            if(e.get_dest() == node_id2):
                self._edges[node_id1].remove(e)
                self._edgeSize = self._edgeSize-1
                self._MCsize = self._MCsize + 1
                self.isConnected = False
                return True
        return False