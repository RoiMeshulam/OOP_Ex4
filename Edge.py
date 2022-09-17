class Edge:
    def __init__(self,src:int,dest:int,weight:float):
        self._src = src
        self._dest = dest
        self._weight = weight

    def get_src(self):
        return self._src
    def get_dest(self):
        return self._dest
    def get_weight(self):
        return self._weight



    def __lt__(self, other):
        return self._weight<getattr(other,"weight",other)


    def __repr__(self):
        return f"Edge {self.get_src()}->{self.get_dest()} weight:{self.get_weight()}"