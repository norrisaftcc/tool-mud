"""
Dice roller component for game mechanics
"""
import streamlit as st
import random
import time

def parse_dice_notation(notation):
    """
    Parse standard dice notation (e.g., '2d6+3')
    
    Args:
        notation: String in dice notation format
    
    Returns:
        Tuple of (number of dice, dice sides, modifier)
    """
    # Handle basic format like "d20" (implicitly 1d20)
    if notation.startswith('d'):
        notation = '1' + notation
    
    # Split into dice and modifier parts
    if '+' in notation:
        dice_part, mod_part = notation.split('+')
        modifier = int(mod_part)
    elif '-' in notation:
        dice_part, mod_part = notation.split('-')
        modifier = -int(mod_part)
    else:
        dice_part = notation
        modifier = 0
    
    # Parse dice part (e.g., 2d6)
    dice_count, sides = dice_part.split('d')
    
    return (int(dice_count), int(sides), modifier)

def roll_dice(notation, with_animation=False):
    """
    Roll dice based on standard notation
    
    Args:
        notation: String in dice notation format (e.g., '2d6+3')
        with_animation: Boolean to show rolling animation
    
    Returns:
        Dictionary with roll result information
    """
    dice_count, sides, modifier = parse_dice_notation(notation)
    
    # Roll the dice
    rolls = [random.randint(1, sides) for _ in range(dice_count)]
    total = sum(rolls) + modifier
    
    # Create result object
    result = {
        'notation': notation,
        'rolls': rolls,
        'modifier': modifier,
        'total': total
    }
    
    if with_animation:
        # Create placeholder for animation
        dice_display = st.empty()
        roll_display = st.empty()
        
        # Simulate rolling animation
        for i in range(6):  # Animation frames
            temp_rolls = [random.randint(1, sides) for _ in range(dice_count)]
            dice_symbols = get_dice_symbols(sides, temp_rolls)
            
            # Show dice and temporary result
            dice_display.markdown(f"### {''.join(dice_symbols)}")
            roll_display.markdown(f"Rolling...")
            
            # Short pause between animation frames
            time.sleep(0.15)
        
        # Show final result
        dice_symbols = get_dice_symbols(sides, rolls)
        dice_display.markdown(f"### {''.join(dice_symbols)}")
        
        # Format final result text
        if modifier != 0:
            mod_text = f" {'+' if modifier > 0 else '-'} {abs(modifier)}"
            roll_display.markdown(f"Result: {total} ({' + '.join([str(r) for r in rolls])}{mod_text})")
        else:
            roll_display.markdown(f"Result: {total} ({' + '.join([str(r) for r in rolls])})")
    
    return result

def get_dice_symbols(sides, rolls):
    """Get Unicode dice face symbols for common dice types"""
    symbols = []
    
    for roll in rolls:
        if sides == 6:
            # Unicode dice faces for d6
            d6_symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
            symbols.append(d6_symbols[roll - 1])
        elif sides == 20:
            # No Unicode for d20, use text representation
            symbols.append(f"[{roll}]")
        else:
            # Default for other dice
            symbols.append(f"[{roll}]")
    
    return symbols

def dice_roller_component(key_prefix="dice"):
    """
    Create an interactive dice roller widget
    
    Args:
        key_prefix: String prefix for component keys
    
    Returns:
        The roll result if rolled, otherwise None
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        dice_options = {
            "d4": "4-sided die",
            "d6": "6-sided die",
            "d8": "8-sided die",
            "d10": "10-sided die",
            "d12": "12-sided die",
            "d20": "20-sided die",
            "d100": "Percentile die",
            "2d6": "2 six-sided dice",
            "3d6": "3 six-sided dice",
            "4d6": "4 six-sided dice (drop lowest)",
        }
        
        selected_dice = st.selectbox(
            "Select dice to roll",
            options=list(dice_options.keys()),
            format_func=lambda x: f"{x} - {dice_options[x]}",
            key=f"{key_prefix}_select"
        )
        
        # Additional modifier
        modifier = st.number_input(
            "Modifier",
            min_value=-20,
            max_value=20,
            value=0,
            step=1,
            key=f"{key_prefix}_mod"
        )
        
        # Format final dice notation
        if modifier != 0:
            dice_notation = f"{selected_dice}{'+' if modifier > 0 else ''}{modifier}"
        else:
            dice_notation = selected_dice
    
    with col2:
        st.write("&nbsp;")  # Spacing
        roll_button = st.button("🎲 Roll", key=f"{key_prefix}_roll", use_container_width=True)
    
    # Roll results area
    results_area = st.container()
    
    if roll_button:
        # Handle special case for 4d6 drop lowest
        if selected_dice == "4d6" and "(drop lowest)" in dice_options[selected_dice]:
            # Roll 4d6 and drop lowest
            rolls = [random.randint(1, 6) for _ in range(4)]
            dropped = min(rolls)
            kept_rolls = [r for r in rolls if r != dropped or rolls.index(r) != rolls.index(dropped)]
            
            with results_area:
                st.write(f"Rolled: {', '.join([str(r) for r in rolls])}")
                st.write(f"Dropped lowest: {dropped}")
                st.write(f"Result: {sum(kept_rolls) + modifier}")
                
            return {
                'notation': "4d6 (drop lowest)",
                'rolls': rolls,
                'kept': kept_rolls,
                'dropped': dropped,
                'modifier': modifier,
                'total': sum(kept_rolls) + modifier
            }
        else:
            # Standard dice roll
            with results_area:
                result = roll_dice(dice_notation, with_animation=True)
                return result
    
    return None

if __name__ == "__main__":
    # For testing as standalone
    st.title("Dice Roller Test")
    dice_roller_component()