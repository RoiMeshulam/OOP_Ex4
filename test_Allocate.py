import unittest
from GraphAlgo import *



class MyTestCase(unittest.TestCase):

    def test_allocateAnAgent(self):

        def _allocateAnAgent(agent_src: int, pokemons: list, graphAlgo: GraphAlgo):
            minpath = float("inf")
            movelist: list
            edgeToMove: Edge
            ans_src = -1
            pokemon_to_delete = None
            # ans is the closest node to agent src
            # we can make pokemon a class later
            for pokemon in pokemons:
                pokemon_dict = pokemon['Pokemon']
                pokemon_type = pokemon_dict['type']
                pokemon_pos = "" + pokemon_dict['pos']
                pos = pokemon_pos.split(",")
                x = float(pos[0])
                y = float(pos[1])
                pokemon_pos: tuple = (x, y)

                nodedict = graphAlgo.get_graph().get_all_v()
                pokemon_edge: Edge = None
                isOn: bool = False
                for node in nodedict:
                    if (isOn == True):
                        break
                    edgedict = graphAlgo.get_graph().all_out_edges_of_node(node)
                    for edge in edgedict:
                        e = Edge(node, edge, edgedict[edge])
                        isOn = graphAlgo.get_graph().isOnEdge(e, pokemon_pos)
                        if (isOn == True):
                            pokemon_edge: Edge = e
                            # pokemon_edge is the specific edge that the pokemon posses
                            break
                # type negative -> src--> dest
                if (pokemon_type < 0):
                    dest: int = pokemon_edge.get_src()
                    temp = graphAlgo.shortest_path(agent_src, dest)
                    if (temp[0] < minpath):
                        minpath = temp[0]
                        movelist = temp[1]
                        edgeToMove = pokemon_edge
                        ans_src = dest
                        pokemon_to_delete = pokemon
                # type positive -> dest-->src
                if (pokemon_type > 0):
                    dest: int = pokemon_edge.get_dest()
                    temp = graphAlgo.shortest_path(agent_src, dest)
                    if (temp[0] < minpath):
                        minpath = temp[0]
                        movelist = temp[1]
                        edgeToMove = pokemon_edge
                        ans_src = dest
                        pokemon_to_delete = pokemon

            pokemons.remove(pokemon_to_delete)
            return (minpath, ans_src, movelist, edgeToMove)




        g = DiGraph()
        g.add_node(0, (0, 6))
        g.add_node(1, (1, 0))
        g.add_node(2, (6, 0))
        g.add_node(3, (12, 3))
        g.add_node(4, (6, 6))
        g.add_edge(0, 1, 1)
        g.add_edge(0, 4, 6)
        g.add_edge(1, 2, 1)
        g.add_edge(2, 3, 1)
        g.add_edge(4, 3, 6)
        gh = GraphAlgo(g)

        # agent is on node 0
        agent_src = 0

        # The pokemon list
        pokemon_list =[{'Pokemon': {'value': 8.0, 'type': -1, 'pos': '8.0,5.0,0.0'}}, {'Pokemon': {'value': 8.0, 'type': -1, 'pos': '3.0,0.0,0.0'}}]

        a= _allocateAnAgent(agent_src,pokemon_list,gh)
        print(a)
        minpath_ans= 1
        src_ans= 1
        movelist_ans=[0,1]

        self.assertEqual(minpath_ans, a[0])
        self.assertEqual(src_ans, a[1])
        self.assertEqual(movelist_ans, a[2])

