import carcassonne_tile
'''
File: carcassonne_map.py
Author: Bryan Le
Date: April 19, 2022
Purpose: This program will hold a class with multiple methods dealing with 
the Carcassonne game.
'''

class CarcassonneMap:
    ''' This class represents the Carcassonne Map game
        board. It contains some of the functions
        necessary to properly play the game and add
        tiles according to the rules.

        The constructor simply creates the game board with
        tile01 at (0, 0).
    '''


    def __init__(self):
        ''' This constructor initializes the Map with
            tile01 at (0, 0).
            Arguments: self
            Return Value: this returns nothing.
        '''
        self._map = {(0, 0): carcassonne_tile.tile01}


    def get_all_coords(self):
        ''' This function returns all the coordinates
            of placed tiles as a key and then convert it to a set.
            Arguments: self
            Return Value: this will reset all_cords (a set).
        '''
        all_coords = self._map.keys()
        all_coords = set(all_coords)
        return all_coords


    def find_map_border(self):
        '''
        This function checks to see where there are available spots on
        the map for potential moves. The available spots are returned as a
        set of tuples.
            Arguments: self
            Return Value: this will return a set of tuples.
        '''
        border_coords = set()
        for coord in self._map:
            if (coord[0] + 1, coord[1]) not in self._map:
                border_coords.add((coord[0] + 1, coord[1]))
            if (coord[0] - 1, coord[1]) not in self._map:
                border_coords.add((coord[0] - 1, coord[1]))
            if (coord[0], coord[1] + 1) not in self._map:
                border_coords.add((coord[0], coord[1] + 1))
            if (coord[0], coord[1] - 1) not in self._map:
                border_coords.add((coord[0], coord[1] - 1))

        return border_coords


    def get(self, x, y):
        ''' This function returns the tile at a
            a requested spot on the board. If it doesn't exist it will
            return None.
            Arguments: self, x and y (integers)
            Return Value: tile object or None
        '''
        coords = (x, y)
        if coords in self._map:
            return self._map[coords]
        else:
            return None

    def trace_road_one_direction(self, x,y, side):
        '''
        This method lets the user trace a road in one direction.
        It'll keep on tracing until there are no tiles left or if it is a
        crossroads.
        Arguments: self, int x, int y, int side
        Return Value: list of tuples with
            tile coords and directions of road
        '''
        tiles, cur_x, cur_y = [], x, y

        while True:
            if side == -1:
                break
            elif side == 0:
                if (cur_x, cur_y + 1) in self._map:
                    cur_y, side = cur_y + 1, 2
                else:
                    break
            elif side == 1:
                if (cur_x + 1, cur_y) in self._map:
                    cur_x, side = cur_x + 1, 3
                else:
                    break
            elif side == 2:
                if (cur_x, cur_y - 1) in self._map:
                    cur_y, side = cur_y - 1, 0
                else:
                    break
            elif side == 3:
                if (cur_x - 1, cur_y) in self._map:
                    cur_x, side = cur_x - 1, 1
                else:
                    break

            if (cur_x, cur_y, side, \
                self._map[(cur_x, cur_y)].road_get_connection(side)) in tiles:
                break
            else:
                tiles.append((cur_x, cur_y, side, \
                              self._map[(cur_x, cur_y)].road_get_connection(
                                  side)))
                side = self._map[(cur_x, cur_y)].road_get_connection(side)

        return tiles

    def add(self, x, y, tile, confirm = True, tryOnly = False):
        ''' This function allows the player to add a tile
            to the game board. The function runs a series of
            error checks to see if it's valid, and it can check before actually
            adding the tile.
            Arguments: self, ints x and y, booleans confirm
            and tryOnly for specifying checks
            Return Value: a boolean (True or False)
        '''
        border_coords = self.find_map_border()
        flag, coord = True, (x,y)
        x, y = coord[0], coord[1]
        # These are the bunch of checks.
        if (x, y) in border_coords:
            if (x + 1, y) in self._map:
                if self._map[(x + 1, y)].get_edge(3) != tile.get_edge(1):
                    flag = False
            if (x - 1, y) in self._map:
                if self._map[(x - 1, y)].get_edge(1) != tile.get_edge(3):
                    flag = False
            if (x, y + 1) in self._map:
                if self._map[(x, y + 1)].get_edge(2) != tile.get_edge(0):
                    flag = False
            if (x, y - 1) in self._map:
                if self._map[(x, y - 1)].get_edge(0) != tile.get_edge(2):
                    flag = False
        else:
            flag = False

        # These are the all the potential confirm and tryOnlys.

        if confirm == True and tryOnly == False:
            if flag == True:
                self._map[(x, y)] = tile
                return True
            return False
        elif confirm == True and tryOnly == True:
            if flag == True:
                return True
            return False
        elif confirm == False and tryOnly == False:
            self._map[(x, y)] = tile
            return True

    def trace_road(self, x, y, side):
        ''' This function allows the player trace a given
            road in both directions. It will trace the road
            until there is no tile left at either end or if
            the roads hit crossroads. It uses
            road_get_connection as a helper function.
            Arguments: self, int x, int y, and int side
            Return Value: array of tuples with tile coords and directions of
            road
        '''

        array_to_compare = []
        # These are the three helper function statements we would need.
        given_dir = self.trace_road_one_direction(x, y, side)
        # In terms of position, this would be like forward.
        other_side = self.trace_road_one_direction(x,y,
        carcassonne_tile.CarcassonneTile.road_get_connection
        (self._map[(x,y)],side))
        # In terms of position, this would be like middle
        other_dir = [(x,y,carcassonne_tile.CarcassonneTile.road_get_connection(
                          self._map[(x,y)],side),side)]
        # In terms of position, this would be like the middle.

        for tile in reversed(other_side):
            tile = list(tile)
            tile[2],tile[3] = tile[3],tile[2]
            tile = tuple(tile)
            array_to_compare.append(tile)

        copied_directions = array_to_compare[:]

        if len(copied_directions) > 0:
            copied_directions.append(copied_directions[0])
            copied_directions.pop(0)

        if copied_directions == given_dir and copied_directions != []:
            return given_dir

        else:
            # If the array is 0.
            return array_to_compare + other_dir + given_dir

    def trace_city(self, x, y, side):
        ''' This function allows the player trace an entire
            city. It takes a given location within a city
            and extends out into the given tile and
            surrounding tiles to find all portions of
            the connected city.
            Arguments: self, int coords x and y, int side
            Return Value: tuple: boolean value of whether or not
            city is complete and tuples with tile coords and city edges
        '''
        city, keep_searching, completed = {(x, y, side)}, True, True
        while keep_searching:
            keep_searching, dup = False, list(city)
            for tile in dup:
                cur_x, cur_y, edge = tile[0], tile[1], tile[2]
                for edge2 in range(4):
                    if self._map[(cur_x, cur_y)].edge_has_city(edge2) == True\
                            and self._map[(cur_x, cur_y)].city_connects(edge,
                                                                        edge2)\
                            and (cur_x, cur_y, edge2) not in city:
                        city.add((cur_x, cur_y, edge2))
                        keep_searching = True

                if edge == 0:
                    # These all of the checks for the respective directions.
                    neigh = (cur_x, cur_y + 1, 2)
                elif edge == 1:
                    neigh = (cur_x + 1, cur_y, 3)
                elif edge == 2:
                    neigh = (cur_x, cur_y - 1, 0)
                elif edge == 3:
                    neigh = (cur_x - 1, cur_y, 1)

                if (neigh[0], neigh[1]) in self._map:
                    # The check for neighbors.
                    if self._map[(neigh[0],neigh[1])].edge_has_city(neigh[2])\
                        and neigh not in city:
                        city.add(neigh)
                        keep_searching = True
                else:
                    completed = False
        return (completed, city)




