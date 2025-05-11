"""
Character creation and management page
"""
import streamlit as st
import random
import sys
import os

# Import from local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.dice import roll_dice, attribute_modifier
from models.character import Character

# Page config
st.set_page_config(
    page_title="Character - Neon D&D Isekai",
    page_icon="👤",
    layout="wide"
)

# Title and description
st.title("Character Creation")
st.subheader("Create your digital adventurer")

# Character creation form
def create_character_form():
    with st.form("character_creation"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Character Name")

            character_class = st.selectbox(
                "Character Class",
                ["Warrior", "Wizard", "White Mage", "Wanderer"]
            )

            isekai_origin = st.selectbox(
                "How were you transported to this world?",
                [
                    "Suspicious Website Download",
                    "Arcade Cabinet Malfunction",
                    "VR Headset Glitch",
                    "Old Gaming Magazine Ritual",
                    "Lightning Strike While Gaming"
                ]
            )

            # Display class description
            class_descriptions = {
                "Warrior": "A combat specialist with high strength. Excels at melee attacks and tanking damage.",
                "Wizard": "An arcane spellcaster with high wisdom. Specializes in powerful damage spells.",
                "White Mage": "A healing specialist with balanced attributes. Provides support and restoration.",
                "Wanderer": "A versatile adventurer with high dexterity. Adapts to many situations with varied skills."
            }

            st.info(class_descriptions[character_class])

        with col2:
            st.write("### Attributes")
            st.write("Roll for your attributes or choose a balanced preset.")

            if st.button("🎲 Roll Attributes (4d6 drop lowest)", form_submit=False):
                # Roll 4d6 drop lowest for each attribute
                attributes = {}
                for attr in ["strength", "dexterity", "wisdom"]:
                    rolls = [random.randint(1, 6) for _ in range(4)]
                    attributes[attr] = sum(sorted(rolls)[1:])  # Drop lowest

                st.session_state.temp_attributes = attributes
                st.session_state.temp_attr_rolls = {
                    "strength": rolls,
                    "dexterity": [random.randint(1, 6) for _ in range(4)],
                    "wisdom": [random.randint(1, 6) for _ in range(4)]
                }

            # Get attributes from session state or use defaults
            attributes = st.session_state.get('temp_attributes', {
                "strength": 12,
                "dexterity": 12,
                "wisdom": 12
            })

            # Display attributes with modifiers
            for attr_name, attr_value in attributes.items():
                mod = attribute_modifier(attr_value)
                mod_display = f"+{mod}" if mod >= 0 else f"{mod}"
                st.metric(
                    attr_name.capitalize(),
                    value=attr_value,
                    delta=mod_display
                )

            # Adjust attributes based on class (optional)
            if character_class == "Warrior":
                st.write("Class Bonus: +2 Strength")
                attributes["strength"] += 2
            elif character_class == "Wizard":
                st.write("Class Bonus: +2 Wisdom")
                attributes["wisdom"] += 2
            elif character_class == "White Mage":
                st.write("Class Bonus: +1 Wisdom, +1 Strength")
                attributes["wisdom"] += 1
                attributes["strength"] += 1
            elif character_class == "Wanderer":
                st.write("Class Bonus: +2 Dexterity")
                attributes["dexterity"] += 2

        submitted = st.form_submit_button("Create Character")

        if submitted:
            if not name:
                st.error("Please enter a character name")
                return None

            # Create character object
            character = Character(name, character_class, isekai_origin, attributes)

            # Set session state flag to proceed to forge for starting item
            st.session_state.proceed_to_forge = True

            return character.to_dict()

    return None

# Character display
def display_character(character):
    col1, col2 = st.columns([1, 2])

    with col1:
        # Character avatar (placeholder)
        class_avatars = {
            "Warrior": "🧑‍🚀",  # Closest to a warrior in emoji
            "Wizard": "🧙",
            "White Mage": "🧝",  # Elf as white mage
            "Wanderer": "🥷"      # Ninja as wanderer
        }
        avatar = class_avatars.get(character['class'], "🧑‍🚀")

        st.markdown(f"<h1 style='text-align: center; font-size: 72px;'>{avatar}</h1>", unsafe_allow_html=True)
        st.subheader(f"{character['name']}")
        st.write(f"Level {character['level']} {character['class']}")
        st.write(f"**Origin:** {character['origin']}")

    with col2:
        # Tabs for different character sheet sections
        tab1, tab2, tab3 = st.tabs(["Stats", "Equipment", "Skills"])

        with tab1:
            # Basic stats
            st.write("### Attributes")

            col2a, col2b, col2c = st.columns(3)

            with col2a:
                str_mod = attribute_modifier(character["attributes"]["strength"])
                str_mod_display = f"+{str_mod}" if str_mod >= 0 else f"{str_mod}"
                st.metric("Strength", character["attributes"]["strength"], str_mod_display)

            with col2b:
                dex_mod = attribute_modifier(character["attributes"]["dexterity"])
                dex_mod_display = f"+{dex_mod}" if dex_mod >= 0 else f"{dex_mod}"
                st.metric("Dexterity", character["attributes"]["dexterity"], dex_mod_display)

            with col2c:
                wis_mod = attribute_modifier(character["attributes"]["wisdom"])
                wis_mod_display = f"+{wis_mod}" if wis_mod >= 0 else f"{wis_mod}"
                st.metric("Wisdom", character["attributes"]["wisdom"], wis_mod_display)

            # HP and MP
            st.write("### Health & Mana")

            # Calculate max values
            max_hp = character.get('max_hp', 10 + (character["attributes"]["strength"] // 2))
            max_mp = character.get('max_mp', 10 + (character["attributes"]["wisdom"] // 2))

            # Get current values
            current_hp = character.get('hp', max_hp)
            current_mp = character.get('mp', max_mp)

            col_hp, col_mp = st.columns(2)

            with col_hp:
                st.write(f"HP: {current_hp}/{max_hp}")
                st.progress(current_hp/max_hp)

            with col_mp:
                st.write(f"MP: {current_mp}/{max_mp}")
                st.progress(current_mp/max_mp)

        with tab2:
            st.write("### Equipment")

            # Equipment slots
            equipment = character.get('equipment', {
                'weapon': 'None',
                'armor': 'None',
                'accessory': 'None'
            })

            equip_cols = st.columns(3)

            with equip_cols[0]:
                st.write("**Weapon**")
                if equipment.get('weapon', 'None') != 'None':
                    st.success(equipment.get('weapon', 'None'))
                else:
                    st.warning("No weapon equipped")

            with equip_cols[1]:
                st.write("**Armor**")
                if equipment.get('armor', 'None') != 'None':
                    st.success(equipment.get('armor', 'None'))
                else:
                    st.warning("No armor equipped")

            with equip_cols[2]:
                st.write("**Accessory**")
                if equipment.get('accessory', 'None') != 'None':
                    st.success(equipment.get('accessory', 'None'))
                else:
                    st.warning("No accessory equipped")

            # Inventory
            st.write("### Inventory")

            inventory = character.get('inventory', [])
            if inventory:
                for item in inventory:
                    with st.expander(f"{item.get('name', 'Unknown Item')}"):
                        st.write(f"**Type:** {item.get('type', 'Unknown')}")
                        if 'damage' in item:
                            st.write(f"**Damage:** {item['damage']}")
                        if 'defense' in item:
                            st.write(f"**Defense:** {item['defense']}")
                        if 'effect' in item:
                            st.write(f"**Effect:** {item['effect']}")
            else:
                st.info("Your inventory is empty. Visit The Forge to craft items!")

        with tab3:
            st.write("### Skills & Abilities")

            # Display skills based on class
            skills = character.get('skills', [])

            if skills:
                for skill in skills:
                    with st.expander(f"{skill.get('name', 'Unknown Skill')}"):
                        st.write(f"**MP Cost:** {skill.get('mp_cost', 0)}")
                        st.write(f"**Description:** {skill.get('description', 'No description available')}")
            else:
                # Fallback class skills
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

# Main app logic
if 'character' not in st.session_state or st.session_state.character is None:
    # No character exists, show creation form
    character = create_character_form()

    if character:
        st.session_state.character = character
        st.success("Character created successfully!")

        # Proceed to forge for starting item
        if st.session_state.get('proceed_to_forge', False):
            st.info("Head to The Forge to craft your starting item!")
            if st.button("Go to The Forge"):
                st.switch_page("pages/02_⚒️_Forge.py")
else:
    # Character exists, show character sheet
    st.sidebar.success("Character loaded!")
    if st.sidebar.button("Create New Character (Deletes Current)"):
        st.session_state.character = None
        st.session_state.pop('proceed_to_forge', None)
        st.rerun()

    # Add button to go to The Forge
    if st.sidebar.button("Visit The Forge"):
        st.switch_page("pages/02_⚒️_Forge.py")

    display_character(st.session_state.character)