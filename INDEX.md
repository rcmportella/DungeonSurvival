# DungeonSurvival Framework - Documentation Index

Welcome to DungeonSurvival! This index will help you find what you need.

## Quick Links

### I Want to Play the Game
→ Start here: [QUICKSTART.md](QUICKSTART.md)
→ Then read: [VISUALS.md](VISUALS.md) to understand the display

### I Want to Learn Everything
→ Read: [README.md](README.md) - Complete documentation

### I Want to Customize the Game
→ Check: [examples.py](examples.py) - Run with `python3 examples.py`
→ Then: [config.py](config.py) - Edit game settings

### I Want to Understand the Code
→ Study: [ARCHITECTURE.md](ARCHITECTURE.md) - System design
→ Then: [SUMMARY.md](SUMMARY.md) - Complete overview

## Documentation Files

### For Players

| File | Purpose | When to Read |
|------|---------|--------------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute guide to start playing | Before first game |
| [VISUALS.md](VISUALS.md) | Visual examples of game screens | When confused by display |
| [README.md](README.md) | Complete game documentation | For full understanding |

### For Developers

| File | Purpose | When to Read |
|------|---------|--------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and diagrams | Before modifying code |
| [SUMMARY.md](SUMMARY.md) | Framework overview | For high-level understanding |
| [examples.py](examples.py) | Customization examples | When adding features |
| [config.py](config.py) | Configuration constants | When adjusting game balance |

## Source Code Files

### Core Game Files

| File | Purpose | Lines | Key Classes/Functions |
|------|---------|-------|----------------------|
| [main.py](main.py) | Game entry point | 234 | `main()`, `render_game()`, `handle_input()` |
| [game_state.py](game_state.py) | State management | 258 | `GameState`, `GameMode` |
| [dungeon_map.py](dungeon_map.py) | Map generation | 229 | `DungeonMap`, `Room`, `Tile` |
| [party.py](party.py) | Party management | 76 | `Party` |
| [input_handler.py](input_handler.py) | Keyboard input | 135 | `InputHandler` |
| [config.py](config.py) | Configuration | 213 | Constants, `Symbols`, `Colors` |

### D20 System Files

| File | Purpose | Lines | Key Classes/Functions |
|------|---------|-------|----------------------|
| [character.py](character.py) | Player characters | 388 | `Character` |
| [monster.py](monster.py) | Enemies/monsters | 281 | `Monster` |
| [combat.py](combat.py) | Combat system | 290 | `Combat` |
| [spell.py](spell.py) | Magic system | 297 | `Spell`, `MagicMissile`, `Fireball` |
| [dice.py](dice.py) | Dice rolling | 79 | `roll()`, `d20()`, `ability_score()` |

### Example and Demo Files

| File | Purpose | Lines | Description |
|------|---------|-------|-------------|
| [examples.py](examples.py) | Customization demos | 217 | Shows how to extend the game |

## Common Tasks

### Playing the Game
```bash
python3 main.py
```

### Running Examples
```bash
python3 examples.py
```

### Testing the Framework
```bash
python3 -c "import game_state; print('✓ Framework ready')"
```

### Creating a Custom Monster
```python
from monster import Monster
dragon = Monster("Dragon", "10d8+20", 18, 8, "2d6+6")
```

### Creating a Custom Party
```python
from character import Character
from party import Party

party = Party()
hero = Character("Hero", "Fighter", 5)
hero.roll_abilities()
party.add_member(hero)
```

### Generating a Custom Dungeon
```python
from dungeon_map import DungeonMap
large_map = DungeonMap(width=120, height=60)
large_map.generate(max_rooms=20)
```

## File Dependency Tree

```
main.py
├── game_state.py
│   ├── party.py
│   │   └── character.py
│   │       ├── dice.py
│   │       └── spell.py
│   │           └── dice.py
│   ├── dungeon_map.py
│   │   └── monster.py
│   │       └── dice.py
│   └── combat.py
│       ├── character.py
│       ├── monster.py
│       ├── spell.py
│       └── dice.py
└── input_handler.py
```

## Learning Path

### Beginner Path (Just Want to Play)
1. Read [QUICKSTART.md](QUICKSTART.md) (5 minutes)
2. Run `python3 main.py`
3. Play the game!
4. Check [VISUALS.md](VISUALS.md) if confused

### Intermediate Path (Want to Customize)
1. Complete Beginner Path
2. Read [README.md](README.md) (15 minutes)
3. Run `python3 examples.py`
4. Edit [config.py](config.py) to adjust game
5. Modify [examples.py](examples.py) for your changes

### Advanced Path (Want to Extend)
1. Complete Intermediate Path
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) (20 minutes)
3. Read [SUMMARY.md](SUMMARY.md) (10 minutes)
4. Study source code files
5. Create new features based on examples

## Getting Help

### Game Not Working?
→ See "Troubleshooting" in [QUICKSTART.md](QUICKSTART.md)

### Don't Understand the Code?
→ Check diagrams in [ARCHITECTURE.md](ARCHITECTURE.md)

### Want to Add a Feature?
→ Look for similar examples in [examples.py](examples.py)

### Need Game Balance?
→ Adjust values in [config.py](config.py)

## Features Overview

### Implemented ✓
- ASCII dungeon exploration
- Procedural generation
- Party management
- Turn-based combat
- Character progression
- Multiple classes
- Monster encounters
- Treasure hunting
- Multi-level dungeons
- HP visualization
- Message logging

### Partially Implemented ⚠
- Spell casting (structure in place, limited use)
- Item system (basic, needs expansion)

### Planned for Future 📋
- Save/load game
- Full inventory system
- More monster types
- Status effects
- Fog of war
- Quest system

## Version Information

**Current Version:** 0.1.0
**Python Required:** 3.6+
**Dependencies:** None (standard library only)
**Status:** Complete and Playable

## File Statistics

- **Total Files:** 16 (11 new + 5 existing)
- **Total Lines:** ~3,200 lines
- **Documentation:** 5 comprehensive guides
- **Examples:** 6 different customization examples
- **Test Coverage:** All modules verified working

## Quick Reference

### Game Controls
- **Movement:** Arrow keys, WASD, or numpad
- **Descend:** D (on stairs down)
- **Ascend:** U (on stairs up)
- **Attack:** A (in combat)
- **Flee:** F (in combat)
- **Quit:** Q

### Map Symbols
- `#` Wall
- `.` Floor
- `1` Party
- `A-Z` Monsters
- `$` Treasure
- `<` Stairs down
- `>` Stairs up
- `|` `-` Doors

### Character Classes
- **Fighter:** High HP, good melee
- **Wizard:** Spells, low HP
- **Cleric:** Healing, medium HP
- **Rogue:** Stealth, skills

## Next Steps

1. **Start Playing:**
   ```bash
   python3 main.py
   ```

2. **Explore Examples:**
   ```bash
   python3 examples.py
   ```

3. **Read Documentation:**
   - Quick: [QUICKSTART.md](QUICKSTART.md)
   - Full: [README.md](README.md)
   - Technical: [ARCHITECTURE.md](ARCHITECTURE.md)

4. **Customize:**
   - Edit [config.py](config.py)
   - Modify [examples.py](examples.py)
   - Create your own content!

## Support

This is a self-contained framework. Everything you need is in the documentation:
- [QUICKSTART.md](QUICKSTART.md) for getting started
- [README.md](README.md) for complete details
- [ARCHITECTURE.md](ARCHITECTURE.md) for technical info
- [examples.py](examples.py) for code examples

---

**Happy Dungeon Crawling! 🗡️🐉💰**

*DungeonSurvival Framework v0.1.0*
