"""
Dice rolling utilities for Neon D&D Isekai

Provides functions for dice rolls, attribute checks, and combat calculations using
the 3d6 system that replaces the traditional d20 for more consistent outcomes.
"""
import random
import time
from typing import List, Dict, Any, Tuple, Union
import streamlit as st

def roll_die(sides=6):
    """Roll a single die with the specified number of sides"""
    return random.randint(1, sides)

def roll_dice(num_dice=3, sides=6):
    """Roll multiple dice and return individual results and sum"""
    results = [roll_die(sides) for _ in range(num_dice)]
    return {
        'results': results,
        'total': sum(results)
    }

def roll_check(attribute_mod=0, difficulty=10, num_dice=3, sides=6):
    """
    Roll a check against a difficulty value
    
    Args:
        attribute_mod: Modifier from character attribute
        difficulty: Target number to meet or exceed
        num_dice: Number of dice to roll
        sides: Number of sides on each die
        
    Returns:
        Dictionary with roll information and success/failure
    """
    dice_roll = roll_dice(num_dice, sides)
    total = dice_roll['total'] + attribute_mod
    
    return {
        'dice_results': dice_roll['results'],
        'dice_total': dice_roll['total'],
        'modifier': attribute_mod,
        'modified_total': total,
        'difficulty': difficulty,
        'success': total >= difficulty,
        'margin': total - difficulty
    }

def show_dice_roll_animation(container, num_dice=3, sides=6, delay=0.15, frames=8):
    """
    Show animated dice roll in a Streamlit container
    
    Args:
        container: Streamlit container to display animation in
        num_dice: Number of dice to roll
        sides: Number of sides on each die
        delay: Delay between animation frames in seconds
        frames: Number of animation frames
        
    Returns:
        Final dice results
    """
    # Dice symbols for d6 (can be expanded for other dice types)
    d6_symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
    
    # Animation frames
    for i in range(frames):
        # Random dice for animation
        temp_results = [roll_die(sides) for _ in range(num_dice)]
        
        # For d6, use symbols
        if sides == 6:
            dice_display = " ".join([d6_symbols[r-1] for r in temp_results])
        else:
            dice_display = " ".join([f"[{r}]" for r in temp_results])
        
        # Update display
        container.markdown(f"### {dice_display}")
        time.sleep(delay)
    
    # Final roll
    final_roll = roll_dice(num_dice, sides)
    
    # Display final result
    if sides == 6:
        final_display = " ".join([d6_symbols[r-1] for r in final_roll['results']])
    else:
        final_display = " ".join([f"[{r}]" for r in final_roll['results']])
    
    container.markdown(f"### {final_display}")
    
    return final_roll

def attribute_modifier(attribute_value):
    """Calculate attribute modifier like in D&D ((attribute - 10) / 2)"""
    return (attribute_value - 10) // 2

def roll_with_advantage(attribute_mod=0, difficulty=10):
    """Roll two 3d6 checks and take the better result"""
    roll1 = roll_check(attribute_mod, difficulty)
    roll2 = roll_check(attribute_mod, difficulty)
    
    return roll1 if roll1['modified_total'] > roll2['modified_total'] else roll2

def roll_with_disadvantage(attribute_mod=0, difficulty=10):
    """Roll two 3d6 checks and take the worse result"""
    roll1 = roll_check(attribute_mod, difficulty)
    roll2 = roll_check(attribute_mod, difficulty)
    
    return roll1 if roll1['modified_total'] < roll2['modified_total'] else roll2

def streamlit_dice_roller():
    """Streamlit component for rolling dice with animation"""
    st.write("## Dice Roller")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        dice_options = {
            "3d6": "Standard check (3 six-sided dice)",
            "2d10": "Alternative check (2 ten-sided dice)",
            "1d20": "Classic D&D roll (1 twenty-sided die)",
            "1d6": "Single six-sided die",
            "2d6": "Two six-sided dice",
            "4d6": "Attribute roll (4d6, drop lowest)"
        }
        
        selected_dice = st.selectbox(
            "Select dice to roll",
            options=list(dice_options.keys()),
            format_func=lambda x: f"{x} - {dice_options[x]}"
        )
        
        # Parse selected dice
        num_dice, sides = selected_dice.split('d')
        num_dice = int(num_dice)
        sides = int(sides)
        
        # Modifier
        modifier = st.number_input("Modifier", min_value=-10, max_value=10, value=0, step=1)
        
        # Difficulty for checks
        if selected_dice in ["3d6", "2d10", "1d20"]:
            difficulty = st.number_input("Target Difficulty", min_value=5, max_value=20, value=10, step=1)
        else:
            difficulty = None
    
    with col2:
        st.write("&nbsp;")  # Spacing
        roll_button = st.button("🎲 Roll Dice", use_container_width=True)
    
    # Results area
    results_container = st.container()
    dice_container = st.empty()
    result_container = st.empty()
    
    if roll_button:
        # Special case for 4d6 drop lowest
        if selected_dice == "4d6" and "drop lowest" in dice_options[selected_dice]:
            # Animation for all 4 dice
            roll = show_dice_roll_animation(dice_container, num_dice=4, sides=6)
            
            # Calculate result dropping lowest
            results = roll['results']
            dropped = min(results)
            kept = sorted([r for r in results if r != dropped or results.index(r) != results.index(dropped)], reverse=True)
            total = sum(kept)
            
            # Show result
            result_container.markdown(f"""
            **Rolled:** {', '.join([str(r) for r in results])}  
            **Dropped lowest:** {dropped}  
            **Result:** {total + modifier} ({' + '.join([str(r) for r in kept])} + {modifier} modifier)
            """)
            
        # Normal check
        elif difficulty:
            roll = show_dice_roll_animation(dice_container, num_dice=num_dice, sides=sides)
            
            total = roll['total'] + modifier
            success = "Success!" if total >= difficulty else "Failure"
            
            # Show check result
            if modifier != 0:
                mod_text = f" + {modifier}" if modifier > 0 else f" - {abs(modifier)}"
                result_container.markdown(f"""
                **Total:** {total} ({' + '.join([str(r) for r in roll['results']])} = {roll['total']}{mod_text})  
                **Target:** {difficulty}  
                **Result:** {success} by {abs(total - difficulty)}
                """)
            else:
                result_container.markdown(f"""
                **Total:** {total} ({' + '.join([str(r) for r in roll['results']])})  
                **Target:** {difficulty}  
                **Result:** {success} by {abs(total - difficulty)}
                """)
        
        # Simple dice roll
        else:
            roll = show_dice_roll_animation(dice_container, num_dice=num_dice, sides=sides)
            
            total = roll['total'] + modifier
            
            # Show roll result
            if modifier != 0:
                mod_text = f" + {modifier}" if modifier > 0 else f" - {abs(modifier)}"
                result_container.markdown(f"""
                **Total:** {total} ({' + '.join([str(r) for r in roll['results']])} = {roll['total']}{mod_text})
                """)
            else:
                result_container.markdown(f"""
                **Total:** {total} ({' + '.join([str(r) for r in roll['results']])})
                """)

# Additional functions for combat system
def calculate_damage(attack: int, defense: int) -> int:
    """Calculate damage for a combat attack

    Args:
        attack: The attacker's attack rating
        defense: The defender's defense rating

    Returns:
        Amount of damage dealt
    """
    # Base damage is half of attack rating
    base_damage = attack // 2

    # Random component
    variance = random.randint(1, 6)

    # Calculate total (minimum 1)
    total_damage = max(1, base_damage + variance)

    return total_damage
def roll_3d6() -> int:
    """Roll three six-sided dice and sum the results

    This is the core mechanic for the game, replacing the traditional d20 with a
    3d6 bell curve for more consistent outcomes.

    Returns:
        Sum of three d6 rolls (range 3-18)
    """
    return roll_die() + roll_die() + roll_die()

def check_success(roll: int, difficulty: int) -> bool:
    """Check if a roll is successful against a difficulty

    Args:
        roll: The dice roll result
        difficulty: The target number to meet or exceed

    Returns:
        True if roll >= difficulty, False otherwise
    """
    return roll >= difficulty

def combat_attribute_check(attribute_value: int, difficulty: int = 10) -> Tuple[bool, int]:
    """Make an attribute check for combat using 3d6

    The difficulty defaults to 10, which is considered an average check.

    Args:
        attribute_value: The attribute value (typically 3-18)
        difficulty: The target difficulty (default: 10)

    Returns:
        Tuple containing (success, roll)
    """
    roll = roll_3d6()

    # Calculate modifier based on attribute
    modifier = (attribute_value // 2) - 5  # Similar to d20 system but scaled

    # Apply modifier to roll
    modified_roll = roll + modifier

    # Check success
    success = check_success(modified_roll, difficulty)

    return (success, roll)

def contested_check(attacker_attr: int, defender_attr: int) -> Tuple[bool, int, int]:
    """Perform a contested check between two entities

    Args:
        attacker_attr: The attacker's attribute value
        defender_attr: The defender's attribute value

    Returns:
        Tuple containing (attacker_wins, attacker_roll, defender_roll)
    """
    attacker_roll = roll_3d6() + ((attacker_attr // 2) - 5)
    defender_roll = roll_3d6() + ((defender_attr // 2) - 5)

    return (attacker_roll >= defender_roll, attacker_roll, defender_roll)

def calculate_damage(attack: int, defense: int) -> int:
    """Calculate damage for a combat attack

    Args:
        attack: The attacker's attack rating
        defense: The defender's defense rating

    Returns:
        Amount of damage dealt
    """
    # Base damage is half of attack rating
    base_damage = attack // 2

    # Random component
    variance = random.randint(1, 6)

    # Calculate total (minimum 1)
    total_damage = max(1, base_damage + variance)

    return total_damage

if __name__ == "__main__":
    # For testing as standalone
    st.title("Dice System Test")
    streamlit_dice_roller()