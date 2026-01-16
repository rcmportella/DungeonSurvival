# Quick Reference: Predefined Monster Placement

## Basic Usage

### 1. Add Monsters to Your Map JSON

```json
{
  "width": 40,
  "height": 20,
  "tiles": [...],
  "stairs_up": [10, 5],
  "stairs_down": [30, 15],
  "chests": [[20, 10]],
  "monsters": [
    {
      "name": "Boss Orc",
      "hit_dice": "5d8+10",
      "armor_class": 16,
      "attack_bonus": 5,
      "damage": "2d6+3",
      "position": [20, 10]
    }
  ]
}
```

### 2. For Random Spawning

Leave array empty or omit entirely:

```json
{
  "monsters": []
}
```

OR

```json
{
  "width": 40,
  "height": 20,
  "tiles": [...]
  // No monsters field = random spawn
}
```

## Monster Stat Quick Reference

### Easy Monsters (Levels 1-2)
```json
{
  "name": "Goblin",
  "hit_dice": "1d8",
  "armor_class": 12,
  "attack_bonus": 1,
  "damage": "1d6"
}
```

### Medium Monsters (Levels 3-5)
```json
{
  "name": "Orc Warrior",
  "hit_dice": "3d8+3",
  "armor_class": 14,
  "attack_bonus": 3,
  "damage": "1d8+2"
}
```

### Hard Monsters (Levels 6+)
```json
{
  "name": "Ogre",
  "hit_dice": "5d8+15",
  "armor_class": 16,
  "attack_bonus": 6,
  "damage": "2d8+4"
}
```

### Boss Monsters
```json
{
  "name": "Dragon",
  "hit_dice": "10d10+30",
  "armor_class": 18,
  "attack_bonus": 10,
  "damage": "3d8+6"
}
```

## Dice Notation Cheat Sheet

| Formula | Meaning | Average |
|---------|---------|---------|
| 1d4 | Roll one 4-sided die | 2.5 |
| 1d6 | Roll one 6-sided die | 3.5 |
| 1d8 | Roll one 8-sided die | 4.5 |
| 2d6 | Roll two 6-sided dice | 7 |
| 2d8+3 | Roll two 8-sided dice, add 3 | 12 |
| 5d10+15 | Roll five 10-sided dice, add 15 | 42.5 |

## Position Coordinates

Positions are `[x, y]` where:
- `x` = horizontal position (left to right)
- `y` = vertical position (top to bottom)
- Both start at 0
- Must be on a floor tile (not wall, stairs, or chest)

Example:
```
01234567890...  (x-axis)
###########     0
#.........#     1
#....M....#     2  Monster at [5, 2]
#.........#     3
###########     4
(y-axis)
```

## Common Patterns

### Boss Fight with Minions
```json
"monsters": [
  {
    "name": "Boss",
    "hit_dice": "8d8+16",
    "armor_class": 17,
    "attack_bonus": 7,
    "damage": "2d8+4",
    "position": [20, 10]
  },
  {
    "name": "Minion",
    "hit_dice": "2d8",
    "armor_class": 13,
    "attack_bonus": 2,
    "damage": "1d6",
    "position": [18, 9]
  },
  {
    "name": "Minion",
    "hit_dice": "2d8",
    "armor_class": 13,
    "attack_bonus": 2,
    "damage": "1d6",
    "position": [22, 11]
  }
]
```

### Guard Posts
```json
"monsters": [
  {
    "name": "Guard",
    "hit_dice": "3d8",
    "armor_class": 15,
    "attack_bonus": 3,
    "damage": "1d8+1",
    "position": [5, 5]
  },
  {
    "name": "Guard",
    "hit_dice": "3d8",
    "armor_class": 15,
    "attack_bonus": 3,
    "damage": "1d8+1",
    "position": [5, 15]
  }
]
```

### Ambush
```json
"monsters": [
  {
    "name": "Assassin",
    "hit_dice": "4d8+4",
    "armor_class": 16,
    "attack_bonus": 5,
    "damage": "1d6+3",
    "position": [10, 5]
  },
  {
    "name": "Assassin",
    "hit_dice": "4d8+4",
    "armor_class": 16,
    "attack_bonus": 5,
    "damage": "1d6+3",
    "position": [30, 5]
  },
  {
    "name": "Assassin",
    "hit_dice": "4d8+4",
    "armor_class": 16,
    "attack_bonus": 5,
    "damage": "1d6+3",
    "position": [20, 15]
  }
]
```

## Testing Your Monsters

Run the test:
```bash
python test_monster_placement.py
```

Or demo:
```bash
python demo_monster_feature.py
```

## Troubleshooting

**Monsters not appearing?**
- Check position is on a floor tile (`.`)
- Verify coordinates are within map bounds
- Make sure position isn't on stairs or chest

**Game crashes on load?**
- Verify JSON syntax is correct
- Check all required fields are present
- Ensure hit_dice and damage use valid dice notation

**Monsters spawning randomly despite definition?**
- Check monsters array is not empty `[]`
- Verify monsters array is at the right level in JSON structure

## Files to Check

- Example maps: `maps/mini_test_dungeon.json`, `maps/mixed_spawn_example.json`
- Full guide: `MONSTER_PLACEMENT_GUIDE.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
