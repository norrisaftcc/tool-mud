"""
Character creation and management page
"""
import streamlit as st
import random

# Import from models when implemented
# from models.character import Character

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
        
        with col2:
            st.write("### Attributes")
            st.write("Roll for your attributes or choose a balanced preset.")
            
            if st.button("🎲 Roll Attributes", form_submit=False):
                # Simulate dice rolls
                strength = random.randint(8, 18)
                dexterity = random.randint(8, 18)
                wisdom = random.randint(8, 18)
                
                st.session_state.temp_attributes = {
                    "strength": strength,
                    "dexterity": dexterity,
                    "wisdom": wisdom
                }
            
            attributes = st.session_state.get('temp_attributes', {
                "strength": 12,
                "dexterity": 12, 
                "wisdom": 12
            })
            
            st.metric("Strength", attributes["strength"])
            st.metric("Dexterity", attributes["dexterity"])
            st.metric("Wisdom", attributes["wisdom"])
        
        submitted = st.form_submit_button("Create Character")
        
        if submitted:
            if not name:
                st.error("Please enter a character name")
                return None
            
            # In the future, this would create a Character object
            character = {
                "name": name,
                "class": character_class,
                "origin": isekai_origin,
                "attributes": attributes,
                "level": 1,
                "hp": 10 + (attributes["strength"] // 2),
                "mp": 10 + (attributes["wisdom"] // 2),
                "inventory": []
            }
            
            return character
    
    return None

# Character display
def display_character(character):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{character['name']} - Level {character['level']} {character['class']}")
        st.write(f"**Origin:** {character['origin']}")
        
        # Progress bars for HP/MP
        st.write("HP")
        st.progress(1.0)  # Replace with actual HP percentage
        st.write("MP")
        st.progress(1.0)  # Replace with actual MP percentage
    
    with col2:
        st.subheader("Attributes")
        col2a, col2b, col2c = st.columns(3)
        
        with col2a:
            st.metric("Strength", character["attributes"]["strength"])
        with col2b:
            st.metric("Dexterity", character["attributes"]["dexterity"])
        with col2c:
            st.metric("Wisdom", character["attributes"]["wisdom"])
    
    st.subheader("Equipment")
    # Display equipment here when implemented
    
    st.subheader("Skills & Abilities")
    # Display skills based on class when implemented

# Main app logic
if 'character' not in st.session_state or st.session_state.character is None:
    # No character exists, show creation form
    character = create_character_form()
    
    if character:
        st.session_state.character = character
        st.success("Character created successfully!")
        st.rerun()
else:
    # Character exists, show character sheet
    st.sidebar.success("Character loaded!")
    if st.sidebar.button("Create New Character (Deletes Current)"):
        st.session_state.character = None
        st.rerun()
    
    display_character(st.session_state.character)