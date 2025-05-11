"""
Unit tests for crafting system
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.character import Character

# Create a simple crafting module that we can test, based on The Forge implementation
class CraftingSystem:
    @staticmethod
    def check_recipe(component_names, recipes):
        """Check if components match a known recipe"""
        for recipe in recipes:
            if sorted(recipe["components"]) == sorted(component_names):
                return recipe
        return None
    
    @staticmethod
    def determine_quality(roll):
        """Determine item quality based on roll"""
        if roll >= 18:
            return "Excellent", 3, 8
        elif roll >= 15:
            return "Great", 2, 6  
        elif roll >= 10:
            return "Good", 1, 4
        else:
            return "Poor", 0, 4
    
    @staticmethod
    def process_stats(recipe, quality_value, quality_dice):
        """Process stats from recipe with quality values"""
        stats = {}
        for stat_name, stat_formula in recipe.get("stats", {}).items():
            # Replace placeholders with actual values
            stat_value = stat_formula.replace("[QUALITY]", str(quality_value))
            stat_value = stat_value.replace("[DICE]", str(quality_dice))
            stats[stat_name] = stat_value
        return stats
    
    @staticmethod
    def craft_item(components, character, roll, recipes):
        """Main crafting function"""
        # Check if components match a recipe
        component_names = [c["name"] for c in components]
        recipe = CraftingSystem.check_recipe(component_names, recipes)
        
        if not recipe:
            return {
                "success": False,
                "reason": "Components don't form a known recipe"
            }
        
        # Apply character modifier based on item type and class
        item_type = recipe["type"]
        character_class = character["class"]
        
        if item_type == "weapon" and character_class == "Warrior":
            attribute_name = "strength"
        elif (item_type == "weapon" and character_class == "Wizard") or item_type == "accessory":
            attribute_name = "wisdom"
        else:
            attribute_name = "dexterity"
        
        # Calculate attribute modifier
        attribute_value = character["attributes"][attribute_name]
        mod = (attribute_value - 10) // 2
        
        # Apply class affinity bonus
        affinity_bonus = 2 if recipe.get("class_affinity") == character_class else 0
        
        # Calculate total roll
        total_roll = roll + mod + affinity_bonus
        
        # Check if crafting succeeds (difficulty 10)
        if total_roll < 10:
            return {
                "success": False,
                "reason": "Crafting attempt failed"
            }
        
        # Determine quality
        quality, quality_value, quality_dice = CraftingSystem.determine_quality(total_roll)
        
        # Process stats
        stats = CraftingSystem.process_stats(recipe, quality_value, quality_dice)
        
        # Create item
        item = {
            "name": recipe["name"],
            "type": recipe["type"],
            "description": recipe["description"],
            "quality": quality,
            "stats": stats
        }
        
        return {
            "success": True,
            "item": item
        }

class TestCrafting(unittest.TestCase):
    """Test cases for crafting system"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Sample recipes
        self.test_recipes = [
            {
                "name": "Flaming Sword",
                "type": "weapon",
                "class_affinity": "Warrior",
                "components": ["Iron Chunk", "Fire Essence", "Damage Rune"],
                "description": "A sword imbued with the power of fire.",
                "stats": {
                    "damage": "1d8+[QUALITY]",
                    "elemental": "1d[DICE] fire"
                }
            },
            {
                "name": "Healing Charm",
                "type": "accessory",
                "class_affinity": "White Mage",
                "components": ["Glowing Herb", "Mana Crystal", "Shield Rune"],
                "description": "A charm that heals over time.",
                "stats": {
                    "effect": "Regenerate [QUALITY] HP per turn",
                    "uses": "[QUALITY] uses per day"
                }
            }
        ]
        
        # Sample components
        self.test_components = [
            {"name": "Iron Chunk", "type": "metal", "quality": "basic", "icon": "🔩"},
            {"name": "Fire Essence", "type": "elemental", "element": "fire", "icon": "🔥"},
            {"name": "Damage Rune", "type": "rune", "effect": "damage", "icon": "🔆"}
        ]
        
        # Test character
        self.test_character = {
            "name": "Test Warrior",
            "class": "Warrior",
            "attributes": {
                "strength": 14,
                "dexterity": 12,
                "wisdom": 10
            }
        }
    
    def test_recipe_matching(self):
        """Test that component combinations match recipes correctly"""
        # Test matching recipe
        components = ["Iron Chunk", "Fire Essence", "Damage Rune"]
        recipe = CraftingSystem.check_recipe(components, self.test_recipes)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe["name"], "Flaming Sword")
        
        # Test mismatched recipe
        components = ["Iron Chunk", "Fire Essence", "Shield Rune"]  # Wrong combination
        recipe = CraftingSystem.check_recipe(components, self.test_recipes)
        self.assertIsNone(recipe)
        
        # Test order independence
        components = ["Damage Rune", "Fire Essence", "Iron Chunk"]  # Different order
        recipe = CraftingSystem.check_recipe(components, self.test_recipes)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe["name"], "Flaming Sword")
    
    def test_quality_determination(self):
        """Test quality levels based on roll results"""
        # Test different roll ranges
        quality, value, dice = CraftingSystem.determine_quality(18)
        self.assertEqual(quality, "Excellent")
        self.assertEqual(value, 3)
        self.assertEqual(dice, 8)
        
        quality, value, dice = CraftingSystem.determine_quality(15)
        self.assertEqual(quality, "Great")
        self.assertEqual(value, 2)
        self.assertEqual(dice, 6)
        
        quality, value, dice = CraftingSystem.determine_quality(10)
        self.assertEqual(quality, "Good")
        self.assertEqual(value, 1)
        self.assertEqual(dice, 4)
        
        quality, value, dice = CraftingSystem.determine_quality(9)
        self.assertEqual(quality, "Poor")
        self.assertEqual(value, 0)
        self.assertEqual(dice, 4)
    
    def test_stat_processing(self):
        """Test that item stats are processed correctly"""
        recipe = self.test_recipes[0]  # Flaming Sword
        
        # Test excellent quality
        stats = CraftingSystem.process_stats(recipe, 3, 8)
        self.assertEqual(stats["damage"], "1d8+3")
        self.assertEqual(stats["elemental"], "1d8 fire")
        
        # Test good quality
        stats = CraftingSystem.process_stats(recipe, 1, 4)
        self.assertEqual(stats["damage"], "1d8+1")
        self.assertEqual(stats["elemental"], "1d4 fire")
    
    def test_successful_crafting(self):
        """Test successful item crafting"""
        # Craft with high roll
        result = CraftingSystem.craft_item(
            self.test_components, 
            self.test_character,
            15,  # High roll
            self.test_recipes
        )
        
        # Check success
        self.assertTrue(result["success"])
        self.assertEqual(result["item"]["name"], "Flaming Sword")
        
        # Check item has expected attributes
        self.assertIn("quality", result["item"])
        self.assertIn("stats", result["item"])
        self.assertIn("damage", result["item"]["stats"])
    
    def test_failed_crafting(self):
        """Test failed crafting attempts"""
        # Test with invalid recipe
        wrong_components = [
            {"name": "Iron Chunk", "type": "metal"},
            {"name": "Fire Essence", "type": "elemental"},
            {"name": "Shield Rune", "type": "rune"}  # Wrong rune
        ]
        
        result = CraftingSystem.craft_item(
            wrong_components,
            self.test_character,
            15,
            self.test_recipes
        )
        
        # Should fail due to recipe mismatch
        self.assertFalse(result["success"])
        self.assertIn("recipe", result["reason"].lower())
        
        # Test with low roll
        result = CraftingSystem.craft_item(
            self.test_components,
            self.test_character,
            5,  # Low roll
            self.test_recipes
        )
        
        # Should fail due to low roll
        self.assertFalse(result["success"])
        self.assertIn("failed", result["reason"].lower())
    
    def test_class_affinity_bonus(self):
        """Test class affinity bonuses"""
        # Warrior has affinity with Flaming Sword
        warrior_result = CraftingSystem.craft_item(
            self.test_components,
            self.test_character,  # Warrior
            10,  # Borderline roll, with affinity bonus should succeed well
            self.test_recipes
        )
        
        # Should succeed with better quality due to affinity
        self.assertTrue(warrior_result["success"])
        
        # Change to White Mage (no affinity)
        mage_character = self.test_character.copy()
        mage_character["class"] = "White Mage"
        
        mage_result = CraftingSystem.craft_item(
            self.test_components,
            mage_character,
            10,  # Same roll, but no affinity bonus
            self.test_recipes
        )
        
        # Should still succeed but with lower quality
        self.assertTrue(mage_result["success"])
        
        # Warrior should get better quality than mage with same roll
        self.assertNotEqual(
            warrior_result["item"]["quality"],
            mage_result["item"]["quality"]
        )

if __name__ == '__main__':
    unittest.main()