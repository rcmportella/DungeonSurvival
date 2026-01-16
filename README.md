# DungeonSurvival - Roguelike Game Framework

A text-based roguelike dungeon crawler using the OGL D20 game system.

## Overview

DungeonSurvival is a roguelike game where you control a party of adventurers exploring procedurally generated dungeons or predefined maps read through a JSON file. The game features turn-based combat, character progression, and treasure hunting.

## Game Features

### Map Symbols
- `#` - Walls (impassable)
- `.` - Floor (walkable)
- `1` - Party position (exploration mode)
- `1-6` - Individual party members (combat mode)
- `A-Z` - Monsters (letter represents monster type)
- `|` or `-` - Doors
- `$` - Treasure chests
- `<` - Stairs down to deeper levels
- `>` - Stairs up to previous levels

### Controls

#### Exploration Mode
- **Arrow Keys / WASD** - Move the party
- **D** - Descend stairs (when standing on `<`)
- **U** - Ascend stairs (when standing on `>`)
- **I** - Open inventory (not yet implemented)
- **C** - View character sheet (not yet implemented)
- **Q** - Quit game

#### Combat Mode
- **A** - Attack with equipped weapon
- **S** - Cast spell (partial implementation)
- **I** - Use item (not yet implemented)
- **F** - Flee from combat
- **Q** - Quit game

### Numpad Support
You can also use the numpad for movement including diagonals:
```
7 8 9
4 . 6
1 2 3
```

## File Structure

### Core Game Files

#### `main.py`
- Main entry point for the game
- Game loop implementation
- Rendering and input processing
- Creates default party and initializes game

#### `game_state.py`
- Manages overall game state
- Handles game modes (exploration, combat, game over, etc.)
- Turn management
- Message logging
- Dungeon level progression

#### `dungeon_map.py`
- Procedural dungeon generation
- Room and corridor creation
- Monster and treasure placement
- Map rendering
- Tile management

#### `party.py`
- Manages the party of player characters
- Gold and experience distribution
- Party positioning
- Rest and healing management

#### `input_handler.py`
- Cross-platform keyboard input handling
- Arrow key detection
- Movement key parsing
- Context manager for terminal raw mode

### D20 System Files (Pre-existing)

#### `character.py`
- Player character class with D20 attributes
- Ability scores (STR, DEX, CON, INT, WIS, CHA)
- Character classes: Fighter, Wizard, Rogue, Cleric
- Combat mechanics (attack rolls, damage)
- Experience and leveling system
- Spell slots for casters

#### `monster.py`
- Monster/enemy class
- Hit dice based HP calculation
- Attack and damage mechanics
- Special abilities support
- Treasure drops

#### `combat.py`
- Turn-based combat system
- Initiative rolling
- Combat round execution
- Attack resolution
- Victory/defeat conditions

#### `spell.py`
- Spell system with D20 rules
- Example spells: Magic Missile, Fireball, Cure Wounds
- Spell levels and schools
- Casting mechanics

#### `dice.py`
- Dice rolling utilities
- Standard RPG dice (d4, d6, d8, d10, d12, d20, d100)
- Ability score generation (4d6 drop lowest)
- Modifier calculation

## How to Run

```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

## Game Flow

1. **Game Start**: A default party of 3 characters (Fighter, Wizard, Cleric) is created
2. **Exploration**: Navigate the dungeon using arrow keys
3. **Encounters**: Moving onto a monster tile triggers combat
4. **Combat**: Turn-based combat with attack, spell, and flee options
5. **Treasure**: Collect gold from treasure chests
6. **Progression**: Descend stairs to reach deeper, more challenging levels
7. **Victory**: Escape by ascending stairs from level 1

## Architecture

### Game Modes (GameMode enum)
- `EXPLORATION` - Main exploration mode
- `COMBAT` - Turn-based combat
- `MENU` - Menu screens (not yet implemented)
- `INVENTORY` - Inventory management (not yet implemented)
- `CHARACTER_SHEET` - Character details (not yet implemented)
- `GAME_OVER` - Defeat condition
- `VICTORY` - Win condition

### Game Loop
1. Render current game state
2. Get player input
3. Process input based on current mode
4. Update game state
5. Check win/lose conditions
6. Repeat

### Dungeon Generation
- Rooms placed randomly with non-overlapping constraint
- Rooms connected by horizontal and vertical corridors
- Stairs placed at first and last rooms
- Monsters and treasure randomly placed in rooms

### Combat System
- Initiative-based turn order
- Attack rolls: d20 + BAB + ability modifier vs AC
- Damage rolls based on weapon/attack type
- Experience and gold rewards on victory

## Customization

### Creating Custom Monsters
```python
from monster import Monster

goblin = Monster(
    name="Goblin",
    hit_dice="1d8",
    armor_class=12,
    attack_bonus=1,
    damage="1d6"
)
```

### Creating Custom Characters
```python
from character import Character

fighter = Character("Conan", "Fighter", level=1)
fighter.roll_abilities()
# Or set manually:
fighter.set_abilities(str_score=16, dex=14, con=15, int_score=10, wis=12, cha=8)
```

### Monster Placement Options

The game now supports **two monster spawning modes**:

#### 1. Random Spawning (Default)
Monsters are automatically generated and placed randomly in each level.

#### 2. Predefined Placement
Define specific monsters at exact positions in your map JSON files:

```json
{
  "monsters": [
    {
      "name": "Boss Goblin",
      "hit_dice": "4d8+4",
      "armor_class": 16,
      "attack_bonus": 4,
      "damage": "2d6+2",
      "position": [20, 7]
    }
  ]
}
```

**Benefits:**
- Create boss encounters with specific monsters
- Design scripted ambushes and encounters
- Mix predefined and random spawning in the same dungeon
- Full control over monster placement and types

**See [MONSTER_PLACEMENT_GUIDE.md](MONSTER_PLACEMENT_GUIDE.md) for detailed documentation.**

Example map files:
- `maps/mixed_spawn_example.json` - Demonstrates both modes
- `maps/mini_test_dungeon.json` - Simple example with predefined guards

### Door System

The game features an interactive door system with multiple mechanics:

#### Door Types
- **Unlocked doors**: Open automatically when touched
- **Locked doors**: Require lockpicking, smashing, or a key

#### Player Actions
When encountering a locked door:
- **Lockpick (L key)**: Skill-based DEX check (Rogues get bonus)
- **Smash (S key)**: Strength check (Fighters get bonus)
- **Move away**: Cancel interaction

```json
{
  "doors": [
    {
      "horizontal": false,
      "locked": true,
      "lockpick_dc": 15,
      "smash_dc": 18,
      "position": [10, 5]
    }
  ]
}
```

**Features:**
- Different difficulty levels (Easy/Medium/Hard/Very Hard)
- Class-based bonuses (Rogues excel at lockpicking, Fighters at smashing)
- Persistent door states (open/closed/destroyed)
- Visual feedback with tile updates

**See [DOOR_SYSTEM_GUIDE.md](DOOR_SYSTEM_GUIDE.md) for complete documentation.**

Example map file:
- `maps/door_example.json` - Dungeon with various door types and difficulties

### Adjusting Dungeon Parameters
In `game_state.py`, modify `generate_dungeon_level()`:
```python
self.current_map.generate(
    max_rooms=15,      # Number of rooms
    min_room_size=5,   # Minimum room dimensions
    max_room_size=12   # Maximum room dimensions
)
```

## Future Enhancements

### Planned Features
- [ ] Full inventory system with item management
- [ ] Character sheet viewing and equipment
- [ ] Spell casting in combat
- [ ] Item usage (potions, scrolls, etc.)
- [ ] Save/load game functionality
- [ ] More monster types with special abilities
- [ ] Traps and secret doors
- [ ] Multiple dungeon themes
- [ ] Boss encounters
- [ ] Quest system
- [ ] Party creation/customization
- [ ] Permadeath mode

### Combat Enhancements
- [ ] Multi-character combat (full party vs multiple monsters)
- [ ] Positioning and area-of-effect spells
- [ ] Status effects (poison, stun, etc.)
- [ ] Critical hits and fumbles
- [ ] Flanking and tactical bonuses

### Map Features
- [ ] Fog of war / line of sight
- [ ] Dynamic lighting
- [ ] Different dungeon types (caves, castles, crypts)
- [ ] Interactive objects (levers, buttons)
- [ ] Locked doors requiring keys

## Technical Notes

### Platform Compatibility
- **Linux/Unix**: Full support with termios
- **Windows**: Uses msvcrt for keyboard input
- Arrow keys work on both platforms

### Terminal Requirements
- Minimum 80x30 terminal size recommended
- Supports standard ASCII characters
- Works in most terminal emulators

### Dependencies
- Python 3.6+
- Standard library only (no external packages required)

## D20 System Implementation

The game follows Open Gaming License (OGL) D20 system rules:

### Ability Scores
- Range: 3-18 (standard)
- Generated using 4d6 drop lowest
- Modifiers: (Score - 10) / 2

### Combat
- Attack roll: d20 + BAB + ability modifier
- Critical hits: Not yet implemented
- Armor Class: 10 + DEX modifier + armor

### Character Classes
- **Fighter**: High HP, good BAB, strong saves
- **Wizard**: Spellcaster, low HP, arcane spells
- **Cleric**: Healer, divine spells, medium HP
- **Rogue**: Skill-focused, sneak attack potential

### Experience and Leveling
- 1000 XP per level
- Automatic level up when threshold reached
- HP, BAB, and saves improve on level up

## License

This game uses mechanics compatible with the Open Gaming License (OGL) for D20 system rules.

## Credits

Developed as a roguelike framework using classic D20 RPG mechanics.
