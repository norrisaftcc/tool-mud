"""
The Forge - CREATE system for crafting items and equipment
"""
import streamlit as st
import random

# Import from models when implemented
# from models.crafting import craft_item

# Page config
st.set_page_config(
    page_title="The Forge - Neon D&D Isekai",
    page_icon="⚒️",
    layout="wide"
)

# Title and description
st.title("The Forge")
st.subheader("Craft legendary items by combining magical components")

# Check if character exists
if 'character' not in st.session_state or st.session_state.character is None:
    st.warning("You need to create a character before using The Forge!")
    if st.button("Create Character"):
        st.switch_page("pages/01_👤_Character.py")
    st.stop()

# Initialize forge state if needed
if 'forge_state' not in st.session_state:
    st.session_state.forge_state = {
        "essence": 10,
        "max_essence": 20,
        "selected_components": [],
        "known_recipes": [
            {
                "name": "Flaming Sword",
                "components": ["Iron Chunk", "Fire Essence", "Damage Rune"],
                "description": "A sword imbued with the power of fire, dealing additional fire damage with each strike."
            },
            {
                "name": "Frost Staff",
                "components": ["Mithril Alloy", "Frost Shard", "Mana Crystal"],
                "description": "A magical staff that channels the power of ice, freezing enemies and creating barriers of frost."
            }
        ],
        "inventory_components": [
            {"name": "Iron Chunk", "type": "metal", "quality": "basic", "icon": "🔩"},
            {"name": "Mithril Alloy", "type": "metal", "quality": "rare", "icon": "⚙️"},
            {"name": "Fire Essence", "type": "elemental", "element": "fire", "icon": "🔥"},
            {"name": "Frost Shard", "type": "elemental", "element": "ice", "icon": "❄️"},
            {"name": "Lightning Core", "type": "elemental", "element": "lightning", "icon": "⚡"},
            {"name": "Mana Crystal", "type": "catalyst", "power": "minor", "icon": "💎"},
            {"name": "Damage Rune", "type": "rune", "effect": "damage", "icon": "🔆"},
            {"name": "Shield Rune", "type": "rune", "effect": "protection", "icon": "🛡️"}
        ]
    }

# Layout
col1, col2, col3 = st.columns([1, 2, 1])

# Components panel
with col1:
    st.subheader("Components")
    
    # Essence meter
    essence = st.session_state.forge_state["essence"]
    max_essence = st.session_state.forge_state["max_essence"]
    st.progress(essence / max_essence)
    st.caption(f"Essence: {essence}/{max_essence}")
    
    # Component selection
    st.write("#### Available Components")
    
    # Create a grid of component buttons
    components_grid = [st.session_state.forge_state["inventory_components"][i:i+2] 
                      for i in range(0, len(st.session_state.forge_state["inventory_components"]), 2)]
    
    for row in components_grid:
        cols = st.columns(2)
        for i, component in enumerate(row):
            with cols[i]:
                if st.button(f"{component['icon']} {component['name']}", 
                            key=f"component_{component['name']}",
                            use_container_width=True):
                    if len(st.session_state.forge_state["selected_components"]) < 3:
                        st.session_state.forge_state["selected_components"].append(component)
                        st.rerun()
    
    # Known recipes
    st.write("#### Known Recipes")
    for recipe in st.session_state.forge_state["known_recipes"]:
        with st.expander(recipe["name"]):
            st.write(recipe["description"])
            st.write("**Components needed:**")
            for component in recipe["components"]:
                st.write(f"- {component}")

# Forge area
with col2:
    st.subheader("Forge Area")
    
    # Selected components display
    st.write("#### Selected Components")
    selected_cols = st.columns(3)
    
    for i in range(3):
        with selected_cols[i]:
            if i < len(st.session_state.forge_state["selected_components"]):
                component = st.session_state.forge_state["selected_components"][i]
                st.markdown(f"### {component['icon']}")
                st.caption(component["name"])
            else:
                st.markdown("### 🔲")
                st.caption("Empty slot")
    
    # Forge action
    st.write("")
    forge_col1, forge_col2 = st.columns([1, 1])
    
    with forge_col1:
        if st.button("Clear Components", use_container_width=True):
            st.session_state.forge_state["selected_components"] = []
            st.rerun()
            
    with forge_col2:
        forge_disabled = len(st.session_state.forge_state["selected_components"]) < 3 or st.session_state.forge_state["essence"] < 5
        
        if st.button("Forge Item", disabled=forge_disabled, type="primary", use_container_width=True):
            # Roll for crafting
            roll = random.randint(1, 20)
            st.session_state.forge_state["last_roll"] = roll
            st.session_state.forge_state["essence"] -= 5
            
            # Check if components match a known recipe
            component_names = [c["name"] for c in st.session_state.forge_state["selected_components"]]
            recipe_found = None
            
            for recipe in st.session_state.forge_state["known_recipes"]:
                if sorted(recipe["components"]) == sorted(component_names):
                    recipe_found = recipe
                    break
            
            if recipe_found and roll >= 10:
                # Successful crafting
                st.session_state.forge_state["last_result"] = {
                    "success": True,
                    "name": recipe_found["name"],
                    "description": recipe_found["description"],
                    "quality": "Good" if roll < 15 else "Great" if roll < 18 else "Excellent"
                }
            else:
                # Failed crafting
                st.session_state.forge_state["last_result"] = {
                    "success": False,
                    "reason": "Components don't form a known recipe" if not recipe_found else "Crafting attempt failed"
                }
            
            st.session_state.forge_state["selected_components"] = []
            st.rerun()

    # Dice roll animation (when implemented)
    if "last_roll" in st.session_state.forge_state:
        st.write("")
        st.write(f"#### Dice Roll: {st.session_state.forge_state['last_roll']}")

# Result panel
with col3:
    st.subheader("Crafting Result")
    
    if "last_result" in st.session_state.forge_state:
        result = st.session_state.forge_state["last_result"]
        
        if result["success"]:
            st.success(f"Successfully crafted: {result['name']}")
            st.write(f"**Quality:** {result['quality']}")
            st.write(result["description"])
            
            # Item stats based on quality
            if "Sword" in result["name"]:
                damage = "1d8+2" if result["quality"] == "Good" else "1d8+3" if result["quality"] == "Great" else "1d8+4"
                st.write(f"**Damage:** {damage}")
                
                elem_damage = "1d4" if result["quality"] == "Good" else "1d6" if result["quality"] == "Great" else "1d8"
                st.write(f"**Elemental Damage:** {elem_damage}")
            
            # Add to inventory button
            if st.button("Add to Inventory"):
                # Add crafted item to character inventory when implemented
                st.toast(f"{result['name']} added to inventory!")
                
        else:
            st.error(f"Crafting Failed: {result['reason']}")
            st.write("Try a different combination or roll better next time!")
    else:
        st.info("No items crafted yet. Select components and forge an item to see results here.")