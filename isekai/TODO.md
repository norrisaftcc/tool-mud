# Neon D&D Isekai: Project TODO List

## TOP PRIORITY
- [x] Set up basic project structure
- [x] Create initial Streamlit app scaffolding
- [x] Implement character creation skeleton
- [x] Build prototype of The Forge (CREATE system)
- [x] **Convert core mechanic from d20 to bell curve (3d6) for more consistent outcomes**
- [x] **Plan MVP for each quadrant (CREATE, EXPLAIN, CODE, EXPLORE)**
- [ ] **Implement strict separation of concerns (UI, game logic, data layers)**
- [ ] **Add comprehensive automated testing for all components**

## SPRINT 2 GOALS
- [ ] Implement basic dungeon exploration (EXPLORE quadrant)
  - [ ] Week 1: Core structure (DungeonLevel, Room, generation algorithm)
  - [ ] Week 2: Room content and exploration interface
  - [ ] Week 3: Combat system with 3d6 mechanics
  - [ ] Week 4: Integration and polish
- [ ] **Apply strict separation of concerns to all new code:**
  - [ ] Isolate UI, game logic, and data layers
  - [ ] Apply MVC pattern to EXPLORE quadrant implementation
- [ ] **Implement comprehensive automated testing:**
  - [ ] Write unit tests alongside all new code (test-driven development)
  - [ ] Add integration tests for critical gameplay loops
- [ ] Add more crafted items and recipes to The Forge
- [ ] Implement save/load functionality for game state
- [ ] Create minimal version of Lore Halls (EXPLAIN) if time permits
- [ ] Add tutorial and help system for new players

## MVP Status by Quadrant

### CREATE (The Forge) - IMPLEMENTED
- [x] Define core crafting mechanics 
- [x] Create component/recipe data structure
- [x] Implement basic item generation logic
- [x] Connect crafting to character inventory
- [x] Design simple crafting UI
- [x] Add starting item system for roguelike runs
- [x] Implement class affinities for items

### EXPLAIN (The Lore Halls) - PLANNED
- [ ] Define NPC interaction model
- [ ] Create basic conversation system
- [ ] Design knowledge collection mechanics
- [ ] Implement basic lore database
- [ ] Create LLM prompt templates for NPC responses

### CODE (The Arcane Matrix) - PLANNED
- [ ] Design simplified pseudocode system for spells
- [ ] Create drag-and-drop interface for spell components
- [ ] Implement spell validation logic
- [ ] Define core spell effects
- [ ] Connect spell creation to character abilities

### EXPLORE (The Neon Wilderness) - NEXT PRIORITY
- [x] Design basic dungeon generation algorithm (adapted from MazeBuilder)
- [x] Create detailed implementation plan with architecture design
- [ ] Implement DungeonLevel and Room classes
- [ ] Create BSP dungeon generation algorithm
- [ ] Build dungeon visualization with neon theming
- [ ] Implement exploration interface and movement system
- [ ] Create monster generation system
- [ ] Implement turn-based combat with 3d6 mechanics
- [ ] Add treasure and reward system
- [ ] Connect exploration to character progression

## Technical Tasks
- [x] Set up proper state management using session_state
- [x] Create character data model
- [x] Build component library for reusable UI elements
- [x] Implement inventory system
- [x] Design data structures for game objects
- [x] Create utility functions for common operations
- [x] Set up basic test framework
- [x] Document core mechanics with complete technical specifications
- [x] Create comprehensive development documentation

### Separation of Concerns (CRITICAL)
- [ ] **Refactor existing code to follow strict MVC architecture:**
  - [ ] UI layer (Streamlit pages and components)
    - [ ] Move all UI rendering code to dedicated view classes/functions
    - [ ] Ensure UI components only handle presentation and user input
    - [ ] Create consistent UI component library with standardized styling
  - [ ] Game logic layer (models and core mechanics)
    - [ ] Move all game logic to dedicated model classes
    - [ ] Ensure models have no UI or persistence dependencies
    - [ ] Implement controller classes to connect UI and models
  - [ ] Data persistence layer (save/load functionality)
    - [ ] Create data access objects (DAOs) for all persistent data
    - [ ] Implement serialization/deserialization for game state
    - [ ] Ensure data layer is isolated from game logic and UI

### Automated Testing (CRITICAL)
- [ ] **Implement comprehensive test suite for all game components:**
  - [ ] Unit tests for all model classes and functions
    - [ ] Character and inventory tests
    - [ ] Crafting system tests
    - [ ] Dungeon generation tests
    - [ ] Combat system tests
    - [ ] Dice mechanics tests
  - [ ] Integration tests for complex system interactions
    - [ ] Character-inventory-crafting workflow tests
    - [ ] Dungeon exploration-encounter-combat workflow tests
    - [ ] Complete gameplay loop tests
  - [ ] UI tests for critical user interactions
    - [ ] Character creation flow tests
    - [ ] Crafting interface tests
    - [ ] Exploration interface tests
  - [ ] Set up CI/CD pipeline for automated test runs
  - [ ] Achieve minimum 80% code coverage

### Other Technical Tasks
- [ ] Create visualization system for dungeon maps
- [ ] Optimize for performance with larger dungeons
- [ ] Implement save/load functionality with proper error handling

## Future Features
- [ ] Advanced LLM integration for NPC interactions
- [ ] Cloud save functionality
- [ ] Advanced combat mechanics
- [ ] Quest system
- [ ] Visual effects and animations
- [ ] Sound effects and music
- [ ] Mobile device optimization
- [ ] Multiplayer features