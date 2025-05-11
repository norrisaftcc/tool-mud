"""
Unit tests for the Character class
"""
import os
import sys
import unittest
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.character import Character

class TestCharacter(unittest.TestCase):
    """Test cases for the Character class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a test character with predefined attributes
        self.test_attributes = {
            'strength': 14,
            'dexterity': 12,
            'wisdom': 10
        }
        self.test_character = Character(
            name="Test Character",
            char_class="Warrior",
            origin="Arcade Cabinet Malfunction",
            attributes=self.test_attributes
        )
    
    def test_character_creation(self):
        """Test character creation with specified attributes"""
        # Check basic character properties
        self.assertEqual(self.test_character.name, "Test Character")
        self.assertEqual(self.test_character.char_class, "Warrior")
        self.assertEqual(self.test_character.origin, "Arcade Cabinet Malfunction")
        self.assertEqual(self.test_character.level, 1)
        
        # Check attributes
        self.assertEqual(self.test_character.attributes['strength'], 14)
        self.assertEqual(self.test_character.attributes['dexterity'], 12)
        self.assertEqual(self.test_character.attributes['wisdom'], 10)
        
        # Check derived stats
        self.assertEqual(self.test_character.max_hp, 10 + (14 // 2))  # 10 + 7
        self.assertEqual(self.test_character.max_mp, 10 + (10 // 2))  # 10 + 5
    
    def test_attribute_rolling(self):
        """Test that attributes are generated correctly when not specified"""
        # Patch the _roll_attributes method to return known values
        with patch.object(Character, '_roll_attributes') as mock_roll:
            mock_roll.return_value = {
                'strength': 16,
                'dexterity': 14,
                'wisdom': 12
            }
            
            # Create character without specifying attributes
            rolled_character = Character(
                name="Rolled Character",
                char_class="Wizard",
                origin="VR Headset Glitch"
            )
            
            # Check attributes were set from roll
            self.assertEqual(rolled_character.attributes['strength'], 16)
            self.assertEqual(rolled_character.attributes['dexterity'], 14)
            self.assertEqual(rolled_character.attributes['wisdom'], 12)
    
    def test_starting_equipment(self):
        """Test that character gets appropriate starting equipment"""
        # Warrior should start with specific equipment
        warrior = Character("Warrior Test", "Warrior", "Test Origin", self.test_attributes)
        self.assertIn({"name": "Iron Sword", "type": "weapon", "damage": "1d8"}, warrior.inventory)
        self.assertEqual(warrior.equipment['weapon'], "Iron Sword")
        
        # Wizard should start with different equipment
        wizard = Character("Wizard Test", "Wizard", "Test Origin", self.test_attributes)
        self.assertIn({"name": "Apprentice Staff", "type": "weapon", "damage": "1d6"}, wizard.inventory)
        self.assertEqual(wizard.equipment['weapon'], "Apprentice Staff")
    
    def test_to_dict(self):
        """Test conversion to dictionary for serialization"""
        char_dict = self.test_character.to_dict()
        
        # Check main attributes
        self.assertEqual(char_dict['name'], "Test Character")
        self.assertEqual(char_dict['class'], "Warrior")
        self.assertEqual(char_dict['attributes'], self.test_attributes)
        
        # Check that dict has all required fields
        required_fields = ['name', 'class', 'origin', 'level', 'xp', 'attributes', 
                          'hp', 'mp', 'max_hp', 'max_mp', 'inventory', 'equipment', 'skills']
        for field in required_fields:
            self.assertIn(field, char_dict)
    
    def test_from_dict(self):
        """Test creating character from dictionary"""
        # Convert character to dict, then create new character from it
        char_dict = self.test_character.to_dict()
        restored_character = Character.from_dict(char_dict)
        
        # Check they're equivalent
        self.assertEqual(restored_character.name, self.test_character.name)
        self.assertEqual(restored_character.char_class, self.test_character.char_class)
        self.assertEqual(restored_character.attributes, self.test_character.attributes)
        self.assertEqual(restored_character.inventory, self.test_character.inventory)
    
    def test_level_up(self):
        """Test level up mechanics"""
        # Record initial stats
        initial_level = self.test_character.level
        initial_max_hp = self.test_character.max_hp
        initial_max_mp = self.test_character.max_mp
        
        # Level up the character
        self.test_character.level_up()
        
        # Check level increased
        self.assertEqual(self.test_character.level, initial_level + 1)
        
        # Check HP and MP increased
        self.assertGreater(self.test_character.max_hp, initial_max_hp)
        self.assertGreater(self.test_character.max_mp, initial_max_mp)
        
        # Check HP and MP are fully restored
        self.assertEqual(self.test_character.hp, self.test_character.max_hp)
        self.assertEqual(self.test_character.mp, self.test_character.max_mp)
    
    def test_gain_xp(self):
        """Test gaining XP and level up trigger"""
        # Character starts at level 1, needs 1000 XP to level up
        self.assertEqual(self.test_character.level, 1)
        self.assertEqual(self.test_character.xp, 0)
        
        # Add some XP but not enough to level up
        level_up_occurred = self.test_character.gain_xp(500)
        self.assertFalse(level_up_occurred)
        self.assertEqual(self.test_character.level, 1)
        self.assertEqual(self.test_character.xp, 500)
        
        # Add enough XP to level up
        level_up_occurred = self.test_character.gain_xp(500)
        self.assertTrue(level_up_occurred)
        self.assertEqual(self.test_character.level, 2)
        self.assertEqual(self.test_character.xp, 1000)
    
    def test_use_skill(self):
        """Test using character skills"""
        # Character should have skills based on their class
        self.assertGreater(len(self.test_character.skills), 0)
        
        # Test using a skill
        skill_name = self.test_character.skills[0]['name']
        result = self.test_character.use_skill(skill_name)
        
        # Skill use should succeed
        self.assertTrue(result['success'])
        self.assertEqual(result['skill'], skill_name)
        
        # MP should be used
        skill_mp_cost = self.test_character.skills[0]['mp_cost']
        self.assertEqual(self.test_character.mp, self.test_character.max_mp - skill_mp_cost)
        
        # Test using a non-existent skill
        result = self.test_character.use_skill("Nonexistent Skill")
        self.assertFalse(result['success'])

if __name__ == '__main__':
    unittest.main()