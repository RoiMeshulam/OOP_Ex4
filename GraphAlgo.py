import json
import sys

from GraphAlgoInterface import *
from DiGraph import *
from queue import PriorityQueue
from Node import *
from Edge import *


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: DiGraph = None):
        if g is not None:
            self._graph = g
        else:
            self._graph = DiGraph()

    def get_graph(self) -> GraphInterface:
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        g = DiGraph()
        with open(file_name, 'r') as fp:
            obj = json.load(fp)
            listnodes = obj['Nodes']
            for i in range(len(listnodes)):
                node_id = int(listnodes[i].get('id'))
                if(listnodes[i].get('pos')!=None):
                    node_pos = "" + (listnodes[i].get('pos'))
                    pos = node_pos.split(",")
                    x = float(pos[0])
                    y = float(pos[1])
                    g.add_node(node_id, (x, y, 0))
                else:
                    g.add_node(node_id)
            listedges = obj['Edges']
            for i in range(len(listedges)):
                src = int(listedges[i].get('src'))
                dest = int(listedges[i].get('dest'))
                weight = float(listedges[i].get('w'))
                g.add_edge(src, dest, weight)

            self._graph = g

        return True

    def save_to_json(self, file_name: str) -> bool:
        with open(file_name,'w') as fp:
            data ={}
            nodedict=self._graph.get_all_v()
            data['Edges']=[]
            for i in nodedict:
                edgefromdict=self._graph.all_out_edges_of_node(nodedict[i].get_id())
                for e in edgefromdict:
                    dictedge={"src" : nodedict[i].get_id(),
                              "w" : edgefromdict[e],
                              "dest" : nodedict[e].get_id()}
                    data['Edges'].append(dictedge)
            data['Nodes']=[]
            for i in nodedict:
                dict={"pos" : ','.join(map(str,nodedict[i].get_pos())),
                    "src" :nodedict[i].get_id()}
                data['Nodes'].append(dict)
            json.dump(data,fp,indent=2)

        return True

    def _relax(self, e: Edge) -> None:
        src = e.get_src()
        dest = e.get_dest()
        nodedict = self._graph.get_all_v()
        vs = nodedict[src]
        vd = nodedict[dest]
        vsw = vs.get_weight()
        vdw = vd.get_weight()
        ew = e.get_weight()
        if (vdw > vsw + ew):
            new_weight = vsw + ew
            vd.set_weight(new_weight)
            vd.set_father(vs)
            return

    def _dijkstra(self, id: int) -> None:
        nodedict = self._graph.get_all_v()
        for i in nodedict:
            v = nodedict[i]
            if (i == id):
                v.set_father(None)
                v.set_weight(0)
                continue

            v.set_father(None)
            v.set_weight(sys.maxsize)

        pq = PriorityQueue()
        for node in nodedict:
            v = nodedict[node]
            pq.put(v)

        while not pq.empty():
            temp = pq.get()
            neighbors = self._graph.all_out_edges_of_node(temp.get_id())
            for x in neighbors:
                edge = Edge(temp.get_id(), x, neighbors[x])
                self._relax(edge)

            helpingpq = PriorityQueue()

            while not pq.empty():
                item = pq.get()
                helpingpq.put(item)

            while not helpingpq.empty():
                item = helpingpq.get()
                pq.put(item)

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if (id1 == id2):
            return (0, [id1])
        else:
            self._dijkstra(id1)
            ans = []
            nodeList = self._graph.get_all_v()
            n = nodeList[id2]
            if (n.get_weight() == sys.maxsize):
                return (float('inf'), [])
            totalWeight = n.get_weight()
            while (n != None):
                ans.insert(0,n.get_id())
                n = n.get_father()
            return (totalWeight, ans)

    def _isConnected(self) -> bool:
        if (self._graph.connectivity() == True):
            return True
        allNodes = self._graph.get_all_v()
        n: Node = None
        for i in allNodes:
            n = allNodes[i]
            break
        self.BFS(n)
        for i in allNodes:
            if (allNodes[i].get_tag() != 1):
                return False
        self._revBFS(n)
        for i in allNodes:
            if (allNodes[i].get_tag() != 1):
                return False
        self._graph.setconnectivity()
        return True

    def BFS(self, n: Node) -> None:
        allNodes = self._graph.get_all_v()
        for i in allNodes:
            allNodes[i].set_tag(0)
        queue = []
        n.set_tag(1)
        queue.append(n)
        while (queue):
            s = queue.pop()
            sEdges = self._graph.all_out_edges_of_node(s.get_id())
            for e in sEdges:
                curr: Node = allNodes[e]
                if (curr.get_tag() == 1):
                    continue
                curr.set_tag(1)
                queue.append(curr)
        return

    def _revBFS(self, n: Node) -> None:
        allNodes = self._graph.get_all_v()
        for i in allNodes:
            allNodes[i].set_tag(0)
        queue = []
        n.set_tag(1)
        queue.append(n)
        while (queue):
            s = queue.pop()
            sEdges = self._graph.all_out_rev_edges_of_node(s.get_id())
            for e in sEdges:
                curr: Node = allNodes[e]
                if (curr.get_tag() == 1):
                    continue
                curr.set_tag(1)
                queue.append(curr)
        return

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        self._dijkstra(node_lst[0])
        allNodes = self._graph.get_all_v()
        for i in node_lst:
            if (allNodes[i].get_weight() == sys.maxsize):
                return ([], float('inf'))
        totalWeight = 0
        TSPlist = []
        lstlen = len(node_lst)
        i = 0
        while (i < lstlen - 1):
            curr = self.shortest_path(node_lst[i], node_lst[i + 1])
            totalWeight = totalWeight + curr[0]
            for x in curr[1]:
                TSPlist.append(x)
            i = i + 1
        finalTSP = []
        i = 0
        while(i<len(TSPlist)):
            if (i==len(TSPlist) -1 ):
                finalTSP.append((TSPlist[i]))
                break
            if (TSPlist[i] == TSPlist[i+1]):
                finalTSP.append(TSPlist[i])
                i=i+2
            else:
                finalTSP.append(TSPlist[i])
                i=i+1

        return (finalTSP, totalWeight)

    def centerPoint(self) -> (int, float):
        if (self._isConnected() == False):
            return (None, float('inf'))
        ans: Node = None
        ansWeight: float = sys.maxsize
        allNodes = self._graph.get_all_v()
        for i in allNodes:
            n: Node = allNodes[i]
            self._dijkstra(i)
            n_id = 0
            w = 0
            for j in allNodes:
                nodeValue = allNodes[j].get_weight()
                if (nodeValue > w):
                    w = nodeValue
            if (w < ansWeight):
                ansWeight = w
                ans = allNodes[i]
        return (ans.get_id(), ansWeight)
