'''
File: carcassonne_tile.py
Author: Bryan Le
Date: April 19, 2022
Purpose: This program will hold a class with multiple methods dealing with
the Carcassonne game.
'''
class CarcassonneTile:
    '''This class represents the Carcassonne Tiles
        of the game. This class will contain methods that will properly
        create/label/classify the tiles of the game.
    '''
    def __init__(self, n, e, s, w, city_connects):
        ''' This constructor will contain the potential directions of the
        tiles. There will also be a list of the directions for future use in
        other methods. City_connects will be a boolean value (either True or
        False)
        Arguments:self,n,e,s,w,city_connects
        Return Value: none
        '''
        self._north = n
        self._south = s
        self._east = e
        self._west = w
        self._city_connects = city_connects

        self._edges = [self._north, self._east, self._south, self._west]
        # west, north, east, south

    def get_edge(self, side):
        '''
        This method will return an edge of the tile of one of the four
        directions. The argument 'side' will determine what direction it is.
        Arguments: side (integer)
        :return: a string of the respective direction
        '''
        if side == 0:
            return self._north
        if side == 1:
            return self._east
        if side == 2:
            return self._south
        if side == 3:
            return self._west

        return False

    def edge_has_road(self, side):
        '''
        This method will return whether or not the the edge of a tile has a
        road.
        Arguments: self, side (int)
        :return: It will return a boolean (True if it is a "grass+road")
        '''
        return self._edges[side] == 'grass+road'

    def edge_has_city(self, side):
        '''
        This method will return whether or not the the edge of a tile has a
        city.
        Arguments: self
        :return: It will return a boolean (True if it is a "city")
        '''
        return self._edges[side] == 'city'

    def has_crossroads(self):
        '''
        This will check if the tile has a crossroad. It will return a
        boolean value if so.
        Arguments: self
        :return: Will return a boolean (True or False)
        '''
        ns = (self._edges[0] == 'grass+road' and \
              self._edges[2] == 'grass+road')
        ew = (self._edges[1] == 'grass+road' and \
              self._edges[3] == 'grass+road')

        if ns and ew:
            return True
        elif ns and (self._edges[1] == 'grass+road' or \
                     self._edges[3] == 'grass+road'):
            return True
        elif ew and (self._edges[0] == 'grass+road' or \
                     self._edges[2] == 'grass+road'):
            return True
        else:
            return False

    def road_get_connection(self, from_side):
        '''This method will return the side at which the roads connect.
        Arguments: self, from_side (integer)
        :return: It will return an integer representing the side at which it
        has the rest of tile's roads.
        '''

        # The case for when it has a crossroads.
        if self.has_crossroads():
            return -1

        if from_side == 0:
            if self.edge_has_road(1):
                return 1
            if self.edge_has_road(2):
                return 2
            if self.edge_has_road(3):
                return 3
        if from_side == 1:
            if self.edge_has_road(0):
                return 0
            if self.edge_has_road(2):
                return 2
            if self.edge_has_road(3):
                return 3
        if from_side == 2:
            if self.edge_has_road(1):
                return 1
            if self.edge_has_road(0):
                return 0
            if self.edge_has_road(3):
                return 3
        if from_side == 3:
            if self.edge_has_road(1):
                return 1
            if self.edge_has_road(2):
                return 2
            if self.edge_has_road(0):
                return 0

    def city_connects(self, sideA, sideB):
        ''' This method will show if a tile's city connects. It may connect
        to another edge or through the middle.
        Arguments: self, sideA (integer), and SideB (integer)
        :return: It will return a boolean value based on the cases. (True or
        False).
        '''
        if self._edges[sideA] == self._edges[sideB]:
            if sideA == sideB:
                return True

            if self._city_connects == False:
                return False

            if sideA == sideB:
                return True
            elif sideA == 0 and (sideB == 1 or sideB == 3):
                return True
            elif sideA == 1 and (sideB == 0 or sideB == 2):
                return True
            elif sideA == 2 and (sideB == 1 or sideB == 3):
                return True
            elif sideA == 3 and (sideB == 0 or sideB == 2):
                return True
            elif (sideA == 1 and sideB == 3) or (sideA == 3 and sideB == 1):
                if self._city_connects == True:
                    return True
            elif (sideA == 0 and sideB == 2) or (sideA == 2 and sideB == 0):
                if self._city_connects == True:
                    return True

        return False

    def rotate(self):
        '''
        This method will rotate a tile clockwise.
        Arguments: self
        :return: It will return the rotated tile object.
        '''
        rotated = CarcassonneTile(self._west, self._north, self._east,
                                  self._south, self._city_connects)
        return rotated


c = 'city'
g = 'grass'
gr = 'grass+road'

tile01 = CarcassonneTile(c, gr, g, gr, False)
tile02 = CarcassonneTile(c, c, g, c, True)
tile03 = CarcassonneTile(gr, gr, gr, gr, False)
tile04 = CarcassonneTile(c, gr, gr, g, False)
tile05 = CarcassonneTile(c, c, c, c, True)
tile06 = CarcassonneTile(gr, g, gr, g, False)
tile07 = CarcassonneTile(g, c, g, c, False)
tile08 = CarcassonneTile(g, c, g, c, True)
tile09 = CarcassonneTile(c, c, g, g, True)
tile10 = CarcassonneTile(g, gr, gr, gr, False)
tile11 = CarcassonneTile(c, gr, gr, c, True)
tile12 = CarcassonneTile(c, g, gr, gr, False)
tile13 = CarcassonneTile(c, gr, gr, gr, False)
tile14 = CarcassonneTile(c, c, g, g, False)
tile15 = CarcassonneTile(g, g, gr, gr, False)
tile16 = CarcassonneTile(c, g, g, g, False)