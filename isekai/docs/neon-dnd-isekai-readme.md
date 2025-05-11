# Neon D&D Isekai: Retro Realm Reboot

![Neon D&D Isekai Logo](assets/images/logo.png)

A text-based RPG that blends classic D&D mechanics with neon aesthetics and isekai anime tropes. Built with Python and Streamlit.

## 🚀 Project Overview

Neon D&D Isekai is an educational game project that combines 1980s D&D nostalgia with modern isekai tropes and synthwave aesthetics. The game serves as both an entertaining adventure and a framework for learning programming concepts, with its four main gameplay areas (CREATE, EXPLAIN, CODE, EXPLORE) mapping to educational objectives.

### Key Features:
- Interactive character creation with classic D&D attributes
- Component-based crafting system with recipe discovery
- Turn-based combat system with neon-themed abilities
- Dungeon exploration with procedural generation
- Programming-based spell creation system
- LLM-powered NPC interaction engine

## 💻 System Requirements

- Works on Windows, macOS, and Linux
- Python 3.9+ (3.10 recommended)
- Git
- 4GB RAM minimum (8GB recommended)
- 1GB free disk space

## 🏗️ Project Structure

```
neon-dnd-isekai/
├── .github/                      # GitHub workflow configurations
├── venv/                         # Python virtual environment (gitignored)
├── app/                          # Main application directory
│   ├── pages/                    # Streamlit multipage app structure
│   │   ├── 00_🏠_Home.py         # Home page / main menu
│   │   ├── 01_👤_Character.py    # Character creation/management
│   │   ├── 02_⚒️_Forge.py        # CREATE system (The Forge)
│   │   ├── 03_🧙_Lore.py         # EXPLAIN system (Lore Halls)
│   │   ├── 04_💻_Arcane.py       # CODE system (Arcane Matrix)
│   │   └── 05_🔍_Dungeon.py      # EXPLORE system (Neon Wilderness)
│   └── components/               # Reusable UI components
│       ├── character_sheet.py    # Character info display
│       ├── dice_roller.py        # Dice rolling component
│       ├── inventory.py          # Inventory management
│       └── terminal.py           # Code/terminal component
├── assets/                       # Static assets
│   ├── css/                      # Custom CSS for Streamlit
│   ├── images/                   # Game images
│   ├── fonts/                    # Custom fonts
│   └── sounds/                   # Sound effects/music
├── data/                         # Game data files
│   ├── classes.json              # Class definitions
│   ├── items.json                # Item definitions
│   ├── monsters.json             # Monster definitions
│   ├── recipes.json              # Crafting recipes
│   ├── spells.json               # Spell definitions
│   └── npcs.json                 # NPC definitions
├── models/                       # Core game logic
│   ├── character.py              # Character class
│   ├── combat.py                 # Combat system
│   ├── crafting.py               # Crafting system
│   ├── dungeon.py                # Dungeon generation
│   ├── llm.py                    # LLM integration
│   └── spell_system.py           # Spell programming system
├── utils/                        # Utility functions
│   ├── dice.py                   # Dice rolling functions
│   ├── game_state.py             # Game state management
│   ├── formatters.py             # Text formatting utilities
│   └── file_io.py                # File operations
├── tests/                        # Test suite
│   ├── test_character.py
│   ├── test_combat.py
│   ├── test_crafting.py
│   └── test_dungeon.py
├── .gitignore                    # Git ignore file
├── LICENSE                       # Project license
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
└── streamlit_app.py              # Main Streamlit application entry point
```

## 🔧 Installation & Setup

### Prerequisites
1. Install Python 3.9+ from [python.org](https://python.org)
2. Install Git from [git-scm.com](https://git-scm.com)

### Project Setup (Cross-Platform Instructions)

#### Step 1: Clone the repository
```bash
git clone https://github.com/your-organization/neon-dnd-isekai.git
cd neon-dnd-isekai
```

#### Step 2: Create and activate virtual environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

For development (optional):
```bash
pip install -r requirements-dev.txt
```

## 🚀 Running the Application

**On Windows:**
```bash
# Make sure your virtual environment is activated
venv\Scripts\activate

# Start the Streamlit app
streamlit run streamlit_app.py
```

**On macOS/Linux:**
```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Start the Streamlit app
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501` by default.

### Troubleshooting Common Issues

#### Port already in use
If port 8501 is already in use, Streamlit will automatically try to use the next available port. You can also specify a port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

#### Python version issues
Make sure you're using Python 3.9 or higher. Check your version with:
```bash
python --version  # Windows
python3 --version  # macOS/Linux
```

#### Package installation failures
If you have issues installing packages on Windows, try:
```bash
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
```

On macOS, you might need to install developer tools first:
```bash
xcode-select --install
```

## 🧪 Development Workflow

### State Management
We use Streamlit's `st.session_state` for managing game state:

```python
# Initialize game state
if 'character' not in st.session_state:
    st.session_state.character = None

if 'dungeon' not in st.session_state:
    st.session_state.dungeon = None

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
```

### Streamlit Best Practices
- Use caching (`@st.cache_data`, `@st.cache_resource`) for expensive operations
- Leverage session state for persistent data between reruns
- Create modular components for reusability
- Use columns and containers for layout management

### Game Data Management
Game data is stored in JSON files in the `data/` directory. Use the utilities in `utils/file_io.py` to load and save game data:

```python
from utils.file_io import load_game_data

# Load class definitions
classes = load_game_data('classes.json')
```

## ✨ Key Components

### The Forge (CREATE System)
- Interactive crafting interface
- Component combination system
- Recipe discovery and management
- Quality determination based on dice rolls

Implementation:
```python
# models/crafting.py
def craft_item(components, character, roll):
    """Craft an item from components based on character skills and dice roll."""
    # Implementation details...
```

### The Lore Halls (EXPLAIN System)
- LLM-powered NPC interactions
- Knowledge collection and documentation
- Persuasion mechanics
- Lore discovery

Implementation:
```python
# models/llm.py
def generate_npc_response(npc_id, player_input, relationship_level):
    """Generate contextually appropriate NPC response."""
    # Implementation details...
```

### The Arcane Matrix (CODE System)
- Visual programming interface for spell creation
- Drag-and-drop spell components
- Syntax validation and debugging
- Spell execution and effects

Implementation:
```python
# models/spell_system.py
def validate_spell_syntax(spell_components):
    """Validate that a spell's components form valid syntax."""
    # Implementation details...
```

### The Neon Wilderness (EXPLORE System)
- Procedural dungeon generation
- Interactive exploration interface
- Trap and hazard management
- Monster encounters and treasure discovery

Implementation:
```python
# models/dungeon.py
def generate_dungeon_level(level, character_level):
    """Generate a dungeon level appropriate for the character."""
    # Implementation details...
```

## 🧠 LLM Integration

The game integrates with LLMs for:
- Dynamic NPC interactions
- Spell effect generation
- Custom item descriptions
- Hint systems for puzzles

```python
# models/llm.py
def get_llm_completion(prompt, context, temperature=0.7):
    """Get completion from LLM with appropriate context."""
    # Implementation details...
```

## 🧪 Testing

Run tests using pytest:

**On Windows:**
```bash
# Activate your virtual environment first
venv\Scripts\activate

# Run all tests
pytest

# Run specific test file
pytest tests\test_character.py

# Run with coverage report
pytest --cov=.
```

**On macOS/Linux:**
```bash
# Activate your virtual environment first
source venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_character.py

# Run with coverage report
pytest --cov=.
```

### Visual Studio Code Integration
If you're using VS Code (recommended for students):

1. Install the Python extension
2. Open the command palette (Ctrl+Shift+P or Cmd+Shift+P)
3. Type "Python: Configure Tests" and select pytest
4. Run and debug tests using the Test Explorer

## 📊 Deployment Options for Students

### Local Development
This is the simplest approach for classroom use:
- Run locally on your own machine
- Share your work via GitHub
- Present your project directly from your laptop

### Streamlit Cloud (Free Tier)
For showcasing your project:
- Create a GitHub repository with your code
- Sign up for a free [Streamlit Cloud](https://streamlit.io/cloud) account
- Connect your repository to deploy your app
- Share the provided URL with others

### GitHub Codespaces
For consistent development environments:
- Your instructor may set up GitHub Codespaces
- This provides a cloud-based development environment
- Works in any browser without local installation
- Includes all dependencies pre-configured

## 🤝 Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎲 Player Types & Game Areas

Our four game areas are designed to appeal to different types of players and learning styles. Based on Bartle's taxonomy of player types, here's how each area might align with your preferences:

### CREATE (The Forge)
**Game Area:** Crafting items, building equipment, designing magical tools

**Appeals to:**
- **Achievers** - You enjoy mastering systems, creating powerful items, and seeing tangible results of your efforts
- **Explorers** - You like discovering new recipes, experimenting with different component combinations, and understanding how crafting systems work

**If you enjoy:** Minecraft crafting, RPG gear progression, building things, or creative design

### EXPLAIN (The Lore Halls)
**Game Area:** Collecting knowledge, interacting with NPCs, documenting the world

**Appeals to:**
- **Socializers** - You enjoy character interactions, dialogue choices, and forming relationships with NPCs
- **Explorers** - You like uncovering lore, understanding the world's history, and solving knowledge-based puzzles

**If you enjoy:** Visual novels, dialogue-rich RPGs, world-building, or storytelling games

### CODE (The Arcane Matrix)
**Game Area:** Creating spells through programming logic, solving coding puzzles

**Appeals to:**
- **Achievers** - You enjoy mastering logical systems, optimizing your solutions, and creating powerful combinations
- **Explorers** - You like discovering how the coding systems work, finding hidden interactions, and testing the limits of the magical system

**If you enjoy:** Programming puzzles, logic games, optimization challenges, or systems thinking

### EXPLORE (The Neon Wilderness)
**Game Area:** Dungeon crawling, discovering new areas, finding treasure, combat

**Appeals to:**
- **Explorers** - You enjoy mapping new territories, finding secret passages, and discovering hidden content
- **Killers** - You like tactical combat, overcoming challenges, and testing your skills against powerful enemies
- **Achievers** - You enjoy finding rare loot, completing dungeons, and earning rewards

**If you enjoy:** Dungeon crawlers, roguelikes, adventure games, or tactical combat

Most players will enjoy aspects of all four areas, but understanding your preferences can help you focus on the parts of the game that will be most engaging for you! As you develop and modify the game, consider leaning into the areas that match your player type.

## 👥 Team

- GM - Project Lead & Game Designer
- Teacherbot.help Claude - Systems Designer & Content Developer
- Kai "Circuit" Chen - Visual Designer & Technical Lead

## 🎮 Student Development Guide

This project is designed to be accessible for students at various skill levels. Here are some tips for getting started:

### For Beginners
1. Start by running the application and exploring the code
2. Make simple changes to the UI text or colors
3. Modify game data in the JSON files to create new items or monsters
4. Try implementing a simple feature like a new dice rolling function

### For Intermediate Students
1. Create a new class with unique abilities
2. Add a new crafting recipe with special effects
3. Implement a new dungeon room type
4. Extend the character sheet with additional stats

### For Advanced Students
1. Implement a new game subsystem
2. Add LLM integration for dynamic content
3. Create a custom visualization for the game map
4. Implement save/load functionality for game progress

### Learning Objectives
Each area of the game corresponds to specific learning objectives:
- **CREATE**: Asset generation, procedural content, UI design
- **EXPLAIN**: Documentation, communication, knowledge representation
- **CODE**: Logic implementation, system architecture, debugging
- **EXPLORE**: Data structures, information retrieval, world-building

---

*Remember: The most important thing is that this is FUN to play while learning!*