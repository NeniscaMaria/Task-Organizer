import math
class Edge():
    '''
    This class models an edge of a directed graph as follows:
        ->two integers representing the origin and the target vertex of the edge
    '''
    def __init__(self, origin, target):
        self.__origin=origin
        self.__target=target

    def get_origin(self):
        return self.__origin

    def get_target(self):
        return self.__target

    origin = property(get_origin, None, None, None)
    target = property(get_target, None, None, None)
       
class DirectedGraph:
    def __init__(self,n=0,m=0):
        """
        This class models a directed graph represented as two dictionaries:
            ->both have all the vertices as keys;
            ->one has the list of out bound neighbors as values for each key(vertex);
            ->the other has the list of in bound neighbors as values for each key(vertex);
        There is an additional dictionary, the one dedicated for costs:
            ->the key: the edge represented as follows: (origin,target);
            ->the value: the cost of the edge(integer);
        """
        self.__noVertices=n
        self.__noEdges=m
        self.__Predecessor={}
        self.__Successor={}
        self.__cost={}
        for i in range(0,n):
            for j in range(0,n):
                if i==j:
                    self.__cost[(i,j)]=0
                else:
                    self.__cost[(i,j)]=math.inf
        for i in range(self.__noVertices):
            self.__Successor[i]=[]
            self.__Predecessor[i]=[]

    def get_cost(self):
        return self.__cost

    def get_no_vertices(self):
        return self.__noVertices

    def get_no_edges(self):
        return self.__noEdges

    def parseVertices(self):
        '''
        This function returns an iterator containing all the vertices.
        In other words, it returns the list of vertices.
        '''
        return self.__Successor.keys()
        #return Iterator(list(self.__Successor.keys()))

    def parseOutboundNeighbors(self,vertex):
        #This function returns an iterator containing the out bound neighbors of the vertex
        return self.__Successor[vertex]

    def parseInboundNeighbors(self,vertex):
        #This function returns an iterator containing the in bound neighbors of x
        return self.__Predecessor[vertex]

    def _isedge(self, edge):
        '''
        This function checks whether an edge already exists in the graph.
        INPUT: edge=of type Edge
        OUTPUT: boolean:
            TRUE=the edge exists
            FALSE=the edge does not exist
        '''
        if edge.get_origin() in self.__Successor.keys():
            if edge.get_target() in self.__Successor[edge.get_origin()]:
                return True
        return False  
    
    def _addCost(self, edge, cost):
        '''
        This functions adds the cost of an edge in the dictionary of costs
        INPUT:edge=of type Edge
            cost=integer
        '''
        self.__cost[edge.get_origin(),edge.get_target()]=cost
            
    def _addEdge(self, edge,cost):
        '''
        This function adds an edge to the graph.
        INPUT:edge= of type Edge
            cost=integer
        OUTPUT:- 
        THROWS: ValueError if the edge already exists
        '''
        if self._isedge(edge)==True:
            raise ValueError("This edge exists!")
        origin=edge.get_origin()
        target=edge.get_target()
        self.__Successor[origin].append(target)
        self.__Predecessor[target].append(origin)
        self._addCost(edge,cost)
    
    def _removeEdge(self,edge):
        '''
        This function removes an edge from the graph
        INPUT:edge of type edge
        THROWS: ValueError if the edge does not exist
        '''
        if self._isedge(edge)==False:
            raise ValueError("The edge does not exist!\n")
        origin=edge.get_origin()
        target=edge.get_target()
        #first we remove it from the successor dictionary
        if origin in self.__Successor.keys():
            self.__Successor[origin].remove(target)
        #then we remove it from the predecessor dictionary
        if target in self.__Predecessor.keys():
            self.__Predecessor[target].remove(origin)
        del self.__cost[(edge.get_origin(),edge.get_target())]
    
    def _removeVertex(self,vertex):
        '''
        This function removes a vertex from the graph.
        INPUT: vertex=integer
        OUTPUT:-
        THROWS:ValueError if the vertex does not exist
        '''
        if vertex not in self.__Successor.keys():
            raise ValueError("The vertex does not exist!\n")
        #we remove the vertex from the successors dictionary
        if vertex in self.__Successor.keys():
            self.__noEdges=self.__noEdges-len(self.__Successor[vertex])
            for target in self.__Successor[vertex]:
                edge=Edge(vertex,target)
                del self.__cost[(edge.get_origin(),edge.get_target())]
                self.__Predecessor[target].remove(vertex)
                self.__noEdges-=1
            del self.__Successor[vertex]
        #we remove the vertex from the predecessors list
        if vertex in self.__Predecessor.keys():
            self.__noEdges-=len(self.__Predecessor[vertex])
            for origin in self.__Predecessor[vertex]:
                edge=Edge(origin,vertex)
                del self.__cost[(edge.get_origin(),edge.get_target())]
                self.__Successor[origin].remove(vertex)
            del self.__Predecessor[vertex]    
        self.__noVertices-=1
    
    def _addVertex(self,vertex):
        '''
        This function adds a vertex
        INPUT:vertex=integer
        THROWS:ValueError if the vertex already exists
        '''
        if vertex in self.__Successor.keys():
            raise ValueError("The vertex already exists!\n")
        self.__Successor.update({vertex:[]})
        self.__Predecessor.update({vertex:[]})
        self.__noVertices+=1
    
    def _setCost(self,edge,newCost):
        '''
        This function modifies the cost of an edge
        INPUT:edge of type Edge
            newCost:integer
        THROWS: ValueError if the edge does not exist
        '''
        if self._isedge(edge)==False:
            raise ValueError("This edge does not exist!\n")
        self.__cost[(edge.get_origin(),edge.get_target())]=newCost
        
    def _getCost(self,edge):
        '''
        This function gets the cost of an edge
        INPUT: edge of type Edge
        OUTPUT: cost of type integer
        THROWS:ValueError if the edge does not exist
        '''
        if self._isedge(edge)==False:
            raise ValueError("The edge does not exist!\n")
        cost=self.__cost[(edge.get_origin(),edge.get_target())]
        return cost
    
    def _getIndegree(self,vertex):
        '''
        This function determines the in degree of a vertex.
        INPUT: vertex=integer
        OUTPUTL: in degree=Integer
        THROWS:ValueError if the vertex does not exist
        '''
        if vertex not in self.__Successor.keys():
            raise ValueError("This vertex does not exist!\n")
        if vertex not in self.__Predecessor.keys():
            indegree=0
        else:
            indegree=len(self.__Predecessor[vertex])
        return indegree

    
    def _getOutdegree(self,vertex):
        '''
        This function determines the outdegree of a vertex.
        INPUT: vertex=integer
        OUTPUTL: outdegree=Integer
        THROWS:ValueError if the vertex does not exist
        '''
        if vertex not in self.__Successor.keys():
            raise ValueError("This vertex does not exist!\n")
        if vertex not in self.__Successor.keys():
            outdegree=0
        else:
            outdegree=len(self.__Successor[vertex])
        return outdegree
    
    
    noVertices = property(get_no_vertices, None, None, None)
    noEdges = property(get_no_edges, None, None, None)
    cost = property(get_cost, None, None, None)

    
    def copyGraph(self):
        newGraph=DirectedGraph(self.__noVertices,self.__noEdges)
        for origin in self.__Successor:
            for i in range(len(self.__Successor[origin])):
                target=self.__Successor[origin][i]
                edge=Edge(origin,target)
                cost=self.__cost[(origin,target)]
                newGraph._addEdge(edge, cost)
        for target in self.__Predecessor:
            for i in range(len(self.__Predecessor[target])):
                origin=self.__Predecessor[target][i]
                edge=Edge(origin,target)
                cost=self.__cost[(origin,target)]
                newGraph._addEdge(edge, cost)
        return newGraph
    
    
    
import unittest
class Test(unittest.TestCase):
    def setUp(self):
        self.__graph=DirectedGraph(4,2)
        self.__edge=Edge(1,2)
        self.__edge2=Edge(1,3)
        self.__cost=1
        
    def tearDown(self):
        self.__graph=None
        self.__edge=None
        self.__edge2=None
        self.__cost=None
        
    def test1(self):
        #addition of an edge
        self.assertEqual(list(self.__graph.parseVertices()),[0,1,2,3])
        self.__graph._addEdge(self.__edge, self.__cost)
        self.assertEqual(self.__graph._isedge(self.__edge), True)
        with self.assertRaises(ValueError):
            self.__graph._addEdge(self.__edge, self.__cost)
        self.assertEqual(self.__graph.parseOutboundNeighbors(self.__edge.get_origin()),[self.__edge.get_target()])
        self.assertEqual(self.__graph.parseInboundNeighbors(self.__edge.get_target()),[self.__edge.get_origin()])
        self.assertEqual(self.__graph.get_cost()[(self.__edge.get_origin(),self.__edge.get_target())],self.__cost)
        #removal of an edge and of a vertexs
        self.__graph._removeEdge(self.__edge)
        self.__graph._addEdge(self.__edge, self.__cost)
        self.__graph._addEdge(self.__edge2, self.__cost)
        self.assertEqual(self.__graph.parseOutboundNeighbors(1),[2,3])
        self.assertEqual(self.__graph.parseInboundNeighbors(1),[])
        self.__graph._removeVertex(1)
        self.assertEqual(self.__graph.get_no_vertices(), 3)
        self.assertEqual(self.__graph.get_no_edges(), 0)    
        self.assertEqual(list(self.__graph.parseVertices()),[0,2,3])