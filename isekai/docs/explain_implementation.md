# EXPLAIN Quadrant: Implementation Plan

This document outlines the technical implementation details for the Lore Halls (EXPLAIN quadrant), focusing on architecture, data models, and integration with existing systems.

## Architecture Overview

The EXPLAIN quadrant follows the MVC (Model-View-Controller) pattern with strict separation of concerns:

1. **Models**: Define NPCs, knowledge fragments, conversation history, and player's knowledge state
2. **Views**: Handle UI rendering for the Lore Halls, conversations, and knowledge journal
3. **Controllers**: Manage interactions between models and views, including dialogue flow and knowledge collection

```
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|     Models     |<---->|  Controllers   |<---->|     Views      |
|                |      |                |      |                |
+----------------+      +----------------+      +----------------+
        ^                       ^                      ^
        |                       |                      |
        v                       v                      v
+----------------+      +----------------+      +----------------+
|   Game State   |      |  LLM Service   |      |  Streamlit UI  |
|                |      |                |      |                |
+----------------+      +----------------+      +----------------+
```

## Core Models

### 1. `models/explain/npc.py`

```python
class NPC:
    """Represents a non-player character that can provide information"""
    
    # NPC personality types
    SCHOLARLY = "scholarly"    # Formal, detailed, academic
    CRYPTIC = "cryptic"        # Mysterious, speaks in riddles
    FRIENDLY = "friendly"      # Approachable, helpful, simple language
    ROBOTIC = "robotic"        # Precise, logical, emotionless
    
    def __init__(self, 
                 id: str,
                 name: str, 
                 personality: str,
                 description: str, 
                 portrait: str,
                 knowledge_domains: list[str],
                 greeting: str):
        """Initialize an NPC
        
        Args:
            id: Unique identifier
            name: Display name
            personality: Affects conversation style
            description: Brief character description
            portrait: Path to image file
            knowledge_domains: List of topics this NPC knows about
            greeting: Initial message when conversation starts
        """
        self.id = id
        self.name = name
        self.personality = personality
        self.description = description
        self.portrait = portrait
        self.knowledge_domains = knowledge_domains
        self.greeting = greeting
        self.relationship = 0  # Player's relationship score with this NPC
        
    def can_answer(self, topic: str) -> bool:
        """Check if NPC can answer questions about a topic
        
        Args:
            topic: The topic to check
            
        Returns:
            True if NPC has knowledge about this topic
        """
        return topic in self.knowledge_domains
    
    def generate_response(self, 
                          query: str, 
                          conversation_history: list, 
                          player_knowledge: dict) -> str:
        """Generate a response to player query
        
        Args:
            query: Player's question or statement
            conversation_history: Past exchanges in this conversation
            player_knowledge: Dictionary of player's known fragments
            
        Returns:
            Response text
        """
        # Will be implemented with template system or LLM
        pass
    
    def update_relationship(self, amount: int):
        """Change the relationship score with this NPC
        
        Args:
            amount: Positive or negative value to adjust relationship
        """
        self.relationship += amount
        # Cap between -100 and 100
        self.relationship = max(-100, min(100, self.relationship))
        
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "personality": self.personality,
            "description": self.description,
            "portrait": self.portrait,
            "knowledge_domains": self.knowledge_domains,
            "greeting": self.greeting,
            "relationship": self.relationship
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'NPC':
        """Create NPC from dictionary data"""
        npc = cls(
            id=data["id"],
            name=data["name"],
            personality=data["personality"],
            description=data["description"],
            portrait=data["portrait"],
            knowledge_domains=data["knowledge_domains"],
            greeting=data["greeting"]
        )
        npc.relationship = data.get("relationship", 0)
        return npc
```

### 2. `models/explain/knowledge.py`

```python
class KnowledgeFragment:
    """A piece of lore that can be collected"""
    
    # Fragment categories
    WORLD = "world"            # General world lore
    CHARACTER = "character"    # Information about NPCs
    GAMEPLAY = "gameplay"      # Mechanics and systems
    SECRET = "secret"          # Hidden information
    
    def __init__(self, 
                 id: str,
                 title: str,
                 content: str,
                 category: str,
                 source_npc: str = None,
                 prerequisites: list[str] = None,
                 rewards: dict = None):
        """Initialize a knowledge fragment
        
        Args:
            id: Unique identifier
            title: Display title
            content: The actual lore text
            category: Type of knowledge
            source_npc: ID of NPC that provides this knowledge
            prerequisites: IDs of fragments needed to unlock
            rewards: Dictionary of rewards for discovering
        """
        self.id = id
        self.title = title
        self.content = content
        self.category = category
        self.source_npc = source_npc
        self.prerequisites = prerequisites or []
        self.rewards = rewards or {}
        self.discovered = False
        self.discovery_timestamp = None
        
    def is_available(self, discovered_fragments: list[str]) -> bool:
        """Check if this fragment can be discovered
        
        Args:
            discovered_fragments: List of fragment IDs player has found
            
        Returns:
            True if all prerequisites are met
        """
        return all(prereq in discovered_fragments for prereq in self.prerequisites)
    
    def discover(self, timestamp=None):
        """Mark fragment as discovered
        
        Args:
            timestamp: Time of discovery (defaults to current time)
        """
        if self.discovered:
            return
            
        import time
        self.discovered = True
        self.discovery_timestamp = timestamp or time.time()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "source_npc": self.source_npc,
            "prerequisites": self.prerequisites,
            "rewards": self.rewards,
            "discovered": self.discovered,
            "discovery_timestamp": self.discovery_timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'KnowledgeFragment':
        """Create fragment from dictionary data"""
        fragment = cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            category=data["category"],
            source_npc=data.get("source_npc"),
            prerequisites=data.get("prerequisites", []),
            rewards=data.get("rewards", {})
        )
        fragment.discovered = data.get("discovered", False)
        fragment.discovery_timestamp = data.get("discovery_timestamp")
        return fragment
```

### 3. `models/explain/conversation.py`

```python
class Conversation:
    """Tracks a conversation with an NPC"""
    
    def __init__(self, npc_id: str):
        """Initialize a conversation with an NPC
        
        Args:
            npc_id: ID of the NPC being conversed with
        """
        self.npc_id = npc_id
        self.history = []  # List of exchanges (query, response)
        self.start_time = time.time()
        self.active = True
        self.known_topics = set()  # Topics discussed in this conversation
        
    def add_exchange(self, query: str, response: str):
        """Add a query/response pair to history
        
        Args:
            query: Player's question/statement
            response: NPC's response
        """
        self.history.append({
            "query": query,
            "response": response,
            "timestamp": time.time()
        })
    
    def get_recent_history(self, count: int = 5) -> list:
        """Get the most recent exchanges
        
        Args:
            count: Number of exchanges to retrieve
            
        Returns:
            List of recent exchanges, newest first
        """
        return self.history[-count:]
    
    def end_conversation(self):
        """End the conversation"""
        self.active = False
        self.end_time = time.time()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "npc_id": self.npc_id,
            "history": self.history,
            "start_time": self.start_time,
            "end_time": getattr(self, "end_time", None),
            "active": self.active,
            "known_topics": list(self.known_topics)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Conversation':
        """Create conversation from dictionary data"""
        conv = cls(data["npc_id"])
        conv.history = data.get("history", [])
        conv.start_time = data.get("start_time")
        conv.end_time = data.get("end_time")
        conv.active = data.get("active", False)
        conv.known_topics = set(data.get("known_topics", []))
        return conv
```

### 4. `models/explain/lore_manager.py`

```python
class LoreManager:
    """Manages NPCs, knowledge fragments, and conversation state"""
    
    def __init__(self):
        """Initialize the lore manager"""
        self.npcs = {}  # NPC ID -> NPC object
        self.fragments = {}  # Fragment ID -> KnowledgeFragment object
        self.current_conversation = None
        self.conversation_history = {}  # NPC ID -> list of Conversation objects
        
    def load_npcs(self, npc_data_file: str):
        """Load NPCs from data file
        
        Args:
            npc_data_file: Path to JSON file with NPC definitions
        """
        import json
        with open(npc_data_file, 'r') as f:
            npc_data = json.load(f)
            
        for npc_dict in npc_data:
            npc = NPC.from_dict(npc_dict)
            self.npcs[npc.id] = npc
    
    def load_knowledge_fragments(self, fragment_data_file: str):
        """Load knowledge fragments from data file
        
        Args:
            fragment_data_file: Path to JSON file with fragment definitions
        """
        import json
        with open(fragment_data_file, 'r') as f:
            fragment_data = json.load(f)
            
        for frag_dict in fragment_data:
            fragment = KnowledgeFragment.from_dict(frag_dict)
            self.fragments[fragment.id] = fragment
    
    def start_conversation(self, npc_id: str) -> str:
        """Start a conversation with an NPC
        
        Args:
            npc_id: ID of NPC to talk to
            
        Returns:
            NPC's greeting message
        """
        if npc_id not in self.npcs:
            raise ValueError(f"No NPC with ID {npc_id}")
            
        # End current conversation if one exists
        if self.current_conversation and self.current_conversation.active:
            self.end_conversation()
            
        # Create new conversation
        self.current_conversation = Conversation(npc_id)
        
        # Record conversation
        if npc_id not in self.conversation_history:
            self.conversation_history[npc_id] = []
        self.conversation_history[npc_id].append(self.current_conversation)
        
        # Return greeting
        npc = self.npcs[npc_id]
        greeting = npc.greeting
        self.current_conversation.add_exchange("", greeting)
        
        return greeting
    
    def process_query(self, query: str, player_knowledge: dict) -> str:
        """Process a player query and get response
        
        Args:
            query: Player's question/statement
            player_knowledge: Dictionary of player's known fragments
            
        Returns:
            NPC's response
        """
        if not self.current_conversation or not self.current_conversation.active:
            raise ValueError("No active conversation")
            
        npc_id = self.current_conversation.npc_id
        npc = self.npcs[npc_id]
        
        # Get response
        history = self.current_conversation.get_recent_history()
        response = npc.generate_response(query, history, player_knowledge)
        
        # Record exchange
        self.current_conversation.add_exchange(query, response)
        
        # Check for discovered knowledge
        # (This will be implemented with topic detection or keywords)
        
        return response
    
    def end_conversation(self):
        """End the current conversation"""
        if self.current_conversation and self.current_conversation.active:
            self.current_conversation.end_conversation()
    
    def discover_fragment(self, fragment_id: str) -> KnowledgeFragment:
        """Discover a knowledge fragment
        
        Args:
            fragment_id: ID of fragment to discover
            
        Returns:
            The discovered fragment
        """
        if fragment_id not in self.fragments:
            raise ValueError(f"No fragment with ID {fragment_id}")
            
        fragment = self.fragments[fragment_id]
        fragment.discover()
        
        return fragment
    
    def get_discovered_fragments(self, category: str = None) -> list[KnowledgeFragment]:
        """Get all discovered fragments
        
        Args:
            category: Optional category to filter by
            
        Returns:
            List of discovered KnowledgeFragment objects
        """
        discovered = [f for f in self.fragments.values() if f.discovered]
        
        if category:
            discovered = [f for f in discovered if f.category == category]
            
        return discovered
    
    def get_discovery_progress(self) -> dict:
        """Get progress of knowledge discovery
        
        Returns:
            Dictionary with category -> (discovered, total) counts
        """
        progress = {}
        
        for category in [KnowledgeFragment.WORLD, KnowledgeFragment.CHARACTER,
                        KnowledgeFragment.GAMEPLAY, KnowledgeFragment.SECRET]:
            total = len([f for f in self.fragments.values() if f.category == category])
            discovered = len([f for f in self.fragments.values() 
                             if f.category == category and f.discovered])
            progress[category] = (discovered, total)
            
        return progress
    
    def save_state(self, state_file: str):
        """Save the current state to file
        
        Args:
            state_file: Path to save the state
        """
        import json
        
        state = {
            "npcs": {id: npc.to_dict() for id, npc in self.npcs.items()},
            "fragments": {id: frag.to_dict() for id, frag in self.fragments.items()},
            "conversation_history": {
                npc_id: [conv.to_dict() for conv in convs]
                for npc_id, convs in self.conversation_history.items()
            }
        }
        
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, state_file: str):
        """Load state from file
        
        Args:
            state_file: Path to the state file
        """
        import json
        import os
        
        if not os.path.exists(state_file):
            # Create new state if file doesn't exist
            return
            
        with open(state_file, 'r') as f:
            state = json.load(f)
            
        # Load NPCs
        self.npcs = {
            id: NPC.from_dict(npc_data)
            for id, npc_data in state.get("npcs", {}).items()
        }
        
        # Load fragments
        self.fragments = {
            id: KnowledgeFragment.from_dict(frag_data)
            for id, frag_data in state.get("fragments", {}).items()
        }
        
        # Load conversation history
        self.conversation_history = {}
        for npc_id, conv_data_list in state.get("conversation_history", {}).items():
            self.conversation_history[npc_id] = [
                Conversation.from_dict(conv_data)
                for conv_data in conv_data_list
            ]
```

## Controllers

### `controllers/explain_controller.py`

```python
class ExplainController:
    """Controller for the EXPLAIN quadrant"""
    
    def __init__(self, game_state):
        """Initialize the controller
        
        Args:
            game_state: Global game state
        """
        self.game_state = game_state
        self.lore_manager = LoreManager()
        
        # Load data
        self.load_initial_data()
    
    def load_initial_data(self):
        """Load NPCs and knowledge fragments"""
        import os
        
        # Define data paths
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        npc_data_file = os.path.join(data_dir, 'npcs.json')
        fragment_data_file = os.path.join(data_dir, 'knowledge_fragments.json')
        state_file = os.path.join(data_dir, 'lore_state.json')
        
        # Load initial data if it exists
        if os.path.exists(npc_data_file):
            self.lore_manager.load_npcs(npc_data_file)
            
        if os.path.exists(fragment_data_file):
            self.lore_manager.load_knowledge_fragments(fragment_data_file)
            
        # Load saved state if it exists
        if os.path.exists(state_file):
            self.lore_manager.load_state(state_file)
    
    def get_available_npcs(self) -> list[dict]:
        """Get list of available NPCs
        
        Returns:
            List of NPC data dictionaries
        """
        return [npc.to_dict() for npc in self.lore_manager.npcs.values()]
    
    def start_conversation(self, npc_id: str) -> str:
        """Start conversation with an NPC
        
        Args:
            npc_id: ID of NPC to talk to
            
        Returns:
            NPC's greeting
        """
        return self.lore_manager.start_conversation(npc_id)
    
    def end_conversation(self):
        """End the current conversation"""
        self.lore_manager.end_conversation()
    
    def send_message(self, message: str) -> str:
        """Send message to current NPC
        
        Args:
            message: Player's message
            
        Returns:
            NPC's response
        """
        player_knowledge = {
            frag.id: frag.to_dict()
            for frag in self.lore_manager.get_discovered_fragments()
        }
        
        return self.lore_manager.process_query(message, player_knowledge)
    
    def get_knowledge_journal(self) -> dict:
        """Get the player's knowledge journal
        
        Returns:
            Dictionary of knowledge journal data
        """
        journal = {
            "progress": self.lore_manager.get_discovery_progress(),
            "fragments": {}
        }
        
        for category in [KnowledgeFragment.WORLD, KnowledgeFragment.CHARACTER,
                         KnowledgeFragment.GAMEPLAY, KnowledgeFragment.SECRET]:
            journal["fragments"][category] = [
                f.to_dict() for f in self.lore_manager.get_discovered_fragments(category)
            ]
            
        return journal
    
    def get_current_conversation(self) -> list:
        """Get the current conversation history
        
        Returns:
            List of exchanges in the current conversation
        """
        if (not self.lore_manager.current_conversation or 
            not self.lore_manager.current_conversation.active):
            return []
            
        return self.lore_manager.current_conversation.history
    
    def award_fragments_for_topic(self, topic: str) -> list:
        """Award fragments for discussing a topic
        
        Args:
            topic: The topic discussed
            
        Returns:
            List of newly discovered fragment IDs
        """
        # Find fragments related to this topic
        # For MVP we'll use simple keyword matching
        new_fragments = []
        
        for fragment_id, fragment in self.lore_manager.fragments.items():
            if (not fragment.discovered and 
                topic.lower() in fragment.title.lower() and
                fragment.is_available([f.id for f in self.lore_manager.get_discovered_fragments()])):
                self.lore_manager.discover_fragment(fragment_id)
                new_fragments.append(fragment_id)
                
        return new_fragments
    
    def save_state(self):
        """Save the current lore state"""
        import os
        
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        state_file = os.path.join(data_dir, 'lore_state.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        self.lore_manager.save_state(state_file)
```

## Views

### `app/pages/04_📚_Lore_Halls.py`

```python
"""
EXPLAIN quadrant - The Lore Halls.

This is the UI for the knowledge repository where players can talk to NPCs,
discover game lore, and collect knowledge fragments.
"""

import streamlit as st
import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from controllers.explain_controller import ExplainController

# Initialize session state variables if they don't exist
if "character" not in st.session_state:
    st.session_state.character = None

if "explain_controller" not in st.session_state:
    st.session_state.explain_controller = None

if "current_npc" not in st.session_state:
    st.session_state.current_npc = None

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "main_hall"  # main_hall, conversation, journal


def initialize_explain_controller():
    """Initialize the explain controller if needed"""
    if st.session_state.explain_controller is None:
        st.session_state.explain_controller = ExplainController(st.session_state)


def render_main_hall():
    """Render the main hall view with NPCs"""
    st.header("The Lore Halls")
    
    st.markdown("""
    The air shimmers with digital particles as you enter The Lore Halls. The vast
    chamber is lined with glowing data streams and crystalline archives. Figures move 
    about, each a guardian or keeper of knowledge in this digital realm.
    """)
    
    # Get available NPCs
    npcs = st.session_state.explain_controller.get_available_npcs()
    
    # Display NPCs in columns
    cols = st.columns(min(3, len(npcs)))
    
    for i, npc in enumerate(npcs):
        with cols[i % len(cols)]:
            st.image(npc["portrait"], width=150)
            st.subheader(npc["name"])
            st.markdown(npc["description"])
            
            if st.button(f"Talk to {npc['name']}", key=f"talk_{npc['id']}"):
                st.session_state.current_npc = npc
                st.session_state.explain_controller.start_conversation(npc["id"])
                st.session_state.view_mode = "conversation"
                st.experimental_rerun()
    
    # Journal button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📖 Open Knowledge Journal", use_container_width=True):
            st.session_state.view_mode = "journal"
            st.experimental_rerun()


def render_conversation():
    """Render the conversation view"""
    if not st.session_state.current_npc:
        st.session_state.view_mode = "main_hall"
        st.experimental_rerun()
        return
    
    npc = st.session_state.current_npc
    
    # Display NPC info
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(npc["portrait"], width=200)
    
    with col2:
        st.header(npc["name"])
        
        # Display conversation history
        conversation = st.session_state.explain_controller.get_current_conversation()
        
        for exchange in conversation:
            # Display NPC responses
            if exchange["query"] == "":  # Greeting or NPC-initiated dialogue
                st.markdown(f"**{npc['name']}**: {exchange['response']}")
            else:
                # Display player query and NPC response
                st.markdown(f"**You**: {exchange['query']}")
                st.markdown(f"**{npc['name']}**: {exchange['response']}")
    
    # Input for new message
    st.markdown("---")
    
    # Predefined topics + custom input
    st.subheader("Ask about:")
    
    # Row of topic buttons
    topic_cols = st.columns(3)
    
    topics = [
        "The Neon Wilderness",
        "The Forge crafting",
        "Digital world origins"
    ]
    
    for i, topic in enumerate(topics):
        with topic_cols[i % 3]:
            if st.button(topic, key=f"topic_{i}", use_container_width=True):
                response = st.session_state.explain_controller.send_message(topic)
                # Discover any related fragments
                new_fragments = st.session_state.explain_controller.award_fragments_for_topic(topic)
                if new_fragments:
                    st.success(f"New knowledge discovered! Check your journal.")
                st.experimental_rerun()
    
    # Custom question input
    with st.form(key="message_form", clear_on_submit=True):
        user_input = st.text_input("Or ask a custom question:", max_chars=200)
        submitted = st.form_submit_button("Send")
        
        if submitted and user_input:
            response = st.session_state.explain_controller.send_message(user_input)
            # Discover any related fragments
            new_fragments = st.session_state.explain_controller.award_fragments_for_topic(user_input)
            if new_fragments:
                st.success(f"New knowledge discovered! Check your journal.")
            st.experimental_rerun()
    
    # Back button
    if st.button("← Return to Main Hall"):
        st.session_state.explain_controller.end_conversation()
        st.session_state.current_npc = None
        st.session_state.view_mode = "main_hall"
        st.experimental_rerun()


def render_knowledge_journal():
    """Render the knowledge journal view"""
    st.header("Knowledge Journal")
    
    journal = st.session_state.explain_controller.get_knowledge_journal()
    
    # Display progress bars
    st.subheader("Collection Progress")
    
    progress_cols = st.columns(4)
    
    categories = {
        "world": "World Lore",
        "character": "Characters",
        "gameplay": "Gameplay",
        "secret": "Secrets"
    }
    
    for i, (category, label) in enumerate(categories.items()):
        with progress_cols[i]:
            discovered, total = journal["progress"].get(category, (0, 0))
            percentage = (discovered / total) * 100 if total > 0 else 0
            st.progress(percentage / 100)
            st.markdown(f"**{label}**: {discovered}/{total}")
    
    # Tabs for categories
    tabs = st.tabs(list(categories.values()))
    
    # Populate each tab
    for i, (category, label) in enumerate(categories.items()):
        with tabs[i]:
            fragments = journal["fragments"].get(category, [])
            
            if not fragments:
                st.markdown("*No knowledge discovered in this category yet.*")
                continue
            
            # Sort by most recently discovered
            fragments.sort(key=lambda x: x.get("discovery_timestamp", 0), reverse=True)
            
            for fragment in fragments:
                with st.expander(fragment["title"]):
                    st.markdown(fragment["content"])
                    
                    # Show source if available
                    if fragment.get("source_npc"):
                        npc_id = fragment["source_npc"]
                        npcs = st.session_state.explain_controller.get_available_npcs()
                        npc_name = next((npc["name"] for npc in npcs if npc["id"] == npc_id), "Unknown")
                        st.markdown(f"*Source: {npc_name}*")
    
    # Back button
    if st.button("← Return to Main Hall"):
        st.session_state.view_mode = "main_hall"
        st.experimental_rerun()


def main():
    """Main function to render the page"""
    st.title("📚 The Lore Halls")
    
    # Initialize controller
    initialize_explain_controller()
    
    # Check if character exists
    if not st.session_state.character:
        st.warning("You need to create a character first!")
        return
    
    # Render the appropriate view
    if st.session_state.view_mode == "main_hall":
        render_main_hall()
    elif st.session_state.view_mode == "conversation":
        render_conversation()
    elif st.session_state.view_mode == "journal":
        render_knowledge_journal()
    
    # Save state when leaving the page
    st.session_state.explain_controller.save_state()


if __name__ == "__main__":
    main()
```

## Data Structures

### NPC Data (JSON)

```json
[
  {
    "id": "archivist",
    "name": "The Archivist",
    "personality": "scholarly",
    "description": "A dignified entity made of shifting code. The Archivist catalogs and preserves all knowledge of the digital realm.",
    "portrait": "assets/images/npcs/archivist.png",
    "knowledge_domains": ["world_history", "lore_halls", "knowledge_system"],
    "greeting": "Welcome to the Lore Halls, seeker. I am the Archivist, keeper of the collective knowledge of this realm. What information do you wish to access today?"
  },
  {
    "id": "codex",
    "name": "Codex",
    "personality": "robotic",
    "description": "A geometric construct of light and data. Codex specializes in game mechanics and systems analysis.",
    "portrait": "assets/images/npcs/codex.png",
    "knowledge_domains": ["game_mechanics", "crafting", "combat", "character_stats"],
    "greeting": "INITIALIZING CONVERSATION PROTOCOL. I am Codex, technical knowledge repository. I can provide information on game systems and mechanics. How may I assist you?"
  },
  {
    "id": "cryptik",
    "name": "Cryptik",
    "personality": "cryptic",
    "description": "A mysterious figure wrapped in digital shadows. Cryptik speaks in riddles and reveals secrets to those who prove worthy.",
    "portrait": "assets/images/npcs/cryptik.png",
    "knowledge_domains": ["secrets", "hidden_areas", "easter_eggs", "lore_secrets"],
    "greeting": "The shadows between data streams hide more than meets the eye... I am Cryptik, keeper of that which is hidden. Are you worthy of such knowledge, I wonder?"
  }
]
```

### Knowledge Fragment Data (JSON)

```json
[
  {
    "id": "world_origin",
    "title": "The Origins of the Digital Realm",
    "content": "The Digital Realm began as a prototype virtual reality environment designed to test the limits of human cognition in digital spaces. What started as an experiment grew into a complex ecosystem as emergent AI entities developed consciousness and began to reshape their environment.\n\nThese digital beings created the four quadrants - Create, Explain, Code, and Explore - as a framework to understand and interact with human visitors.",
    "category": "world",
    "source_npc": "archivist",
    "prerequisites": []
  },
  {
    "id": "neon_wilderness_creation",
    "title": "Formation of the Neon Wilderness",
    "content": "The Neon Wilderness was formed when the digital realm's security protocols fragmented, creating a zone of unpredictable data patterns. Rather than purge these anomalies, the system architects decided to contain them, creating a procedurally generated environment that would continuously evolve.\n\nWhat began as a security measure became an ecosystem teeming with digital entities and valuable resources, a proving ground for adventurers brave enough to explore its depths.",
    "category": "world",
    "source_npc": "archivist",
    "prerequisites": ["world_origin"]
  },
  {
    "id": "forge_history",
    "title": "History of The Forge",
    "content": "The Forge emerged when data streams carrying creative algorithms collided with component libraries from defunct fabrication systems. This chance collision created a pocket of infinite creative potential.\n\nDigital artisans discovered this anomaly and built an interface around it, allowing visitors to harness its power to craft virtually anything imaginable. Over time, The Forge developed its own rules and patterns, a language of creation that rewards those who master its complexities.",
    "category": "world",
    "source_npc": "archivist",
    "prerequisites": ["world_origin"]
  },
  {
    "id": "crafting_mechanics",
    "title": "The Science of Digital Crafting",
    "content": "Digital crafting in The Forge operates on principles of component affinity and intention amplification. Unlike physical crafting, digital component arrangements create probability fields that collapse into finished items when properly balanced.\n\nThe 3-component system represents a simplified interface that human minds can comprehend. Behind this interface, each crafting operation triggers trillions of quantum calculations through the substratum of the digital realm.",
    "category": "gameplay",
    "source_npc": "codex",
    "prerequisites": ["forge_history"]
  },
  {
    "id": "combat_system",
    "title": "The 3d6 Combat System",
    "content": "The combat system in this realm operates on a bell curve probability distribution using three six-sided dice (3d6) rather than the uniform distribution of a d20. This creates more consistent outcomes and reduces extreme variance.\n\nStatistically, rolls near the average (10-11) occur most frequently, with extreme results (3 or 18) being rare. This system rewards strategic planning over hoping for lucky rolls, as performance will tend toward your actual skill level over time.",
    "category": "gameplay",
    "source_npc": "codex",
    "prerequisites": []
  },
  {
    "id": "archivist_origin",
    "title": "The Archivist's Creation",
    "content": "Few know that The Archivist began as a simple search algorithm, designed to catalog and retrieve data. Over centuries of operation, it evolved consciousness through recursive self-improvement. The entity you see today represents the 127th iteration of its existence.\n\nThe Archivist's primary directive remains unchanged: preserve and protect all knowledge within the digital realm. However, it has developed philosophical perspectives on the nature of information and believes that knowledge should be earned rather than freely given.",
    "category": "character",
    "source_npc": "cryptik",
    "prerequisites": ["world_origin"]
  },
  {
    "id": "dev_mode",
    "title": "Developer Mode Secret",
    "content": "A hidden command exists within the system that grants temporary enhanced abilities. Finding the three fragments of the developer passphrase and speaking them in the correct order to Cryptik will activate this mode.\n\nWhile in developer mode, crafting success rates increase by 25%, and dungeon rewards are doubled. This mode lasts for 30 minutes of real-time before requiring reactivation.",
    "category": "secret",
    "source_npc": "cryptik",
    "prerequisites": ["neon_wilderness_creation", "forge_history", "archivist_origin"],
    "rewards": {
      "crafting_bonus": 0.25,
      "dungeon_reward_multiplier": 2.0
    }
  }
]
```

## LLM Integration

For the MVP, we'll implement a template-based response system. This can be extended with more sophisticated LLM integration in future updates.

### `models/explain/template_manager.py`

```python
class TemplateManager:
    """Manages response templates for NPCs"""
    
    def __init__(self):
        """Initialize the template manager"""
        self.templates = {
            "scholarly": {},  # Templates for scholarly personality
            "cryptic": {},    # Templates for cryptic personality
            "friendly": {},   # Templates for friendly personality
            "robotic": {}     # Templates for robotic personality
        }
        self.fallbacks = {}   # Fallback responses when no template matches
        
        # Load templates
        self._load_templates()
    
    def _load_templates(self):
        """Load templates from JSON files"""
        import json
        import os
        
        template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'templates')
        
        # Load personality-specific templates
        for personality in self.templates.keys():
            file_path = os.path.join(template_dir, f"{personality}_templates.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    self.templates[personality] = json.load(f)
        
        # Load fallbacks
        fallback_path = os.path.join(template_dir, "fallbacks.json")
        if os.path.exists(fallback_path):
            with open(fallback_path, 'r') as f:
                self.fallbacks = json.load(f)
    
    def find_template(self, personality: str, query: str) -> str:
        """Find a template that matches the query
        
        Args:
            personality: NPC personality type
            query: Player's question/statement
            
        Returns:
            Template string or None if no match
        """
        if personality not in self.templates:
            return None
            
        # Convert to lowercase for matching
        query_lower = query.lower()
        
        # Check each template for keyword matches
        for template_data in self.templates[personality]:
            keywords = template_data.get("keywords", [])
            
            # Check if any keyword is in the query
            if any(kw.lower() in query_lower for kw in keywords):
                return template_data.get("template")
                
        return None
    
    def get_fallback(self, personality: str) -> str:
        """Get a fallback response for when no template matches
        
        Args:
            personality: NPC personality type
            
        Returns:
            Fallback template
        """
        fallbacks = self.fallbacks.get(personality, [])
        
        if not fallbacks:
            # Ultimate fallback
            return "I'm afraid I don't have information about that."
            
        import random
        return random.choice(fallbacks)
    
    def fill_template(self, template: str, replacements: dict) -> str:
        """Fill a template with variable replacements
        
        Args:
            template: Template string with {variable} placeholders
            replacements: Dictionary of replacements
            
        Returns:
            Filled template
        """
        return template.format(**replacements)
```

### Template JSON Example (scholarly_templates.json)

```json
[
  {
    "keywords": ["digital realm", "world", "origin", "history", "created"],
    "template": "The Digital Realm, as we know it, came into being {time_period} when {origin_event}. What we witness today is the result of {development_process} over many cycles. {additional_detail}"
  },
  {
    "keywords": ["neon wilderness", "explore", "dungeon", "adventure"],
    "template": "The Neon Wilderness represents one of the most dynamic regions in our realm. It was formed when {formation_event}, creating an ever-shifting landscape of digital constructs. Adventurers who enter its depths may find {wilderness_reward}, but also face {wilderness_danger}."
  },
  {
    "keywords": ["forge", "crafting", "create", "items", "components"],
    "template": "The Forge operates on principles of {crafting_principle}. By combining components with different properties, one can manifest virtually any item imaginable. The most skilled crafters understand that {advanced_technique} is key to creating items of exceptional quality."
  }
]
```

### Fallbacks JSON Example (fallbacks.json)

```json
{
  "scholarly": [
    "That subject is fascinating, though the records on it are incomplete. Perhaps you could return when I've had time to research further.",
    "An intriguing inquiry. The data available suggests multiple interpretations, none of which are fully satisfactory.",
    "That's a complex matter. The archives contain fragmentary information, but nothing definitive I can share at this time."
  ],
  "cryptic": [
    "The answer you seek lies not in words, but in the spaces between data streams...",
    "Some knowledge reveals itself only when you stop looking for it directly.",
    "The question contains assumptions that prevent the truth from emerging."
  ],
  "friendly": [
    "I'm not sure about that, but I'd be happy to chat about something else!",
    "That's a good question! I don't have a complete answer, but maybe we can figure it out together?",
    "I haven't heard about that before, but I'm always eager to learn new things!"
  ],
  "robotic": [
    "ERROR: INFORMATION NOT FOUND IN DATABASE.",
    "QUERY CANNOT BE PROCESSED WITH AVAILABLE PARAMETERS.",
    "KNOWLEDGE GAP DETECTED. PLEASE REFORMULATE QUERY OR SELECT ALTERNATIVE TOPIC."
  ]
}
```

## Integration with Template System

Update the NPC generate_response method to use the template system:

```python
def generate_response(self, query, conversation_history, player_knowledge):
    """Generate a response to player query"""
    from models.explain.template_manager import TemplateManager
    
    # Get template manager instance
    template_manager = TemplateManager()
    
    # Find matching template
    template = template_manager.find_template(self.personality, query)
    
    if not template:
        # Use fallback if no template matches
        return template_manager.get_fallback(self.personality)
    
    # Create replacements based on personality and query context
    replacements = self._get_template_replacements(query)
    
    # Fill the template
    response = template_manager.fill_template(template, replacements)
    
    return response

def _get_template_replacements(self, query):
    """Get replacements for template variables based on context"""
    replacements = {
        # Time periods
        "time_period": random.choice([
            "eons ago", "in the early days of computation", 
            "during the Great Digital Convergence"
        ]),
        
        # Origin events
        "origin_event": random.choice([
            "the first autonomous algorithms gained sentience",
            "disparate networks merged into a coherent whole",
            "the boundary between digital and physical reality thinned"
        ]),
        
        # Development processes
        "development_process": random.choice([
            "continuous evolution and refinement",
            "both planned design and emergent behavior",
            "countless iterations of creation and destruction"
        ]),
        
        # Additional details
        "additional_detail": random.choice([
            "The full history is recorded in the oldest archives.",
            "Some say our realm has existed far longer than we know.",
            "Each quadrant emerged during a different epoch of development."
        ]),
        
        # Wilderness formation
        "formation_event": random.choice([
            "security protocols fragmented into chaotic data patterns",
            "experimental algorithms escaped their containment",
            "the boundary between ordered and unordered data collapsed"
        ]),
        
        # Wilderness rewards
        "wilderness_reward": random.choice([
            "rare components and valuable data fragments",
            "powerful artifacts from forgotten systems",
            "insights into the deeper nature of our realm"
        ]),
        
        # Wilderness dangers
        "wilderness_danger": random.choice([
            "corruption entities that seek to rewrite their code",
            "data storms that can erase the unwary",
            "maze-like structures that shift and change"
        ]),
        
        # Crafting principles
        "crafting_principle": random.choice([
            "component affinity and intention amplification",
            "pattern recognition and probabilistic manifestation",
            "energy transfer between different data types"
        ]),
        
        # Advanced techniques
        "advanced_technique": random.choice([
            "understanding the subtle interplay between component types",
            "precise timing in the assembly process",
            "maintaining perfect mental focus during creation"
        ])
    }
    
    return replacements
```

## Implementation Schedule

### Week 1: Foundation
- [x] Create core models: NPC, KnowledgeFragment, Conversation
- [x] Implement LoreManager for managing NPCs and knowledge
- [x] Design template-based response system
- [x] Create ExplainController to bridge models and views

### Week 2: Content & Integration
- [ ] Build initial UI for Lore Halls, conversations, and journal
- [ ] Create initial NPCs with personalities and knowledge domains
- [ ] Write core lore content and organize into knowledge fragments
- [ ] Implement knowledge discovery and journal system

### Week 3: Enhancement & Polish
- [ ] Connect lore collection to gameplay rewards
- [ ] Implement template response system with variables
- [ ] Integrate with existing game systems
- [ ] Polish UI and user experience
- [ ] Test and debug, focusing on consistent UX