# The Assemblage Point: A Shared Hallucination Game
## Design Document v1.0

### Table of Contents
1. [Executive Summary](#executive-summary)
2. [Game Overview](#game-overview)
3. [Core Gameplay Loop](#core-gameplay-loop)
4. [Game Mechanics](#game-mechanics)
5. [Technical Architecture](#technical-architecture)
6. [User Interface Design](#user-interface-design)
7. [World & Content Design](#world-content-design)
8. [Progression Systems](#progression-systems)
9. [Social Features](#social-features)
10. [Development Roadmap](#development-roadmap)
11. [Technical Requirements](#technical-requirements)
12. [Risk Assessment](#risk-assessment)

---

## Executive Summary

**The Assemblage Point** is a text-based multiplayer game where reality itself is malleable through collective perception. Inspired by Carlos Castaneda's teachings and classic MUDs, players shift their consciousness to collaboratively shape a fluid, ever-changing world. Using SpacetimeDB's real-time architecture and Streamlit's rapid prototyping capabilities, the game creates a unique experience where perception determines reality and consensus builds worlds.

### Key Features
- **Consciousness-based gameplay**: Players manipulate their "assemblage point" to perceive and alter reality
- **Collaborative world-building**: Multiple players' perceptions merge to create consensus reality
- **Dynamic ASCII art**: Visual representations shift based on collective perception
- **Retroactive reality**: Past events can change based on present consciousness
- **Power word system**: Language becomes a tool for reality manipulation

### Target Audience
- Fans of experimental/artistic games
- Text-based game enthusiasts (MUD/MUSH players)
- Philosophy and consciousness exploration communities
- Creative writers and collaborative storytellers

---

## Game Overview

### Core Concept
Players are apprentice sorcerers learning to shift their assemblage point - the position of perception that determines what reality they experience. Through various practices inspired by Castaneda's works, players can:
- See multiple layers of reality simultaneously
- Collaboratively dream new worlds into existence
- Use intent and power words to alter the fabric of reality
- Navigate non-Euclidean spaces through consciousness shifts

### Victory Conditions
There is no traditional "winning" - success is measured by:
- Depth of reality layers accessed
- Stability of created consensus realities
- Mastery of consciousness-shifting techniques
- Quality of collaborative world-building

### Core Pillars
1. **Perception as Gameplay**: Every action involves shifting how you see reality
2. **Collaborative Creation**: Reality strengthens through collective agreement
3. **Fluid Navigation**: Movement through space depends on consciousness state
4. **Language as Power**: Words and descriptions literally reshape the world

---

## Core Gameplay Loop

### Minute-to-Minute (Exploration Phase)
1. **Observe** current reality through ASCII art and text descriptions
2. **Shift perception** using commands like `/gaze`, `/stop`, or `/notdoing`
3. **Discover** new reality layers or hidden aspects of objects
4. **Describe** what you perceive to strengthen or alter it

### Session-to-Session (Creation Phase)
1. **Collaborate** with other players to align assemblage points
2. **Build consensus** around shared perceptions to solidify reality
3. **Create spaces** through collective dreaming and intent
4. **Establish power words** that become tools for future reality manipulation

### Long-term (Mastery Phase)
1. **Master techniques** for assemblage point control
2. **Lead group consciousness** expeditions to unexplored reality layers
3. **Architect stable realms** that persist across sessions
4. **Teach newcomers** the arts of perception (player-driven tutorials)

---

## Game Mechanics

### Assemblage Point System
Each player has an assemblage point with X,Y coordinates:
- **X-axis**: Lateral shift (different perspectives of same reality)
- **Y-axis**: Vertical shift (depth of awareness)
- **Stability**: How fixed vs. fluid the point is

#### Shifting Techniques
1. **Gazing** (`/gaze [object]`)
   - Gradual lateral shifts
   - Reveals hidden properties of objects
   - Low energy cost, requires sustained focus

2. **Not-Doing** (`/notdoing [action]`)
   - Breaks perceptual patterns
   - Causes moderate shifts in any direction
   - Examples: "/notdoing walk backwards", "/notdoing speak in colors"

3. **Stopping the World** (`/stop`)
   - Dramatic vertical shift if successful
   - Requires multiple players or deep focus
   - Reveals entirely new reality layers

4. **Dreaming** (`/dream`)
   - Creates "double" that explores while body remains
   - Can establish new room connections
   - Group dreaming creates stable alternate realms

5. **Recapitulation** (`/recap [memory]`)
   - Allows editing of past events
   - Changes propagate through reality if enough players agree
   - Can undo previous actions or create new histories

### Consensus Reality System
Reality has multiple simultaneous states:
- **Personal Layer**: What only you perceive (0-30% reality strength)
- **Shared Vision**: 2-3 players perceiving similarly (30-70% strength)
- **Consensus Reality**: Majority agreement (70-100% strength)

When players describe the same thing similarly, reality strength increases. At 100%, it becomes "fixed" reality that requires significant effort to change.

### Power Word Mechanics
Players can discover and create words of power:
- **Discovery**: Found through exploration in high awareness states
- **Binding**: Link words to specific reality effects
- **Casting**: Speak words to force reality shifts
- **Resistance**: Other players can resist based on their stability

Example power words:
- "Intent" - Manifests desired changes
- "Voir" - Forces energy sight
- "Tonal/Nagual" - Shifts between ordered/chaotic reality

### Non-Euclidean Navigation
Movement changes based on consciousness:
- **First Attention** (Y < 0.3): Normal cardinal directions
- **Second Attention** (Y 0.3-0.6): Diagonal/unusual paths appear
- **Heightened Awareness** (Y > 0.6): Navigate by intent rather than direction
- **Total Freedom** (Y > 0.8): Teleportation through will

### ASCII Art Reality Rendering
Visual feedback indicates reality state:
```
Stable Reality (>80% consensus):
╔═══════════════════╗
║  🏛️ THE PLAZA 🏛️  ║
║                   ║
║  ╱▔▔▔▔▔▔▔▔▔▔▔╲   ║
║ ▕ ╱▔▔▔▔▔▔▔▔╲ ▏   ║
║ ▕▕  ●    ●  ▏▏   ║
║ ▕▕     ▿     ▏▏   ║
║ ▕ ╲▁▁▁▁▁▁▁▁╱ ▏   ║
║  ╲▁▁▁▁▁▁▁▁▁▁▁╱   ║
╚═══════════════════╝

Shifting Reality (30-80% consensus):
╔═══════════════════╗
║  🌊 THE PL̸A̷Z̴A 🌊  ║
║                   ║
║  ╱▔▔▔▔░▔▔▔▔▔╲   ║
║ ▕ ╱▔▔▒▒▒▔▔▔╲ ▏   ║
║ ▕▕  ●  ▓  ●  ▏▏   ║
║ ▕▕   ░ ▿ ░   ▏▏   ║
║ ▕ ╲▁▒▒▒▒▒▁▁╱ ▏   ║
║  ╲▁▁▁░▁▁▁▁▁▁╱   ║
╚═══════════════════╝

Hallucination (<30% consensus):
╔═══════════════════╗
║  🌀 T̶̅H̷̍Ë̸́ ̶̾P̸̏L̷̇Ä̶́Z̷̾A̶̅ 🌀  ║
║  ░▒▓█▓▒░▒▓█▓▒░   ║
║  ▒╱▔░▔▔▓▔▔░▔╲▓   ║
║ ░▕▓╱░▒▓█▓▒░╲▒▏   ║
║ ▓▕▕░●░▓█▓░●░▏▏░  ║
║ ▒▕▕▓░▒▿▒░▓█▓▏▏▒  ║
║ ░▕▒╲░▓▒░▒▓░╱▓▏   ║
║  ▓╲▒░▓█▓░▒▓░╱░   ║
╚═══════════════════╝
```

---

## Technical Architecture

### Technology Stack
- **Backend**: SpacetimeDB (Rust modules)
- **Frontend**: Streamlit (Python)
- **Bridge**: FastAPI + WebSockets
- **Authentication**: SpacetimeDB OpenID Connect
- **Hosting**: SpacetimeDB Cloud + Streamlit Community Cloud

### Data Flow Architecture
```
┌─────────────┐     WebSocket    ┌─────────────┐     Events     ┌─────────────┐
│  Streamlit  │◄─────────────────►│   FastAPI   │◄──────────────►│ SpacetimeDB │
│   Frontend  │                   │   Bridge    │                 │   Backend   │
└─────────────┘                   └─────────────┘                 └─────────────┘
       ▲                                 ▲                               ▲
       │                                 │                               │
       └─────────── UI Renders ──────────┴───── Game Logic ────────────┘
```

### Database Schema (SpacetimeDB Tables)

```rust
// Core player data
#[table(name = player)]
pub struct Player {
    #[primary_key]
    pub id: u64,
    pub name: String,
    pub current_room: u64,
    pub energy_level: f32,
    pub personal_power: f32,
    pub joined_at: Timestamp,
}

// Assemblage point tracking
#[table(name = assemblage_point)]
pub struct AssemblagePoint {
    #[primary_key]
    pub player_id: u64,
    pub x_position: f32,
    pub y_position: f32,
    pub stability: f32,
    pub last_shift: Timestamp,
    pub shift_method: String,
}

// Room/location data
#[table(name = room)]
pub struct Room {
    #[primary_key]
    pub id: u64,
    pub base_name: String,
    pub base_description: String,
    pub creator_id: u64,
    pub creation_method: String,  // "physical", "dreamed", "intent"
    pub stability: f32,
}

// Perception layers
#[table(name = perception_layer)]
pub struct PerceptionLayer {
    #[primary_key]
    pub layer_id: u64,
    pub entity_id: u64,
    pub entity_type: String,  // "room", "object", "player"
    pub perceiver_id: u64,
    pub description: String,
    pub reality_strength: f32,
    pub created_at: Timestamp,
}

// Reality consensus tracking
#[table(name = reality_consensus)]
pub struct RealityConsensus {
    pub entity_id: u64,
    pub description_hash: String,
    pub agreeing_players: String,  // JSON array
    pub consensus_level: f32,
    pub last_updated: Timestamp,
}

// Power words
#[table(name = power_word)]
pub struct PowerWord {
    #[primary_key]
    pub word: String,
    pub discovered_by: u64,
    pub effect_type: String,
    pub power_level: f32,
    pub usage_count: u32,
}

// Game events log (for recapitulation)
#[table(name = game_event)]
pub struct GameEvent {
    #[primary_key]
    pub event_id: u64,
    pub event_type: String,
    pub actor_id: u64,
    pub target_id: Option<u64>,
    pub description: String,
    pub timestamp: Timestamp,
    pub reality_version: u32,  // Increments when past changes
}
```

### Core Reducers (Game Actions)

```rust
#[reducer]
pub fn shift_assemblage_point(ctx: &ReducerContext, 
                             technique: String, 
                             target: Option<String>)

#[reducer]
pub fn describe_reality(ctx: &ReducerContext, 
                       entity_id: u64, 
                       entity_type: String,
                       description: String)

#[reducer]
pub fn speak_power_word(ctx: &ReducerContext, 
                       word: String, 
                       target_players: Vec<u64>)

#[reducer]
pub fn move_through_intent(ctx: &ReducerContext, 
                          intent: String)

#[reducer]
pub fn create_consensus(ctx: &ReducerContext, 
                       entity_id: u64, 
                       agreed_description: String)

#[reducer]
pub fn recapitulate_event(ctx: &ReducerContext, 
                         event_id: u64, 
                         new_description: String)
```

---

## User Interface Design

### Main Game Screen Layout

```
╔═══════════════════════════════════════════════════════════════╗
║  THE ASSEMBLAGE POINT - Reality Layer: Consensus (78%)        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌─────────────────────────────────────────┐  ┌────────────┐ ║
║  │          ROOM ASCII ART HERE             │  │ PLAYERS:   │ ║
║  │                                          │  │ • You ✨   │ ║
║  │         [Dynamic based on consensus]     │  │ • Zara 🌊  │ ║
║  │                                          │  │ • Ken 🏛️   │ ║
║  └─────────────────────────────────────────┘  │            │ ║
║                                                │ AP DISPLAY: │ ║
║  Current Reality: The Plaza of Shifting Sands  │  ⠀⠀⣀⣀⣀⣀⠀⠀  │ ║
║  ────────────────────────────────────────────  │  ⢀⣴⣿⣿⣿⣦⡀  │ ║
║  You perceive a plaza where geometric patterns │  ⣾⣿⣿●⣿⣿⣷  │ ║
║  shift like living kaleidoscopes. The benches │  ⠈⢿⣿⣿⣿⡿⠁  │ ║
║  seem to breathe with an ancient rhythm.       │ X:0.3 Y:0.5│ ║
║                                                │ Shifting   │ ║
║  [Your Reality - 34% strength]:               └────────────┘ ║
║  The tiles whisper secrets of the first world.               ║
║                                                               ║
║  [Consensus Reality - 78% strength]:                         ║
║  A sun-drenched plaza with worn stone benches.               ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║ > /gaze bench                                    [Send] [Help]║
╚═══════════════════════════════════════════════════════════════╝
```

### UI Components

1. **Reality Layer Indicator**: Shows current perception mode and consensus strength
2. **Dynamic ASCII Display**: Changes based on reality consensus and AP position
3. **Multi-layer Description**: Shows personal, shared, and consensus realities
4. **Player List with States**: Visual indicators for each player's awareness level
5. **Assemblage Point Visualizer**: Real-time position display
6. **Command Input**: Supports both "/" commands and natural language

### Streamlit Implementation Strategy

```python
# Main game loop in Streamlit
def main():
    st.set_page_config(page_title="The Assemblage Point", 
                      layout="wide",
                      initial_sidebar_state="collapsed")
    
    # Custom CSS for terminal aesthetic
    st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize game connection
    if 'game_bridge' not in st.session_state:
        st.session_state.game_bridge = SpacetimeDBBridge()
    
    # Main layout columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # ASCII art display
        ascii_container = st.empty()
        
        # Reality descriptions
        reality_container = st.container()
        
        # Command input
        command = st.chat_input("Enter command or description...")
        
    with col2:
        # Player list
        players_container = st.container()
        
        # AP visualizer
        ap_display = st.empty()
    
    # Real-time update loop
    if command:
        process_command(command)
    
    update_display(ascii_container, reality_container, 
                  players_container, ap_display)
```

---

## World & Content Design

### Starting Area: The Academy of Perception
New players begin in a tutorial realm designed to teach core mechanics:

1. **Hall of Mirrors**: Learn gazing and perception shifting
2. **Garden of Not-Doing**: Practice pattern-breaking
3. **Dream Chamber**: Introduction to group consciousness
4. **Word Sanctuary**: Discover first power words

### Core Realms

#### The First Attention (Default Reality)
- **The Market**: Social hub, trading descriptions
- **Crystal Caves**: Perception puzzles
- **The Infinite Library**: Repository of player-created lore
- **Temporal Gardens**: Practice recapitulation

#### The Second Attention (Shifted Reality)
- **The Inverse City**: Geometry defies logic
- **Emotion Seas**: Navigate by feeling
- **The Probability Forest**: Multiple simultaneous paths
- **Echo Valley**: Past and future blur

#### Heightened Awareness Realms
- **The Energy Grid**: See the underlying code of reality
- **Consciousness Nexus**: Direct mind-to-mind linking
- **The Void Between**: Navigate pure possibility
- **Archive of All Things**: Access collective unconscious

### Environmental Storytelling
Rather than quests, the game uses:
- **Perception Breadcrumbs**: Hidden details visible at certain AP positions
- **Consensus Mysteries**: Puzzles requiring group agreement
- **Reality Archaeology**: Uncover past player creations
- **Dream Echoes**: Traces left by sleeping players

---

## Progression Systems

### Mastery Tracks (Not Levels)

1. **Awareness Depth**
   - Unlock higher Y-axis positions
   - See more reality layers simultaneously
   - Resist forced perception shifts

2. **Stability Control**
   - Maintain AP position under stress
   - Shift others more effectively
   - Create lasting reality changes

3. **Word Power**
   - Discover ancient power words
   - Create custom reality commands
   - Bind words to specific effects

4. **Dream Architecture**
   - Build in dream state
   - Link dream realms
   - Bring dream objects to consensus

5. **Social Influence**
   - Lead group consciousness shifts
   - Teach techniques to others
   - Harmonize conflicting realities

### Recognition Systems
- **Perception Tokens**: Earned for discovering new reality layers
- **Consensus Medals**: Awarded for successful group creations
- **Reality Architect**: Title for prolific world builders
- **Dream Walker**: Recognition for dream realm mastery
- **Word Keeper**: Status for power word discoveries

---

## Social Features

### Group Consciousness Mechanics
- **AP Alignment Circles**: Players synchronize assemblage points
- **Consensus Councils**: Formal reality-agreement sessions
- **Dream Parties**: Coordinated exploration of dream realms
- **Reality Raids**: Large group attempts to shift major areas

### Communication Systems
- **Proximity Chat**: Normal talking in same room
- **Awareness Whispers**: Communication between aligned APs
- **Dream Messages**: Leave notes in dream state
- **Power Word Telegraph**: Long-distance reality pulses

### Mentorship Program
- **Nagual/Apprentice System**: Experienced players guide newcomers
- **Technique Demonstrations**: Visual AP tracking during teaching
- **Shared Perception Mode**: See through teacher's eyes
- **Graduation Ceremonies**: Community recognition of mastery

---

## Development Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [ ] SpacetimeDB module setup with core tables
- [ ] Basic movement and perception system
- [ ] Streamlit UI with ASCII rendering
- [ ] FastAPI bridge implementation
- [ ] Authentication and player persistence

### Phase 2: Core Mechanics (Weeks 5-8)
- [ ] Assemblage point system
- [ ] Consensus reality calculations
- [ ] Basic shifting techniques (gaze, stop)
- [ ] Multi-layer perception rendering
- [ ] Power word discovery system

### Phase 3: Advanced Features (Weeks 9-12)
- [ ] Dream state implementation
- [ ] Recapitulation mechanics
- [ ] Non-Euclidean navigation
- [ ] Group consciousness features
- [ ] Reality archaeology system

### Phase 4: Polish & Content (Weeks 13-16)
- [ ] Tutorial realm completion
- [ ] Advanced ASCII art generation
- [ ] Performance optimization
- [ ] Community tools
- [ ] Launch preparation

### Post-Launch Roadmap
- Month 2: Dream realm expansion
- Month 3: Power word crafting system
- Month 4: Reality tournament events
- Month 6: Player-created tutorial realms

---

## Technical Requirements

### Minimum Server Requirements
- **SpacetimeDB Instance**: 2 vCPU, 4GB RAM
- **FastAPI Bridge**: 1 vCPU, 2GB RAM
- **Streamlit Frontend**: Standard Community Cloud tier

### Performance Targets
- Support 100+ concurrent players per instance
- Sub-100ms response time for actions
- 30fps ASCII animation capability
- Real-time consensus calculations

### Scalability Plan
- Multiple SpacetimeDB instances for different regions
- Realm sharding based on player density
- Consensus calculation optimization
- Caching frequently accessed perception layers

---

## Risk Assessment

### Technical Risks
1. **SpacetimeDB Python SDK Status**
   - *Risk*: Unmaintained SDK
   - *Mitigation*: FastAPI bridge pattern, consider Rust client

2. **Real-time Performance**
   - *Risk*: Consensus calculations at scale
   - *Mitigation*: Efficient algorithms, caching strategies

3. **ASCII Rendering Performance**
   - *Risk*: Complex animations in Streamlit
   - *Mitigation*: Pre-rendered frames, efficient updates

### Design Risks
1. **Onboarding Complexity**
   - *Risk*: Concepts too abstract for new players
   - *Mitigation*: Structured tutorial, mentorship system

2. **Griefing Through Reality Manipulation**
   - *Risk*: Players forcing unwanted perceptions
   - *Mitigation*: Resistance mechanics, safe zones

3. **Content Persistence**
   - *Risk*: Reality too fluid, nothing permanent
   - *Mitigation*: Stability thresholds, anchor points

### Community Risks
1. **Niche Appeal**
   - *Risk*: Limited audience
   - *Mitigation*: Free-to-play, low barriers

2. **Complexity Barrier**
   - *Risk*: Too philosophical/abstract
   - *Mitigation*: Multiple play styles supported

---

## Conclusion

The Assemblage Point represents a unique fusion of consciousness exploration, collaborative creation, and emergent gameplay. By leveraging SpacetimeDB's real-time capabilities and Streamlit's rapid development framework, we can create an experience that pushes the boundaries of what multiplayer games can be - a space where reality itself becomes the canvas for collective imagination.

The game's success will depend on creating an accessible entry point to complex concepts while maintaining depth for those who wish to master the arts of perception. Through careful implementation of Castaneda-inspired mechanics and strong community features, The Assemblage Point can become a unique space for creative collaboration and consciousness exploration in game form.