# Core Game Mechanics

## Dice Mechanic
Traditional D&D uses a d20 for most checks, but our system will use a bell curve distribution for more consistent outcomes. We're considering two options:

### 3d6 System (Recommended)
- Roll 3 six-sided dice and sum the results (range: 3-18)
- Target numbers scale from 9 (easy) to 18 (nearly impossible)
- **Advantages:**
  - Natural bell curve with most results falling in the 10-11 range
  - Character skill matters more than lucky rolls
  - Familiar to players of GURPS and other systems
  - Simple to implement and understand

### 2d10 System (Alternative)
- Roll 2 ten-sided dice and sum the results (range: 2-20)
- Target numbers scale from 8 (easy) to 20 (nearly impossible)
- **Advantages:**
  - Slightly wider range than 3d6
  - Still has bell curve properties
  - Maps well to percentile chances

## Attributes
Characters have three primary attributes:

1. **Strength (STR)**: Physical power and combat ability
2. **Dexterity (DEX)**: Agility, reflexes, and fine motor skills
3. **Wisdom (WIS)**: Mental acuity, perception, and magical aptitude

Attributes range from 3 (terrible) to 18 (exceptional) with 10-11 being average human capacity.

## Attribute Checks
When a character attempts an action with uncertain outcome:
- Roll dice (3d6) and add relevant attribute modifier
- Compare to target number or opposing roll
- Modifiers: (Attribute - 10) / 2, rounded down

## Character Classes
Four archetypal classes, each with unique abilities:

1. **Warrior**: Combat specialist with high STR
   - Power Attack, Defend, Whirlwind (advanced)
   - HP Bonus: +2 per level

2. **Wizard**: Arcane spellcaster with high WIS
   - Arcane Missile, Shield, Fireball (advanced)
   - MP Bonus: +2 per level

3. **White Mage**: Healing specialist with balanced attributes
   - Heal, Bless, Mass Heal (advanced)
   - HP/MP Bonus: +1 each per level

4. **Wanderer**: Versatile adventurer with high DEX
   - Quick Shot, Evade, Sneak Attack (advanced)
   - HP/MP Bonus: +1 each per level

## Combat System
Turn-based combat with initiative:

1. **Initiative**: DEX check determines turn order
2. **Actions**: Characters can move and take one action per turn
   - Attack: Roll vs. opponent's defense
   - Cast Spell: Use MP to cast a spell
   - Use Item: Apply an item effect
   - Defend: Gain temporary defense bonus
   - Flee: DEX check to escape combat

3. **Damage**: Determined by weapon/spell plus attribute modifier
   - Physical damage: Based on STR modifier
   - Spell damage: Based on WIS modifier
   
4. **Defense**: 10 + DEX modifier + armor

## Leveling System
- Experience points (XP) gained from combat, crafting, and discoveries
- Level up formula: Current Level × 1000 XP needed
- Each level provides:
  - Increased HP and MP
  - Improved skill effectiveness
  - New skills at levels 3, 6, 9, etc.

## Crafting System (The Forge)
- Components have types (metal, elemental, catalyst, rune, binding)
- Recipes require specific component combinations
- Crafting check: 3d6 + (STR or DEX modifier)
- Quality determined by check result:
  - 9-12: Functional
  - 13-15: Good
  - 16-17: Great
  - 18+: Excellent

## Magic System (The Arcane Matrix)
- Spells constructed from code-like components
- MP cost based on spell complexity
- Casting check: 3d6 + WIS modifier
- Failed checks may have unintended consequences

## Exploration (The Neon Wilderness)
- Grid-based movement through procedurally generated dungeons
- Encounter types: Combat, Treasure, Puzzle, NPC
- Area difficulty scales with character level
- Discovery checks: 3d6 + (DEX or WIS modifier)

## Lore System (The Lore Halls)
- Knowledge collected through NPC interactions and discoveries
- Persuasion check: 3d6 + (STR, DEX, or WIS modifier depending on approach)
- Higher results reveal more detailed or secret information