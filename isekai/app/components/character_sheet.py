"""
Character sheet component for displaying character information
"""
import streamlit as st

def display_character_sheet(character, compact=False):
    """
    Display a character sheet with formatted stats and information
    
    Args:
        character: Character data object/dictionary
        compact: Boolean to show a more compact version for sidebars
    """
    if compact:
        # Compact version for sidebar
        st.write(f"### {character['name']}")
        st.write(f"Level {character['level']} {character['class']}")
        
        # Attribute dots (visual representation)
        for attr_name, attr_value in character['attributes'].items():
            filled_dots = min(attr_value // 2, 10)  # Max 10 dots
            dots = "●" * filled_dots + "○" * (10 - filled_dots)
            st.write(f"{attr_name.capitalize()}: {dots}")
        
        # HP/MP as progress bars
        hp_max = 10 + (character['attributes']['strength'] // 2)
        mp_max = 10 + (character['attributes']['wisdom'] // 2)
        
        hp_current = character.get('hp_current', hp_max)
        mp_current = character.get('mp_current', mp_max)
        
        st.write(f"HP: {hp_current}/{hp_max}")
        st.progress(hp_current/hp_max)
        
        st.write(f"MP: {mp_current}/{mp_max}")
        st.progress(mp_current/mp_max)
        
    else:
        # Full character sheet
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.write(f"## {character['name']}")
            st.write(f"**Level {character['level']} {character['class']}**")
            st.write(f"**Origin:** {character['origin']}")
            
            # Character portrait placeholder
            st.image("https://via.placeholder.com/150?text=Character", width=150)
            
        with col2:
            # Attributes with bars
            st.write("### Attributes")
            
            # Create 3-column layout for attributes
            attr_cols = st.columns(3)
            
            # Display each attribute in its own column
            attributes = list(character['attributes'].items())
            for i, (attr_name, attr_value) in enumerate(attributes):
                with attr_cols[i % 3]:
                    st.metric(
                        label=attr_name.capitalize(),
                        value=attr_value,
                        delta=calculate_modifier(attr_value)
                    )
        
        # Stats section
        st.write("### Stats")
        stat_cols = st.columns(4)
        
        hp_max = 10 + (character['attributes']['strength'] // 2)
        mp_max = 10 + (character['attributes']['wisdom'] // 2)
        
        hp_current = character.get('hp_current', hp_max)
        mp_current = character.get('mp_current', mp_max)
        
        with stat_cols[0]:
            st.write("**HP**")
            st.progress(hp_current/hp_max)
            st.write(f"{hp_current}/{hp_max}")
            
        with stat_cols[1]:
            st.write("**MP**")
            st.progress(mp_current/mp_max)
            st.write(f"{mp_current}/{mp_max}")
            
        with stat_cols[2]:
            st.write("**XP**")
            xp_current = character.get('xp', 0)
            xp_next = character['level'] * 1000
            st.progress(xp_current/xp_next)
            st.write(f"{xp_current}/{xp_next}")
            
        with stat_cols[3]:
            st.write("**Defense**")
            defense = 10 + (character['attributes']['dexterity'] // 4)
            st.write(f"{defense}")
            
        # Equipment section
        st.write("### Equipment")
        equip_cols = st.columns(3)
        
        equipment_slots = {
            "Weapon": character.get('equipment', {}).get('weapon', "None"),
            "Armor": character.get('equipment', {}).get('armor', "None"),
            "Accessory": character.get('equipment', {}).get('accessory', "None")
        }
        
        for i, (slot, item) in enumerate(equipment_slots.items()):
            with equip_cols[i]:
                st.write(f"**{slot}**")
                st.write(item)
        
        # Skills section
        st.write("### Skills & Abilities")
        
        # Placeholder for class-specific abilities
        if character['class'] == "Warrior":
            st.write("- **Power Attack**: Deal extra damage but with reduced accuracy")
            st.write("- **Defend**: Reduce damage taken until your next turn")
        elif character['class'] == "Wizard":
            st.write("- **Arcane Missile**: Deal 1d4+1 damage to a target")
            st.write("- **Shield**: Create a protective barrier for 1d4 turns")
        elif character['class'] == "White Mage":
            st.write("- **Heal**: Restore 1d6+1 HP to a target")
            st.write("- **Bless**: Increase an ally's next roll by 2")
        elif character['class'] == "Wanderer":
            st.write("- **Quick Shot**: Deal 1d6 damage from range")
            st.write("- **Evade**: High chance to avoid the next attack")

def calculate_modifier(attribute_value):
    """Calculate the D&D-style modifier for an attribute"""
    return (attribute_value - 10) // 2