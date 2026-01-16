# DungeonSurvival Framework Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                    (Game Entry Point)                        │
│  - Main game loop                                            │
│  - Rendering                                                 │
│  - Input routing                                             │
└───────────────────┬─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐      ┌──────────────────┐
│ input_handler │      │   game_state     │
│               │      │                  │
│ - Arrow keys  │      │ - Game modes     │
│ - WASD        │      │ - Turn tracking  │
│ - Commands    │      │ - Message log    │
└───────────────┘      │ - Level mgmt     │
                       └────────┬─────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌───────────┐   ┌─────────────┐  ┌──────────┐
        │   party   │   │ dungeon_map │  │  combat  │
        │           │   │             │  │          │
        │ - Members │   │ - Generate  │  │ - Turns  │
        │ - Gold    │   │ - Render    │  │ - Init   │
        │ - XP      │   │ - Tiles     │  │ - Attack │
        └─────┬─────┘   │ - Monsters  │  └────┬─────┘
              │         └──────┬──────┘       │
              │                │              │
              ▼                ▼              ▼
        ┌──────────┐    ┌──────────┐   ┌─────────┐
        │character │    │ monster  │   │  spell  │
        │          │    │          │   │         │
        │ - Stats  │    │ - Stats  │   │ - Cast  │
        │ - Class  │    │ - HD     │   │ - Level │
        │ - Attack │    │ - Attack │   │ - Dmg   │
        └────┬─────┘    └────┬─────┘   └─────────┘
             │               │
             └───────┬───────┘
                     │
                     ▼
              ┌──────────┐
              │   dice   │
              │          │
              │ - d4-d20 │
              │ - Mods   │
              └──────────┘
```

## Module Dependencies

### Core Game Loop
- **main.py** depends on:
  - game_state
  - character
  - party
  - input_handler

### Game State Management
- **game_state.py** depends on:
  - party
  - dungeon_map
  - combat
  - monster

### Map and Exploration
- **dungeon_map.py** depends on:
  - monster (for placement)
  - No circular dependencies

### Party and Character System
- **party.py** depends on:
  - character

- **character.py** depends on:
  - dice
  - (optional) spell for spellcasters

### Combat System
- **combat.py** depends on:
  - character
  - monster
  - dice
  - spell (for spell combat)

### Supporting Systems
- **monster.py** depends on:
  - dice

- **spell.py** depends on:
  - dice

- **dice.py** depends on:
  - No dependencies (pure utility)

- **input_handler.py** depends on:
  - No game dependencies (pure I/O)

## Game Flow Diagrams

### Main Game Loop

```
Start
  │
  ├──> Initialize Game State
  │    ├──> Create Party
  │    ├──> Generate Dungeon
  │    └──> Place Party
  │
  ├──> GAME LOOP ────┐
  │                  │
  │    ┌─────────────┘
  │    │
  │    ├──> Render Current State
  │    │    ├──> Clear Screen
  │    │    ├──> Draw Map
  │    │    ├──> Show Party Info
  │    │    └──> Show Messages
  │    │
  │    ├──> Get Player Input
  │    │
  │    ├──> Process Input
  │    │    ├──> Movement?
  │    │    ├──> Combat?
  │    │    └──> Other Commands?
  │    │
  │    ├──> Update Game State
  │    │
  │    ├──> Check Win/Loss
  │    │    ├──> Victory? ──> END
  │    │    ├──> Defeat? ──> END
  │    │    └──> Continue ──┘
  │
  └──> Cleanup & Exit
```

### Exploration Mode Flow

```
Exploration Mode
      │
      ├──> Get Movement Input
      │    ├──> Arrow Keys
      │    ├──> WASD
      │    └──> Numpad
      │
      ├──> Calculate New Position
      │
      ├──> Check Tile
      │    ├──> Wall? ──> Block & Message
      │    ├──> Monster? ──> Start Combat
      │    ├──> Chest? ──> Open & Loot
      │    ├──> Stairs? ──> Change Level
      │    └──> Empty? ──> Move Party
      │
      └──> Update Display
```

### Combat Mode Flow

```
Combat Start
      │
      ├──> Roll Initiative
      │    ├──> Party Members
      │    └──> Monsters
      │
      ├──> Sort by Initiative
      │
      ├──> COMBAT ROUND ────┐
      │                     │
      │    ┌────────────────┘
      │    │
      │    ├──> For Each Combatant (by init order)
      │    │    │
      │    │    ├──> Is Alive?
      │    │    │
      │    │    ├──> Player Turn
      │    │    │    ├──> Attack
      │    │    │    ├──> Cast Spell
      │    │    │    ├──> Use Item
      │    │    │    └──> Flee
      │    │    │
      │    │    └──> Monster Turn
      │    │         └──> Attack Party
      │    │
      │    ├──> Check Combat End
      │    │    ├──> All Monsters Dead? ──> Victory
      │    │    ├──> All Party Dead? ──> Defeat
      │    │    └──> Continue ──┘
      │
      └──> Award XP & Gold
           │
           └──> Return to Exploration
```

## Data Flow

### Character Action Data Flow

```
Player Input
     │
     ▼
Input Handler ──> Parsed Command
     │
     ▼
Game State ──> Validate Action
     │
     ▼
Character ──> Execute Action
     │         (Attack, Move, Spell)
     ▼
Target (Monster/Tile)
     │
     ▼
Roll Dice ──> Calculate Result
     │
     ▼
Update State
     │
     ├──> Update HP
     ├──> Update Position
     ├──> Update Inventory
     └──> Add Message
     │
     ▼
Render Display
```

### Dungeon Generation Data Flow

```
Game State
     │
     ▼
Create DungeonMap(width, height)
     │
     ▼
Generate Rooms
     │  ├──> Place Random Rooms
     │  ├──> Check Overlaps
     │  └──> Connect with Corridors
     │
     ▼
Place Stairs
     │  ├──> Stairs Up (first room)
     │  └──> Stairs Down (last room)
     │
     ▼
Populate Monsters
     │  ├──> Random Positions
     │  └──> Level-Appropriate Types
     │
     ▼
Place Treasures
     │  └──> 30% chance per room
     │
     ▼
Return Complete Map
```

## State Machine Diagram

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  ┌─────────────┐                                │
│  │    MENU     │                                │
│  └──────┬──────┘                                │
│         │                                        │
│         │ Start Game                            │
│         ▼                                        │
│  ┌─────────────┐     Monster           ┌──────────┐
│  │ EXPLORATION │──────Encounter────────>│  COMBAT  │
│  └──────┬──────┘                        └────┬─────┘
│         │  ▲                                 │
│         │  │ Victory/Flee                    │
│         │  └─────────────────────────────────┘
│         │
│         ├──> Press 'I' ──> INVENTORY (Future)
│         │
│         ├──> Press 'C' ──> CHARACTER_SHEET (Future)
│         │
│         ├──> Stairs Down ──> Next Level
│         │                    (stay in EXPLORATION)
│         │
│         └──> Stairs Up ──> Previous Level OR Victory
│                             (EXPLORATION or VICTORY)
│
│  ┌─────────────┐           ┌─────────────┐
│  │  GAME_OVER  │           │   VICTORY   │
│  └─────────────┘           └─────────────┘
│
└──────────────────────────────────────────────────┘
```

## Class Relationships

### Core Classes

```
Character
├── Properties
│   ├── name: str
│   ├── char_class: str
│   ├── level: int
│   ├── ability_scores: int (x6)
│   ├── current_hp: int
│   ├── max_hp: int
│   ├── armor_class: int
│   ├── base_attack_bonus: int
│   ├── inventory: list
│   └── known_spells: list
│
└── Methods
    ├── roll_abilities()
    ├── attack_roll(target_ac, weapon)
    ├── take_damage(amount)
    ├── is_alive()
    ├── gain_experience(xp)
    └── level_up()

Monster
├── Properties
│   ├── name: str
│   ├── hit_dice: str
│   ├── armor_class: int
│   ├── attack_bonus: int
│   ├── damage: str
│   ├── current_hp: int
│   └── max_hp: int
│
└── Methods
    ├── attack(target)
    ├── take_damage(amount)
    └── is_alive()

Party
├── Properties
│   ├── members: list[Character]
│   └── position: [int, int]
│
└── Methods
    ├── add_member(character)
    ├── distribute_gold(amount)
    ├── distribute_experience(amount)
    └── is_alive()

DungeonMap
├── Properties
│   ├── width: int
│   ├── height: int
│   ├── tiles: 2D array
│   ├── rooms: list[Room]
│   ├── monsters: list[(Monster, x, y)]
│   └── chests: list[(x, y)]
│
└── Methods
    ├── generate(max_rooms, sizes)
    ├── place_monster(monster, x, y)
    ├── is_blocked(x, y)
    └── render(party_x, party_y)

GameState
├── Properties
│   ├── mode: GameMode
│   ├── party: Party
│   ├── current_map: DungeonMap
│   ├── dungeon_level: int
│   ├── combat_instance: Combat
│   └── message_log: list[str]
│
└── Methods
    ├── initialize_game()
    ├── move_party(dx, dy)
    ├── start_combat(x, y)
    ├── descend_stairs()
    ├── ascend_stairs()
    └── get_display()
```

## Extension Points

The framework is designed for easy extension:

1. **Custom Monsters**: Subclass `Monster` or use factory functions
2. **Custom Character Classes**: Extend `Character._update_derived_stats()`
3. **Custom Spells**: Subclass `Spell` and override `cast()`
4. **Custom Map Generation**: Subclass `DungeonMap` and override `generate()`
5. **Custom Game Modes**: Add to `GameMode` enum and handle in game loop
6. **Custom Items**: Create item system and integrate with inventory
7. **Custom AI**: Extend monster combat logic in `Combat` class

## Performance Considerations

- Map rendering is done every frame - optimize for terminal output
- Combat calculations are event-driven - no continuous polling
- Monster pathfinding not implemented - stationary until engaged
- No need for threading - turn-based gameplay is sequential
- Memory usage is minimal - simple data structures

## Future Architecture Improvements

1. **Separation of Concerns**
   - Extract rendering into dedicated module
   - Separate game logic from display logic

2. **Event System**
   - Implement event bus for game events
   - Decouple combat from direct state manipulation

3. **Save System**
   - Serialize game state to JSON
   - Implement load/save functions

4. **Configuration System**
   - Load settings from config file
   - Support modding through data files

5. **AI System**
   - Monster AI behaviors
   - Pathfinding for movement

6. **Sound System**
   - Text-based sound effects
   - Background "music" using ASCII art
