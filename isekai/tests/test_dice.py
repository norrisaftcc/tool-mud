"""
Unit tests for the dice utilities
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.dice import roll_die, roll_dice, roll_check, attribute_modifier

class TestDice(unittest.TestCase):
    """Test cases for dice rolling functions"""
    
    def test_roll_die(self):
        """Test that roll_die returns value within correct range"""
        # Test d6
        for _ in range(100):  # Multiple tests to check randomization
            result = roll_die(6)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)
        
        # Test d20
        for _ in range(100):
            result = roll_die(20)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 20)
    
    def test_roll_dice(self):
        """Test that roll_dice returns correct number of values and totals them"""
        # Test 3d6
        result = roll_dice(3, 6)
        self.assertEqual(len(result['results']), 3)
        self.assertEqual(result['total'], sum(result['results']))
        
        # Test individual die values are in correct range
        for die_result in result['results']:
            self.assertGreaterEqual(die_result, 1)
            self.assertLessEqual(die_result, 6)
        
        # Test 2d10
        result = roll_dice(2, 10)
        self.assertEqual(len(result['results']), 2)
        self.assertEqual(result['total'], sum(result['results']))
    
    def test_roll_check(self):
        """Test attribute checks against difficulty values"""
        # Mock the dice roll to return a fixed value
        with patch('utils.dice.roll_dice') as mock_roll:
            # Set up mock to return a specific dice result
            mock_roll.return_value = {
                'results': [3, 4, 5],
                'total': 12
            }
            
            # Test success (12 + 2 = 14 >= 10)
            result = roll_check(attribute_mod=2, difficulty=10)
            self.assertTrue(result['success'])
            self.assertEqual(result['modified_total'], 14)
            self.assertEqual(result['margin'], 4)
            
            # Test failure (12 + 0 = 12 < 15)
            result = roll_check(attribute_mod=0, difficulty=15)
            self.assertFalse(result['success'])
            self.assertEqual(result['modified_total'], 12)
            self.assertEqual(result['margin'], -3)
    
    def test_attribute_modifier(self):
        """Test attribute modifier calculation"""
        # Test various attribute values
        self.assertEqual(attribute_modifier(10), 0)  # Average, no modifier
        self.assertEqual(attribute_modifier(11), 0)  # Still no modifier
        self.assertEqual(attribute_modifier(12), 1)  # +1 modifier
        self.assertEqual(attribute_modifier(16), 3)  # +3 modifier
        self.assertEqual(attribute_modifier(8), -1)  # -1 modifier
        self.assertEqual(attribute_modifier(3), -3)  # -3 modifier

if __name__ == '__main__':
    unittest.main()