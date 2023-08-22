import math
import random
from itertools import chain
import ps3_visualize
import pylab
from ps3_verify_movement27 import test_robot_movement

class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.
        Does NOT test whether the returned position fits inside the room.
        Args:
            angle: float representing angle in degrees, 0 <= angle < 360
            speed: positive float representing speed
        Returns: Position object representing the new position.        """
        old_x, old_y = self.get_x(), self.get_y()

        # change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.
    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """

    def __init__(self, width, height, dirt_amount: int):
        """
        width: int > 0
        height: int > 0
        dirt_amount: int > 0      """
        self.width = width
        self.height = height
        self.tiles = [[dirt_amount for _ in range(height)] for _ in range(width)]

    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.
        Assumes that pos represents a valid position inside this room.
        Args: 
            pos: a Position object
            capacity: the amount of dirt to be cleaned in a single time-step
                    can be negative which would mean adding dirt to the tile    """
        x = int(pos.get_x())
        y = int(pos.get_y())
        self.tiles[x][y] -= capacity
        if self.tiles[x][y] < 0:
            self.tiles[x][y] = 0

    def is_tile_cleaned(self, m, n):
        """Assumes that (m, n) represents a valid tile inside the room.
        Args:
            m: int
            n: int        
        Returns: True if the tile (m, n) is cleaned, False otherwise     """
        return self.tiles[m][n] <= 0

    def get_num_cleaned_tiles(self):
        """
        Returns: int; the total number of clean tiles in the room        """
        return sum([1 for elt in chain(*self.tiles) if elt <= 0])

    def is_position_in_room(self, pos):
        """Determines if pos is inside the room.
        Args:
            pos: Position object.
        Returns: True if pos is in the room, False otherwise.        """
        return 0 <= pos.get_x() < self.width and 0 <= pos.get_y() < self.height

    def get_dirt_amount(self, m, n):
        """Assumes that (m, n) represents a valid tile inside the room.
        Args:
            m: int
            n: int
        Returns: int, amount of dirt on tile (m, n)    """
        return self.tiles[m][n]

    def get_num_tiles(self):
        """
        Returns: int, the total number of tiles in the room        """
        # dummy func, to be implemented in subclasses
        raise NotImplementedError

    def is_position_valid(self, pos):
        """
        pos: Position object        
        Returns: True if pos is in the room and if position is unfurnished, False otherwise.        """
        # dummy func, to be implemented in subclasses
        raise NotImplementedError

    def get_random_position(self):
        """
        Returns: Position object; a random position inside the room        """
        # dummy func, to be implemented in subclasses
        raise NotImplementedError


class Robot(object):
    """Represents a robot cleaning a particular room.
    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.
    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.    """

    def __init__(self, room, speed, capacity):
        """The robot initially has a random direction and a random position in the room.
        Args:
            room:  RectangularRoom object
            speed: float > 0
            capacity: int > 0; the amount of dirt cleaned by the robot in a single time-step       """
        self.room = room
        self.speed = speed
        self.capacity = capacity
        self.position = room.get_random_position()
        self.angle = random.random() * 360

    def get_robot_position(self):
        """
        Returns: Position object giving the robot's position in the room        """
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in degrees, 0.0 <= d < 360.0        """
        return self.angle

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.
        Args:
            position: Position object        """
        self.position = position

    def set_robot_direction(self, direction):
        """Set the direction of the robot to direction.
        Args:
            direction: float representing an angle in degrees        """
        self.angle = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # dummy func, to be implemented in subclasses
        raise NotImplementedError


class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.    """

    def get_num_tiles(self):
        """
        Returns: int; the total number of tiles in the room        """
        return self.width * self.height

    def is_position_valid(self, pos):
        """
        pos: Position object.
        Returns: True if pos is in the room, False otherwise.        """
        return self.is_position_in_room(pos)

    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).        """
        return Position(random.random() * self.width, random.random() * self.height)


class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.    """

    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).        """
        RectangularRoom.__init__(self, width, height, dirt_amount)
        self.furniture_tiles = []

    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.        """
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # randomly choosing bottom left corner of the furniture item.
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # filling list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i, j))

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.        """
        return (m, n) in self.furniture_tiles

    def is_position_furnished(self, pos):
        """
        pos: Position object.
        Returns True if pos is furnished and False otherwise        """
        return (math.floor(pos.get_x()), math.floor(pos.get_y())) in self.furniture_tiles

    def is_position_valid(self, pos):
        """
        pos: Position object.
        returns: True if pos is in the room and is unfurnished, False otherwise.        """
        return self.is_position_in_room(pos) and not self.is_position_furnished(pos)

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.        """
        return (self.width * self.height) - len(self.furniture_tiles)

    def get_random_position(self):
        """
        Returns: Position object; a valid random position (inside the room and not in a furnished area).        """
        while True:
            position = Position(random.randint(0, self.width), random.randint(0, self.height))
            if self.is_position_valid(position):
                return position


class StandardRobot(Robot):
    """    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furniture, it chooses a new direction randomly.    """

    def update_position_and_clean(self):
        """
        Simulates the raise passage of a single time-step.
        Moves the robot to a new random position (if the new position is invalid,
        rotates once to a random new direction, and stays stationary) and cleans the dirt on the tile
        by its given capacity.         """
        curr_position = self.position
        new_position = curr_position.get_new_position(self.angle, self.speed)
        try:
            valid = self.room.is_position_valid(new_position)
        except:
            valid = self.room.is_position_in_room(new_position)
        if valid:
            self.position = new_position
            self.room.clean_tile_at_position(new_position, self.capacity)
        else:
            self.set_robot_direction(random.random() * 360)


# Uncomment one of these lines to see visualisation of a StandardRobot in action!
#test_robot_movement(StandardRobot, EmptyRoom)
#test_robot_movement(StandardRobot, FurnishedRoom)


class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to prob.
        prob: a float (0 <= prob <= 1)        """
        FaultyRobot.p = prob

    def gets_faulty(self):
        """Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.
        returns: True if the FaultyRobot gets faulty, False otherwise.        """
        return random.random() < FaultyRobot.p

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.
        Checks if the robot gets faulty. If the robot gets faulty,
        does not clean the current tile and changes its direction randomly.
        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step         """
        curr_position = self.position
        new_position = curr_position.get_new_position(self.angle, self.speed)
        try:
            valid = self.room.is_position_valid(new_position)
        except:
            valid = self.room.is_position_in_room(new_position)
        if valid:
            self.position = new_position
            if not self.gets_faulty():
                self.room.clean_tile_at_position(new_position, self.capacity)
        else:
            self.set_robot_direction(random.randint(0, 360))

# Uncomment one of these lines to see visualisation of a FaultyRobot in action!
#test_robot_movement(FaultyRobot, EmptyRoom)
#test_robot_movement(FaultyRobot, FurnishedRoom)