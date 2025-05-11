"""
Dungeon system for the EXPLORE quadrant.

This module contains the core classes for dungeon generation and exploration,
including DungeonLevel and Room classes that form the foundation of the
Neon Wilderness.
"""

import random
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class Room:
    """
    Room represents a single room in the dungeon.
    Tracks its position, connections to other rooms, and content.
    """
    # Room types
    ENTRANCE = 0     # Dungeon entrance
    EXIT = 1         # Dungeon exit
    COMBAT = 2       # Room with enemies
    TREASURE = 3     # Room with loot
    PUZZLE = 4       # Room with interactive elements
    REST = 5         # Safe room for recovery
    BOSS = 6         # Room with boss encounter
    
    # Direction constants
    NORTH = 1
    SOUTH = 2
    EAST = 4
    WEST = 8
    
    # Direction opposites
    OPPOSITES = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }
    
    # Direction names for display and interaction
    DIRECTION_NAMES = {
        NORTH: "north",
        SOUTH: "south",
        EAST: "east",
        WEST: "west"
    }
    
    # Room type names for display
    ROOM_TYPE_NAMES = {
        ENTRANCE: "Entrance",
        EXIT: "Exit",
        COMBAT: "Combat Chamber",
        TREASURE: "Treasure Vault",
        PUZZLE: "Puzzle Room",
        REST: "Rest Area",
        BOSS: "Boss Chamber"
    }
    
    def __init__(self, row, col):
        """Initialize a new room at the given row and column position."""
        self.row = row
        self.col = col
        self.links = 0  # Bitwise flags for linked directions
        self.room_type = None
        self.discovered = False
        self.visited = False
        self.encounters = []
        self.treasures = []
        self.description = ""
        self.features = []
        self.difficulty = 1
        
    def linked(self, direction):
        """Check if this room is linked in the given direction."""
        return (self.links & direction) != 0
    
    def link(self, direction):
        """Link this room in the given direction."""
        self.links |= direction
    
    def unlink(self, direction):
        """Unlink this room from the given direction."""
        self.links &= ~direction
    
    def get_links(self):
        """Get a list of all directions where this room has links."""
        links = []
        if self.linked(Room.NORTH): links.append(Room.NORTH)
        if self.linked(Room.SOUTH): links.append(Room.SOUTH)
        if self.linked(Room.EAST): links.append(Room.EAST)
        if self.linked(Room.WEST): links.append(Room.WEST)
        return links
    
    def get_link_directions(self):
        """Get a list of direction names for all links."""
        return [Room.DIRECTION_NAMES[direction] for direction in self.get_links()]
    
    def add_encounter(self, encounter):
        """Add an encounter to this room."""
        self.encounters.append(encounter)
        return self
    
    def add_treasure(self, treasure):
        """Add a treasure to this room."""
        self.treasures.append(treasure)
        return self
    
    def set_description(self, desc):
        """Set the room description."""
        self.description = desc
        return self
    
    def add_feature(self, feature):
        """Add a feature to this room."""
        self.features.append(feature)
        return self
    
    def set_room_type(self, room_type):
        """Set the room type."""
        self.room_type = room_type
        
        # Set default description based on room type
        if not self.description:
            if room_type == Room.ENTRANCE:
                self.description = "Neon light spills through a gateway as you enter the dungeon. The walls pulse with digital energy, and the air hums with the promise of adventure."
            elif room_type == Room.EXIT:
                self.description = "A shimmering portal marks the exit from this level. Beyond it, you can see the digital landscape of the next challenge."
            elif room_type == Room.COMBAT:
                self.description = "The room crackles with hostile energy. Digital constructs materialize, their code forming aggressive patterns as they detect your presence."
            elif room_type == Room.TREASURE:
                self.description = "Glowing containers line the walls, their contents casting prismatic light across the room. Valuable data and resources await collection."
            elif room_type == Room.PUZZLE:
                self.description = "Strange symbols illuminate panels on the walls. A central pedestal contains an interactive interface that seems to require specific input."
            elif room_type == Room.REST:
                self.description = "The gentle hum of maintenance protocols fills this room. The aggressive code of the dungeon seems dampened here, offering a moment of respite."
            elif room_type == Room.BOSS:
                self.description = "The room expands into a massive chamber. At its center, a powerful entity composed of concentrated digital energy awaits, its presence distorting the surrounding space."
        
        return self
    
    def set_difficulty(self, difficulty):
        """Set the room difficulty level."""
        self.difficulty = difficulty
        return self
    
    def enter_room(self, character):
        """Process effects when a character enters the room."""
        self.visited = True
        
        # Room type-specific effects
        result = {
            "events": [],
            "encounters_triggered": False,
            "treasures_found": []
        }
        
        # Auto-discover adjacent rooms
        result["events"].append("You enter " + self.get_room_name() + ".")
        
        # Trigger encounters if room has any and is a combat room
        if self.room_type == Room.COMBAT and self.encounters and not self.is_cleared():
            result["encounters_triggered"] = True
            result["events"].append("Hostile entities detected!")
        
        # Automatic treasure discovery in treasure rooms
        if self.room_type == Room.TREASURE and self.treasures:
            perception_check = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
            perception_mod = (character["attributes"]["wisdom"] - 10) // 2
            
            if perception_check + perception_mod >= 10:
                found_treasures = []
                for treasure in self.treasures:
                    if not treasure.get("found", False):
                        treasure["found"] = True
                        found_treasures.append(treasure)
                
                if found_treasures:
                    result["treasures_found"] = found_treasures
                    result["events"].append(f"You found {len(found_treasures)} items!")
        
        # Rest area healing
        if self.room_type == Room.REST:
            # Heal 1d6 HP
            heal_amount = random.randint(1, 6)
            if character["hp"] < character["max_hp"]:
                character["hp"] = min(character["hp"] + heal_amount, character["max_hp"])
                result["events"].append(f"The room's restorative protocols heal you for {heal_amount} HP.")
        
        return result
    
    def is_cleared(self):
        """Check if the room has been cleared of encounters."""
        return all(encounter.get("completed", False) for encounter in self.encounters)
    
    def get_room_name(self):
        """Get the room name based on its type."""
        if self.room_type is not None:
            return Room.ROOM_TYPE_NAMES[self.room_type]
        return "Unknown Room"
    
    def to_dict(self):
        """Convert room to a dictionary for serialization."""
        return {
            "row": self.row,
            "col": self.col,
            "links": self.links,
            "room_type": self.room_type,
            "discovered": self.discovered,
            "visited": self.visited,
            "encounters": self.encounters,
            "treasures": self.treasures,
            "description": self.description,
            "features": self.features,
            "difficulty": self.difficulty
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a room from a dictionary."""
        room = cls(data["row"], data["col"])
        room.links = data["links"]
        room.room_type = data["room_type"]
        room.discovered = data["discovered"]
        room.visited = data["visited"]
        room.encounters = data["encounters"]
        room.treasures = data["treasures"]
        room.description = data["description"]
        room.features = data["features"]
        room.difficulty = data["difficulty"]
        return room


class DungeonLevel:
    """
    DungeonLevel represents an entire level of the dungeon as a grid of rooms.
    """
    # Direction offsets (row, col)
    DIRECTION_OFFSETS = {
        Room.NORTH: (-1, 0),  # North decreases row
        Room.SOUTH: (1, 0),   # South increases row
        Room.EAST: (0, 1),    # East increases column
        Room.WEST: (0, -1)    # West decreases column
    }
    
    def __init__(self, rows, cols, level_num=1, theme="neon"):
        """
        Initialize a new dungeon level.
        
        Args:
            rows: Number of rows in the dungeon grid
            cols: Number of columns in the dungeon grid
            level_num: The depth/difficulty level number
            theme: Visual theme for the dungeon
        """
        self.rows = rows
        self.cols = cols
        self.level_num = level_num
        self.theme = theme
        self.rooms = self._initialize_rooms()
        self.entrance = None  # Room object for entrance
        self.exit = None      # Room object for exit
        self.name = f"Level {level_num}: The Digital Deep"
        self.description = "A labyrinthine network of neon corridors stretching into the digital unknown."
    
    def _initialize_rooms(self):
        """Create and configure rooms for the dungeon grid."""
        # Create rooms
        rooms = [[Room(r, c) for c in range(self.cols)] for r in range(self.rows)]
        return rooms
    
    def is_valid(self, row, col):
        """Check if the given row and column are within the dungeon bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def at(self, row, col):
        """Get the room at the given row and column."""
        if not self.is_valid(row, col):
            raise IndexError(f"Room position ({row}, {col}) is outside the dungeon")
        return self.rooms[row][col]
    
    def get_adjacent_room(self, room, direction):
        """
        Get the adjacent room in the specified direction.
        
        Args:
            room: The starting room
            direction: The direction to move
            
        Returns:
            The adjacent room or None if there is no room in that direction
        """
        row_offset, col_offset = DungeonLevel.DIRECTION_OFFSETS[direction]
        new_row = room.row + row_offset
        new_col = room.col + col_offset
        
        if self.is_valid(new_row, new_col):
            return self.at(new_row, new_col)
        
        return None
    
    def link_rooms(self, room1, direction):
        """
        Link room1 to its adjacent room in the given direction.
        
        Args:
            room1: The first room to link
            direction: The direction from room1 to room2
            
        Returns:
            True if the link was created, False otherwise
        """
        room2 = self.get_adjacent_room(room1, direction)
        
        if room2 is None:
            return False
        
        # Link both rooms
        room1.link(direction)
        room2.link(Room.OPPOSITES[direction])
        
        return True
    
    def set_entrance(self, row, col):
        """Set the dungeon entrance room."""
        room = self.at(row, col)
        room.set_room_type(Room.ENTRANCE)
        self.entrance = room
        return self
    
    def set_exit(self, row, col):
        """Set the dungeon exit room."""
        room = self.at(row, col)
        room.set_room_type(Room.EXIT)
        self.exit = room
        return self
    
    def discover_room(self, row, col):
        """
        Mark a room as discovered.
        
        Args:
            row: Row of the room to discover
            col: Column of the room to discover
            
        Returns:
            The discovered room
        """
        room = self.at(row, col)
        room.discovered = True
        
        # Also discover adjacent rooms
        for direction in [Room.NORTH, Room.SOUTH, Room.EAST, Room.WEST]:
            if room.linked(direction):
                adjacent = self.get_adjacent_room(room, direction)
                if adjacent:
                    adjacent.discovered = True
        
        return room
    
    def to_dict(self):
        """Convert dungeon level to a dictionary for serialization."""
        # Convert rooms to dictionaries
        room_dicts = []
        for row in self.rooms:
            for room in row:
                room_dicts.append(room.to_dict())
        
        return {
            "rows": self.rows,
            "cols": self.cols,
            "level_num": self.level_num,
            "theme": self.theme,
            "rooms": room_dicts,
            "entrance": (self.entrance.row, self.entrance.col) if self.entrance else None,
            "exit": (self.exit.row, self.exit.col) if self.exit else None,
            "name": self.name,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a dungeon level from a dictionary."""
        dungeon = cls(data["rows"], data["cols"], data["level_num"], data["theme"])
        
        # Reconstruct rooms
        for room_data in data["rooms"]:
            row, col = room_data["row"], room_data["col"]
            room = Room.from_dict(room_data)
            dungeon.rooms[row][col] = room
        
        # Set entrance and exit
        if data["entrance"]:
            dungeon.entrance = dungeon.at(*data["entrance"])
        
        if data["exit"]:
            dungeon.exit = dungeon.at(*data["exit"])
        
        dungeon.name = data["name"]
        dungeon.description = data["description"]
        
        return dungeon


class DungeonGenerator:
    """
    Generator for dungeon levels using various algorithms.
    """
    
    @staticmethod
    def generate_dungeon(rows=10, cols=10, algorithm="bsp", level_num=1, 
                         theme="neon", difficulty=1, seed=None):
        """
        Generate a complete dungeon level.
        
        Args:
            rows: Number of rows in the dungeon
            cols: Number of columns in the dungeon
            algorithm: The generation algorithm to use
            level_num: The depth/difficulty level number
            theme: Visual theme for the dungeon
            difficulty: Base difficulty modifier
            seed: Random seed for reproducible dungeons
            
        Returns:
            A fully generated DungeonLevel instance
        """
        # Set random seed if provided
        if seed is not None:
            random.seed(seed)
        
        # Create empty dungeon
        dungeon = DungeonLevel(rows, cols, level_num, theme)
        
        # Apply the selected generation algorithm
        if algorithm == "bsp":
            DungeonGenerator.binary_space_partition(dungeon, theme, difficulty)
        elif algorithm == "maze":
            DungeonGenerator.maze_based(dungeon, theme, difficulty)
        elif algorithm == "cellular":
            DungeonGenerator.cellular_automata(dungeon, theme, difficulty)
        else:
            # Default to binary space partition
            DungeonGenerator.binary_space_partition(dungeon, theme, difficulty)
        
        # Set entrance and exit
        DungeonGenerator.set_entrance_exit(dungeon)
        
        # Populate the dungeon with content
        DungeonGenerator.populate_dungeon(dungeon, theme, difficulty)
        
        # Generate room descriptions
        DungeonGenerator.generate_descriptions(dungeon, theme)
        
        return dungeon
    
    @staticmethod
    def binary_space_partition(dungeon, theme, difficulty):
        """
        Generate a dungeon using binary space partitioning.
        This creates a more structured dungeon with rooms of varying sizes.
        
        Args:
            dungeon: The DungeonLevel to generate
            theme: Visual theme
            difficulty: Difficulty level modifier
            
        Returns:
            The modified dungeon
        """
        # For initial implementation, simplify by creating a maze-like structure
        # We'll enhance this with true BSP in a future iteration
        
        # First, create a simple connected grid
        for r in range(dungeon.rows):
            for c in range(dungeon.cols):
                # Link to east and south with probability
                room = dungeon.at(r, c)
                
                # Eastern connections (higher probability)
                if c < dungeon.cols - 1 and random.random() < 0.7:
                    dungeon.link_rooms(room, Room.EAST)
                
                # Southern connections (higher probability)
                if r < dungeon.rows - 1 and random.random() < 0.7:
                    dungeon.link_rooms(room, Room.SOUTH)
        
        return dungeon
    
    @staticmethod
    def maze_based(dungeon, theme, difficulty):
        """
        Generate a dungeon using a maze-based algorithm.
        This creates winding corridors and a more maze-like structure.
        
        Args:
            dungeon: The DungeonLevel to generate
            theme: Visual theme
            difficulty: Difficulty level modifier
            
        Returns:
            The modified dungeon
        """
        # Implementation will be added in a future iteration
        # For now, just create a simple connected grid
        for r in range(dungeon.rows):
            for c in range(dungeon.cols):
                room = dungeon.at(r, c)
                
                # Consider linking east
                if c < dungeon.cols - 1:
                    if random.random() < 0.5:
                        dungeon.link_rooms(room, Room.EAST)
                
                # Consider linking south
                if r < dungeon.rows - 1:
                    if random.random() < 0.5:
                        dungeon.link_rooms(room, Room.SOUTH)
        
        return dungeon
    
    @staticmethod
    def cellular_automata(dungeon, theme, difficulty):
        """
        Generate a dungeon using cellular automata.
        This creates organic-looking cave-like structures.
        
        Args:
            dungeon: The DungeonLevel to generate
            theme: Visual theme
            difficulty: Difficulty level modifier
            
        Returns:
            The modified dungeon
        """
        # Implementation will be added in a future iteration
        # For now, just create a simple connected grid
        for r in range(dungeon.rows):
            for c in range(dungeon.cols):
                room = dungeon.at(r, c)
                
                # Consider linking east
                if c < dungeon.cols - 1:
                    if random.random() < 0.6:
                        dungeon.link_rooms(room, Room.EAST)
                
                # Consider linking south
                if r < dungeon.rows - 1:
                    if random.random() < 0.6:
                        dungeon.link_rooms(room, Room.SOUTH)
        
        return dungeon
    
    @staticmethod
    def set_entrance_exit(dungeon):
        """
        Set the entrance and exit for the dungeon.
        
        Args:
            dungeon: The DungeonLevel to modify
            
        Returns:
            The modified dungeon
        """
        # Place entrance at the bottom row, preferring the center
        entrance_row = dungeon.rows - 1
        entrance_col = dungeon.cols // 2
        
        # Make sure the entrance has at least one connection
        entrance_room = dungeon.at(entrance_row, entrance_col)
        if not entrance_room.get_links():
            # If no connections, connect to the room above
            if entrance_row > 0:
                dungeon.link_rooms(entrance_room, Room.NORTH)
        
        dungeon.set_entrance(entrance_row, entrance_col)
        
        # Place exit at the top row, preferring the center
        exit_row = 0
        exit_col = dungeon.cols // 2
        
        # Make sure the exit has at least one connection
        exit_room = dungeon.at(exit_row, exit_col)
        if not exit_room.get_links():
            # If no connections, connect to the room below
            if exit_row < dungeon.rows - 1:
                dungeon.link_rooms(exit_room, Room.SOUTH)
        
        dungeon.set_exit(exit_row, exit_col)
        
        return dungeon
    
    @staticmethod
    def populate_dungeon(dungeon, theme, difficulty):
        """
        Populate the dungeon with encounters, treasures, and features.
        
        Args:
            dungeon: The DungeonLevel to populate
            theme: Visual theme
            difficulty: Difficulty level modifier
            
        Returns:
            The modified dungeon
        """
        # Determine room distribution
        num_rooms = dungeon.rows * dungeon.cols - 2  # Excluding entrance and exit
        
        # Target distribution (adjust based on desired gameplay balance)
        combat_percent = 0.4
        treasure_percent = 0.2
        puzzle_percent = 0.1
        rest_percent = 0.1
        # Remaining rooms will be empty corridors
        
        # Calculate target counts
        num_combat = int(num_rooms * combat_percent)
        num_treasure = int(num_rooms * treasure_percent)
        num_puzzle = int(num_rooms * puzzle_percent)
        num_rest = int(num_rooms * rest_percent)
        
        # For now, just assign room types
        available_rooms = []
        
        # Build list of available rooms (exclude entrance and exit)
        for r in range(dungeon.rows):
            for c in range(dungeon.cols):
                room = dungeon.at(r, c)
                if room != dungeon.entrance and room != dungeon.exit:
                    available_rooms.append(room)
        
        # Shuffle for random assignment
        random.shuffle(available_rooms)
        
        # Assign room types
        room_index = 0
        
        # Combat rooms
        for i in range(min(num_combat, len(available_rooms) - room_index)):
            room = available_rooms[room_index]
            room.set_room_type(Room.COMBAT)
            room_index += 1
            
            # Add encounters based on room position and level difficulty
            room_difficulty = difficulty + (dungeon.rows - room.row) / dungeon.rows
            
            # Simple encounter
            encounter = {
                "type": "combat",
                "enemies": [
                    {
                        "name": f"Level {int(room_difficulty)} Digital Construct",
                        "hp": 5 + int(room_difficulty) * 2,
                        "attack": 1 + int(room_difficulty) // 2,
                        "defense": 10 + int(room_difficulty) // 3
                    }
                ],
                "completed": False
            }
            
            room.add_encounter(encounter)
        
        # Treasure rooms
        for i in range(min(num_treasure, len(available_rooms) - room_index)):
            room = available_rooms[room_index]
            room.set_room_type(Room.TREASURE)
            room_index += 1
            
            # Add treasures based on room position and level difficulty
            room_difficulty = difficulty + (dungeon.rows - room.row) / dungeon.rows
            
            # Simple treasure - components for crafting
            component_types = ["metal", "elemental", "catalyst", "binding", "rune"]
            component_type = random.choice(component_types)
            
            treasure = {
                "type": "component",
                "component_type": component_type,
                "name": f"{theme.capitalize()} {component_type.capitalize()}",
                "value": 5 + int(room_difficulty) * 2,
                "found": False
            }
            
            room.add_treasure(treasure)
        
        # Puzzle rooms
        for i in range(min(num_puzzle, len(available_rooms) - room_index)):
            room = available_rooms[room_index]
            room.set_room_type(Room.PUZZLE)
            room_index += 1
            
            # Add puzzle features based on room difficulty
            room_difficulty = difficulty + (dungeon.rows - room.row) / dungeon.rows
            
            # Simple puzzle feature
            feature = {
                "type": "puzzle",
                "name": "Neon Circuit Array",
                "description": "A grid of glowing circuits that can be reconfigured to unlock a hidden cache.",
                "difficulty": int(room_difficulty),
                "solved": False
            }
            
            room.add_feature(feature)
            
            # Add treasure that is unlocked by solving the puzzle
            treasure = {
                "type": "item",
                "name": "Digital Artifact",
                "description": "A rare item recovered from the puzzle.",
                "value": 10 + int(room_difficulty) * 3,
                "found": False,
                "requires_puzzle": True
            }
            
            room.add_treasure(treasure)
        
        # Rest areas
        for i in range(min(num_rest, len(available_rooms) - room_index)):
            room = available_rooms[room_index]
            room.set_room_type(Room.REST)
            room_index += 1
            
            # Add rest area features
            feature = {
                "type": "rest",
                "name": "Data Stream Confluence",
                "description": "A peaceful merging of data streams that offers rejuvenating properties.",
                "heal_amount": 1 + difficulty
            }
            
            room.add_feature(feature)
        
        return dungeon
    
    @staticmethod
    def generate_descriptions(dungeon, theme):
        """
        Generate themed descriptions for each room in the dungeon.
        
        Args:
            dungeon: The DungeonLevel to enhance
            theme: Visual theme
            
        Returns:
            The modified dungeon
        """
        # Theme-specific adjectives
        theme_adjectives = {
            "neon": ["glowing", "pulsing", "vibrant", "luminous", "fluorescent", "iridescent", "radiant"],
            "cyber": ["digital", "electronic", "virtual", "cybernetic", "holographic", "synthetic", "artificial"],
            "retro": ["pixelated", "8-bit", "vintage", "classic", "old-school", "nostalgic", "retro-futuristic"]
        }
        
        # Default to neon if theme not found
        adjectives = theme_adjectives.get(theme, theme_adjectives["neon"])
        
        # Generate descriptions for each room based on type
        for r in range(dungeon.rows):
            for c in range(dungeon.cols):
                room = dungeon.at(r, c)
                
                # Skip rooms that already have descriptions
                if room.description:
                    continue
                
                # Get a random adjective
                adj = random.choice(adjectives)
                
                # Generate description based on room type
                if room.room_type == Room.COMBAT:
                    room.description = f"A {adj} chamber with hostile energy patterns forming in the air. Digital constructs begin to take shape as you enter."
                elif room.room_type == Room.TREASURE:
                    room.description = f"A {adj} vault with data crystals embedded in the walls. Valuable resources appear to be stored here."
                elif room.room_type == Room.PUZZLE:
                    room.description = f"A {adj} room with complex patterns on the floor and walls. A central mechanism appears to be waiting for input."
                elif room.room_type == Room.REST:
                    room.description = f"A {adj} sanctuary with calm energy flows. The hostile code of the dungeon seems unable to penetrate this space."
                else:
                    # Generic corridor description
                    exits = room.get_link_directions()
                    exit_str = ", ".join(exits[:-1]) + (" and " + exits[-1] if exits else "")
                    room.description = f"A {adj} corridor with exits leading {exit_str}."
        
        return dungeon