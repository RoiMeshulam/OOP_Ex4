from unittest import TestCase
from DiGraph import *
from Node import *
from Edge import *


class TestDiGraph(TestCase):

    def test_Nodes(self):
        g = DiGraph()
        g.add_node(0, (1, -1))
        g.add_node(1, (2, 3))
        g.add_node(2, (4, 6))
        g.add_node(3, (3, 13))
        g.add_node(4, (1, -5))
        g.add_node(5, (7, 7))
        g.add_node(6, (8, 2))
        self.assertEqual(7,g.v_size())
        g.remove_node(6)
        self.assertEqual(6,g.v_size())

    def test_Edges(self):
        g = DiGraph()
        g.add_node(0, (1, -1))
        g.add_node(1, (2, 3))
        g.add_node(2, (4, 6))
        g.add_node(3, (3, 13))
        g.add_node(4, (1, -5))
        g.add_node(5, (7, 7))
        g.add_node(6, (8, 2))
        g.add_edge(0,1,1)
        g.add_edge(0, 2, 1)
        g.add_edge(1, 4, 1)
        g.add_edge(5, 4, 1)
        g.add_edge(2, 4, 1)
        g.add_edge(5, 2, 1)
        g.add_edge(6, 5, 1)
        g.add_edge(2, 6, 1)
        g.add_edge(2, 3, 1)
        g.add_edge(3, 6, 1)
        self.assertEqual(10,g.e_size())
        g.remove_edge(2,3)
        g.remove_edge(3,6)
        self.assertEqual(8,g.e_size())
        g.add_edge(2, 3, 1)
        g.add_edge(3, 6, 1)
        g.remove_node(3)
        self.assertEqual(8,g.e_size())

    def test_MC(self):
        g = DiGraph()
        g.add_node(0, (1, -1))
        g.add_node(1, (2, 3))
        g.add_node(2, (4, 6))
        g.add_node(3, (3, 13))
        g.add_node(4, (1, -5))
        g.add_node(5, (7, 7))
        g.add_node(6, (8, 2))
        self.assertEqual(7,g.get_mc())
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(1, 4, 1)
        g.add_edge(5, 4, 1)
        g.add_edge(2, 4, 1)
        g.add_edge(5, 2, 1)
        g.add_edge(6, 5, 1)
        g.add_edge(2, 6, 1)
        g.add_edge(2, 3, 1)
        g.add_edge(3, 6, 1)
        self.assertEqual(17,g.get_mc())
        g.remove_edge(0,1)
        self.assertEqual(18,g.get_mc())
        g.remove_node(3)
        self.assertEqual(21,g.get_mc())

    def test_all_nodes(self):
        g = DiGraph()
        g.add_node(0, (1, -1))
        g.add_node(1, (2, 3))
        g.add_node(2, (4, 6))
        g.add_node(3, (3, 13))
        g.add_node(4, (1, -5))
        g.add_node(5, (7, 7))
        g.add_node(6, (8, 2))
        allNodes = g.get_all_v()
        i=0
        while (i<7):
            check = allNodes[i].get_id()
            self.assertEqual(i,check)
            i=i+1

    def test_in_out_edges(self):
        g = DiGraph()
        g.add_node(0, (1, -1))
        g.add_node(1, (2, 3))
        g.add_node(2, (4, 6))
        g.add_node(3, (3, 13))
        g.add_node(4, (1, -5))
        g.add_node(5, (7, 7))
        g.add_node(6, (8, 2))
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(1, 4, 1)
        g.add_edge(5, 4, 1)
        g.add_edge(2, 4, 1)
        g.add_edge(5, 2, 1)
        g.add_edge(6, 5, 1)
        g.add_edge(2, 6, 1)
        g.add_edge(2, 3, 1)
        g.add_edge(3, 6, 1)
        inEdges = g.all_in_edges_of_node(4)
        outEdges = g.all_out_edges_of_node(2)
        inans = [1,5,2]
        outans = [4,6,3]
        for e in inEdges:
            self.assertIn(e, inans)
        for e in outEdges:
            self.assertIn(e,outans)