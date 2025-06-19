# Building a Text-Based Shared Hallucination Game with SpacetimeDB

SpacetimeDB's revolutionary database-server hybrid architecture combined with Streamlit's rapid prototyping capabilities creates a unique opportunity for building a collaborative text-based game where reality itself becomes malleable through collective player perception. This guide provides a comprehensive roadmap for implementing such a game, drawing from MUD traditions while introducing innovative reality-shifting mechanics.

## SpacetimeDB's game-changing architecture for multiplayer

SpacetimeDB fundamentally reimagines multiplayer game architecture by **eliminating the traditional client-server-database separation**. Instead of managing separate services, your entire game logic runs as WebAssembly modules inside the database itself, achieving ~100 microsecond transaction times and supporting 1,000+ concurrent players on a single instance.

The platform's real-time synchronization happens through SQL subscription queries. When players enter a room, they simply subscribe to `SELECT * FROM players WHERE current_room = ?` and automatically receive updates whenever the room state changes. This declarative approach eliminates complex networking code while providing ACID transaction guarantees that prevent item duplication bugs and ensure consistent game state.

For authentication, SpacetimeDB uses OpenID Connect with persistent identities across sessions. Every game action executes as an atomic "reducer" function - either succeeding completely or failing entirely. This single-threaded programming model lets developers write simple logic while SpacetimeDB handles concurrency behind the scenes.

## Data modeling for collaborative hallucination mechanics

The game's unique "shared hallucination" concept requires careful data modeling that supports multiple perception layers and reality consensus. Here's the core entity structure optimized for SpacetimeDB:

```rust
// Reality layers - different perceptions of same objects
#[table(name = perception_layer, public)]
pub struct PerceptionLayer {
    #[primary_key]
    layer_id: u64,
    entity_id: u64,  // What object/room this perception describes
    perceiver_id: u64,  // Player or group seeing this version
    description: String,
    reality_strength: f32,  // 0.0-1.0 consensus level
    created_at: Timestamp,
}

// Assemblage point tracking (Castaneda-inspired mechanic)
#[table(name = assemblage_point, public)]
pub struct AssemblagePoint {
    #[primary_key]
    player_id: u64,
    x_position: f32,  // Position on perception grid
    y_position: f32,  // Higher Y = heightened awareness
    stability: f32,   // How fixed vs fluid the point is
    last_shift: Timestamp,
    shift_method: String,  // "intent", "power_plant", "dreaming", etc.
}

// Consensus tracking for reality-shaping
#[table(name = reality_consensus, public)]
pub struct RealityConsensus {
    entity_id: u64,
    description_hash: String,
    agreeing_players: String,  // JSON array of player IDs
    consensus_level: f32,
    last_updated: Timestamp,
}

// Dynamic room connections for dream-like navigation
#[table(name = room_connection, public)]
pub struct RoomConnection {
    from_room: u64,
    to_room: u64,
    direction: String,
    stability: f32,  // How "real" this connection is
    discovered_by: u64,  // Player who first found this path
    awareness_level_required: f32,  // Minimum assemblage point Y to perceive
}
```

This schema enables multiple players to perceive different versions of reality while tracking consensus. As players agree on descriptions, `reality_strength` increases, making that perception more "real" for everyone.

## Real-time synchronization patterns for shared consciousness

SpacetimeDB's subscription system perfectly supports the game's reality-shifting mechanics. Players subscribe not just to physical locations but to perception layers and assemblage point alignments:

```rust
// Players see consensus reality plus their unique perceptions
let consensus_query = "SELECT * FROM perception_layer 
    WHERE entity_id IN (SELECT entity_id FROM current_room_entities) 
    AND reality_strength > 0.7";

let personal_query = format!("SELECT * FROM perception_layer 
    WHERE perceiver_id = {} 
    AND entity_id IN (SELECT entity_id FROM current_room_entities)", 
    player_id);

// Subscribe to nearby assemblage points for group work
let ap_query = "SELECT * FROM assemblage_point 
    WHERE ABS(x_position - ?) < 0.2 
    AND ABS(y_position - ?) < 0.2";
```

The key innovation is using **reality consensus as a game mechanic**. When multiple players describe something similarly, the system detects this through a reducer:

```rust
#[reducer]
pub fn describe_entity(ctx: &ReducerContext, entity_id: u64, description: String) {
    let player_id = get_player_id(&ctx.sender);
    
    // Create/update player's perception
    ctx.db.perception_layer().upsert(PerceptionLayer {
        entity_id,
        perceiver_id: player_id,
        description: description.clone(),
        reality_strength: 0.3,  // Individual perceptions start weak
        created_at: ctx.timestamp,
    });
    
    // Check for consensus with other players
    update_reality_consensus(ctx, entity_id, &description);
}
```

### Example player commands inspired by Castaneda:

- `/gaze [object]` - Soften focus to shift perception of an object
- `/stop` - Attempt to stop the world (requires sustained focus)
- `/recap [memory]` - Recapitulate past events to change them
- `/dream` - Enter dreaming state to explore alternate realities
- `/stalk [player]` - Subtly influence another's perception
- `/intent [action]` - Use pure intent to manifest changes
- `/see` - Attempt to see energy directly (voir)
- `/notdoing [action]` - Perform actions that break patterns

## Streamlit integration strategies despite SDK limitations

While SpacetimeDB's Python SDK is unmaintained, integration remains feasible through a **FastAPI middleware pattern**. This approach provides better control over real-time features while maintaining Streamlit's rapid development advantages:

```python
# FastAPI bridge between SpacetimeDB and Streamlit
class SpacetimeDBBridge:
    def __init__(self):
        self.spacetime_client = SpacetimeDBAsyncClient(module_bindings)
        self.game_state = {}
        self.event_queue = asyncio.Queue()
    
    async def on_perception_update(self, perception_data):
        # Update local cache and notify Streamlit
        self.game_state[perception_data.entity_id] = perception_data
        await self.event_queue.put(("perception_update", perception_data))

# Streamlit app polls bridge for updates
def render_game_view():
    placeholder = st.empty()
    
    # Get merged reality view
    consensus_reality = st.session_state.bridge.get_consensus_view()
    personal_reality = st.session_state.bridge.get_personal_view()
    
    with placeholder.container():
        # ASCII art header changes based on reality stability
        reality_stability = calculate_reality_stability()
        if reality_stability > 0.8:
            st.code(figlet_format("CONSENSUS", font='standard'))
        else:
            st.code(figlet_format("FLUX", font='weird'))
        
        # Render scene with perception layers
        render_layered_reality(consensus_reality, personal_reality)
```

The Streamlit interface uses `st.chat_message()` for player interactions and `st.empty()` containers for dynamic content updates. Session state bridges the gap between SpacetimeDB's event-driven model and Streamlit's rerun cycle.

## Learning from MUD heritage while innovating

Classic MUDs like **LambdaMOO** demonstrated that player empowerment through building tools creates deep engagement. Modern games can leverage this while adding reality-manipulation mechanics inspired by Carlos Castaneda's concept of the **assemblage point** - the position of perception that determines what reality we experience. Key innovations include:

**Assemblage point mechanics**: Drawing from Castaneda's teachings, each player has an "assemblage point" that can shift through various in-game practices. When multiple players align their assemblage points, they collectively enter alternate reality layers - from heightened awareness to completely alien perceptual worlds.

**Pose-based reality shaping**: Instead of simple chat, players write descriptive actions that literally alter the game world when consensus is reached. The more vivid and agreed-upon a description, the more "real" it becomes - essentially moving the collective assemblage point.

**Sorcery through syntax**: Certain linguistic patterns and "power words" (inspired by don Juan's teachings) can forcibly shift other players' perception, creating gameplay around learning and mastering these reality-altering techniques.

**Collaborative approval through gameplay**: Rather than explicit voting, the game tracks linguistic patterns. When players unconsciously adopt each other's descriptions, those elements solidify into consensus reality.

**Emergent narrative through perception drift**: Past events can retroactively change as collective memory shifts, creating a truly dynamic story that no single author controls - what Castaneda might call "erasing personal history."

## ASCII art and emoji as reality indicators

Visual feedback becomes crucial for indicating reality stability and assemblage point positions. Dynamic ASCII generation reflects the current state of consciousness:

```python
def generate_reality_ascii(entity, consensus_level):
    if consensus_level > 0.8:
        # Stable reality - clear ASCII art
        return image_to_ascii(entity.stable_image, columns=60)
    elif consensus_level > 0.5:
        # Shifting reality - glitched ASCII
        base_ascii = image_to_ascii(entity.stable_image, columns=60)
        return apply_glitch_effect(base_ascii, intensity=0.3)
    else:
        # Unstable reality - abstract patterns
        return generate_noise_ascii(60, 20)

# Assemblage point visualization (inspired by Castaneda's energy body)
def render_assemblage_point_display(player_state):
    ap_display = """
    ╔══════════════════════╗
    ║  ASSEMBLAGE POINT    ║
    ║                      ║
    ║    ⠀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠀⠀  ║
    ║    ⠀⢀⣴⣿⣿⣿⣿⣿⣿⣦⡀⠀  ║
    ║    ⢀⣾⣿⣿{0}⣿⣿⣷⡀  ║
    ║    ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷  ║
    ║    ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿  ║
    ║    ⠈⢿⣿⣿⣿⣿⣿⣿⣿⡿⠁  ║
    ║    ⠀⠀⠙⠿⣿⣿⣿⠿⠋⠀⠀  ║
    ║                      ║
    ║  Position: {1:.2f}, {2:.2f}  ║
    ║  State: {3}         ║
    ╚══════════════════════╝
    """.format(
        get_ap_indicator(player_state.ap_x, player_state.ap_y),
        player_state.ap_x,
        player_state.ap_y,
        get_awareness_state(player_state.ap_y)
    )
    return ap_display

# Emoji as perception indicators
REALITY_EMOJIS = {
    'stable': '🏛️',
    'shifting': '🌊',
    'personal': '👁️',
    'consensus': '👥',
    'hallucination': '🌀',
    'heightened': '✨',
    'dreaming': '🌙',
    'stalking': '🐾'
}

# Awareness states from Castaneda's teachings
def get_awareness_state(ap_y):
    if ap_y < 0.3: return "First Attention"
    elif ap_y < 0.6: return "Second Attention" 
    elif ap_y < 0.8: return "Heightened Awareness"
    else: return "Total Freedom"
```

## MVP implementation roadmap

### Week 1: Core Framework
1. Set up SpacetimeDB module with basic tables (rooms, players, perceptions, assemblage_points)
2. Implement simple movement and description reducers
3. Create Streamlit interface with chat input and ASCII display
4. Establish FastAPI bridge for real-time updates
5. Add basic assemblage point visualization

### Week 2: Reality Mechanics & Castaneda Integration
1. Add perception layer system with consensus tracking
2. Implement assemblage point shifting through "gazing" and "not-doing" commands
3. Create reality strength calculations based on description similarity and AP alignment
4. Add "stopping the world" mechanic that reveals hidden reality layers
5. Implement power words system for influencing other players' perception
6. Create dynamic room connections that shift based on collective belief and awareness levels
7. Add visual indicators (ASCII glitching) for reality stability and AP positions

### Week 3: Advanced Collaborative Features
1. Implement "dreaming together" - synchronized assemblage point journeys
2. Add "recapitulation" command for retroactive reality editing
3. Create stalking mechanics for subtle reality manipulation
4. Implement object metamorphosis when descriptions converge
5. Add "memory drift" where past events change based on collective assemblage point movements
6. Create whisper networks for sub-group reality manipulation ("party of sorcerers")
7. Polish UI with emoji indicators, dynamic ASCII art, and energy body visualizations

## Technical implementation details

The game leverages SpacetimeDB's unique features for innovative mechanics inspired by Castaneda's teachings:

```rust
// Assemblage point shifting through various practices
#[reducer]
pub fn shift_assemblage_point(ctx: &ReducerContext, technique: String, 
                              intensity: f32) {
    let player_id = get_player_id(&ctx.sender);
    let mut ap = get_assemblage_point(ctx, player_id);
    
    match technique.as_str() {
        "gazing" => {
            // Gazing at objects shifts perception gradually
            ap.x_position += (random_f32() - 0.5) * intensity * 0.1;
            ap.stability *= 0.95;  // Destabilizes the point
        },
        "not_doing" => {
            // Breaking routines creates larger shifts
            let shift_vector = calculate_not_doing_vector(&ctx.action_history);
            ap.x_position += shift_vector.x * intensity;
            ap.y_position += shift_vector.y * intensity;
        },
        "stopping_the_world" => {
            // Complete cessation of internal dialogue
            if intensity > 0.8 {
                ap.y_position = 0.7;  // Jump to heightened awareness
                ap.stability = 0.1;   // Very fluid state
                
                // Reveal hidden reality layers
                unlock_perception_layers(ctx, player_id, 3);
            }
        },
        "dreaming" => {
            // Conscious dreaming practice
            ap.x_position = interpolate_to_dream_position(ap.x_position);
            create_dream_double(ctx, player_id);
        },
        "recapitulation" => {
            // Reviewing memories can alter past events
            enable_retroactive_reality_editing(ctx, player_id);
        },
        _ => {}
    }
    
    // Update player's assemblage point
    ctx.db.assemblage_point().update(ap);
    
    // Check for alignment with other players
    check_assemblage_point_alignment(ctx, player_id);
}

// Power words that forcibly shift others' perception
#[reducer]
pub fn speak_power_word(ctx: &ReducerContext, word: String, target_players: Vec<u64>) {
    let speaker_id = get_player_id(&ctx.sender);
    let speaker_power = calculate_personal_power(ctx, speaker_id);
    
    // Certain words from don Juan's vocabulary have special effects
    let shift_power = match word.as_str() {
        "intent" => 0.8,
        "voir" => 0.6,  // Seeing energy directly
        "tonal" | "nagual" => 0.7,
        _ => calculate_word_power(&word)
    };
    
    for target_id in target_players {
        if speaker_power * shift_power > get_resistance(ctx, target_id) {
            force_assemblage_point_shift(ctx, target_id, &word);
        }
    }
}

// Reality shifts when consensus reaches threshold
#[reducer]
pub fn check_reality_shift(ctx: &ReducerContext, entity_id: u64) {
    let consensus = calculate_consensus(ctx, entity_id);
    
    // Players with aligned assemblage points create stronger consensus
    let aligned_players = get_aligned_assemblage_points(ctx);
    let alignment_multiplier = aligned_players.len() as f32 / 10.0 + 1.0;
    
    if consensus.level * alignment_multiplier > REALITY_SHIFT_THRESHOLD {
        // Merge perception layers into new base reality
        merge_perceptions_to_reality(ctx, entity_id, &consensus);
        
        // Retroactively update history ("erasing personal history")
        update_historical_events(ctx, entity_id, &consensus.description);
        
        // Notify all players of reality shift
        broadcast_reality_shift(ctx, entity_id);
    }
}

// Non-Euclidean navigation through shifted awareness
#[reducer]
pub fn navigate_through_awareness(ctx: &ReducerContext, intended_direction: String) {
    let player_id = get_player_id(&ctx.sender);
    let ap = get_assemblage_point(ctx, player_id);
    
    // Higher awareness reveals hidden paths
    let available_paths = ctx.db.room_connection()
        .filter(|conn| conn.awareness_level_required <= ap.y_position)
        .collect();
    
    // In heightened states, intention matters more than direction
    if ap.y_position > 0.6 {
        let best_path = find_path_by_intent(available_paths, &intended_direction);
        move_player_through_intent(ctx, player_id, best_path);
    } else {
        // Normal movement in first attention
        standard_movement(ctx, player_id, &intended_direction);
    }
}
```

## Conclusion

This architecture creates a unique game where reality itself becomes the medium for collaborative storytelling, deeply inspired by Carlos Castaneda's concepts of perception and consciousness. SpacetimeDB's atomic transactions ensure consistency even as multiple players simultaneously reshape the world through their shifting assemblage points, while its real-time subscriptions enable immediate propagation of reality shifts across all connected consciousness.

The integration of Castaneda's teachings transforms what could be a simple collaborative building game into a profound exploration of perception, consensus reality, and the nature of consciousness itself. Players don't just build rooms and objects - they learn to "stop the world," shift their assemblage points, and collectively dream new realities into existence.

The key to success lies in embracing both the technical possibilities of SpacetimeDB and the philosophical depth of the "shared hallucination" concept. By making assemblage point mechanics, power words, and awareness levels core gameplay elements rather than mere narrative devices, the game offers an unprecedented experience where players navigate not just through space but through layers of perception.

This synthesis of modern database technology with ancient wisdom traditions creates a game that is both technically innovative and philosophically rich - a true digital nagual space where the boundaries between individual and collective consciousness blur, and where reality becomes as fluid as our ability to perceive it.