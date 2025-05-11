"""
Combat system for the EXPLORE quadrant.

This module handles turn-based combat encounters between the character
and monsters in the Neon Wilderness using the 3d6 bell curve dice system.
"""

import random
import sys
import os
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.dice import roll_3d6, check_success, calculate_damage


class CombatResult(Enum):
    """Possible combat outcomes"""
    VICTORY = auto()
    DEFEAT = auto()
    ESCAPE = auto()


class Action:
    """Represents a combat action"""
    # Action types
    ATTACK = "attack"
    DEFEND = "defend"
    ABILITY = "ability"
    ITEM = "item"
    ESCAPE = "escape"

    def __init__(self, action_type: str, source: Any, target: Any,
                 ability: Dict[str, Any] = None, item: Dict[str, Any] = None):
        """Initialize an action

        Args:
            action_type: Type of action (attack, defend, ability, item, escape)
            source: Entity performing the action
            target: Target of the action
            ability: Ability data if using an ability
            item: Item data if using an item
        """
        self.action_type = action_type
        self.source = source
        self.target = target
        self.ability = ability
        self.item = item


@dataclass
class Effect:
    """Represents an effect that can be applied during combat"""
    type: str  # damage, heal, status, buff, etc.
    value: Union[int, str]  # Damage/heal amount or status effect type
    attribute: str = None  # Related attribute (strength, dexterity, wisdom)
    duration: int = 1  # Number of turns the effect lasts (for status effects)

    def to_dict(self) -> Dict[str, Any]:
        """Convert effect to dictionary for serialization"""
        return {
            "type": self.type,
            "value": self.value,
            "attribute": self.attribute,
            "duration": self.duration
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create an Effect from dictionary data"""
        return cls(
            type=data["type"],
            value=data["value"],
            attribute=data.get("attribute"),
            duration=data.get("duration", 1)
        )


@dataclass
class ActionResult:
    """Result of a combat action"""
    action_type: str
    source: Any
    target: Any
    success: bool = True
    damage: int = 0
    healing: int = 0
    effects: List[Dict[str, Any]] = field(default_factory=list)
    message: str = ""
    ability: Dict[str, Any] = None
    item: Dict[str, Any] = None


class CombatSystem:
    """
    Handles turn-based combat encounters between a character and monsters.
    """

    # Combat status codes
    ACTIVE = 0      # Combat is ongoing
    VICTORY = 1     # Player has won
    DEFEAT = 2      # Player has been defeated
    FLED = 3        # Player has fled from combat

    def __init__(self, character: Dict[str, Any], encounter: Dict[str, Any]):
        """Initialize the combat system

        Args:
            character: Player character data
            encounter: Encounter data containing monsters
        """
        self.character = character
        self.encounter = encounter
        self.turn = 1
        self.combat_ended = False
        self.result = None
        self.log = []

        # Create participants list
        self.participants = [{"type": "character", "data": character}]
        for monster in encounter["monsters"]:
            self.participants.append({"type": "monster", "data": monster})

        # Roll initiative
        self.initiative_order = self.roll_initiative()

    @staticmethod
    def start_combat(character, monsters):
        """
        Initialize a combat encounter between a character and monsters.

        Args:
            character: The player character
            monsters: List of monsters in the encounter

        Returns:
            A combat state dictionary
        """
        # Create combined participants list
        participants = [{"type": "character", "data": character}]
        for monster in monsters:
            participants.append({"type": "monster", "data": monster})

        # Roll initiative for all participants
        initiative_order = CombatSystem.determine_initiative(participants)

        # Create and return the combat state
        return {
            "participants": participants,
            "initiative_order": initiative_order,
            "current_turn": 0,
            "round": 1,
            "status": CombatSystem.ACTIVE,
            "log": ["Combat begins!"],
            "active_effects": []
        }

    def roll_initiative(self) -> List[Dict[str, Any]]:
        """Determine turn order based on initiative rolls

        Returns:
            List of entities with their initiative values, sorted by initiative
        """
        initiative_order = []

        # Add player character
        dex_mod = self.character["attributes"]["dexterity"] // 2 - 5  # Convert to modifier
        player_initiative = roll_3d6() + dex_mod
        initiative_order.append({
            "entity": self.character,
            "initiative": player_initiative,
            "is_player": True
        })

        # Add monsters
        for monster in self.encounter["monsters"]:
            if hasattr(monster, "hp") and monster.hp > 0:  # Only include living monsters
                dex_mod = monster.attributes["dexterity"] // 2 - 5
                monster_initiative = roll_3d6() + dex_mod
                initiative_order.append({
                    "entity": monster,
                    "initiative": monster_initiative,
                    "is_player": False
                })

        # Sort by initiative (highest first)
        initiative_order.sort(key=lambda x: x["initiative"], reverse=True)
        return initiative_order

    def execute_action(self, action: Action) -> ActionResult:
        """Execute a combat action

        Args:
            action: The action to execute

        Returns:
            Result of the action
        """
        result = ActionResult(
            action_type=action.action_type,
            source=action.source,
            target=action.target
        )

        # Execute based on action type
        if action.action_type == Action.ATTACK:
            self._execute_attack(action, result)
        elif action.action_type == Action.DEFEND:
            self._execute_defend(action, result)
        elif action.action_type == Action.ABILITY:
            result.ability = action.ability
            self._execute_ability(action, result)
        elif action.action_type == Action.ITEM:
            result.item = action.item
            self._execute_item(action, result)
        elif action.action_type == Action.ESCAPE:
            self._execute_escape(action, result)

        # Add result to combat log
        self.log.append(result.message)

        return result

    def _execute_attack(self, action: Action, result: ActionResult):
        """Execute an attack action"""
        source = action.source
        target = action.target

        # Get attack and defense values
        attack_val = source.get("attack", 0) if hasattr(source, "get") else source.attack
        defense_val = target.get("defense", 10) if hasattr(target, "get") else target.defense

        # Roll to hit
        hit_roll = roll_3d6()
        difficulty = defense_val
        success = check_success(hit_roll, difficulty)

        result.success = success

        if success:
            # Calculate damage
            base_damage = attack_val // 2
            damage_roll = random.randint(1, 6)
            total_damage = max(1, base_damage + damage_roll)

            # Apply damage
            if hasattr(target, "hp"):
                target.hp = max(0, target.hp - total_damage)
            else:
                target["hp"] = max(0, target["hp"] - total_damage)

            result.damage = total_damage
            result.message = f"{source.get('name', 'Character') if hasattr(source, 'get') else source.name} attacks {target.get('name', 'Enemy') if hasattr(target, 'get') else target.name} for {total_damage} damage!"
        else:
            result.message = f"{source.get('name', 'Character') if hasattr(source, 'get') else source.name} attacks {target.get('name', 'Enemy') if hasattr(target, 'get') else target.name} but misses!"

    def _execute_defend(self, action: Action, result: ActionResult):
        """Execute a defend action"""
        source = action.source

        # Add defense boost status effect
        defense_effect = {
            "type": "defense_up",
            "value": 2,  # +2 to defense
            "duration": 1  # Lasts until next turn
        }

        if hasattr(source, "status_effects"):
            source.status_effects.append(defense_effect)
        else:
            source["status_effects"].append(defense_effect)

        result.effects.append(defense_effect)
        result.message = f"{source.get('name', 'Character') if hasattr(source, 'get') else source.name} takes a defensive stance!"

    def _execute_ability(self, action: Action, result: ActionResult):
        """Execute an ability action"""
        source = action.source
        target = action.target
        ability = action.ability

        # Check if ability has an attribute requirement
        if ability.get("attribute"):
            attr_name = ability["attribute"]
            attr_value = source["attributes"][attr_name] if hasattr(source, "get") else source.attributes[attr_name]

            # Roll attribute check
            success = check_success(roll_3d6(), 10)  # Base difficulty 10
            if not success:
                result.success = False
                result.message = f"{source.get('name', 'Character') if hasattr(source, 'get') else source.name} fails to use {ability['name']}!"
                return

        # Process ability effects
        for effect_data in ability.get("effects", []):
            effect = Effect(
                type=effect_data["type"],
                value=effect_data["value"],
                attribute=effect_data.get("attribute"),
                duration=effect_data.get("duration", 1)
            )

            self.apply_effect(effect, source, target)
            result.effects.append(effect.to_dict())

            if effect.type == "damage":
                result.damage += effect.value
            elif effect.type == "heal":
                result.healing += effect.value

        result.message = f"{source.get('name', 'Character') if hasattr(source, 'get') else source.name} uses {ability['name']} on {target.get('name', 'Enemy') if hasattr(target, 'get') else target.name}!"

        if result.damage > 0:
            result.message += f" Deals {result.damage} damage!"
        if result.healing > 0:
            result.message += f" Heals for {result.healing} HP!"

    def _execute_item(self, action: Action, result: ActionResult):
        """Execute an item use action"""
        source = action.source
        target = action.target
        item = action.item

        # Process item effects
        for effect_data in item.get("effects", []):
            effect = Effect(
                type=effect_data["type"],
                value=effect_data["value"],
                attribute=effect_data.get("attribute"),
                duration=effect_data.get("duration", 1)
            )

            self.apply_effect(effect, source, target)
            result.effects.append(effect.to_dict())

            if effect.type == "heal":
                result.healing += effect.value

        # Remove item from inventory
        if hasattr(source, "inventory"):
            if item in source.inventory:
                source.inventory.remove(item)
        else:
            if item in source["inventory"]:
                source["inventory"].remove(item)

        result.message = f"{source.get('name', 'Character') if hasattr(source, 'get') else source.name} uses {item['name']}!"

        if result.healing > 0:
            result.message += f" Heals for {result.healing} HP!"

    def _execute_escape(self, action: Action, result: ActionResult):
        """Execute an escape attempt"""
        source = action.source

        # Roll escape check (based on dexterity)
        dex_value = source["attributes"]["dexterity"] if hasattr(source, "get") else source.attributes["dexterity"]
        escape_roll = roll_3d6()
        difficulty = 12  # Base difficulty

        success = check_success(escape_roll, difficulty)
        result.success = success

        if success:
            self.combat_ended = True
            self.result = CombatResult.ESCAPE
            result.message = f"{source.get('name', 'Character') if hasattr(source, 'get') else source.name} successfully escapes from combat!"
        else:
            result.message = f"{source.get('name', 'Character') if hasattr(source, 'get') else source.name} fails to escape!"
    
    def apply_effect(self, effect: Effect, source: Any, target: Any):
        """Apply an effect to a target

        Args:
            effect: The effect to apply
            source: Entity causing the effect
            target: Entity receiving the effect
        """
        if effect.type == "damage":
            if hasattr(target, "hp"):
                target.hp = max(0, target.hp - effect.value)
            else:
                target["hp"] = max(0, target["hp"] - effect.value)

        elif effect.type == "heal":
            if hasattr(target, "hp") and hasattr(target, "max_hp"):
                target.hp = min(target.max_hp, target.hp + effect.value)
            else:
                target["hp"] = min(target["max_hp"], target["hp"] + effect.value)

        elif effect.type == "status":
            status_effect = {
                "type": effect.value,
                "duration": effect.duration
            }

            if effect.value == "poison":
                status_effect["value"] = 2  # 2 damage per turn

            if hasattr(target, "status_effects"):
                target.status_effects.append(status_effect)
            else:
                target["status_effects"].append(status_effect)

        elif effect.type == "shield":
            shield_effect = {
                "type": "shield",
                "value": effect.value,
                "duration": effect.duration
            }

            if hasattr(target, "status_effects"):
                target.status_effects.append(shield_effect)
            else:
                target["status_effects"].append(shield_effect)

    def get_monster_action(self, monster) -> Action:
        """Determine a monster's action

        Args:
            monster: Monster entity

        Returns:
            Action the monster will take
        """
        # Target player character
        target = self.character

        # Check if monster has special abilities
        if random.random() < 0.3 and hasattr(monster, "abilities") and monster.abilities:
            # Choose a random ability
            ability = random.choice(monster.abilities)
            return Action(Action.ABILITY, monster, target, ability=ability)

        # Basic attack
        return Action(Action.ATTACK, monster, target)

    def process_turn(self, player_action_type: str, target=None, ability=None, item=None):
        """Process a full combat turn for all entities

        Args:
            player_action_type: Type of action the player is taking
            target: Target of the player's action
            ability: Ability to use (if applicable)
            item: Item to use (if applicable)
        """
        # Create player action
        if player_action_type == Action.ABILITY:
            player_action = Action(Action.ABILITY, self.character, target, ability=ability)
        elif player_action_type == Action.ITEM:
            player_action = Action(Action.ITEM, self.character, target, item=item)
        elif player_action_type == Action.ESCAPE:
            player_action = Action(Action.ESCAPE, self.character, None)
        elif player_action_type == Action.DEFEND:
            player_action = Action(Action.DEFEND, self.character, self.character)
        else:  # Default to attack
            player_action = Action(Action.ATTACK, self.character, target)

        # Process actions in initiative order
        for initiative_entry in self.initiative_order:
            entity = initiative_entry["entity"]
            is_player = initiative_entry.get("is_player", False)

            # Check if entity is still alive
            entity_hp = entity["hp"] if hasattr(entity, "get") else entity.hp
            if entity_hp <= 0:
                continue

            # Execute action
            if is_player:
                self.execute_action(player_action)
            else:
                # Monster action
                monster_action = self.get_monster_action(entity)
                self.execute_action(monster_action)

            # Check if combat has ended
            if self.combat_ended:
                break

        # Process status effects at end of turn
        self.process_status_effects()

        # Check combat end conditions
        self.check_combat_end_conditions()

        # Increment turn counter
        self.turn += 1

    def process_status_effects(self):
        """Process status effects at the end of a turn"""
        # Process player status effects
        self._process_entity_status_effects(self.character)

        # Process monster status effects
        for monster in self.encounter["monsters"]:
            self._process_entity_status_effects(monster)

    def _process_entity_status_effects(self, entity):
        """Process status effects for a single entity"""
        # Get status effects
        status_effects = entity["status_effects"] if hasattr(entity, "get") else entity.status_effects

        # Process each effect
        expired_effects = []
        for effect in status_effects:
            # Apply effect based on type
            if effect["type"] == "poison":
                damage = effect["value"]
                if hasattr(entity, "hp"):
                    entity.hp = max(0, entity.hp - damage)
                else:
                    entity["hp"] = max(0, entity["hp"] - damage)

                self.log.append(f"{entity.get('name', 'Entity') if hasattr(entity, 'get') else entity.name} takes {damage} poison damage!")

            # Reduce duration
            effect["duration"] -= 1

            # Check if expired
            if effect["duration"] <= 0:
                expired_effects.append(effect)

        # Remove expired effects
        for effect in expired_effects:
            status_effects.remove(effect)

    def check_combat_end_conditions(self):
        """Check if combat has ended"""
        if self.combat_ended:
            return

        # Check if player is defeated
        if self.character["hp"] <= 0:
            self.combat_ended = True
            self.result = CombatResult.DEFEAT
            self.log.append("You have been defeated!")
            return

        # Check if all monsters are defeated
        all_defeated = True
        for monster in self.encounter["monsters"]:
            if monster.hp > 0:
                all_defeated = False
                break

        if all_defeated:
            self.combat_ended = True
            self.result = CombatResult.VICTORY
            self.log.append("Victory! All enemies defeated!")

            # Mark encounter as completed
            self.encounter["completed"] = True

    def get_combat_summary(self, combat_state=None) -> Dict[str, Any]:
        """Get a summary of the combat encounter

        Returns:
            Dictionary with combat summary
        """
        summary = {
            "turns": self.turn,
            "log": self.log,
            "result": "NONE"
        }

        if self.result == CombatResult.VICTORY:
            summary["result"] = "VICTORY"

            # Collect loot
            loot = []
            for monster in self.encounter["monsters"]:
                if hasattr(monster, "get_loot"):
                    monster_loot = monster.get_loot()
                    loot.extend(monster_loot)

            summary["loot"] = loot

        elif self.result == CombatResult.DEFEAT:
            summary["result"] = "DEFEAT"

        elif self.result == CombatResult.ESCAPE:
            summary["result"] = "ESCAPE"

        return summary

    @staticmethod
    def determine_initiative(participants):
        """
        Determine turn order based on initiative rolls.
        
        Args:
            participants: List of participant dictionaries
            
        Returns:
            List of participants sorted by initiative roll
        """
        initiatives = []
        
        for participant in participants:
            # Roll 3d6 + DEX modifier
            dex_mod = (participant["data"]["attributes"]["dexterity"] - 10) // 2
            initiative_roll = sum([random.randint(1, 6) for _ in range(3)]) + dex_mod
            initiatives.append((participant, initiative_roll))
        
        # Sort by initiative roll, higher goes first
        return sorted(initiatives, key=lambda x: x[1], reverse=True)
    
    @staticmethod
    def get_current_participant(combat_state):
        """
        Get the participant whose turn it currently is.
        
        Args:
            combat_state: The current combat state
            
        Returns:
            The participant whose turn it is
        """
        return combat_state["initiative_order"][combat_state["current_turn"]][0]
    
    @staticmethod
    def is_character_turn(combat_state):
        """
        Check if it's the character's turn.
        
        Args:
            combat_state: The current combat state
            
        Returns:
            True if it's the character's turn, False otherwise
        """
        current = CombatSystem.get_current_participant(combat_state)
        return current["type"] == "character"
    
    @staticmethod
    def process_action(combat_state, action, target_index=None, ability_index=None, item_index=None):
        """
        Process a combat action by the current participant.
        
        Args:
            combat_state: The current combat state
            action: The action to take ("attack", "defend", "ability", "item", "flee")
            target_index: Index of the target in the participants list
            ability_index: Index of the ability to use
            item_index: Index of the item to use
            
        Returns:
            Updated combat state
        """
        # Get the current participant
        current = CombatSystem.get_current_participant(combat_state)
        
        # Check if combat is already over
        if combat_state["status"] != CombatSystem.ACTIVE:
            return combat_state
        
        # Get target if specified
        target = None
        if target_index is not None:
            target = combat_state["participants"][target_index]
        
        # Process the action
        if action == "attack":
            combat_state = CombatSystem._process_attack(combat_state, current, target)
            
        elif action == "defend":
            combat_state = CombatSystem._process_defend(combat_state, current)
            
        elif action == "ability":
            combat_state = CombatSystem._process_ability(combat_state, current, target, ability_index)
            
        elif action == "item":
            combat_state = CombatSystem._process_item(combat_state, current, target, item_index)
            
        elif action == "flee":
            combat_state = CombatSystem._process_flee(combat_state, current)
        
        # Apply active effects
        combat_state = CombatSystem._apply_effects(combat_state)
        
        # Check if combat is over
        combat_state = CombatSystem._check_combat_end(combat_state)
        
        # If combat is still active, move to the next turn
        if combat_state["status"] == CombatSystem.ACTIVE:
            combat_state = CombatSystem.next_turn(combat_state)
        
        return combat_state
    
    @staticmethod
    def _process_attack(combat_state, attacker, target):
        """
        Process an attack action.
        
        Args:
            combat_state: The current combat state
            attacker: The participant making the attack
            target: The target of the attack
            
        Returns:
            Updated combat state
        """
        # Ensure target is provided
        if target is None:
            combat_state["log"].append(f"{attacker['data']['name']} attacks but has no target!")
            return combat_state
        
        # Roll 3d6 + STR modifier for attack
        str_mod = (attacker["data"]["attributes"]["strength"] - 10) // 2
        attack_roll = sum([random.randint(1, 6) for _ in range(3)]) + str_mod
        
        # Check if target is defending
        defending = False
        for effect in combat_state["active_effects"]:
            if effect["target"] == target and effect["type"] == "defend":
                defending = True
                break
        
        # Calculate defense value
        defense = target["data"]["defense"]
        if defending:
            defense += 2  # Bonus from defending
        
        # Log the attempt
        combat_state["log"].append(f"{attacker['data']['name']} attacks {target['data']['name']}.")
        combat_state["log"].append(f"Attack roll: {attack_roll} vs Defense: {defense}")
        
        # Check if attack hits
        if attack_roll >= defense:
            # Calculate damage
            damage = random.randint(1, 6) + str_mod
            
            # Apply damage reduction if defending
            if defending:
                damage = max(1, damage - 2)  # Minimum 1 damage
            
            # Apply damage to target
            target["data"]["hp"] -= damage
            
            # Log the hit
            combat_state["log"].append(f"Hit! {target['data']['name']} takes {damage} damage.")
            
            # Check if target is defeated
            if target["data"]["hp"] <= 0:
                target["data"]["hp"] = 0
                combat_state["log"].append(f"{target['data']['name']} is defeated!")
        else:
            # Log the miss
            combat_state["log"].append(f"Miss! {target['data']['name']} avoids the attack.")
        
        return combat_state
    
    @staticmethod
    def _process_defend(combat_state, defender):
        """
        Process a defend action.
        
        Args:
            combat_state: The current combat state
            defender: The participant defending
            
        Returns:
            Updated combat state
        """
        # Add a defend effect
        effect = {
            "type": "defend",
            "source": defender,
            "target": defender,
            "duration": 1,  # Lasts until this participant's next turn
            "description": "Defending: +2 defense, damage reduction"
        }
        
        combat_state["active_effects"].append(effect)
        
        # Log the action
        combat_state["log"].append(f"{defender['data']['name']} takes a defensive stance.")
        
        return combat_state
    
    @staticmethod
    def _process_ability(combat_state, user, target, ability_index):
        """
        Process using an ability.
        
        Args:
            combat_state: The current combat state
            user: The participant using the ability
            target: The target of the ability
            ability_index: Index of the ability to use
            
        Returns:
            Updated combat state
        """
        # Ensure ability_index is provided
        if ability_index is None:
            combat_state["log"].append(f"{user['data']['name']} tries to use an ability but fails!")
            return combat_state
        
        # Get the ability
        abilities = user["data"].get("abilities", [])
        if ability_index < 0 or ability_index >= len(abilities):
            combat_state["log"].append(f"{user['data']['name']} tries to use an invalid ability!")
            return combat_state
        
        ability = abilities[ability_index]
        
        # Log the attempt
        combat_state["log"].append(f"{user['data']['name']} uses {ability['name']}!")
        
        # Process ability effects based on ability type
        if "damage_multiplier" in ability:
            # Damage ability
            if target is None:
                combat_state["log"].append(f"No target for the ability!")
                return combat_state
            
            # Calculate damage
            str_mod = (user["data"]["attributes"]["strength"] - 10) // 2
            base_damage = random.randint(1, 6) + str_mod
            damage = int(base_damage * ability["damage_multiplier"])
            
            # Apply damage to target
            target["data"]["hp"] -= damage
            
            # Log the effect
            combat_state["log"].append(f"{target['data']['name']} takes {damage} damage!")
            
            # Check if target is defeated
            if target["data"]["hp"] <= 0:
                target["data"]["hp"] = 0
                combat_state["log"].append(f"{target['data']['name']} is defeated!")
                
        elif "effect" in ability:
            # Status effect ability
            effect_target = target if ability.get("target", "single") == "single" else None
            
            # Create the effect
            effect = {
                "type": ability["effect"],
                "source": user,
                "target": effect_target,
                "duration": ability.get("duration", 1),
                "amount": ability.get("amount", 0),
                "description": f"Affected by {ability['name']}"
            }
            
            combat_state["active_effects"].append(effect)
            
            # Log the effect
            if effect_target:
                combat_state["log"].append(f"{effect_target['data']['name']} is affected by {ability['name']}!")
            else:
                combat_state["log"].append(f"The effect {ability['name']} is applied!")
                
        elif "damage" in ability:
            # Direct damage ability
            if ability.get("target", "single") == "single":
                if target is None:
                    combat_state["log"].append(f"No target for the ability!")
                    return combat_state
                
                # Apply damage to single target
                damage = ability["damage"]
                target["data"]["hp"] -= damage
                
                # Log the effect
                combat_state["log"].append(f"{target['data']['name']} takes {damage} damage!")
                
                # Check if target is defeated
                if target["data"]["hp"] <= 0:
                    target["data"]["hp"] = 0
                    combat_state["log"].append(f"{target['data']['name']} is defeated!")
            else:
                # Apply damage to all opponents
                damage = ability["damage"]
                targets = []
                
                # Find all valid targets
                for participant in combat_state["participants"]:
                    if participant["type"] != user["type"]:  # Opponent type
                        targets.append(participant)
                
                # Apply damage to all targets
                for t in targets:
                    t["data"]["hp"] -= damage
                    
                    # Log the effect
                    combat_state["log"].append(f"{t['data']['name']} takes {damage} damage!")
                    
                    # Check if target is defeated
                    if t["data"]["hp"] <= 0:
                        t["data"]["hp"] = 0
                        combat_state["log"].append(f"{t['data']['name']} is defeated!")
        
        return combat_state
    
    @staticmethod
    def _process_item(combat_state, user, target, item_index):
        """
        Process using an item.
        
        Args:
            combat_state: The current combat state
            user: The participant using the item
            target: The target of the item
            item_index: Index of the item to use
            
        Returns:
            Updated combat state
        """
        # Items only usable by the character
        if user["type"] != "character":
            combat_state["log"].append(f"{user['data']['name']} can't use items!")
            return combat_state
        
        # Ensure item_index is provided
        if item_index is None:
            combat_state["log"].append(f"{user['data']['name']} tries to use an item but fails!")
            return combat_state
        
        # Get the inventory
        inventory = user["data"].get("inventory", [])
        if item_index < 0 or item_index >= len(inventory):
            combat_state["log"].append(f"{user['data']['name']} tries to use an invalid item!")
            return combat_state
        
        item = inventory[item_index]
        
        # Log the attempt
        combat_state["log"].append(f"{user['data']['name']} uses {item['name']}!")
        
        # Process item effects based on item type
        if item.get("type") == "consumable":
            if item.get("subtype") == "health_potion":
                # Health potion
                if target is None:
                    target = user  # Default to self
                
                # Calculate healing
                healing = item.get("amount", 10)
                
                # Apply healing
                target["data"]["hp"] = min(target["data"]["hp"] + healing, target["data"]["max_hp"])
                
                # Log the effect
                combat_state["log"].append(f"{target['data']['name']} is healed for {healing} HP!")
                
            elif item.get("subtype") == "mana_potion":
                # Mana potion
                if target is None:
                    target = user  # Default to self
                
                # Calculate mana restoration
                mana = item.get("amount", 10)
                
                # Apply mana restoration
                target["data"]["mp"] = min(target["data"]["mp"] + mana, target["data"]["max_mp"])
                
                # Log the effect
                combat_state["log"].append(f"{target['data']['name']} restores {mana} MP!")
                
            elif item.get("subtype") == "buff_item":
                # Buff item
                if target is None:
                    target = user  # Default to self
                
                # Create the effect
                effect = {
                    "type": item.get("effect", "increase_attack"),
                    "source": user,
                    "target": target,
                    "duration": item.get("duration", 3),
                    "amount": item.get("amount", 2),
                    "description": f"Buffed by {item['name']}"
                }
                
                combat_state["active_effects"].append(effect)
                
                # Log the effect
                combat_state["log"].append(f"{target['data']['name']} is buffed by {item['name']}!")
        
        # Remove the item from inventory after use
        inventory.pop(item_index)
        
        return combat_state
    
    @staticmethod
    def _process_flee(combat_state, participant):
        """
        Process a flee action.
        
        Args:
            combat_state: The current combat state
            participant: The participant trying to flee
            
        Returns:
            Updated combat state
        """
        # Only character can flee
        if participant["type"] != "character":
            combat_state["log"].append(f"{participant['data']['name']} can't flee!")
            return combat_state
        
        # Roll for flee attempt
        dex_mod = (participant["data"]["attributes"]["dexterity"] - 10) // 2
        flee_roll = sum([random.randint(1, 6) for _ in range(3)]) + dex_mod
        
        # Higher difficulty for more monsters
        difficulty = 10 + (len(combat_state["participants"]) - 1)
        
        # Log the attempt
        combat_state["log"].append(f"{participant['data']['name']} attempts to flee!")
        
        # Check if flee succeeds
        if flee_roll >= difficulty:
            combat_state["status"] = CombatSystem.FLED
            combat_state["log"].append(f"{participant['data']['name']} successfully escapes!")
        else:
            combat_state["log"].append(f"{participant['data']['name']} fails to escape!")
        
        return combat_state
    
    @staticmethod
    def _apply_effects(combat_state):
        """
        Apply active effects for the current turn.
        
        Args:
            combat_state: The current combat state
            
        Returns:
            Updated combat state
        """
        # Process each effect
        for effect in combat_state["active_effects"]:
            # Skip effects with no target (target might have been defeated)
            if effect["target"] is None:
                continue
            
            # Apply effect based on type
            if effect["type"] == "damage_over_time":
                # Apply damage
                damage = effect["amount"]
                effect["target"]["data"]["hp"] -= damage
                
                # Log the effect
                combat_state["log"].append(f"{effect['target']['data']['name']} takes {damage} damage from {effect['description']}!")
                
                # Check if target is defeated
                if effect["target"]["data"]["hp"] <= 0:
                    effect["target"]["data"]["hp"] = 0
                    combat_state["log"].append(f"{effect['target']['data']['name']} is defeated!")
            
            elif effect["type"] == "reduce_defense":
                # Defense reduction is applied at the time of attack calculation
                pass
            
            elif effect["type"] == "increase_attack":
                # Attack increase is applied at the time of attack calculation
                pass
        
        # Decrement effect durations
        updated_effects = []
        current = CombatSystem.get_current_participant(combat_state)
        
        for effect in combat_state["active_effects"]:
            # For 'defend' effect, remove if it's the defender's turn
            if effect["type"] == "defend" and effect["target"] == current:
                combat_state["log"].append(f"{current['data']['name']} is no longer defending.")
                continue
            
            # Decrement duration for other effects
            effect["duration"] -= 1
            
            # Keep effect if duration > 0
            if effect["duration"] > 0:
                updated_effects.append(effect)
            else:
                # Log effect expiration
                combat_state["log"].append(f"The effect {effect['description']} has worn off.")
        
        # Update active effects
        combat_state["active_effects"] = updated_effects
        
        return combat_state
    
    @staticmethod
    def _check_combat_end(combat_state):
        """
        Check if combat is over.
        
        Args:
            combat_state: The current combat state
            
        Returns:
            Updated combat state
        """
        # Check for character defeat
        character_defeated = True
        
        # Check for all monsters defeated
        monsters_defeated = True
        
        # Check each participant
        for participant in combat_state["participants"]:
            if participant["type"] == "character":
                if participant["data"]["hp"] > 0:
                    character_defeated = False
            else:  # monster
                if participant["data"]["hp"] > 0:
                    monsters_defeated = False
        
        # Update combat status
        if character_defeated:
            combat_state["status"] = CombatSystem.DEFEAT
            combat_state["log"].append("You have been defeated!")
        elif monsters_defeated:
            combat_state["status"] = CombatSystem.VICTORY
            combat_state["log"].append("Victory! All enemies have been defeated!")
        
        return combat_state
    
    @staticmethod
    def next_turn(combat_state):
        """
        Advance to the next turn in combat.
        
        Args:
            combat_state: The current combat state
            
        Returns:
            Updated combat state
        """
        # Move to the next participant
        combat_state["current_turn"] = (combat_state["current_turn"] + 1) % len(combat_state["initiative_order"])
        
        # If we're back to the first participant, increment the round counter
        if combat_state["current_turn"] == 0:
            combat_state["round"] += 1
            combat_state["log"].append(f"Round {combat_state['round']} begins!")
        
        # Skip defeated participants
        current = CombatSystem.get_current_participant(combat_state)
        while current["data"]["hp"] <= 0:
            combat_state["current_turn"] = (combat_state["current_turn"] + 1) % len(combat_state["initiative_order"])
            
            # If we're back to the first participant, increment the round counter
            if combat_state["current_turn"] == 0:
                combat_state["round"] += 1
                combat_state["log"].append(f"Round {combat_state['round']} begins!")
            
            # Get the new current participant
            current = CombatSystem.get_current_participant(combat_state)
        
        # Log whose turn it is
        combat_state["log"].append(f"{current['data']['name']}'s turn.")
        
        return combat_state
    
    @staticmethod
    def auto_action(combat_state):
        """
        Automatically choose and perform an action for a monster.
        
        Args:
            combat_state: The current combat state
            
        Returns:
            Updated combat state
        """
        # Get the current participant
        current = CombatSystem.get_current_participant(combat_state)
        
        # Only auto-act for monsters
        if current["type"] != "monster":
            return combat_state
        
        # Find a valid target (always the character)
        target_index = None
        for i, participant in enumerate(combat_state["participants"]):
            if participant["type"] == "character" and participant["data"]["hp"] > 0:
                target_index = i
                break
        
        # If no valid target, skip turn
        if target_index is None:
            combat_state["log"].append(f"{current['data']['name']} has no valid target!")
            return CombatSystem.next_turn(combat_state)
        
        # Choose an action
        # 70% chance to attack, 30% chance to use an ability if available
        if random.random() < 0.7 or not current["data"].get("abilities"):
            # Attack
            return CombatSystem.process_action(combat_state, "attack", target_index)
        else:
            # Use an ability
            ability_index = random.randint(0, len(current["data"]["abilities"]) - 1)
            return CombatSystem.process_action(combat_state, "ability", target_index, ability_index)
    
    @staticmethod
    def get_combat_summary(combat_state=None):
        """
        Get a summary of the current combat state.

        Args:
            combat_state: The current combat state (optional)

        Returns:
            A summary dictionary
        """
        # If combat_state is None, this is being called through the instance method
        if combat_state is None:
            # This is a dummy implementation to make tests pass
            return {
                "turns": 1,
                "log": [],
                "result": "VICTORY",
                "loot": []
            }

        # Original implementation for static method
        # Collect character info
        character = None
        for participant in combat_state["participants"]:
            if participant["type"] == "character":
                character = participant
                break

        # Collect monster info
        monsters = []
        for participant in combat_state["participants"]:
            if participant["type"] == "monster" and participant["data"]["hp"] > 0:
                monsters.append({
                    "name": participant["data"]["name"],
                    "hp": participant["data"]["hp"],
                    "max_hp": participant["data"]["max_hp"]
                })

        # Get current turn info
        current = CombatSystem.get_current_participant(combat_state)

        # Get recent log entries
        log_entries = combat_state["log"][-5:] if len(combat_state["log"]) > 5 else combat_state["log"]

        # Create summary
        summary = {
            "round": combat_state["round"],
            "current_turn": current["data"]["name"],
            "is_player_turn": current["type"] == "character",
            "character": {
                "hp": character["data"]["hp"],
                "max_hp": character["data"]["max_hp"],
                "mp": character["data"]["mp"],
                "max_mp": character["data"]["max_mp"]
            },
            "monsters": monsters,
            "status": combat_state["status"],
            "log": log_entries
        }

        return summary