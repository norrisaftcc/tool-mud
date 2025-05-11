"""
Unit tests for the encounter system
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.encounter import Monster, MonsterGenerator, Encounter, EncounterGenerator
from models.dungeon import Room

class TestMonster(unittest.TestCase):
    """Test cases for Monster class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.monster = Monster("Test Monster", 3, Monster.GLITCH)
    
    def test_init(self):
        """Test monster initialization with defaults"""
        self.assertEqual(self.monster.name, "Test Monster")
        self.assertEqual(self.monster.level, 3)
        self.assertEqual(self.monster.monster_type, Monster.GLITCH)
        
        # Should have attributes
        self.assertIn("strength", self.monster.attributes)
        self.assertIn("dexterity", self.monster.attributes)
        self.assertIn("wisdom", self.monster.attributes)
        
        # Should have HP and stats
        self.assertGreater(self.monster.max_hp, 0)
        self.assertEqual(self.monster.hp, self.monster.max_hp)
        self.assertGreater(self.monster.attack, 0)
        self.assertGreater(self.monster.defense, 0)
        
        # Should have abilities
        self.assertGreater(len(self.monster.abilities), 0)
        
        # Should have loot
        self.assertGreater(len(self.monster.loot), 0)
    
    def test_init_with_custom_attributes(self):
        """Test monster initialization with custom attributes"""
        attributes = {
            "strength": 16,
            "dexterity": 14,
            "wisdom": 12
        }
        
        monster = Monster("Custom Monster", 2, Monster.DIGITAL, attributes)
        
        self.assertEqual(monster.attributes["strength"], 16)
        self.assertEqual(monster.attributes["dexterity"], 14)
        self.assertEqual(monster.attributes["wisdom"], 12)
        
        # Stats should be derived from attributes
        self.assertEqual(monster.attack, 2 + (16 // 2))  # level + (strength // 2)
        self.assertEqual(monster.defense, 10 + (14 // 2))  # 10 + (dexterity // 2)
    
    def test_get_loot(self):
        """Test loot generation"""
        # Mock random to always drop items
        with patch('random.random', return_value=0.1):
            loot = self.monster.get_loot()
            # Should get at least one item
            self.assertGreaterEqual(len(loot), 1)
    
    def test_serialization(self):
        """Test monster serialization and deserialization"""
        monster_dict = self.monster.to_dict()
        
        # Create new monster from dict
        new_monster = Monster.from_dict(monster_dict)
        
        # Compare properties
        self.assertEqual(new_monster.name, self.monster.name)
        self.assertEqual(new_monster.level, self.monster.level)
        self.assertEqual(new_monster.monster_type, self.monster.monster_type)
        self.assertEqual(new_monster.hp, self.monster.hp)
        self.assertEqual(new_monster.attack, self.monster.attack)
        self.assertEqual(new_monster.defense, self.monster.defense)
        self.assertEqual(len(new_monster.abilities), len(self.monster.abilities))


class TestMonsterGenerator(unittest.TestCase):
    """Test cases for MonsterGenerator class"""
    
    def test_generate_monster(self):
        """Test basic monster generation"""
        monster = MonsterGenerator.generate_monster(level=2, theme="neon")
        
        self.assertIsInstance(monster, Monster)
        self.assertEqual(monster.level, 2)
        
        # Name should include level
        self.assertIn("Lvl 2", monster.name)
    
    def test_generate_monster_specific_type(self):
        """Test monster generation with specific type"""
        monster = MonsterGenerator.generate_monster(level=3, monster_type=Monster.VIRUS)
        
        self.assertEqual(monster.monster_type, Monster.VIRUS)
    
    def test_generate_boss(self):
        """Test boss monster generation"""
        boss = MonsterGenerator.generate_boss(level=5, theme="cyber")
        
        self.assertIsInstance(boss, Monster)
        
        # Boss should be higher level
        self.assertEqual(boss.level, 7)  # level + 2
        
        # Boss should have boosted stats
        self.assertGreater(boss.attack, 5)
        self.assertGreater(boss.defense, 10)
        
        # Should have a boss ability
        self.assertGreaterEqual(len(boss.abilities), 1)
        
        # Should have a rare item
        has_rare_item = False
        for item in boss.loot:
            if item.get("type") == "rare_item":
                has_rare_item = True
                break
        
        self.assertTrue(has_rare_item)


class TestEncounter(unittest.TestCase):
    """Test cases for Encounter class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.combat_encounter = Encounter(Encounter.COMBAT, 2)
        self.trap_encounter = Encounter(Encounter.TRAP, 3)
        self.puzzle_encounter = Encounter(Encounter.PUZZLE, 1)
    
    def test_init(self):
        """Test encounter initialization"""
        # Test combat encounter
        self.assertEqual(self.combat_encounter.encounter_type, Encounter.COMBAT)
        self.assertEqual(self.combat_encounter.difficulty, 2)
        self.assertFalse(self.combat_encounter.completed)
        self.assertEqual(self.combat_encounter.monsters, [])
        
        # Test trap encounter
        self.assertEqual(self.trap_encounter.encounter_type, Encounter.TRAP)
        self.assertEqual(self.trap_encounter.difficulty, 3)
        self.assertIn(self.trap_encounter.trap_type, ["damage", "status", "teleport"])
        self.assertFalse(self.trap_encounter.detected)
        self.assertFalse(self.trap_encounter.disarmed)
        
        # Test puzzle encounter
        self.assertEqual(self.puzzle_encounter.encounter_type, Encounter.PUZZLE)
        self.assertEqual(self.puzzle_encounter.difficulty, 1)
        self.assertIn(self.puzzle_encounter.puzzle_type, ["sequence", "pattern", "riddle"])
        self.assertFalse(self.puzzle_encounter.solved)
    
    def test_add_monster(self):
        """Test adding monsters to an encounter"""
        monster = Monster("Test Monster", 2)
        
        # Add to combat encounter
        self.combat_encounter.add_monster(monster)
        self.assertEqual(len(self.combat_encounter.monsters), 1)
        
        # Adding to non-combat should do nothing
        self.trap_encounter.add_monster(monster)
        self.assertEqual(len(self.trap_encounter.monsters), 0)
    
    def test_add_reward(self):
        """Test adding rewards to an encounter"""
        reward = {"type": "gold", "amount": 100}
        
        self.combat_encounter.add_reward(reward)
        self.assertIn(reward, self.combat_encounter.rewards)
    
    def test_complete(self):
        """Test completing an encounter"""
        # Add a monster with loot
        monster = Monster("Test Monster", 2)
        self.combat_encounter.add_monster(monster)
        
        # Add a direct reward
        direct_reward = {"type": "item", "name": "Test Item"}
        self.combat_encounter.add_reward(direct_reward)
        
        # Complete the encounter and get rewards
        rewards = self.combat_encounter.complete()
        
        self.assertTrue(self.combat_encounter.completed)
        self.assertGreaterEqual(len(rewards), 1)
        self.assertIn(direct_reward, rewards)
    
    def test_serialization(self):
        """Test encounter serialization and deserialization"""
        # Add content to encounter
        monster = Monster("Test Monster", 2)
        self.combat_encounter.add_monster(monster)
        self.combat_encounter.add_reward({"type": "item", "name": "Test Item"})
        
        # Serialize
        encounter_dict = self.combat_encounter.to_dict()
        
        # Deserialize
        new_encounter = Encounter.from_dict(encounter_dict)
        
        # Compare
        self.assertEqual(new_encounter.encounter_type, self.combat_encounter.encounter_type)
        self.assertEqual(new_encounter.difficulty, self.combat_encounter.difficulty)
        self.assertEqual(len(new_encounter.monsters), 1)
        self.assertEqual(len(new_encounter.rewards), 1)


class TestEncounterGenerator(unittest.TestCase):
    """Test cases for EncounterGenerator class"""
    
    def test_generate_combat_encounter(self):
        """Test generating a combat encounter"""
        encounter = EncounterGenerator.generate_encounter(Room.COMBAT, 2, "neon")
        
        self.assertIsNotNone(encounter)
        self.assertEqual(encounter.encounter_type, Encounter.COMBAT)
        self.assertGreater(len(encounter.monsters), 0)
    
    def test_generate_boss_encounter(self):
        """Test generating a boss encounter"""
        encounter = EncounterGenerator.generate_encounter(Room.BOSS, 3, "cyber")
        
        self.assertIsNotNone(encounter)
        self.assertEqual(encounter.encounter_type, Encounter.COMBAT)
        
        # Should have at least one monster (the boss)
        self.assertGreaterEqual(len(encounter.monsters), 1)
        
        # First monster should be higher level
        boss = encounter.monsters[0]
        self.assertGreater(boss.level, 3)
    
    def test_generate_puzzle_encounter(self):
        """Test generating a puzzle encounter"""
        encounter = EncounterGenerator.generate_encounter(Room.PUZZLE, 2, "neon")
        
        self.assertIsNotNone(encounter)
        self.assertEqual(encounter.encounter_type, Encounter.PUZZLE)
        self.assertIn(encounter.puzzle_type, ["sequence", "pattern", "riddle"])
        
        # Should have a reward
        self.assertGreater(len(encounter.rewards), 0)
    
    def test_generate_treasure_encounter(self):
        """Test generating a trap in a treasure room"""
        # Mock random to guarantee a trap
        with patch('random.random', return_value=0.1):
            encounter = EncounterGenerator.generate_encounter(Room.TREASURE, 2, "neon")
            
            self.assertIsNotNone(encounter)
            self.assertEqual(encounter.encounter_type, Encounter.TRAP)
    
    def test_generate_invalid_room_type(self):
        """Test generating encounter for room type without encounters"""
        encounter = EncounterGenerator.generate_encounter(Room.REST, 2, "neon")
        
        # Should not generate an encounter for rest rooms
        self.assertIsNone(encounter)


if __name__ == '__main__':
    unittest.main()