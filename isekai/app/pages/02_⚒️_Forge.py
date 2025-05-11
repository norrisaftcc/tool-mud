"""
The Forge - CREATE system for crafting items and equipment
"""
import streamlit as st
import random
import sys
import os

# Import from local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.dice import show_dice_roll_animation, attribute_modifier

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

# Character-specific bonuses for crafting
character = st.session_state.character
craft_modifier = attribute_modifier(character["attributes"]["dexterity"])
craft_bonus_text = f"+{craft_modifier}" if craft_modifier >= 0 else f"{craft_modifier}"

# Display character crafting aptitude
character_class = character["class"]
if character_class == "Wanderer":
    st.info(f"As a Wanderer, you have a natural talent for crafting (DEX modifier: {craft_bonus_text})")
elif character_class == "Warrior":
    st.info(f"Your warrior strength helps you forge weapons (STR bonus applies to weapon crafting)")
elif character_class == "Wizard":
    st.info(f"Your arcane knowledge helps with enchantments (WIS bonus applies to magical items)")
elif character_class == "White Mage":
    st.info(f"Your healing touch improves restorative items (WIS bonus applies to healing items)")

# Initialize forge state if needed
if 'forge_state' not in st.session_state:
    st.session_state.forge_state = {
        "essence": 10,
        "max_essence": 20,
        "selected_components": [],
        "known_recipes": [
            {
                "name": "Flaming Sword",
                "type": "weapon",
                "class_affinity": "Warrior",
                "components": ["Iron Chunk", "Fire Essence", "Damage Rune"],
                "description": "A sword imbued with the power of fire, dealing additional fire damage with each strike.",
                "stats": {
                    "damage": "1d8+[QUALITY]",
                    "elemental": "1d[DICE] fire"
                }
            },
            {
                "name": "Frost Staff",
                "type": "weapon",
                "class_affinity": "Wizard",
                "components": ["Mithril Alloy", "Frost Shard", "Mana Crystal"],
                "description": "A magical staff that channels the power of ice, freezing enemies and creating barriers of frost.",
                "stats": {
                    "damage": "1d6+[QUALITY]",
                    "effect": "Slow target for [QUALITY] turns"
                }
            },
            {
                "name": "Thunder Shield",
                "type": "armor",
                "class_affinity": "Warrior",
                "components": ["Mithril Alloy", "Lightning Core", "Shield Rune"],
                "description": "A shield crackling with electrical energy that protects the bearer and can discharge lightning at attackers.",
                "stats": {
                    "defense": "[QUALITY]+1",
                    "counter": "1d4 lightning damage to melee attackers"
                }
            },
            {
                "name": "Healing Charm",
                "type": "accessory",
                "class_affinity": "White Mage",
                "components": ["Glowing Herb", "Mana Crystal", "Shield Rune"],
                "description": "A magical charm that emanates healing energy, gradually restoring health to the bearer.",
                "stats": {
                    "effect": "Regenerate [QUALITY] HP per turn",
                    "uses": "[QUALITY] uses per day"
                }
            },
            {
                "name": "Shadowstep Boots",
                "type": "accessory",
                "class_affinity": "Wanderer",
                "components": ["Glowing Herb", "Lightning Core", "Damage Rune"],
                "description": "Boots that allow the wearer to briefly step between shadows, moving with incredible speed.",
                "stats": {
                    "effect": "+[QUALITY] to initiative",
                    "ability": "Teleport [QUALITY]×5 feet once per battle"
                }
            }
        ],
        "inventory_components": [
            {"name": "Iron Chunk", "type": "metal", "quality": "basic", "icon": "🔩"},
            {"name": "Mithril Alloy", "type": "metal", "quality": "rare", "icon": "⚙️"},
            {"name": "Fire Essence", "type": "elemental", "element": "fire", "icon": "🔥"},
            {"name": "Frost Shard", "type": "elemental", "element": "ice", "icon": "❄️"},
            {"name": "Lightning Core", "type": "elemental", "element": "lightning", "icon": "⚡"},
            {"name": "Mana Crystal", "type": "catalyst", "power": "minor", "icon": "💎"},
            {"name": "Glowing Herb", "type": "binding", "source": "plant", "icon": "🌿"},
            {"name": "Damage Rune", "type": "rune", "effect": "damage", "icon": "🔆"},
            {"name": "Shield Rune", "type": "rune", "effect": "protection", "icon": "🛡️"}
        ]
    }

# Check if this is starting item creation
starting_item = st.session_state.get('proceed_to_forge', False)
if starting_item:
    st.success("As a new adventurer, you can forge one special item to start your journey!")
    st.session_state.forge_state["essence"] = 20  # Extra essence for starting item

    # Guide the player based on their class
    class_recipes = []
    for recipe in st.session_state.forge_state["known_recipes"]:
        if recipe.get("class_affinity") == character_class:
            class_recipes.append(recipe["name"])

    if class_recipes:
        st.info(f"The forge master suggests these recipes would suit a {character_class}: {', '.join(class_recipes)}")

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
            if i < len(row):
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

            # Show class affinity if exists
            if "class_affinity" in recipe:
                affinity = recipe["class_affinity"]
                if affinity == character_class:
                    st.success(f"**Affinity:** {affinity} (Your class)")
                else:
                    st.info(f"**Affinity:** {affinity}")

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
            # Check if components match a known recipe
            component_names = [c["name"] for c in st.session_state.forge_state["selected_components"]]
            recipe_found = None

            for recipe in st.session_state.forge_state["known_recipes"]:
                if sorted(recipe["components"]) == sorted(component_names):
                    recipe_found = recipe
                    break

            # Set up dice roll container
            dice_container = st.empty()
            result_container = st.empty()

            # Use 3d6 for crafting check
            crafting_roll = show_dice_roll_animation(dice_container, num_dice=3, sides=6)

            # Apply character modifier
            item_type = recipe_found["type"] if recipe_found else "unknown"

            if item_type == "weapon" and character_class == "Warrior":
                mod = attribute_modifier(character["attributes"]["strength"])
            elif (item_type == "weapon" and character_class == "Wizard") or item_type == "accessory":
                mod = attribute_modifier(character["attributes"]["wisdom"])
            else:
                mod = attribute_modifier(character["attributes"]["dexterity"])

            # Class affinity bonus
            affinity_bonus = 0
            if recipe_found and recipe_found.get("class_affinity") == character_class:
                affinity_bonus = 2

            total_roll = crafting_roll["total"] + mod + affinity_bonus
            difficulty = 10  # Base difficulty

            # Use essence
            st.session_state.forge_state["essence"] -= 5

            # Store the roll info
            st.session_state.forge_state["last_roll"] = {
                "dice": crafting_roll["results"],
                "dice_total": crafting_roll["total"],
                "modifier": mod,
                "affinity_bonus": affinity_bonus,
                "total": total_roll
            }

            # Show roll result
            mod_text = f" + {mod}" if mod > 0 else f" - {abs(mod)}" if mod < 0 else ""
            affinity_text = f" + {affinity_bonus} (class affinity)" if affinity_bonus > 0 else ""

            result_container.write(f"**Roll:** {crafting_roll['total']}{mod_text}{affinity_text} = **{total_roll}**")

            if recipe_found and total_roll >= difficulty:
                # Determine quality
                if total_roll >= 18:
                    quality = "Excellent"
                    quality_value = 3
                    quality_dice = 8
                elif total_roll >= 15:
                    quality = "Great"
                    quality_value = 2
                    quality_dice = 6
                elif total_roll >= 10:
                    quality = "Good"
                    quality_value = 1
                    quality_dice = 4
                else:
                    quality = "Poor"
                    quality_value = 0
                    quality_dice = 4

                # Process stats from recipe
                stats = {}
                for stat_name, stat_formula in recipe_found.get("stats", {}).items():
                    # Replace placeholders with actual values
                    stat_value = stat_formula.replace("[QUALITY]", str(quality_value))
                    stat_value = stat_value.replace("[DICE]", str(quality_dice))
                    stats[stat_name] = stat_value

                # Create the item
                item = {
                    "name": recipe_found["name"],
                    "type": recipe_found["type"],
                    "description": recipe_found["description"],
                    "quality": quality,
                    "stats": stats
                }

                # Successful crafting
                st.session_state.forge_state["last_result"] = {
                    "success": True,
                    "item": item
                }
            else:
                # Failed crafting
                st.session_state.forge_state["last_result"] = {
                    "success": False,
                    "reason": "Components don't form a known recipe" if not recipe_found else "Crafting attempt failed"
                }

            st.session_state.forge_state["selected_components"] = []
            st.rerun()

    # Show dice roll result if it exists
    if "last_roll" in st.session_state.forge_state:
        roll_info = st.session_state.forge_state["last_roll"]

        # Dice symbols for d6
        d6_symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
        dice_display = " ".join([d6_symbols[r-1] for r in roll_info["dice"]])

        st.write("")
        st.markdown(f"### {dice_display}")

        # Format the roll details
        roll_text = f"Dice Total: {roll_info['dice_total']}"
        if roll_info['modifier'] != 0:
            mod_text = f"+{roll_info['modifier']}" if roll_info['modifier'] > 0 else f"{roll_info['modifier']}"
            roll_text += f", Modifier: {mod_text}"

        if roll_info.get('affinity_bonus', 0) > 0:
            roll_text += f", Class Affinity: +{roll_info['affinity_bonus']}"

        roll_text += f" = **{roll_info['total']}**"
        st.write(roll_text)

# Result panel
with col3:
    st.subheader("Crafting Result")

    if "last_result" in st.session_state.forge_state:
        result = st.session_state.forge_state["last_result"]

        if result["success"]:
            item = result["item"]

            st.success(f"Successfully crafted: {item['name']}")
            st.write(f"**Quality:** {item['quality']}")
            st.write(item["description"])

            # Item stats
            st.write("**Stats:**")
            for stat_name, stat_value in item["stats"].items():
                st.write(f"- **{stat_name.capitalize()}:** {stat_value}")

            # Add to inventory button
            if st.button("Add to Inventory"):
                # Add crafted item to character inventory
                if "inventory" not in st.session_state.character:
                    st.session_state.character["inventory"] = []

                # Add the item to inventory
                st.session_state.character["inventory"].append(item)

                # If this is a starting item, mark the process as complete
                if starting_item:
                    st.session_state.pop('proceed_to_forge', None)

                    # Equip the item automatically
                    if "equipment" not in st.session_state.character:
                        st.session_state.character["equipment"] = {}

                    st.session_state.character["equipment"][item["type"]] = item["name"]

                    st.success(f"You crafted and equipped your starting {item['name']}!")
                else:
                    st.success(f"{item['name']} added to inventory!")

                # Clear the result
                st.session_state.forge_state.pop("last_result", None)
                st.rerun()

        else:
            st.error(f"Crafting Failed: {result['reason']}")
            st.write("Try a different combination or roll better next time!")
    else:
        st.info("No items crafted yet. Select components and forge an item to see results here.")

# Display buttons to navigate to other pages
st.write("---")
col_buttons = st.columns(3)

with col_buttons[0]:
    if st.button("Character Sheet", use_container_width=True):
        st.switch_page("pages/01_👤_Character.py")

with col_buttons[2]:
    if st.button("Roll Dice", use_container_width=True):
        st.switch_page("pages/dice_test.py")