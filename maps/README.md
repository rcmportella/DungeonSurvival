# Predesigned Maps Directory

This directory contains predesigned dungeon map files in JSON format.

## Included Maps

- **sample_dungeon.json** - A 3-level demonstration dungeon with varied layouts
- **mini_test_dungeon.json** - Simple 2-level dungeon with predefined monster placements
- **mixed_spawn_example.json** - Demonstrates both predefined and random monster spawning
- **door_example.json** - Demonstrates door mechanics with various difficulty levels

## Creating Your Own Maps

To create custom dungeons:

1. Use `create_sample_maps.py` as a template
2. Create your level layouts programmatically
3. Save to this directory with `DungeonMap.save_multilevel_dungeon(levels, "maps/your_map.json")`

See `MAP_DESIGNER_GUIDE.md` in the parent directory for detailed instructions.

## File Format

Maps are stored as JSON with the following structure:
- Map dimensions (width, height)
- Tile layout (2D character array)
- Stair positions
- Chest locations
- **Monster definitions** (optional - new feature!)
- **Door definitions** (optional - new feature!)

### Monster Placement
You can now define monsters at specific positions in your maps:
```json
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
```

If the `monsters` array is empty or omitted, monsters will spawn randomly (default behavior).

**See [MONSTER_PLACEMENT_GUIDE.md](../MONSTER_PLACEMENT_GUIDE.md) for full documentation.**

### Door Placement
You can add interactive doors with locking mechanics:
```json
"doors": [
  {
    "horizontal": false,
    "locked": true,
    "lockpick_dc": 15,
    "smash_dc": 18,
    "position": [10, 5]
  }
]
```

Doors can be:
- Open or closed
- Locked or unlocked
- Pickable or smashable
- Different difficulty levels

**See [DOOR_SYSTEM_GUIDE.md](../DOOR_SYSTEM_GUIDE.md) for complete documentation.**

The game will automatically detect and list all `.json` files in this directory when you choose "Predesigned dungeon" at game start.
