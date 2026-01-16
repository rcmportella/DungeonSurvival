# Predefined Monster Placement Feature

## Overview

The dungeon framework now supports both **random monster spawning** and **predefined monster placement**. You can choose to either let the game randomly populate monsters in each level, or define specific monsters at exact locations in your map files.

## How It Works

### Random Monster Spawning (Default Behavior)
When a level has no predefined monsters, the game will automatically spawn monsters randomly based on:
- The dungeon level (deeper levels = more monsters)
- A factory function that creates appropriate monsters for the level

### Predefined Monster Placement
You can define monsters in your JSON map files by adding a `monsters` array. Each monster in the array specifies:
- Monster stats (name, HP, armor class, attack bonus, damage)
- Exact position on the map

## Map File Format

### Basic Structure
```json
{
  "num_levels": 2,
  "levels": [
    {
      "width": 30,
      "height": 15,
      "tiles": [...],
      "stairs_up": [10, 7],
      "stairs_down": [20, 7],
      "chests": [[15, 7]],
      "monsters": [
        {
          "name": "Goblin Guard",
          "hit_dice": "2d8",
          "armor_class": 14,
          "attack_bonus": 2,
          "damage": "1d6+1",
          "position": [8, 7]
        }
      ]
    }
  ]
}
```

### Monster Definition Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | The monster's name | `"Goblin Guard"` |
| `hit_dice` | string | Hit dice formula for HP | `"2d8"` or `"3d8+3"` |
| `armor_class` | integer | Armor class (D20 rules) | `14` |
| `attack_bonus` | integer | Attack roll bonus | `2` |
| `damage` | string | Damage dice formula | `"1d6+1"` or `"2d6+3"` |
| `position` | array | `[x, y]` coordinates | `[8, 7]` |

### Dice Notation
- `1d8` = Roll one 8-sided die
- `2d6+3` = Roll two 6-sided dice and add 3
- `3d8+5` = Roll three 8-sided dice and add 5

## Usage Examples

### Example 1: Level with Predefined Boss Fight
```json
{
  "monsters": [
    {
      "name": "Dragon Boss",
      "hit_dice": "8d10+24",
      "armor_class": 18,
      "attack_bonus": 8,
      "damage": "2d10+6",
      "position": [25, 12]
    },
    {
      "name": "Dragon Minion",
      "hit_dice": "2d8",
      "armor_class": 13,
      "attack_bonus": 3,
      "damage": "1d6+1",
      "position": [20, 10]
    },
    {
      "name": "Dragon Minion",
      "hit_dice": "2d8",
      "armor_class": 13,
      "attack_bonus": 3,
      "damage": "1d6+1",
      "position": [30, 10]
    }
  ]
}
```

### Example 2: Empty Level (Random Spawning)
```json
{
  "monsters": []
}
```

When the `monsters` array is empty or omitted, the game will spawn monsters randomly.

### Example 3: Mixed Approach
You can create a multi-level dungeon where:
- Some levels have predefined monsters (boss fights, scripted encounters)
- Other levels use random spawning (exploration areas)

See `maps/mixed_spawn_example.json` for a complete example.

## Creating Custom Monsters

When defining monsters, consider these guidelines:

### Monster Difficulty by Level

**Level 1-2 (Easy)**
- Hit Dice: 1d6 to 2d8
- Armor Class: 10-13
- Attack Bonus: 0-2
- Damage: 1d4 to 1d6+1

**Level 3-5 (Medium)**
- Hit Dice: 2d8 to 4d8+4
- Armor Class: 13-16
- Attack Bonus: 2-5
- Damage: 1d6+1 to 2d6+3

**Level 6+ (Hard)**
- Hit Dice: 5d8+10 or higher
- Armor Class: 16-20
- Attack Bonus: 5-10
- Damage: 2d8+4 or higher

### Boss Monsters
For memorable boss fights:
1. Use descriptive names (e.g., "Ancient Dragon", "Lich King")
2. Give them significantly higher stats than regular monsters
3. Consider placing minions nearby
4. Position them in strategic locations (center of room, guarding treasure)

## Testing Your Maps

Run the test script to verify your monster placements:

```bash
python test_monster_placement.py
```

This will test:
- Loading maps with predefined monsters
- Random monster spawning on empty levels
- Monster serialization/deserialization

## Map Examples

The following example maps are included:

1. **mini_test_dungeon.json** - Simple 2-level dungeon with predefined monsters on level 1
2. **mixed_spawn_example.json** - Demonstrates both predefined (level 1) and random spawn (level 2)
3. **sample_dungeon.json** - Original example with random spawning

## Benefits

### Predefined Monsters
✅ **Pros:**
- Control exact encounters
- Design boss fights
- Create scripted gameplay experiences
- Ensure balanced difficulty

❌ **Cons:**
- Less replayability
- More work to design
- Fixed monster HP (rolled once when loaded)

### Random Spawning
✅ **Pros:**
- High replayability
- Quick to set up
- Varied gameplay each time

❌ **Cons:**
- Less control over difficulty
- Can't create scripted encounters
- May be unbalanced (too easy or too hard)

## Best Practices

1. **Use predefined monsters for:**
   - Boss encounters
   - Story-important fights
   - Tutorial/training areas
   - Ambush scenarios

2. **Use random spawning for:**
   - Exploration areas
   - Filler levels
   - Procedurally generated content
   - High replayability

3. **Mix both approaches:**
   - Create a dungeon where key levels have predefined encounters
   - Let other levels randomize for variety

4. **Test your placements:**
   - Make sure monsters aren't on walls or stairs
   - Check that positions are within map bounds
   - Verify difficulty is appropriate for the level

## Technical Details

### Implementation
- Monsters are loaded from the `monsters` field in JSON during `DungeonMap.from_dict()`
- If no monsters are defined, `GameState.generate_dungeon_level()` calls `populate_monsters()`
- Monster HP is rolled when created (not saved in the map file)
- Monster positions are validated when placed

### Monster Lifecycle
1. Map loads → Monsters created from JSON definitions
2. HP rolled based on hit dice
3. Monsters placed at specified positions
4. Game proceeds with predefined encounters

### Compatibility
- Old map files without the `monsters` field work normally (random spawn)
- Adding `"monsters": []` explicitly requests random spawning
- All existing code remains compatible
