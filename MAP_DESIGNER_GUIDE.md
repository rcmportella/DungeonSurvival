# Map Designer Guide

## Overview
DungeonSurvival now supports both randomly generated dungeons and predesigned dungeon levels saved in JSON files.

## Directory Structure
All predesigned maps are stored in the `maps/` directory:
```
DungeonSurvival/
├── main.py
├── maps/
│   ├── sample_dungeon.json
│   └── your_custom_dungeon.json
└── create_sample_maps.py
```

## Using Predesigned Maps

### At Game Start
When you start the game, you'll be asked to choose:
1. Random generated dungeon - Classic procedural generation
2. Predesigned dungeon - Shows list of available maps in `maps/` directory

If you choose predesigned, you'll see all available `.json` files and can select which one to play.

### Sample Dungeon
A sample 3-level dungeon is included: `maps/sample_dungeon.json`
- Level 1: Cross-shaped layout with 5 rooms
- Level 2: Large hall with 4 side chambers
- Level 3: Maze-like structure

## Creating Custom Dungeons

### Method 1: Use the Helper Script
Run `create_sample_maps.py` as a template and modify the level creation functions:

```bash
python3 create_sample_maps.py
```

### Method 2: Programmatically Create Maps

```python
from dungeon_map import DungeonMap, Tile

# Create a new map
dungeon = DungeonMap(width=50, height=20)

# Create rooms by placing floor tiles
for y in range(5, 15):
    for x in range(10, 40):
        dungeon.tiles[y][x] = Tile.create_floor()

# Place stairs
dungeon.stairs_up = (25, 7)
dungeon.stairs_down = (25, 12)
dungeon.tiles[7][25] = Tile(Tile.STAIRS_UP, blocked=False)
dungeon.tiles[12][25] = Tile(Tile.STAIRS_DOWN, blocked=False)

# Place chests
dungeon.place_chest(20, 10)

# Save multiple levels to a file
levels = [level1, level2, level3]
DungeonMap.save_multilevel_dungeon(levels, "maps/my_dungeon.json")
```

## Map File Format

The JSON format stores:
- **width, height**: Map dimensions
- **tiles**: 2D array of characters representing the map
- **stairs_up, stairs_down**: Coordinates for level transitions
- **chests**: List of treasure chest coordinates

### Tile Characters
- `#` - Wall (blocks movement and sight)
- `.` - Floor (walkable)
- `>` - Stairs up
- `<` - Stairs down
- `$` - Treasure chest

## Important Notes

1. **Monsters**: Predesigned maps don't save monster positions. Monsters are spawned at runtime based on dungeon level.

2. **Multiple Levels**: You can have as many levels as you want in a predesigned dungeon. If the player descends beyond predesigned levels, the game will fall back to random generation.

3. **Fog of War**: All maps (random or predesigned) use the fog of war system with a 3-tile vision radius.

4. **File Location**: Place your custom dungeon JSON files in the `maps/` directory.

## Tips for Map Design

1. **Start Small**: Begin with simple rectangular rooms and corridors
2. **Test Frequently**: Run the game to see how your map looks
3. **Balance**: Include enough space for combat but not too open
4. **Progression**: Make deeper levels more complex
5. **Treasures**: Place chests in rewarding but challenging locations

## Example: Creating a Simple Level

```python
def create_simple_level():
    dungeon = DungeonMap(width=40, height=15)
    
    # Single room
    for y in range(3, 12):
        for x in range(5, 35):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Place stairs at opposite ends
    dungeon.stairs_up = (10, 7)
    dungeon.stairs_down = (30, 7)
    dungeon.tiles[7][10] = Tile(Tile.STAIRS_UP, blocked=False)
    dungeon.tiles[7][30] = Tile(Tile.STAIRS_DOWN, blocked=False)
    
    # Add a chest in the middle
    dungeon.place_chest(20, 7)
    
    return dungeon
```

Happy dungeon designing!
