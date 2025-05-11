"""
Encounter system for the EXPLORE quadrant.

This module contains the classes for handling encounters in dungeons,
including combat, traps, and puzzles.
"""

import random
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class Monster:
    """
    Monster represents an enemy in a combat encounter.
    """
    # Monster types
    GLITCH = 1        # Error-based monsters
    DIGITAL = 2       # Data-based monsters
    CORRUPTED = 3     # Corrupted program monsters
    VIRUS = 4         # Malicious code monsters
    
    # Monster type names for display
    TYPE_NAMES = {
        GLITCH: "Glitch",
        DIGITAL: "Digital",
        CORRUPTED: "Corrupted",
        VIRUS: "Virus"
    }
    
    def __init__(self, name, level, monster_type=None, attributes=None, abilities=None):
        """
        Initialize a new monster.
        
        Args:
            name: Monster name
            level: Monster level (determines base stats)
            monster_type: Type of monster (affects abilities and stats)
            attributes: Optional dict of attributes (str, dex, wis)
            abilities: Optional list of special abilities
        """
        self.name = name
        self.level = level
        self.monster_type = monster_type or random.choice([Monster.GLITCH, Monster.DIGITAL, Monster.CORRUPTED, Monster.VIRUS])
        
        # Set attributes based on level and type if not provided
        self.attributes = attributes or self._generate_attributes()
        
        # Set derived stats
        self.max_hp = 5 + (level * 3) + (self.attributes['strength'] // 2)
        self.hp = self.max_hp
        
        # Attack and defense derived from attributes and level
        self.attack = level + (self.attributes['strength'] // 2)
        self.defense = 10 + (self.attributes['dexterity'] // 2)
        
        # Special abilities
        self.abilities = abilities or self._generate_abilities()
        
        # Loot table
        self.loot = self._generate_loot()
    
    def _generate_attributes(self):
        """Generate attributes based on monster level and type."""
        # Base attributes scale with level
        attributes = {
            "strength": 10 + self.level,
            "dexterity": 10 + self.level,
            "wisdom": 10 + self.level
        }
        
        # Adjust based on monster type
        if self.monster_type == Monster.GLITCH:
            attributes["dexterity"] += 2  # Glitches are quick and unpredictable
        elif self.monster_type == Monster.DIGITAL:
            attributes["wisdom"] += 2     # Digital entities are smart
        elif self.monster_type == Monster.CORRUPTED:
            attributes["strength"] += 2   # Corrupted entities are strong
        elif self.monster_type == Monster.VIRUS:
            # Viruses are balanced but dangerous
            attributes["strength"] += 1
            attributes["dexterity"] += 1
        
        return attributes
    
    def _generate_abilities(self):
        """Generate special abilities based on monster type and level."""
        abilities = []
        
        # All monsters get more abilities as they level up
        num_abilities = 1 + (self.level // 3)
        
        # Type-specific ability pools
        type_abilities = {
            Monster.GLITCH: [
                {"name": "Glitch Strike", "damage_multiplier": 1.5, "target": "single"},
                {"name": "Corruption Field", "damage": 2, "target": "all"},
                {"name": "Disrupt", "effect": "reduce_defense", "amount": 2, "duration": 2},
                {"name": "Error Cascade", "damage": 1, "effect": "confusion", "duration": 2}
            ],
            Monster.DIGITAL: [
                {"name": "Data Spike", "damage_multiplier": 1.2, "target": "single"},
                {"name": "Logic Bomb", "damage": 3, "target": "single"},
                {"name": "Firewall", "effect": "shield", "amount": 3, "duration": 2},
                {"name": "System Scan", "effect": "reveal_weakness", "duration": 2}
            ],
            Monster.CORRUPTED: [
                {"name": "Corrupt Strike", "damage_multiplier": 1.3, "target": "single"},
                {"name": "Virus Spread", "damage": 1, "effect": "damage_over_time", "amount": 1, "duration": 3},
                {"name": "Memory Leak", "effect": "reduce_mp", "amount": 2},
                {"name": "System Crash", "damage": 4, "cooldown": 3}
            ],
            Monster.VIRUS: [
                {"name": "Infect", "damage": 1, "effect": "weaken", "amount": 1, "duration": 3},
                {"name": "Replicate", "effect": "summon", "cooldown": 4},
                {"name": "Data Drain", "damage": 2, "heal_percent": 50},
                {"name": "Encryption", "effect": "increase_defense", "amount": 3, "duration": 2}
            ]
        }
        
        # Select abilities from the pool for this monster type
        available_abilities = type_abilities.get(self.monster_type, [])
        
        # Ensure we don't try to get more abilities than available
        num_abilities = min(num_abilities, len(available_abilities))
        
        # Select random abilities without replacement
        selected_indices = random.sample(range(len(available_abilities)), num_abilities)
        
        for index in selected_indices:
            abilities.append(available_abilities[index])
        
        return abilities
    
    def _generate_loot(self):
        """Generate loot table based on monster level and type."""
        loot_table = []
        
        # Chance to drop crafting components
        if random.random() < 0.3 + (self.level * 0.05):
            component_types = ["metal", "elemental", "catalyst", "binding", "rune"]
            component_type = random.choice(component_types)
            
            loot_table.append({
                "type": "component",
                "component_type": component_type,
                "name": f"{Monster.TYPE_NAMES[self.monster_type]} {component_type.capitalize()}",
                "value": 3 + self.level,
                "drop_chance": 0.7
            })
        
        # Chance to drop consumable item
        if random.random() < 0.2 + (self.level * 0.03):
            consumable_types = ["health_potion", "mana_potion", "buff_item"]
            consumable_type = random.choice(consumable_types)
            
            if consumable_type == "health_potion":
                loot_table.append({
                    "type": "consumable",
                    "subtype": "health_potion",
                    "name": "Health Chip",
                    "effect": "restore_hp",
                    "amount": 5 + self.level,
                    "drop_chance": 0.5
                })
            elif consumable_type == "mana_potion":
                loot_table.append({
                    "type": "consumable",
                    "subtype": "mana_potion",
                    "name": "Mana Fragment",
                    "effect": "restore_mp",
                    "amount": 5 + self.level,
                    "drop_chance": 0.5
                })
            else:  # buff_item
                loot_table.append({
                    "type": "consumable",
                    "subtype": "buff_item",
                    "name": "Combat Algorithm",
                    "effect": "increase_attack",
                    "amount": 2,
                    "duration": 3,
                    "drop_chance": 0.4
                })
        
        # Always drop some digital currency (XP)
        loot_table.append({
            "type": "currency",
            "name": "Digital Essence",
            "amount": 10 + (self.level * 5),
            "drop_chance": 1.0
        })
        
        return loot_table
    
    def get_loot(self):
        """Roll for and return dropped loot from this monster."""
        dropped_loot = []
        
        for loot_item in self.loot:
            # Roll for each item based on drop chance
            if random.random() <= loot_item.get("drop_chance", 1.0):
                # Create a copy of the loot item to avoid modifying the original
                dropped = loot_item.copy()
                
                # Add some randomization to amounts
                if "amount" in dropped:
                    variation = dropped["amount"] * 0.2  # 20% variation
                    dropped["amount"] = int(dropped["amount"] + random.uniform(-variation, variation))
                    
                    # Ensure minimum value of 1
                    dropped["amount"] = max(1, dropped["amount"])
                
                dropped_loot.append(dropped)
        
        return dropped_loot
    
    def to_dict(self):
        """Convert monster to a dictionary for serialization."""
        return {
            "name": self.name,
            "level": self.level,
            "monster_type": self.monster_type,
            "attributes": self.attributes,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "abilities": self.abilities,
            "loot": self.loot
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a monster from a dictionary."""
        monster = cls(
            data["name"],
            data["level"],
            data["monster_type"],
            data["attributes"],
            data["abilities"]
        )
        monster.max_hp = data["max_hp"]
        monster.hp = data["hp"]
        monster.attack = data["attack"]
        monster.defense = data["defense"]
        monster.loot = data["loot"]
        return monster


class MonsterGenerator:
    """Generates monsters with appropriate level and type."""
    
    @staticmethod
    def generate_monster(level, theme="neon", monster_type=None):
        """
        Generate a monster of the specified level and type.
        
        Args:
            level: The monster's level
            theme: The dungeon theme
            monster_type: Optional specific monster type to generate
            
        Returns:
            A new Monster instance
        """
        # Either use specified type or choose randomly
        if not monster_type:
            monster_type = random.choice([Monster.GLITCH, Monster.DIGITAL, Monster.CORRUPTED, Monster.VIRUS])
        
        # Generate type-specific name
        prefix = random.choice([
            "Alpha", "Beta", "Delta", "Gamma", "Omega",
            "Prime", "Core", "Nexus", "Vector", "Matrix"
        ])
        
        type_names = {
            Monster.GLITCH: ["Anomaly", "Distortion", "Fragmentation", "Artifact", "Disruption"],
            Monster.DIGITAL: ["Construct", "Algorithm", "Subroutine", "Process", "Protocol"],
            Monster.CORRUPTED: ["Mutation", "Aberration", "Corruption", "Degradation", "Erosion"],
            Monster.VIRUS: ["Infection", "Parasite", "Malware", "Trojan", "Worm"]
        }
        
        suffix = random.choice(type_names.get(monster_type, ["Entity"]))
        
        # Full name with level indicator
        name = f"Lvl {level} {prefix} {suffix}"
        
        # Create and return the monster
        return Monster(name, level, monster_type)
    
    @staticmethod
    def generate_boss(level, theme="neon"):
        """
        Generate a boss monster for the dungeon level.
        
        Args:
            level: The boss's level (usually higher than regular monsters)
            theme: The dungeon theme
            
        Returns:
            A new Monster instance with boss properties
        """
        # Boss names
        boss_names = [
            "The Overclocked Sentinel",
            "Kernel Panic",
            "The Void Protocol",
            "Segmentation Fault",
            "Corrupted Administrator",
            "The Quantum Anomaly",
            "Stack Overflow",
            "Infinite Loop",
            "The Root Daemon",
            "System.Exception"
        ]
        
        name = random.choice(boss_names)
        
        # Create a more powerful monster as the boss
        boss = Monster(name, level + 2)
        
        # Boost boss stats
        boss.max_hp *= 2
        boss.hp = boss.max_hp
        boss.attack += 2
        boss.defense += 2
        
        # Add a special boss ability
        boss_abilities = [
            {"name": "System Purge", "damage": level * 2, "target": "all", "cooldown": 3},
            {"name": "Root Access", "effect": "summon_minions", "cooldown": 4},
            {"name": "Firewall Lockdown", "effect": "prevent_escape", "duration": 2},
            {"name": "Data Corruption", "effect": "status_effect", "target": "all", "duration": 3}
        ]
        
        boss.abilities.append(random.choice(boss_abilities))
        
        # Improve boss loot
        boss.loot.append({
            "type": "rare_item",
            "name": f"{theme.capitalize()} Core Fragment",
            "value": level * 10,
            "drop_chance": 1.0
        })
        
        return boss


class Encounter:
    """
    Represents an encounter in a dungeon room.
    """
    # Encounter types
    COMBAT = 1
    TRAP = 2
    PUZZLE = 3
    
    def __init__(self, encounter_type, difficulty=1):
        """
        Initialize a new encounter.
        
        Args:
            encounter_type: Type of encounter
            difficulty: Base difficulty level
        """
        self.encounter_type = encounter_type
        self.difficulty = difficulty
        self.completed = False
        self.description = ""
        
        # Encounter-specific properties
        if encounter_type == Encounter.COMBAT:
            self.monsters = []
            self.ambush = random.random() < 0.3  # 30% chance of ambush
        elif encounter_type == Encounter.TRAP:
            self.trap_type = random.choice(["damage", "status", "teleport"])
            self.detected = False
            self.disarmed = False
            self.effect = self._generate_trap_effect()
        elif encounter_type == Encounter.PUZZLE:
            self.puzzle_type = random.choice(["sequence", "pattern", "riddle"])
            self.hints = []
            self.solution = ""
            self.solved = False
            self.reward = None
        
        self.rewards = []
    
    def _generate_trap_effect(self):
        """Generate a trap effect based on trap type and difficulty."""
        effect = {}
        
        if self.trap_type == "damage":
            effect = {
                "type": "damage",
                "damage": 2 + self.difficulty,
                "avoidable": True,
                "save_attribute": "dexterity",
                "save_difficulty": 10 + self.difficulty
            }
        elif self.trap_type == "status":
            effect = {
                "type": "status",
                "status": random.choice(["poison", "slow", "weaken"]),
                "duration": 1 + (self.difficulty // 2),
                "avoidable": True,
                "save_attribute": "strength",
                "save_difficulty": 10 + self.difficulty
            }
        elif self.trap_type == "teleport":
            effect = {
                "type": "teleport",
                "distance": 1 + (self.difficulty // 2),
                "avoidable": True,
                "save_attribute": "wisdom",
                "save_difficulty": 10 + self.difficulty
            }
        
        return effect
    
    def add_monster(self, monster):
        """
        Add a monster to this encounter.
        
        Args:
            monster: The Monster instance to add
            
        Returns:
            This Encounter instance for chaining
        """
        if self.encounter_type == Encounter.COMBAT:
            self.monsters.append(monster)
        return self
    
    def add_reward(self, reward):
        """
        Add a reward for completing this encounter.
        
        Args:
            reward: The reward item/object to add
            
        Returns:
            This Encounter instance for chaining
        """
        self.rewards.append(reward)
        return self
    
    def set_description(self, description):
        """Set the encounter description."""
        self.description = description
        return self
    
    def complete(self):
        """
        Mark the encounter as completed and determine rewards.
        
        Returns:
            List of rewards from this encounter
        """
        self.completed = True
        
        # In case of combat, collect loot from all monsters
        collected_rewards = []
        
        if self.encounter_type == Encounter.COMBAT:
            for monster in self.monsters:
                monster_loot = monster.get_loot()
                for loot in monster_loot:
                    collected_rewards.append(loot)
        
        # Add any encounter-specific rewards
        collected_rewards.extend(self.rewards)
        
        return collected_rewards
    
    def to_dict(self):
        """Convert encounter to a dictionary for serialization."""
        data = {
            "encounter_type": self.encounter_type,
            "difficulty": self.difficulty,
            "completed": self.completed,
            "description": self.description,
            "rewards": self.rewards
        }
        
        # Add type-specific data
        if self.encounter_type == Encounter.COMBAT:
            data["monsters"] = [monster.to_dict() for monster in self.monsters]
            data["ambush"] = self.ambush
        elif self.encounter_type == Encounter.TRAP:
            data["trap_type"] = self.trap_type
            data["detected"] = self.detected
            data["disarmed"] = self.disarmed
            data["effect"] = self.effect
        elif self.encounter_type == Encounter.PUZZLE:
            data["puzzle_type"] = self.puzzle_type
            data["hints"] = self.hints
            data["solution"] = self.solution
            data["solved"] = self.solved
            data["reward"] = self.reward
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create an encounter from a dictionary."""
        encounter = cls(data["encounter_type"], data["difficulty"])
        encounter.completed = data["completed"]
        encounter.description = data["description"]
        encounter.rewards = data["rewards"]
        
        # Restore type-specific data
        if encounter.encounter_type == Encounter.COMBAT:
            encounter.monsters = [Monster.from_dict(m) for m in data["monsters"]]
            encounter.ambush = data["ambush"]
        elif encounter.encounter_type == Encounter.TRAP:
            encounter.trap_type = data["trap_type"]
            encounter.detected = data["detected"]
            encounter.disarmed = data["disarmed"]
            encounter.effect = data["effect"]
        elif encounter.encounter_type == Encounter.PUZZLE:
            encounter.puzzle_type = data["puzzle_type"]
            encounter.hints = data["hints"]
            encounter.solution = data["solution"]
            encounter.solved = data["solved"]
            encounter.reward = data["reward"]
        
        return encounter


class EncounterGenerator:
    """Generates encounters appropriate for dungeon rooms."""
    
    @staticmethod
    def generate_encounter(room_type, difficulty=1, theme="neon"):
        """
        Generate an encounter appropriate for the given room type.
        
        Args:
            room_type: The type of room from Room class
            difficulty: Base difficulty level
            theme: The dungeon theme
            
        Returns:
            An Encounter instance or None if this room type doesn't have encounters
        """
        from models.dungeon import Room
        
        if room_type == Room.COMBAT:
            # Create a combat encounter
            encounter = Encounter(Encounter.COMBAT, difficulty)
            
            # Determine number of monsters based on difficulty
            num_monsters = 1 + (difficulty // 2)
            
            # Cap at reasonable number
            num_monsters = min(num_monsters, 4)
            
            # Add monsters
            for i in range(num_monsters):
                monster = MonsterGenerator.generate_monster(difficulty, theme)
                encounter.add_monster(monster)
            
            # Set description
            if num_monsters == 1:
                encounter.set_description(f"A {encounter.monsters[0].name} guards this area.")
            else:
                encounter.set_description(f"A group of {num_monsters} hostile entities detected.")
            
            return encounter
            
        elif room_type == Room.BOSS:
            # Create a boss encounter
            encounter = Encounter(Encounter.COMBAT, difficulty + 2)
            
            # Generate boss monster
            boss = MonsterGenerator.generate_boss(difficulty, theme)
            encounter.add_monster(boss)
            
            # Sometimes add minions
            if random.random() < 0.5:
                num_minions = random.randint(1, 2)
                for i in range(num_minions):
                    minion = MonsterGenerator.generate_monster(difficulty - 1, theme)
                    encounter.add_monster(minion)
            
            # Set description
            encounter.set_description(f"The powerful {boss.name} awaits, radiating dangerous energy.")
            
            return encounter
            
        elif room_type == Room.PUZZLE:
            # Create a puzzle encounter
            encounter = Encounter(Encounter.PUZZLE, difficulty)
            
            # Generate puzzle details
            puzzle_types = {
                "sequence": "A sequence of symbols must be activated in the correct order.",
                "pattern": "A pattern of lights must be replicated on the control panel.",
                "riddle": "A cryptic riddle is inscribed on the wall, hinting at a hidden mechanism."
            }
            
            puzzle_type = random.choice(list(puzzle_types.keys()))
            encounter.puzzle_type = puzzle_type
            encounter.set_description(puzzle_types[puzzle_type])
            
            # Add reward for solving
            theme_prefixes = {
                "neon": "Prismatic",
                "cyber": "Digital",
                "retro": "Vintage"
            }
            prefix = theme_prefixes.get(theme, "Mysterious")
            
            reward = {
                "type": "rare_component",
                "name": f"{prefix} Data Crystal",
                "value": 10 + (difficulty * 5)
            }
            
            encounter.add_reward(reward)
            
            return encounter
            
        elif room_type == Room.TREASURE:
            # Treasure rooms might have trap encounters
            if random.random() < 0.3:  # 30% chance
                # Create a trap encounter guarding the treasure
                encounter = Encounter(Encounter.TRAP, difficulty)
                
                trap_desc = {
                    "damage": "A trigger mechanism will release a surge of harmful energy.",
                    "status": "A strange field surrounds the treasure that might affect your capabilities.",
                    "teleport": "A spatial distortion seems linked to the treasure container."
                }
                
                encounter.set_description(trap_desc[encounter.trap_type])
                
                return encounter
        
        # No encounter for other room types
        return None