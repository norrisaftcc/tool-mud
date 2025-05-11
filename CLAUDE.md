# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains "Neon D&D Isekai: Retro Realm Reboot" - a text-based RPG that blends classic D&D mechanics with neon aesthetics and isekai anime tropes. It's designed as both an entertaining adventure and an educational framework for learning programming concepts.

The game features four main gameplay areas, each mapping to different educational objectives:
- **CREATE (The Forge)**: Crafting system for items and equipment
- **EXPLAIN (The Lore Halls)**: NPC interactions and knowledge collection
- **CODE (The Arcane Matrix)**: Programming-based spell creation
- **EXPLORE (The Neon Wilderness)**: Dungeon exploration and combat

## Development Environment

### Requirements
- Python 3.9+ (3.10 recommended)
- Virtual environment (venv)
- Streamlit (for the web interface)

### Setup Commands

**Create and activate virtual environment:**
```bash
# Windows
python -m venv mudvenv
mudvenv\Scripts\activate

# macOS/Linux
python3 -m venv mudvenv
source mudvenv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**For development (when implemented):**
```bash
pip install -r requirements-dev.txt
```

### Running the Application

**Start the Streamlit app (when implemented):**
```bash
streamlit run streamlit_app.py
```

## Project Structure

The planned project structure follows this organization:
- `app/` - Main application with Streamlit pages
- `models/` - Core game logic (character, combat, crafting, etc.)
- `data/` - Game data files (JSON)
- `utils/` - Utility functions
- `assets/` - Static assets (CSS, images, fonts, sounds)
- `tests/` - Test suite

## Testing

When tests are implemented, they should be run using pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_specific.py

# Run with coverage report
pytest --cov=.
```

## Game Architecture

### State Management
The game uses Streamlit's session state for managing game state with patterns like:

```python
# Initialize game state
if 'character' not in st.session_state:
    st.session_state.character = None

if 'dungeon' not in st.session_state:
    st.session_state.dungeon = None
```

### Core Components

1. **Character System**
   - Classic D&D attributes (Strength, Dexterity, Wisdom)
   - Character creation and progression

2. **The Forge (CREATE System)**
   - Component-based crafting
   - Recipe discovery
   - Quality determination via dice rolls

3. **The Lore Halls (EXPLAIN System)**
   - LLM-powered NPC interactions
   - Knowledge collection

4. **The Arcane Matrix (CODE System)**
   - Visual programming for spell creation
   - Syntax validation and debugging

5. **The Neon Wilderness (EXPLORE System)**
   - Procedural dungeon generation
   - Turn-based combat
   - Treasure discovery

## Player Types

The game is designed around Bartle's taxonomy of player types:

- **CREATE** appeals to Achievers and Explorers
- **EXPLAIN** appeals to Socializers and Explorers
- **CODE** appeals to Achievers and Explorers
- **EXPLORE** appeals to Explorers, Killers, and Achievers

This helps understand how different game elements appeal to different player motivations.