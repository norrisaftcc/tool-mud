"""
Unit tests for the dungeon model and generation
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.dungeon import Room, DungeonLevel, DungeonGenerator

class TestRoom(unittest.TestCase):
    """Test cases for Room class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.room = Room(1, 2)
    
    def test_init(self):
        """Test room initialization"""
        self.assertEqual(self.room.row, 1)
        self.assertEqual(self.room.col, 2)
        self.assertEqual(self.room.links, 0)
        self.assertIsNone(self.room.room_type)
        self.assertFalse(self.room.discovered)
        self.assertFalse(self.room.visited)
        self.assertEqual(self.room.encounters, [])
        self.assertEqual(self.room.treasures, [])
        self.assertEqual(self.room.features, [])
    
    def test_linking(self):
        """Test room linking functions"""
        # Test linking in a direction
        self.room.link(Room.NORTH)
        self.assertTrue(self.room.linked(Room.NORTH))
        self.assertFalse(self.room.linked(Room.SOUTH))
        
        # Test multiple directions
        self.room.link(Room.EAST)
        self.assertTrue(self.room.linked(Room.NORTH))
        self.assertTrue(self.room.linked(Room.EAST))
        
        # Test unlinking
        self.room.unlink(Room.NORTH)
        self.assertFalse(self.room.linked(Room.NORTH))
        self.assertTrue(self.room.linked(Room.EAST))
    
    def test_get_links(self):
        """Test getting linked directions"""
        self.room.link(Room.NORTH)
        self.room.link(Room.EAST)
        
        links = self.room.get_links()
        self.assertEqual(len(links), 2)
        self.assertIn(Room.NORTH, links)
        self.assertIn(Room.EAST, links)
    
    def test_get_link_directions(self):
        """Test getting link direction names"""
        self.room.link(Room.NORTH)
        self.room.link(Room.EAST)
        
        directions = self.room.get_link_directions()
        self.assertEqual(len(directions), 2)
        self.assertIn("north", directions)
        self.assertIn("east", directions)
    
    def test_set_room_type(self):
        """Test setting room type updates description"""
        self.room.set_room_type(Room.ENTRANCE)
        self.assertEqual(self.room.room_type, Room.ENTRANCE)
        self.assertNotEqual(self.room.description, "")
        
        # Test custom description preserved
        custom_desc = "Custom room description"
        self.room.set_description(custom_desc)
        self.room.set_room_type(Room.COMBAT)
        self.assertEqual(self.room.description, custom_desc)
    
    def test_enter_room(self):
        """Test entering a room updates its state"""
        self.room.set_room_type(Room.REST)
        character = {"attributes": {"wisdom": 10}, "hp": 5, "max_hp": 10}
        
        result = self.room.enter_room(character)
        
        self.assertTrue(self.room.visited)
        self.assertIn("events", result)
        self.assertIn("You enter", result["events"][0])
        self.assertGreater(character["hp"], 5)  # Should heal in rest room
    
    def test_serialization(self):
        """Test room serialization and deserialization"""
        self.room.set_room_type(Room.TREASURE)
        self.room.link(Room.SOUTH)
        self.room.add_treasure({"type": "gold", "value": 100})
        
        # Convert to dict
        room_dict = self.room.to_dict()
        
        # Create new room from dict
        new_room = Room.from_dict(room_dict)
        
        # Compare properties
        self.assertEqual(new_room.row, self.room.row)
        self.assertEqual(new_room.col, self.room.col)
        self.assertEqual(new_room.room_type, self.room.room_type)
        self.assertEqual(new_room.links, self.room.links)
        self.assertEqual(len(new_room.treasures), 1)


class TestDungeonLevel(unittest.TestCase):
    """Test cases for DungeonLevel class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.dungeon = DungeonLevel(5, 5, 1, "neon")
    
    def test_init(self):
        """Test dungeon initialization"""
        self.assertEqual(self.dungeon.rows, 5)
        self.assertEqual(self.dungeon.cols, 5)
        self.assertEqual(self.dungeon.level_num, 1)
        self.assertEqual(self.dungeon.theme, "neon")
        
        # Check that rooms were initialized
        for r in range(self.dungeon.rows):
            for c in range(self.dungeon.cols):
                room = self.dungeon.at(r, c)
                self.assertIsInstance(room, Room)
                self.assertEqual(room.row, r)
                self.assertEqual(room.col, c)
    
    def test_is_valid(self):
        """Test position validation"""
        self.assertTrue(self.dungeon.is_valid(0, 0))
        self.assertTrue(self.dungeon.is_valid(4, 4))
        self.assertFalse(self.dungeon.is_valid(-1, 0))
        self.assertFalse(self.dungeon.is_valid(0, -1))
        self.assertFalse(self.dungeon.is_valid(5, 0))
        self.assertFalse(self.dungeon.is_valid(0, 5))
    
    def test_at(self):
        """Test room access"""
        room = self.dungeon.at(2, 3)
        self.assertEqual(room.row, 2)
        self.assertEqual(room.col, 3)
        
        # Test out of bounds
        with self.assertRaises(IndexError):
            self.dungeon.at(10, 10)
    
    def test_linking_rooms(self):
        """Test linking rooms in the dungeon"""
        room1 = self.dungeon.at(1, 1)
        
        # Link to the north
        result = self.dungeon.link_rooms(room1, Room.NORTH)
        self.assertTrue(result)
        
        # Check both rooms are linked
        room2 = self.dungeon.at(0, 1)  # Room to the north
        self.assertTrue(room1.linked(Room.NORTH))
        self.assertTrue(room2.linked(Room.SOUTH))
        
        # Test linking to invalid position
        edge_room = self.dungeon.at(0, 0)
        result = self.dungeon.link_rooms(edge_room, Room.NORTH)
        self.assertFalse(result)
    
    def test_entrance_exit(self):
        """Test setting entrance and exit"""
        self.dungeon.set_entrance(4, 2)
        self.dungeon.set_exit(0, 2)
        
        self.assertEqual(self.dungeon.entrance.row, 4)
        self.assertEqual(self.dungeon.entrance.col, 2)
        self.assertEqual(self.dungeon.entrance.room_type, Room.ENTRANCE)
        
        self.assertEqual(self.dungeon.exit.row, 0)
        self.assertEqual(self.dungeon.exit.col, 2)
        self.assertEqual(self.dungeon.exit.room_type, Room.EXIT)
    
    def test_discover_room(self):
        """Test room discovery"""
        room = self.dungeon.at(2, 2)
        
        # Link to adjacent rooms
        self.dungeon.link_rooms(room, Room.NORTH)
        self.dungeon.link_rooms(room, Room.EAST)
        
        # Discover the room
        self.dungeon.discover_room(2, 2)
        
        # Room should be discovered
        self.assertTrue(room.discovered)
        
        # Linked rooms should be discovered
        north_room = self.dungeon.at(1, 2)
        east_room = self.dungeon.at(2, 3)
        self.assertTrue(north_room.discovered)
        self.assertTrue(east_room.discovered)
        
        # Unlinked rooms should not be discovered
        south_room = self.dungeon.at(3, 2)
        west_room = self.dungeon.at(2, 1)
        self.assertFalse(south_room.discovered)
        self.assertFalse(west_room.discovered)
    
    def test_serialization(self):
        """Test dungeon serialization and deserialization"""
        # Set up a simple dungeon
        self.dungeon.set_entrance(4, 2)
        self.dungeon.set_exit(0, 2)
        
        # Link some rooms
        room = self.dungeon.at(2, 2)
        self.dungeon.link_rooms(room, Room.NORTH)
        self.dungeon.link_rooms(room, Room.EAST)
        
        # Serialize to dict
        dungeon_dict = self.dungeon.to_dict()
        
        # Create new dungeon from dict
        new_dungeon = DungeonLevel.from_dict(dungeon_dict)
        
        # Compare properties
        self.assertEqual(new_dungeon.rows, self.dungeon.rows)
        self.assertEqual(new_dungeon.cols, self.dungeon.cols)
        self.assertEqual(new_dungeon.level_num, self.dungeon.level_num)
        self.assertEqual(new_dungeon.theme, self.dungeon.theme)
        
        # Check entrance and exit
        self.assertEqual(new_dungeon.entrance.row, self.dungeon.entrance.row)
        self.assertEqual(new_dungeon.entrance.col, self.dungeon.entrance.col)
        self.assertEqual(new_dungeon.exit.row, self.dungeon.exit.row)
        self.assertEqual(new_dungeon.exit.col, self.dungeon.exit.col)
        
        # Check a linked room
        room = new_dungeon.at(2, 2)
        self.assertTrue(room.linked(Room.NORTH))
        self.assertTrue(room.linked(Room.EAST))


class TestDungeonGenerator(unittest.TestCase):
    """Test cases for DungeonGenerator class"""
    
    def test_generate_dungeon(self):
        """Test generating a complete dungeon"""
        # Generate with default parameters
        dungeon = DungeonGenerator.generate_dungeon(rows=8, cols=8, seed=42)
        
        # Basic checks
        self.assertEqual(dungeon.rows, 8)
        self.assertEqual(dungeon.cols, 8)
        
        # Entrance and exit should be set
        self.assertIsNotNone(dungeon.entrance)
        self.assertEqual(dungeon.entrance.room_type, Room.ENTRANCE)
        self.assertIsNotNone(dungeon.exit)
        self.assertEqual(dungeon.exit.room_type, Room.EXIT)
        
        # Check room types
        room_types = {}
        for r in range(dungeon.rows):
            for c in range(dungeon.cols):
                room = dungeon.at(r, c)
                if room.room_type is not None:
                    room_types[room.room_type] = room_types.get(room.room_type, 0) + 1
        
        # Should have at least some combat and treasure rooms
        self.assertGreater(room_types.get(Room.COMBAT, 0), 0)
        self.assertGreater(room_types.get(Room.TREASURE, 0), 0)
    
    def test_different_algorithms(self):
        """Test different generation algorithms"""
        # BSP algorithm
        bsp_dungeon = DungeonGenerator.generate_dungeon(
            rows=5, cols=5, algorithm="bsp", seed=42
        )
        self.assertIsNotNone(bsp_dungeon)
        
        # Maze algorithm
        maze_dungeon = DungeonGenerator.generate_dungeon(
            rows=5, cols=5, algorithm="maze", seed=42
        )
        self.assertIsNotNone(maze_dungeon)
        
        # Cellular automata algorithm
        cellular_dungeon = DungeonGenerator.generate_dungeon(
            rows=5, cols=5, algorithm="cellular", seed=42
        )
        self.assertIsNotNone(cellular_dungeon)


if __name__ == '__main__':
    unittest.main()