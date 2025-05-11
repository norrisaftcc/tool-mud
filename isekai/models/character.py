"""
Character class for Neon D&D Isekai
"""
import random

class Character:
    """Character class representing player characters in the game"""
    
    def __init__(self, name, char_class, origin, attributes=None):
        """
        Initialize a new character
        
        Args:
            name: Character name
            char_class: Character class (Warrior, Wizard, White Mage, Wanderer)
            origin: Isekai origin story
            attributes: Dict of attributes (str, dex, wis) or None to roll them
        """
        self.name = name
        self.char_class = char_class
        self.origin = origin
        self.level = 1
        self.xp = 0
        
        # Set attributes - either provided or rolled
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = self._roll_attributes()
            
        # Calculate derived stats
        self.max_hp = 10 + (self.attributes['strength'] // 2)
        self.max_mp = 10 + (self.attributes['wisdom'] // 2)
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # Initialize inventory and equipment
        self.inventory = []
        self.equipment = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }
        
        # Set class-specific starting equipment
        self._set_starting_equipment()
        
        # Set skills based on class
        self.skills = self._get_class_skills()
        
    def _roll_attributes(self):
        """Roll character attributes"""
        attributes = {
            'strength': 0,
            'dexterity': 0,
            'wisdom': 0
        }
        
        # Roll 4d6 drop lowest for each attribute
        for attr in attributes:
            rolls = [random.randint(1, 6) for _ in range(4)]
            attributes[attr] = sum(sorted(rolls)[1:])  # Drop lowest
            
        return attributes
    
    def _set_starting_equipment(self):
        """Set class-specific starting equipment"""
        if self.char_class == "Warrior":
            self.inventory.append({"name": "Iron Sword", "type": "weapon", "damage": "1d8"})
            self.inventory.append({"name": "Leather Armor", "type": "armor", "defense": 2})
            self.equipment['weapon'] = "Iron Sword"
            self.equipment['armor'] = "Leather Armor"
            
        elif self.char_class == "Wizard":
            self.inventory.append({"name": "Apprentice Staff", "type": "weapon", "damage": "1d6"})
            self.inventory.append({"name": "Spellbook", "type": "accessory", "effect": "+1 to spell damage"})
            self.equipment['weapon'] = "Apprentice Staff"
            self.equipment['accessory'] = "Spellbook"
            
        elif self.char_class == "White Mage":
            self.inventory.append({"name": "Healing Rod", "type": "weapon", "damage": "1d4"})
            self.inventory.append({"name": "White Robes", "type": "armor", "defense": 1})
            self.equipment['weapon'] = "Healing Rod"
            self.equipment['armor'] = "White Robes"
            
        elif self.char_class == "Wanderer":
            self.inventory.append({"name": "Shortbow", "type": "weapon", "damage": "1d6"})
            self.inventory.append({"name": "Traveler's Cloak", "type": "armor", "defense": 1})
            self.equipment['weapon'] = "Shortbow"
            self.equipment['armor'] = "Traveler's Cloak"
            
    def _get_class_skills(self):
        """Get class-specific skills"""
        skills = []
        
        if self.char_class == "Warrior":
            skills = [
                {"name": "Power Attack", "mp_cost": 0, "description": "Deal extra damage but with reduced accuracy"},
                {"name": "Defend", "mp_cost": 0, "description": "Reduce damage taken until your next turn"}
            ]
        elif self.char_class == "Wizard":
            skills = [
                {"name": "Arcane Missile", "mp_cost": 3, "description": "Deal 1d4+1 damage to a target"},
                {"name": "Shield", "mp_cost": 4, "description": "Create a protective barrier for 1d4 turns"}
            ]
        elif self.char_class == "White Mage":
            skills = [
                {"name": "Heal", "mp_cost": 3, "description": "Restore 1d6+1 HP to a target"},
                {"name": "Bless", "mp_cost": 2, "description": "Increase an ally's next roll by 2"}
            ]
        elif self.char_class == "Wanderer":
            skills = [
                {"name": "Quick Shot", "mp_cost": 0, "description": "Deal 1d6 damage from range"},
                {"name": "Evade", "mp_cost": 2, "description": "High chance to avoid the next attack"}
            ]
            
        return skills
    
    def gain_xp(self, amount):
        """
        Add XP and handle level ups
        
        Args:
            amount: XP amount to add
            
        Returns:
            Boolean indicating if level up occurred
        """
        self.xp += amount
        
        # Check for level up (simple formula: level * 1000 XP needed)
        xp_needed = self.level * 1000
        
        if self.xp >= xp_needed:
            self.level_up()
            return True
            
        return False
    
    def level_up(self):
        """Handle level up effects"""
        self.level += 1
        
        # Increase HP and MP
        hp_increase = random.randint(1, 6) + (self.attributes['strength'] // 4)
        mp_increase = random.randint(1, 4) + (self.attributes['wisdom'] // 4)
        
        self.max_hp += hp_increase
        self.max_mp += mp_increase
        
        # Heal to full on level up
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # Add new skill every 3 levels
        if self.level % 3 == 0:
            self._add_advanced_skill()
            
    def _add_advanced_skill(self):
        """Add a class-specific advanced skill"""
        advanced_skills = {
            "Warrior": [
                {"name": "Whirlwind", "mp_cost": 2, "description": "Attack all enemies for 1d6 damage"},
                {"name": "Unbreakable", "mp_cost": 4, "description": "Reduce all damage by half for 3 turns"}
            ],
            "Wizard": [
                {"name": "Fireball", "mp_cost": 6, "description": "Deal 2d6 fire damage to all enemies"},
                {"name": "Time Stop", "mp_cost": 8, "description": "Take an extra action"}
            ],
            "White Mage": [
                {"name": "Mass Heal", "mp_cost": 6, "description": "Heal all allies for 1d4+2 HP"},
                {"name": "Revive", "mp_cost": 10, "description": "Restore a fallen ally with 1/2 HP"}
            ],
            "Wanderer": [
                {"name": "Sneak Attack", "mp_cost": 3, "description": "Deal 2d6 damage if enemy hasn't acted"},
                {"name": "Smoke Bomb", "mp_cost": 4, "description": "Escape combat or cause enemies to miss"}
            ]
        }
        
        # Get available skills for this class
        available_skills = advanced_skills.get(self.char_class, [])
        
        # Get skill names we already have
        existing_skill_names = [skill["name"] for skill in self.skills]
        
        # Filter to skills we don't have yet
        new_skills = [skill for skill in available_skills if skill["name"] not in existing_skill_names]
        
        if new_skills:
            # Add a random new skill
            self.skills.append(random.choice(new_skills))
    
    def equip_item(self, item_name):
        """
        Equip an item from inventory
        
        Args:
            item_name: Name of item to equip
            
        Returns:
            Boolean indicating success
        """
        # Find item in inventory
        item = next((item for item in self.inventory if item["name"] == item_name), None)
        
        if not item:
            return False
            
        # Equip based on type
        if item.get("type") in self.equipment:
            self.equipment[item["type"]] = item["name"]
            return True
            
        return False
    
    def use_skill(self, skill_name, target=None):
        """
        Use a character skill
        
        Args:
            skill_name: Name of skill to use
            target: Optional target for the skill
            
        Returns:
            Dictionary with skill result information
        """
        # Find the skill
        skill = next((s for s in self.skills if s["name"] == skill_name), None)
        
        if not skill:
            return {"success": False, "message": f"Skill {skill_name} not found"}
            
        # Check MP cost
        if self.mp < skill["mp_cost"]:
            return {"success": False, "message": "Not enough MP"}
            
        # Use MP
        self.mp -= skill["mp_cost"]
        
        # Implement skill effects (simplified)
        result = {"success": True, "skill": skill_name}
        
        if skill_name == "Power Attack":
            damage = random.randint(1, 8) + self.attributes["strength"] // 2 + 2
            result["damage"] = damage
            result["message"] = f"Powerful attack deals {damage} damage!"
            
        elif skill_name == "Arcane Missile":
            damage = random.randint(1, 4) + 1
            result["damage"] = damage
            result["message"] = f"Magic missile hits for {damage} damage!"
            
        elif skill_name == "Heal":
            healing = random.randint(1, 6) + 1
            result["healing"] = healing
            result["message"] = f"Healing magic restores {healing} HP!"
            
        elif skill_name == "Quick Shot":
            damage = random.randint(1, 6)
            result["damage"] = damage
            result["message"] = f"Quick arrow deals {damage} damage!"
            
        else:
            result["message"] = f"Used {skill_name}!"
            
        return result
    
    def to_dict(self):
        """Convert character to dictionary for storage"""
        return {
            "name": self.name,
            "class": self.char_class,
            "origin": self.origin,
            "level": self.level,
            "xp": self.xp,
            "attributes": self.attributes,
            "hp": self.hp,
            "mp": self.mp,
            "max_hp": self.max_hp,
            "max_mp": self.max_mp,
            "inventory": self.inventory,
            "equipment": self.equipment,
            "skills": self.skills
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create character from dictionary data"""
        # Create a basic character
        character = cls(
            name=data["name"],
            char_class=data["class"],
            origin=data["origin"],
            attributes=data["attributes"]
        )
        
        # Override with saved data
        character.level = data["level"]
        character.xp = data["xp"]
        character.hp = data["hp"]
        character.mp = data["mp"]
        character.max_hp = data["max_hp"]
        character.max_mp = data["max_mp"]
        character.inventory = data["inventory"]
        character.equipment = data["equipment"]
        character.skills = data["skills"]
        
        return character