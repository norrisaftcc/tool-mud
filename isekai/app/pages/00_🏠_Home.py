"""
Home page / main menu for Neon D&D Isekai
"""
import streamlit as st

# Page config
st.set_page_config(
    page_title="Home - Neon D&D Isekai",
    page_icon="🏠",
    layout="wide"
)

# Home page content
st.title("Neon D&D Isekai: Retro Realm Reboot")
st.subheader("Welcome to the Neon Realm")

# Game world introduction
st.markdown("""
## The World of Neon D&D

You find yourself in a strange world that blends the familiar elements of classic tabletop RPGs with 
vibrant neon aesthetics and digital constructs. The skies shimmer with pixelated stars, dungeons glow 
with neon signs, and magic spells leave trails of digital particles.

This world exists in a space between reality and imagination, where the rules of classic D&D apply, 
but with a visual style that feels like stepping into an 80s arcade cabinet crossed with a fantasy realm.

## Your Journey Begins

As an Isekai protagonist suddenly transported to this world, you must navigate its unique challenges, 
discover why you were brought here, and perhaps find a way home—or decide to stay and become a legend 
in this neon-drenched realm.

## Game Areas

Explore the four main regions of the world:

- **The Forge** - Create and craft powerful equipment
- **The Lore Halls** - Gather knowledge and interact with NPCs
- **The Arcane Matrix** - Master the art of spell creation through code
- **The Neon Wilderness** - Explore dungeons and battle foes
""")

# Display character info if exists
if st.session_state.get('character'):
    char = st.session_state.character
    st.sidebar.subheader("Character Info")
    # Display character summary here
else:
    st.sidebar.warning("You don't have a character yet! Visit the Character page to create one.")
    if st.sidebar.button("Create Character"):
        st.switch_page("pages/01_👤_Character.py")