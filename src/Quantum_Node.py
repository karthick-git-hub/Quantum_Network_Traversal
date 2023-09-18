from global_variables import *

class Node():
    def __init__(self, id, oval_id, position, status, number_of_edges):
        self._node_id = id
        self._oval_id = oval_id
        self._color = dot_color
        self._position = position
        self._status = status
        self._number_of_edges = number_of_edges
        self._type = node

    @property
    def oval_id(self):
         return self._oval_id
    
    @property
    def id(self):
         return self._node_id
    
    @property
    def color(self):
         return self._color
       
    @color.setter
    def color(self, color):
         self._color = color
    
    @property
    def status(self):
         return self._status
    
    @property
    def position(self):
         return self._position
       
    @status.setter
    def status(self, status):
         self._status = status

    @property
    def edges(self):
         return self._number_of_edges
       
    @edges.setter
    def edges(self, edges):
         self._number_of_edges = edges

    def show_all(self):
        return str(self._node_id) + ' '+ str(self._oval_id) + ' '+str(self._color)+ ' '+str(self._position)