# EXPLORE Quadrant Implementation Plan

Based on the MazeBuilder codebase, this document outlines our implementation plan for the EXPLORE quadrant (The Neon Wilderness) in the Neon D&D Isekai project.

## Core Architecture

We'll adapt the MazeBuilder architecture while extending it to support dungeon-specific features:

```
+----------------------+      +------------------------+      +-------------------------+
| DungeonGenerator     |----->| DungeonLevel          |----->| Room                    |
|                      |      |                       |      |                         |
| - generate_dungeon() |      | - rooms[]             |      | - room_type             |
| - connect_rooms()    |      | - corridors[]         |      | - encounters[]          |
| - place_encounters() |      | - entrance/exit       |      | - treasures[]           |
| - theme_dungeon()    |      | - navigation()        |      | - description           |
+----------------------+      | - reveal_map()        |      | - enter_room()          |
                              +------------------------+      | - interact()            |
                                                              +-------------------------+
                                                                         |
                                                                         v
                              +------------------------+      +-------------------------+
                              | CombatSystem          |<-----| Encounter               |
                              |                       |      |                         |
                              | - initiative_order    |      | - monsters[]            |
                              | - turn_sequence()     |      | - treasures[]           |
                              | - process_action()    |      | - difficulty            |
                              | - calculate_damage()  |      | - start_encounter()     |
                              +------------------------+      | - end_encounter()       |
                                                              +-------------------------+
```

## Adapting MazeBuilder Components

### 1. Grid and Cell Classes → Dungeon and Room

We'll adapt the `Grid` and `Cell` classes to create `DungeonLevel` and `Room` classes:

```python
class Room:
    """
    Room represents a single room in the dungeon.
    Extension of the Cell class with additional dungeon-specific properties.
    """
    # Room types
    COMBAT = 1       # Room with enemies
    TREASURE = 2     # Room with loot
    PUZZLE = 3       # Room with interactive elements
    REST = 4         # Safe room for recovery
    BOSS = 5         # Room with boss encounter
    
    # Direction constants (same as Cell)
    NORTH = 1
    SOUTH = 2
    EAST = 4
    WEST = 8
    
    def __init__(self, row, col):
        """Initialize a new room at the given position."""
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
        
    # Include all Cell methods plus dungeon-specific methods
    def add_encounter(self, encounter):
        """Add an encounter to this room."""
        self.encounters.append(encounter)
        
    def add_treasure(self, treasure):
        """Add a treasure to this room."""
        self.treasures.append(treasure)
        
    def enter_room(self, character):
        """Process effects when a character enters the room."""
        self.visited = True
        # Trigger encounters or other effects based on room type
        
    def is_cleared(self):
        """Check if the room has been cleared of encounters."""
        return all(encounter.completed for encounter in self.encounters)
```

### 2. Maze Generation Algorithms → Dungeon Generation

Adapt the maze generation algorithms to create dungeon structures:

```python
class DungeonGenerator:
    """Generator for dungeon levels with various algorithms."""
    
    @staticmethod
    def generate_dungeon(rows, cols, algorithm="bsp", theme="neon", difficulty=1):
        """Generate a dungeon level using the specified algorithm."""
        dungeon = DungeonLevel(rows, cols)
        
        if algorithm == "bsp":
            return DungeonGenerator.binary_space_partition(dungeon, theme, difficulty)
        elif algorithm == "cellular":
            return DungeonGenerator.cellular_automata(dungeon, theme, difficulty)
        elif algorithm == "maze_rooms":
            return DungeonGenerator.maze_with_rooms(dungeon, theme, difficulty)
        
        return dungeon
        
    @staticmethod
    def binary_space_partition(dungeon, theme, difficulty):
        """
        BSP algorithm to create a dungeon with rooms of varying sizes.
        More structured than cellular automata.
        """
        # Implementation of BSP dungeon generation algorithm
        # ...
        
        # After generating room structure, assign room types and content
        DungeonGenerator.assign_room_types(dungeon, difficulty)
        DungeonGenerator.place_encounters(dungeon, theme, difficulty)
        DungeonGenerator.place_treasures(dungeon, theme, difficulty)
        
        return dungeon
```

### 3. Text Renderer → Dungeon Visualization

Adapt the text renderer for dungeon visualization with Streamlit:

```python
class DungeonRenderer:
    """Renders dungeon levels with neon-themed visuals."""
    
    def __init__(self, theme_name="neon"):
        """Initialize a dungeon renderer with the specified theme."""
        self.theme = DungeonThemes.get_theme(theme_name)
        
    def render_dungeon(self, dungeon_level, character_position, visited_rooms=None):
        """Render the dungeon level with character position."""
        # Generate the dungeon visualization
        # For Streamlit, we'll use a grid of styled elements
        
        # Return a structure that Streamlit can render
```

## New Components for Dungeon Exploration

### 1. Encounter System

```python
class Encounter:
    """Represents a challenge in a dungeon room."""
    
    # Encounter types
    MONSTER = 1
    TRAP = 2
    PUZZLE = 3
    
    def __init__(self, encounter_type, difficulty):
        """Initialize a new encounter."""
        self.encounter_type = encounter_type
        self.difficulty = difficulty
        self.completed = False
        self.monsters = []
        self.rewards = []
        
    def add_monster(self, monster):
        """Add a monster to this encounter."""
        self.monsters.append(monster)
        
    def start_encounter(self, character):
        """Begin the encounter with a character."""
        if self.encounter_type == Encounter.MONSTER:
            return CombatSystem.start_combat(character, self.monsters)
        # Handle other encounter types
        
    def complete_encounter(self):
        """Mark the encounter as completed and determine rewards."""
        self.completed = True
        return self.rewards
```

### 2. Combat System

```python
class CombatSystem:
    """Handles turn-based combat encounters."""
    
    @staticmethod
    def start_combat(character, monsters):
        """Initialize a combat encounter between a character and monsters."""
        # Roll initiative for all participants
        participants = [character] + monsters
        initiative_order = CombatSystem.determine_initiative(participants)
        
        # Return combat state
        return {
            "participants": participants,
            "initiative_order": initiative_order,
            "current_turn": 0,
            "round": 1,
            "status": "active"
        }
    
    @staticmethod
    def determine_initiative(participants):
        """Determine turn order based on initiative rolls."""
        # Use 3d6 system plus dexterity modifier
        initiatives = []
        for participant in participants:
            # Roll 3d6 + DEX modifier
            dex_mod = (participant.attributes["dexterity"] - 10) // 2
            initiative_roll = sum([random.randint(1, 6) for _ in range(3)]) + dex_mod
            initiatives.append((participant, initiative_roll))
            
        # Sort by initiative roll, higher goes first
        return sorted(initiatives, key=lambda x: x[1], reverse=True)
    
    @staticmethod
    def process_action(combat_state, action, target=None):
        """Process a combat action by the current participant."""
        # Handle attack, defend, use item, cast spell, etc.
        # Update combat state based on action results
```

### 3. Monster Generation

```python
class MonsterGenerator:
    """Generates monsters appropriate for dungeon level and theme."""
    
    @staticmethod
    def generate_monster(level, theme, monster_type=None):
        """Generate a monster of the specified type and level."""
        # Either use specified type or choose randomly
        if not monster_type:
            monster_type = random.choice(["glitch", "digital", "corrupted", "virus"])
        
        # Base attributes scale with level
        attributes = {
            "strength": 10 + level,
            "dexterity": 10 + level,
            "wisdom": 10 + level
        }
        
        # Adjust based on monster type
        if monster_type == "glitch":
            attributes["dexterity"] += 2
        elif monster_type == "digital":
            attributes["wisdom"] += 2
        elif monster_type == "corrupted":
            attributes["strength"] += 2
        
        # Create the monster
        monster = {
            "name": f"Level {level} {monster_type.capitalize()} Entity",
            "level": level,
            "monster_type": monster_type,
            "attributes": attributes,
            "hp": 5 + (level * 3) + (attributes["strength"] // 2),
            "abilities": MonsterGenerator.generate_abilities(level, monster_type),
            "loot": MonsterGenerator.generate_loot(level, monster_type)
        }
        
        return monster
```

## Streamlit Integration

### 1. Main Exploration Page

```python
# app/pages/05_🔍_Dungeon.py

import streamlit as st
import random
import sys
import os

# Import necessary modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.dungeon import DungeonLevel, DungeonGenerator, Room
from models.encounter import Encounter, MonsterGenerator
from models.combat import CombatSystem
from utils.dice import roll_dice

# Page config
st.set_page_config(
    page_title="The Neon Wilderness - Exploration",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'dungeon' not in st.session_state:
    # Create a new dungeon level when first visiting
    st.session_state.dungeon = DungeonGenerator.generate_dungeon(10, 10, algorithm="bsp", theme="neon", difficulty=1)
    st.session_state.current_position = (0, 0)  # Start at entrance
    st.session_state.discovered_rooms = set()
    st.session_state.combat_active = False
    st.session_state.current_room = None

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    # Dungeon map visualization
    st.subheader("Dungeon Map")
    
    # Render the dungeon with character position
    # Implement dungeon rendering in a clean way using Streamlit components
    
with col2:
    # Room description and interaction
    if st.session_state.combat_active:
        # Show combat interface
        st.subheader("Combat")
        # Combat UI implementation
    else:
        # Show exploration interface
        st.subheader("Current Location")
        
        # Get the current room
        current_room = st.session_state.dungeon.at(*st.session_state.current_position)
        
        # Display room description
        st.write(current_room.description)
        
        # Movement controls
        st.write("### Movement")
        movement_cols = st.columns(4)
        
        # Show directional buttons for available exits
        with movement_cols[0]:
            if current_room.linked(Room.NORTH):
                if st.button("North ⬆️"):
                    # Move north
                    st.session_state.current_position = (
                        st.session_state.current_position[0] - 1,
                        st.session_state.current_position[1]
                    )
                    st.rerun()
                    
        with movement_cols[1]:
            if current_room.linked(Room.SOUTH):
                if st.button("South ⬇️"):
                    # Move south
                    st.session_state.current_position = (
                        st.session_state.current_position[0] + 1,
                        st.session_state.current_position[1]
                    )
                    st.rerun()
        
        # East and West buttons
        # Similar implementation...
        
        # Room interactions
        st.write("### Actions")
        
        # Show available actions based on room type and content
        if current_room.room_type == Room.TREASURE:
            if st.button("Search for Treasure"):
                # Logic for finding treasures
                pass
                
        if current_room.room_type == Room.COMBAT and not current_room.is_cleared():
            if st.button("Prepare for Combat"):
                # Start combat encounter
                st.session_state.combat_active = True
                st.session_state.current_encounter = current_room.encounters[0]
                st.session_state.combat_state = CombatSystem.start_combat(
                    st.session_state.character,
                    st.session_state.current_encounter.monsters
                )
                st.rerun()
```

### 2. Combat Interface

```python
def render_combat_interface(combat_state, character, encounter):
    """Render the combat interface for Streamlit."""
    
    st.write(f"### Combat: Round {combat_state['round']}")
    
    # Display initiative order
    st.write("**Initiative Order:**")
    for participant, initiative in combat_state['initiative_order']:
        if participant == character:
            st.write(f"- **{participant['name']} (You)**: {initiative}")
        else:
            st.write(f"- {participant['name']}: {initiative}")
    
    # Current participant
    current_participant = combat_state['initiative_order'][combat_state['current_turn']][0]
    st.write(f"**Current Turn:** {current_participant['name']}")
    
    # If it's the player's turn
    if current_participant == character:
        # Display player actions
        st.write("### Your Turn")
        
        # Character stats
        st.write(f"HP: {character['hp']}/{character['max_hp']}")
        st.write(f"MP: {character['mp']}/{character['max_mp']}")
        
        # Action selection
        action = st.selectbox(
            "Choose an action:",
            ["Attack", "Cast Spell", "Use Item", "Defend", "Flee"]
        )
        
        if action == "Attack":
            # Select target
            if len(encounter.monsters) > 1:
                target = st.selectbox(
                    "Select target:",
                    [monster["name"] for monster in encounter.monsters]
                )
                target_idx = next(i for i, m in enumerate(encounter.monsters) if m["name"] == target)
            else:
                target_idx = 0
            
            if st.button("Execute Attack"):
                # Perform attack
                dice_result = roll_dice(3, 6)
                st.write(f"🎲 Attack roll: {dice_result['total']} ({', '.join(map(str, dice_result['results']))})")
                
                # Process attack and update combat state
                # ...
                
                # Move to next turn
                combat_state['current_turn'] = (combat_state['current_turn'] + 1) % len(combat_state['initiative_order'])
                if combat_state['current_turn'] == 0:
                    combat_state['round'] += 1
                
                st.rerun()
                
        # Implement other actions (Cast Spell, Use Item, etc.)
                
    else:
        # It's an enemy's turn
        st.write("### Enemy Turn")
        
        # Display enemy stats
        st.write(f"{current_participant['name']}: {current_participant['hp']} HP")
        
        # Process enemy action
        if st.button("Continue"):
            # Enemy AI selects and executes an action
            # ...
            
            # Move to next turn
            combat_state['current_turn'] = (combat_state['current_turn'] + 1) % len(combat_state['initiative_order'])
            if combat_state['current_turn'] == 0:
                combat_state['round'] += 1
            
            st.rerun()
```

## Styling and Theme

We'll leverage the theming capabilities from MazeBuilder to create a neon-themed dungeon visualization:

```python
class NeonTheme(DungeonTheme):
    """Neon-themed styling for dungeon visualization."""
    
    def __init__(self):
        super().__init__()
        # Background color
        self.bg_color = "#0a0a15"  # Dark blue-black
        
        # Wall and path colors
        self.wall_color = "#ff00ff"  # Neon pink walls
        self.path_color = "#00ffff"  # Neon blue paths
        
        # Special location colors
        self.entrance_color = "#00ff00"  # Neon green
        self.exit_color = "#9900ff"  # Neon purple
        
        # Room type colors
        self.combat_color = "#ff0000"  # Red for combat
        self.treasure_color = "#ffff00"  # Yellow for treasure
        self.puzzle_color = "#00ffff"  # Blue for puzzles
        self.rest_color = "#00ff00"  # Green for rest areas
        
        # Line styling
        self.line_style = "-"
        self.line_width = 2
        
        # Special symbols
        self.player_symbol = "👤"
        self.entrance_symbol = "⬇️"
        self.exit_symbol = "⬆️"
        self.combat_symbol = "⚔️"
        self.treasure_symbol = "💰"
        self.puzzle_symbol = "🧩"
        self.rest_symbol = "🛌"
```

## Implementation Schedule

1. **Week 1 - Core Structure**
   - Implement basic `DungeonLevel` and `Room` classes
   - Create the dungeon generation system with BSP algorithm
   - Build basic dungeon visualization

2. **Week 2 - Room Content & Exploration**
   - Implement room types and content generation
   - Create the exploration interface
   - Build movement and room discovery mechanics

3. **Week 3 - Combat System**
   - Implement the turn-based combat system
   - Create monster generation and abilities
   - Build combat UI for Streamlit

4. **Week 4 - Integration & Polish**
   - Connect with character system
   - Implement treasure and reward system
   - Add progression between dungeon levels
   - Polish UI and add sound effects

## Technical Advantages from MazeBuilder

The MazeBuilder codebase gives us several advantages:

1. **Grid-Based Structure**: Already has the cell/grid architecture we need
2. **Path Generation**: Perfect for creating connectivity between rooms
3. **Visualization Layer**: Can be adapted for our neon aesthetic
4. **Pathfinding**: Dijkstra's algorithm for finding optimal paths
5. **Theme System**: Framework for visual styling with easy theme switching

## Modifications Needed

1. **Room Extensions**: Add dungeon-specific properties to cells
2. **Encounter System**: Build an entirely new system for combat
3. **Interactivity**: Add Streamlit-specific interactive elements
4. **Visual Style**: Apply neon theming consistently
5. **Game State**: Implement proper saving/loading of dungeon state

By leveraging the MazeBuilder code and extending it with dungeon-specific features, we can create a robust EXPLORE quadrant that delivers an engaging roguelike experience with the unique neon aesthetic of our game.