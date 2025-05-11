"""
Neon D&D Isekai: Retro Realm Reboot
Main Streamlit application entry point
"""
import streamlit as st

# Set page config
st.set_page_config(
    page_title="Neon D&D Isekai",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize game state
if 'character' not in st.session_state:
    st.session_state.character = None

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

if 'game_progress' not in st.session_state:
    st.session_state.game_progress = {
        "quests": [],
        "discoveries": [],
        "level": 1
    }

# Main page content
st.title("Neon D&D Isekai: Retro Realm Reboot")
st.subheader("A text-based RPG blending classic D&D mechanics with neon aesthetics and isekai anime tropes")

# Display game introduction
st.markdown("""
## Welcome, Adventurer!

You've been transported to a world where dungeon crawls are illuminated by neon lights,
dragons breathe laser beams, and magic scrolls glow with digital text.

Use the sidebar navigation to access different areas of the game:
- **Character**: Create or manage your character
- **The Forge**: Craft items and equipment
- **Lore Halls**: Interact with NPCs and collect knowledge
- **Arcane Matrix**: Create spells using programming logic
- **Neon Wilderness**: Explore dungeons and combat enemies
""")

# Character status display in the sidebar if character exists
if st.session_state.character:
    with st.sidebar:
        st.subheader("Character Sheet")
        # Display basic character info here
else:
    with st.sidebar:
        st.info("No character created yet. Visit the Character page to get started!")
        if st.button("Create New Character"):
            st.switch_page("pages/01_👤_Character.py")