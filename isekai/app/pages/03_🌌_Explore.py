"""
Explore quadrant - The Neon Wilderness.

This is the UI for dungeon exploration, handling the player's journey through
procedurally generated dungeons with encounters, combat, and treasures.
"""

import streamlit as st
import random
import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.dungeon import DungeonGenerator, Room
from models.encounter import EncounterGenerator
from models.combat import CombatSystem
from utils.dice import roll_dice, roll_check

# Initialize session state variables if they don't exist
if "character" not in st.session_state:
    st.session_state.character = None

if "dungeon" not in st.session_state:
    st.session_state.dungeon = None

if "current_room" not in st.session_state:
    st.session_state.current_room = None

if "combat_state" not in st.session_state:
    st.session_state.combat_state = None

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "exploration"  # Options: exploration, combat

if "log" not in st.session_state:
    st.session_state.log = []


def add_to_log(message):
    """Add a message to the game log."""
    st.session_state.log.append(message)
    # Keep log at a reasonable size
    if len(st.session_state.log) > 100:
        st.session_state.log = st.session_state.log[-100:]


def enter_dungeon():
    """Create a new dungeon and place the character at the entrance."""
    # Generate a dungeon with appropriate difficulty
    character_level = st.session_state.character.get("level", 1)
    difficulty = max(1, character_level)
    
    dungeon = DungeonGenerator.generate_dungeon(
        rows=8, 
        cols=8, 
        algorithm="bsp",
        level_num=difficulty,
        theme="neon", 
        difficulty=difficulty,
        seed=random.randint(1, 10000)
    )
    
    st.session_state.dungeon = dungeon
    
    # Start at the entrance
    st.session_state.current_room = dungeon.entrance
    
    # Discover the entrance and adjacent rooms
    dungeon.discover_room(dungeon.entrance.row, dungeon.entrance.col)
    
    # Add to log
    add_to_log(f"You enter {dungeon.name}. {dungeon.description}")
    
    # Process entrance room effects
    process_room_entry()


def move_to_room(direction):
    """Move the character to an adjacent room in the specified direction."""
    if st.session_state.current_room.linked(direction):
        # Get the adjacent room
        dungeon = st.session_state.dungeon
        row_offset, col_offset = dungeon.DIRECTION_OFFSETS[direction]
        new_row = st.session_state.current_room.row + row_offset
        new_col = st.session_state.current_room.col + col_offset
        
        # Move to the new room
        st.session_state.current_room = dungeon.at(new_row, new_col)
        
        # Discover the room and adjacent rooms
        dungeon.discover_room(new_row, new_col)
        
        # Process room entry effects
        process_room_entry()
    else:
        add_to_log("You can't move in that direction!")


def process_room_entry():
    """Process effects when entering a room."""
    # Apply room entry effects
    result = st.session_state.current_room.enter_room(st.session_state.character)
    
    # Add events to log
    for event in result.get("events", []):
        add_to_log(event)
    
    # Handle encounters
    if result.get("encounters_triggered", False):
        start_combat()
    
    # Handle found treasures
    for treasure in result.get("treasures_found", []):
        # Add treasure to inventory
        st.session_state.character.setdefault("inventory", []).append(treasure)
        add_to_log(f"Added {treasure['name']} to your inventory!")


def start_combat():
    """Start a combat encounter with monsters in the current room."""
    # Create a list of monsters from the room's encounters
    monsters = []
    for encounter in st.session_state.current_room.encounters:
        if encounter.get("type") == "combat" and not encounter.get("completed", False):
            for monster_data in encounter.get("enemies", []):
                # Create monster objects from data
                from models.encounter import Monster
                monster = Monster(
                    monster_data["name"],
                    st.session_state.character.get("level", 1),
                    None  # Auto-assign type
                )
                monster.hp = monster_data["hp"]
                monster.max_hp = monster_data["hp"]
                monster.attack = monster_data["attack"]
                monster.defense = monster_data["defense"]
                monsters.append(monster)
    
    # If we have monsters, start combat
    if monsters:
        st.session_state.combat_state = CombatSystem.start_combat(
            st.session_state.character,
            monsters
        )
        st.session_state.view_mode = "combat"
        
        # Add combat start message to log
        add_to_log("Combat begins!")
        
        # Add combat log entries
        for entry in st.session_state.combat_state["log"]:
            add_to_log(entry)
    else:
        add_to_log("There are no enemies here.")


def render_dungeon_map():
    """Render a visual representation of the dungeon."""
    if not st.session_state.dungeon:
        return
    
    dungeon = st.session_state.dungeon
    current_room = st.session_state.current_room
    
    # Create a grid for the map
    cols = st.columns(dungeon.cols)
    
    # Loop through rows and columns
    for r in range(dungeon.rows):
        # Create a row container
        row = st.container()
        
        with row:
            cols = st.columns(dungeon.cols)
            for c in range(dungeon.cols):
                room = dungeon.at(r, c)
                
                # Skip rooms that haven't been discovered
                if not room.discovered:
                    continue
                
                with cols[c]:
                    # Determine room display
                    if room == current_room:
                        # Current room
                        room_display = "🟢"
                    elif room == dungeon.entrance:
                        # Entrance
                        room_display = "🚪"
                    elif room == dungeon.exit:
                        # Exit
                        room_display = "🏁"
                    elif room.room_type == Room.COMBAT:
                        # Combat room
                        room_display = "⚔️"
                    elif room.room_type == Room.TREASURE:
                        # Treasure room
                        room_display = "💎"
                    elif room.room_type == Room.PUZZLE:
                        # Puzzle room
                        room_display = "🧩"
                    elif room.room_type == Room.REST:
                        # Rest area
                        room_display = "🛌"
                    elif room.room_type == Room.BOSS:
                        # Boss room
                        room_display = "👑"
                    else:
                        # Regular room
                        room_display = "⬜"
                    
                    st.markdown(f"<div style='text-align: center;'>{room_display}</div>", unsafe_allow_html=True)


def render_room_description():
    """Render the current room description and available exits."""
    if not st.session_state.current_room:
        return
    
    room = st.session_state.current_room
    
    # Room header with type
    st.subheader(f"{room.get_room_name()}")
    
    # Room description
    st.markdown(room.description)
    
    # Available exits
    exits = room.get_link_directions()
    if exits:
        st.markdown(f"**Exits:** {', '.join(exits)}")
    else:
        st.markdown("**Exits:** None")


def render_room_contents():
    """Render the contents of the current room (monsters, treasures, etc.)."""
    if not st.session_state.current_room:
        return
    
    room = st.session_state.current_room
    
    # Encounters
    if room.encounters and not all(enc.get("completed", False) for enc in room.encounters):
        for encounter in room.encounters:
            if not encounter.get("completed", False):
                st.markdown(f"**Encounter:** {encounter.get('type', 'unknown').title()}")
                
                if encounter.get("type") == "combat":
                    for enemy in encounter.get("enemies", []):
                        st.markdown(f"- {enemy['name']} (HP: {enemy['hp']})")
    
    # Treasures
    visible_treasures = [t for t in room.treasures if t.get("found", False)]
    if visible_treasures:
        st.markdown("**Treasures:**")
        for treasure in visible_treasures:
            st.markdown(f"- {treasure['name']}")


def render_movement_controls():
    """Render movement buttons based on available exits."""
    if not st.session_state.current_room or st.session_state.view_mode != "exploration":
        return
    
    room = st.session_state.current_room
    
    # Create columns for directional buttons
    cols = st.columns(3)
    
    # North button
    with cols[1]:
        if room.linked(Room.NORTH):
            st.button("North ⬆️", on_click=move_to_room, args=(Room.NORTH,))
        else:
            st.button("North ⬆️", disabled=True)
    
    # West, Rest/Search, East buttons
    with cols[0]:
        if room.linked(Room.WEST):
            st.button("West ⬅️", on_click=move_to_room, args=(Room.WEST,))
        else:
            st.button("West ⬅️", disabled=True)
    
    with cols[1]:
        if room.room_type == Room.REST:
            if st.button("Rest 💤"):
                # Heal character
                heal_amount = random.randint(1, 6) + random.randint(1, 6)
                st.session_state.character["hp"] = min(
                    st.session_state.character["hp"] + heal_amount,
                    st.session_state.character["max_hp"]
                )
                add_to_log(f"You rest and recover {heal_amount} HP.")
        else:
            if st.button("Search 🔍"):
                # Roll perception check
                wisdom_mod = (st.session_state.character["attributes"]["wisdom"] - 10) // 2
                check = roll_check(wisdom_mod, 10)
                
                if check["success"]:
                    # Successful search
                    found_something = False
                    
                    # Check for hidden treasures
                    for treasure in room.treasures:
                        if not treasure.get("found", False):
                            treasure["found"] = True
                            found_something = True
                            add_to_log(f"You found {treasure['name']}!")
                    
                    if not found_something:
                        add_to_log("You search the room but find nothing of interest.")
                else:
                    add_to_log("Your search reveals nothing.")
    
    with cols[2]:
        if room.linked(Room.EAST):
            st.button("East ➡️", on_click=move_to_room, args=(Room.EAST,))
        else:
            st.button("East ➡️", disabled=True)
    
    # South button
    with cols[1]:
        if room.linked(Room.SOUTH):
            st.button("South ⬇️", on_click=move_to_room, args=(Room.SOUTH,))
        else:
            st.button("South ⬇️", disabled=True)


def render_combat_ui():
    """Render the combat interface."""
    if not st.session_state.combat_state or st.session_state.view_mode != "combat":
        return
    
    combat_state = st.session_state.combat_state
    
    # Get combat summary
    summary = CombatSystem.get_combat_summary(combat_state)
    
    # Display round info
    st.subheader(f"Combat - Round {summary['round']}")
    
    # Character info
    st.markdown(f"**Your HP:** {summary['character']['hp']}/{summary['character']['max_hp']}")
    
    # Enemies
    st.markdown("**Enemies:**")
    for monster in summary['monsters']:
        st.markdown(f"- {monster['name']} (HP: {monster['hp']}/{monster['max_hp']})")
    
    # Current turn indicator
    st.markdown(f"**Current Turn:** {summary['current_turn']}")
    
    # Player actions
    if summary['is_player_turn']:
        # Create action buttons
        action_cols = st.columns(4)
        
        with action_cols[0]:
            if st.button("Attack ⚔️"):
                # Select target (for now, just the first monster)
                target_index = None
                for i, participant in enumerate(combat_state["participants"]):
                    if participant["type"] == "monster" and participant["data"]["hp"] > 0:
                        target_index = i
                        break
                
                if target_index is not None:
                    # Process attack
                    st.session_state.combat_state = CombatSystem.process_action(
                        combat_state, "attack", target_index
                    )
                    
                    # Add new log entries
                    for entry in st.session_state.combat_state["log"]:
                        if entry not in st.session_state.log:
                            add_to_log(entry)
                    
                    # Check if combat is over
                    if st.session_state.combat_state["status"] != CombatSystem.ACTIVE:
                        end_combat()
                else:
                    add_to_log("No valid target!")
        
        with action_cols[1]:
            if st.button("Defend 🛡️"):
                st.session_state.combat_state = CombatSystem.process_action(
                    combat_state, "defend"
                )
                
                # Add new log entries
                for entry in st.session_state.combat_state["log"]:
                    if entry not in st.session_state.log:
                        add_to_log(entry)
                
                # Check if combat is over
                if st.session_state.combat_state["status"] != CombatSystem.ACTIVE:
                    end_combat()
        
        with action_cols[2]:
            if st.button("Use Item 🧪"):
                # Check if character has items
                if st.session_state.character.get("inventory"):
                    # For simplicity, use the first inventory item
                    st.session_state.combat_state = CombatSystem.process_action(
                        combat_state, "item", None, None, 0
                    )
                    
                    # Add new log entries
                    for entry in st.session_state.combat_state["log"]:
                        if entry not in st.session_state.log:
                            add_to_log(entry)
                    
                    # Check if combat is over
                    if st.session_state.combat_state["status"] != CombatSystem.ACTIVE:
                        end_combat()
                else:
                    add_to_log("You have no items to use!")
        
        with action_cols[3]:
            if st.button("Flee 🏃"):
                st.session_state.combat_state = CombatSystem.process_action(
                    combat_state, "flee"
                )
                
                # Add new log entries
                for entry in st.session_state.combat_state["log"]:
                    if entry not in st.session_state.log:
                        add_to_log(entry)
                
                # Check if combat is over
                if st.session_state.combat_state["status"] != CombatSystem.ACTIVE:
                    end_combat()
    else:
        # Monster turn - process automatically
        st.markdown("*Monster is taking action...*")
        
        # Small delay for effect
        time.sleep(0.5)
        
        # Process monster action
        st.session_state.combat_state = CombatSystem.auto_action(st.session_state.combat_state)
        
        # Add new log entries
        for entry in st.session_state.combat_state["log"]:
            if entry not in st.session_state.log:
                add_to_log(entry)
        
        # Check if combat is over
        if st.session_state.combat_state["status"] != CombatSystem.ACTIVE:
            end_combat()
        else:
            # Force rerun to update UI
            st.experimental_rerun()


def end_combat():
    """Process the end of combat."""
    combat_state = st.session_state.combat_state
    
    if combat_state["status"] == CombatSystem.VICTORY:
        # Mark encounters as completed
        for encounter in st.session_state.current_room.encounters:
            if encounter.get("type") == "combat" and not encounter.get("completed", False):
                encounter["completed"] = True
                
                # Award XP
                xp_reward = 50 * st.session_state.dungeon.level_num
                st.session_state.character["xp"] = st.session_state.character.get("xp", 0) + xp_reward
                add_to_log(f"You gained {xp_reward} XP.")
                
                # Check for level up
                level_threshold = 1000 * st.session_state.character.get("level", 1)
                if st.session_state.character.get("xp", 0) >= level_threshold:
                    st.session_state.character["level"] = st.session_state.character.get("level", 1) + 1
                    add_to_log(f"Level up! You are now level {st.session_state.character['level']}.")
        
        add_to_log("Combat ended in victory!")
        
    elif combat_state["status"] == CombatSystem.DEFEAT:
        add_to_log("You have been defeated!")
        
        # Return to entrance with reduced HP
        st.session_state.character["hp"] = max(1, st.session_state.character["max_hp"] // 2)
        st.session_state.current_room = st.session_state.dungeon.entrance
        add_to_log("You wake up at the dungeon entrance with reduced health.")
        
    elif combat_state["status"] == CombatSystem.FLED:
        add_to_log("You fled from combat!")
    
    # Reset combat state and return to exploration
    st.session_state.combat_state = None
    st.session_state.view_mode = "exploration"


def render_game_log():
    """Render the game log."""
    st.subheader("Adventure Log")
    
    log_container = st.container()
    with log_container:
        # Display most recent messages first
        for message in reversed(st.session_state.log[-10:]):
            st.markdown(message)


def render_character_info():
    """Render a sidebar with character information."""
    if not st.session_state.character:
        return
    
    character = st.session_state.character
    
    st.sidebar.subheader(f"{character['name']} (Level {character.get('level', 1)})")
    
    # Character portrait placeholder
    st.sidebar.markdown("👤")
    
    # HP and XP
    hp_percent = character["hp"] / character["max_hp"] * 100
    st.sidebar.progress(hp_percent / 100, f"HP: {character['hp']}/{character['max_hp']}")
    
    # Level and XP
    level = character.get("level", 1)
    xp = character.get("xp", 0)
    xp_for_next = 1000 * level
    xp_percent = min(100, (xp / xp_for_next) * 100)
    st.sidebar.progress(xp_percent / 100, f"XP: {xp}/{xp_for_next}")
    
    # Attributes
    st.sidebar.markdown("**Attributes:**")
    for attr, value in character["attributes"].items():
        st.sidebar.markdown(f"{attr.title()}: {value}")
    
    # Inventory
    st.sidebar.markdown("**Inventory:**")
    if character.get("inventory"):
        for item in character["inventory"]:
            st.sidebar.markdown(f"- {item['name']}")
    else:
        st.sidebar.markdown("*Empty*")


def render_dungeon_controls():
    """Render controls for entering/exiting dungeons."""
    if not st.session_state.character:
        st.warning("You need to create a character first!")
        return
    
    if st.session_state.dungeon is None:
        st.markdown("You stand at the entrance to the Neon Wilderness, a procedurally generated digital landscape filled with challenges and rewards.")
        
        if st.button("Enter the Neon Wilderness 🌌"):
            enter_dungeon()
            st.experimental_rerun()
    else:
        # Actions for when already in a dungeon
        if st.session_state.current_room == st.session_state.dungeon.exit:
            if st.button("Exit Dungeon 🚪"):
                # Complete the dungeon
                add_to_log(f"You have completed {st.session_state.dungeon.name}!")
                
                # Add completion rewards
                xp_reward = 100 * st.session_state.dungeon.level_num
                st.session_state.character["xp"] = st.session_state.character.get("xp", 0) + xp_reward
                add_to_log(f"You gained {xp_reward} XP for completing the dungeon!")
                
                # Reset dungeon state
                st.session_state.dungeon = None
                st.session_state.current_room = None
                st.session_state.combat_state = None
                st.session_state.view_mode = "exploration"
                
                st.experimental_rerun()
        
        # Debug option to exit dungeon from anywhere
        with st.expander("Debug Options"):
            if st.button("Force Exit Dungeon (Debug)"):
                st.session_state.dungeon = None
                st.session_state.current_room = None
                st.session_state.combat_state = None
                st.session_state.view_mode = "exploration"
                add_to_log("You exit the dungeon (via debug command).")
                st.experimental_rerun()


def main():
    """Main function to render the page."""
    st.title("🌌 The Neon Wilderness")
    
    # Character info sidebar
    render_character_info()
    
    # Dungeon entry/exit controls
    render_dungeon_controls()
    
    # If in a dungeon, show the dungeon interface
    if st.session_state.dungeon:
        # Different view modes
        if st.session_state.view_mode == "exploration":
            # Dungeon exploration mode
            col1, col2 = st.columns([2, 3])
            
            with col1:
                # Minimap
                st.subheader("Dungeon Map")
                render_dungeon_map()
            
            with col2:
                # Room information
                render_room_description()
                render_room_contents()
            
            # Movement controls
            render_movement_controls()
            
        elif st.session_state.view_mode == "combat":
            # Combat mode
            render_combat_ui()
    
    # Adventure log at the bottom
    render_game_log()


if __name__ == "__main__":
    main()