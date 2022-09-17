from types import SimpleNamespace
from GraphAlgo import *
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

def findEdges(g: GraphInterface) -> tuple:
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    nodedict=g.get_all_v()
    for i in nodedict:
        curr:Node = nodedict[i]
        if(curr.get_pos()[0]<min_x):
            min_x=curr.get_pos()[0]
        if(curr.get_pos()[0]>max_x):
            max_x=curr.get_pos()[0]
        if (curr.get_pos()[1] < min_y):
            min_y = curr.get_pos()[1]
        if (curr.get_pos()[1] > max_y):
            max_y = curr.get_pos()[1]

    return (min_x,max_x,min_y,max_y)

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

#load from json str "pokemons" into list of pokemons

pokemons_draw=client.get_pokemons()
pokemons_list = json.loads(pokemons_draw)
pokemons_list=pokemons_list['Pokemons']


graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)

#initializing players:
pika = pygame.image.load('data/FixedPicachu.png')
chari = pygame.image.load('data/Charizard.png')
ash = pygame.image.load('data/FixedAsh.png')
bg = pygame.image.load('data/forest.jpg')
quitLogo = pygame.image.load('data/FixedQuit.png')

graphAlgo = GraphAlgo()
# get info from the server before the game start
get_info= client.get_info()
info=json.loads(get_info)
info=info['GameServer']
case= info['graph']
graphAlgo.load_from_json(str(case))

propor:tuple = findEdges(graphAlgo.get_graph())
min_x=propor[0]
max_x=propor[1]
min_y=propor[2]
max_y=propor[3]

def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen

# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)

radius = 15
# return the shortest path and the id of the node we should reach to collect the pokeimon
def _allocateAnAgent(agent_src:int,pokemons:list,graphAlgo:GraphAlgo):
    minpath = float("inf")
    movelist:list
    edgeToMove:Edge
    ans_src=-1
    pokemon_to_delete=None
    # ans is the closest node to agent src
    # we can make pokemon a class later
    for pokemon in pokemons:
        pokemon_dict = pokemon['Pokemon']
        pokemon_type=pokemon_dict['type']
        pokemon_pos=""+pokemon_dict['pos']
        pos = pokemon_pos.split(",")
        x = float(pos[0])
        y = float(pos[1])
        pokemon_pos:tuple=(x,y)

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
            dest:int=pokemon_edge.get_src()
            temp= graphAlgo.shortest_path(agent_src,dest)
            if(temp[0]<minpath):
                minpath=temp[0]
                movelist=temp[1]
                edgeToMove = pokemon_edge
                ans_src=dest
                pokemon_to_delete = pokemon
        # type positive -> dest-->src
        if(pokemon_type>0):
            dest: int = pokemon_edge.get_dest()
            temp = graphAlgo.shortest_path(agent_src, dest)
            if (temp[0] < minpath):
                minpath = temp[0]
                movelist= temp[1]
                edgeToMove = pokemon_edge
                ans_src = dest
                pokemon_to_delete=pokemon

    pokemons.remove(pokemon_to_delete)
    return (minpath,ans_src,movelist,edgeToMove)

agent_num= int(info['agents'])
# Insert all agents to the json string and scatter them in even distribution
delta_x= graphAlgo.get_graph().v_size()//agent_num
for i in range (agent_num):
    agent_starting_node = i * delta_x
    client.add_agent("{\"id\":" + str(agent_starting_node) + "}")

# this commnad starts the server - the game is running now
client.start()

moveCounter = 0

while client.is_running() == 'true':
    # update the pokemon list
    pokemons_draw=client.get_pokemons()
    pokemons_list = json.loads(pokemons_draw)
    pokemons_list = pokemons_list['Pokemons']
    pokemon_dict = pokemons_list[0]['Pokemon']

    agents = client.get_agents()
    agents_list = json.loads(agents)
    agents_list = agents_list['Agents']

    pokemons_draw = json.loads(client.get_pokemons(),
                               object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons_draw = [p.Pokemon for p in pokemons_draw]

    for p in pokemons_draw:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x,click_y = pygame.mouse.get_pos()
            if click_x > 25 and click_x < 75:
                if screen.get_size()[1]-click_y > 5 and screen.get_size()[1]-click_y < 45:
                    pygame.quit()
                    exit(0)

    # draw background
    bg = pygame.transform.scale(bg, (screen.get_size()[0], screen.get_size()[1]))
    screen.blit(bg, (0, 0))

    #draw quit
    quitLogo = pygame.transform.scale(quitLogo,(300,200))
    screen.blit(quitLogo,(-100,screen.get_size()[1]-125))

    # draw nodes
    allnodes:dict= graphAlgo.get_graph().get_all_v()

    for n in allnodes:
        curr:Node=allnodes[n]
        x = my_scale(curr.get_pos()[0], x=True)
        y = my_scale(curr.get_pos()[1], y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(curr.get_id()), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for i in allnodes:
        temp:Node = allnodes[i]
        alledges:dict =graphAlgo.get_graph().all_out_edges_of_node(i)
        for e in alledges:
            # find the edge nodes
            dest_id = e
            vd=None
            for j in allnodes:
                checker:Node = allnodes[j]
                if(dest_id==checker.get_id()):
                    vd=checker
                    break

            # scaled positions
            src_x = my_scale(temp.get_pos()[0], x=True)
            src_y = my_scale(temp.get_pos()[1], y=True)
            dest_x = my_scale(vd.get_pos()[0], x=True)
            dest_y = my_scale(vd.get_pos()[1], y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126),
                             (src_x, src_y), (dest_x, dest_y))

        # draw agents
        scoreSoFar = 0
        for agent in agents:
            ash = pygame.transform.scale(ash, (90, 90))
            imagex = int(agent.pos.x - 40)
            imagey = int(agent.pos.y - 40)
            screen.blit(ash, (imagex, imagey))
            scoreSoFar=scoreSoFar+agent.value

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons_draw:
        type = p.type
        if (type == 1):
            pika = pygame.transform.scale(pika, (50, 50))
            imagex = int(p.pos.x - 20)
            imagey = int(p.pos.y - 20)
            screen.blit(pika, (imagex, imagey))
        else:
            chari = pygame.transform.scale(chari, (50, 50))
            imagex = int(p.pos.x - 20)
            imagey = int(p.pos.y - 20)
            screen.blit(chari, (imagex, imagey))

        # display Score&TTL&Moves
        timeToEnd = (int)(client.time_to_end())//1000
        font = pygame.font.SysFont('comicsansms', 20,bold=True)
        cii = font.render(f'PokeCiiiii', True, (255, 0, 0))
        scoreboard = font.render(f'Score: {scoreSoFar}', True, (255, 0, 0))
        ttl = font.render(f'TTL: {timeToEnd}', True, (255, 0, 0))
        moveDisplay = font.render(f'Moves so far: {moveCounter}',True,(255,0,0))
        screen.blit(scoreboard, (5, 0))
        screen.blit(moveDisplay, (5, 25))
        screen.blit(ttl, (5, 50))
        screen.blit(cii, (screen.get_size()[0] // 2, 5))

    # choose next edge
    #allocate a pokemon to an agent-> remove the pokemon from list & send agent to pokemon

    for i in agents_list:
        agent=i['Agent']
        agent_id=agent['id']
        agent_src=agent['src']
        agent_dest=agent['dest']
        if agent_dest == -1:
            a=_allocateAnAgent(agent_src,pokemons_list,graphAlgo)
            if (a[0] != 0):
                client.choose_next_edge(
                    '{"agent_id":' + str(agent_id) + ', "next_node_id":' + str(a[2][1]) + '}')
            else:
                nextMove:int
                if(a[3].get_src() == a[1]):
                    nextMove=a[3].get_dest()
                else:
                    nextMove=a[3].get_src()
                client.choose_next_edge(
                    '{"agent_id":' + str(agent_id) + ', "next_node_id":' + str(nextMove) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())


    pygame.time.delay(100)
    client.move()
    moveCounter = moveCounter + 1
# game over: