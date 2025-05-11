"""
Test page for 3d6 dice system visualization
"""
import streamlit as st
import time
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Import local modules
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.dice import streamlit_dice_roller

# Page config
st.set_page_config(
    page_title="Dice System - Neon D&D Isekai",
    page_icon="🎲",
    layout="wide"
)

# Title and description
st.title("Dice System Test")
st.subheader("Bell Curve vs. Flat Distribution")

# Introduction
st.markdown("""
This page demonstrates the advantages of using a 3d6 bell curve distribution instead of a 1d20 flat distribution
for the core mechanic of Neon D&D Isekai.

Try the interactive dice roller below to see the 3d6 system in action, or explore the probability distributions
to understand why a bell curve creates more consistent results where character skill matters more than lucky rolls.
""")

# Two column layout
col1, col2 = st.columns([3, 2])

with col1:
    # Interactive dice roller component
    streamlit_dice_roller()
    
    # Additional explanation
    st.markdown("""
    ### Advantages of 3d6 System
    
    1. **More Consistent Results**: The bell curve means results tend to cluster around the average (10-11)
    2. **Less Swingy**: Extreme results (very high or very low) are less common, making gameplay more predictable
    3. **Character Skill Matters More**: Attribute bonuses have a bigger impact since the dice variation is smaller
    4. **Visual Interest**: Rolling three dice is more engaging than a single d20
    5. **Tactical Depth**: Players can make better risk assessments with a more predictable probability curve
    """)

with col2:
    # Distribution comparison tab system
    tab1, tab2 = st.tabs(["Distribution Comparison", "Success Probabilities"])
    
    with tab1:
        # Generate probability distributions
        d20_results = list(range(1, 21))
        d20_probs = [1/20] * 20  # Flat 5% chance per value
        
        # 3d6 results and probabilities (calculated)
        d6_3_results = list(range(3, 19))
        d6_3_probs = [
            1/216, 3/216, 6/216, 10/216, 15/216, 21/216, 25/216, 27/216,
            27/216, 25/216, 21/216, 15/216, 10/216, 6/216, 3/216, 1/216
        ]
        
        # Create dataframe for easy plotting
        df = pd.DataFrame({
            'Value': d20_results + d6_3_results,
            'Probability': d20_probs + d6_3_probs,
            'System': ['1d20'] * 20 + ['3d6'] * 16
        })
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot 1d20 distribution
        d20_df = df[df['System'] == '1d20']
        ax.bar(d20_df['Value'], d20_df['Probability'], alpha=0.7, color='#ff00ff', label='1d20 (Flat)')
        
        # Plot 3d6 distribution
        d6_3_df = df[df['System'] == '3d6'] 
        ax.bar(d6_3_df['Value'], d6_3_df['Probability'], alpha=0.7, color='#00ffff', label='3d6 (Bell Curve)')
        
        # Add grid, legend, and labels
        ax.grid(alpha=0.3)
        ax.legend()
        ax.set_xlabel('Roll Result')
        ax.set_ylabel('Probability')
        ax.set_title('Probability Distribution: 1d20 vs 3d6')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Display the plot
        st.pyplot(fig)
        
        st.caption("The 3d6 system produces a bell curve where middle values are more common, while the 1d20 system has an equal chance for any result.")
    
    with tab2:
        # Create table showing success probabilities for different target numbers
        st.write("### Success Probability by Target Number")
        
        # Generate data
        target_numbers = list(range(8, 19))
        
        # Calculate success probability for each
        d20_success = [(21 - tn) / 20 for tn in target_numbers]  # (values that succeed) / 20
        
        # 3d6 success probabilities (pre-calculated)
        d6_3_success = [
            0.9815, 0.9537, 0.9074, 0.8333, 0.7407, 0.6250, 0.5000,
            0.3750, 0.2593, 0.0926, 0.0463
        ]
        
        # Create dataframe
        success_df = pd.DataFrame({
            'Target Number': target_numbers,
            '1d20 System': [f"{p:.1%}" for p in d20_success],
            '3d6 System': [f"{p:.1%}" for p in d6_3_success]
        })
        
        # Display table
        st.table(success_df)
        
        # Create plot comparing the two
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.plot(target_numbers, d20_success, 'o-', color='#ff00ff', label='1d20 System')
        ax2.plot(target_numbers, d6_3_success, 'o-', color='#00ffff', label='3d6 System')
        
        # Add grid, legend, and labels
        ax2.grid(alpha=0.3)
        ax2.legend()
        ax2.set_xlabel('Target Number')
        ax2.set_ylabel('Success Probability')
        ax2.set_title('Success Probability by Target Number')
        ax2.set_ylim(0, 1)
        
        # Display the plot
        st.pyplot(fig2)
        
        st.caption("The 3d6 system creates a steeper probability curve, with high success rates for easy tasks and low success rates for difficult tasks.")

# Animation demo
st.write("## Dice Rolling Animation")
st.write("This shows how the three dice could be animated during gameplay for added suspense.")

# Side-by-side 3d6 vs 1d20 animation
anim_col1, anim_col2 = st.columns(2)

with anim_col1:
    st.write("### 3d6 System")
    d6_anim = st.empty()
    d6_result = st.empty()
    
    if st.button("Roll 3d6", key="anim_3d6"):
        # Dice symbols for d6
        d6_symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
        
        # Animation frames
        for i in range(6):
            # Random dice for animation
            temp_results = [random.randint(1, 6) for _ in range(3)]
            dice_display = " ".join([d6_symbols[r-1] for r in temp_results])
            
            # Update display
            d6_anim.markdown(f"<h2 style='text-align: center;'>{dice_display}</h2>", unsafe_allow_html=True)
            time.sleep(0.15)
        
        # Final result
        final_results = [random.randint(1, 6) for _ in range(3)]
        final_display = " ".join([d6_symbols[r-1] for r in final_results])
        total = sum(final_results)
        
        d6_anim.markdown(f"<h2 style='text-align: center;'>{final_display}</h2>", unsafe_allow_html=True)
        d6_result.markdown(f"<h3 style='text-align: center;'>Total: {total}</h3>", unsafe_allow_html=True)

with anim_col2:
    st.write("### 1d20 System")
    d20_anim = st.empty()
    d20_result = st.empty()
    
    if st.button("Roll 1d20", key="anim_1d20"):
        # Animation frames
        for i in range(6):
            # Random value for animation
            temp_result = random.randint(1, 20)
            
            # Update display
            d20_anim.markdown(f"<h2 style='text-align: center;'>[{temp_result}]</h2>", unsafe_allow_html=True)
            time.sleep(0.15)
        
        # Final result
        final_result = random.randint(1, 20)
        
        d20_anim.markdown(f"<h2 style='text-align: center;'>[{final_result}]</h2>", unsafe_allow_html=True)
        d20_result.markdown(f"<h3 style='text-align: center;'>Total: {final_result}</h3>", unsafe_allow_html=True)