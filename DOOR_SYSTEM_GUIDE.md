# Door System Guide

## Overview

The game now features a comprehensive door system with multiple interaction modes. Doors can be open or closed, locked or unlocked, and players can interact with them through movement, lockpicking, or brute force smashing.

## Door States

### Open/Closed
- **Open doors**: Represented as floor tiles (`.`), passable and don't block sight
- **Closed doors**: Represented as `-` (horizontal) or `|` (vertical), block movement and sight
- **Destroyed doors**: Appear as floor tiles, permanently passable

### Locked/Unlocked
- **Unlocked doors**: Open automatically when player moves into them
- **Locked doors**: Require lockpicking, smashing, or a key to open

## Player Interactions

### Automatic Opening (Unlocked Doors)
When a player moves into an unlocked door, it opens automatically and the tile becomes passable.

### Locked Door Options
When encountering a locked door, the player receives the message:
```
The door is locked. (L)ockpick it or (S)mash it?
```

The player can then:
1. Press **L** to attempt lockpicking
2. Press **S** to attempt smashing
3. Move away to cancel the interaction

### Lockpicking
- **Skill-based**: Uses DEX modifier + level bonus (Rogues get full level, others get DEX only)
- **Dice roll**: d20 + bonus vs. Lockpick DC
- **Success**: Door unlocks and opens
- **Failure**: Door remains locked, can try again
- **Rogues excel**: Get their full level as bonus plus DEX modifier

### Smashing
- **Strength-based**: Uses STR modifier + Fighter bonus
- **Dice roll**: d20 + bonus vs. Smash DC
- **Success**: Door is destroyed (permanently open)
- **Failure**: Door remains locked, can try again
- **Fighters excel**: Get level/2 bonus plus STR modifier
- **Note**: Smashed doors cannot be closed again

## Door Difficulty Levels

### Easy Doors
- Lockpick DC: 10
- Smash DC: 15
- Suitable for level 1-2 characters

### Medium Doors
- Lockpick DC: 15
- Smash DC: 18
- Suitable for level 3-5 characters

### Hard Doors
- Lockpick DC: 20
- Smash DC: 23
- Suitable for level 6+ characters

### Very Hard Doors
- Lockpick DC: 25
- Smash DC: 28
- Challenging for even high-level characters

## Map File Format

### Basic Door Definition
```json
"doors": [
  {
    "horizontal": true,
    "locked": true,
    "lockpick_dc": 15,
    "smash_dc": 18,
    "key_id": null,
    "is_open": false,
    "is_destroyed": false,
    "position": [15, 5]
  }
]
```

### Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `horizontal` | boolean | Door orientation (true = `-`, false = `|`) | `true` |
| `locked` | boolean | Whether door starts locked | `true` |
| `lockpick_dc` | integer | Difficulty Class for lockpicking (10-30) | `15` |
| `smash_dc` | integer | Difficulty Class for smashing (15-30) | `18` |
| `key_id` | string/null | Optional key ID for unlocking | `"iron_key"` |
| `is_open` | boolean | Door state (usually false initially) | `false` |
| `is_destroyed` | boolean | Whether door is smashed | `false` |
| `position` | array | `[x, y]` coordinates | `[15, 5]` |

## Game Controls

### Exploration Mode
When facing a locked door:
- **L key**: Attempt to lockpick
- **S key**: Attempt to smash
- **Movement keys**: Cancel door interaction

Controls are shown in the game UI when a door interaction is pending.

## Design Tips

### Unlocked Doors
Use for:
- Separating rooms visually
- Simple barriers that don't impede progress
- Tutorial areas

```json
{
  "horizontal": true,
  "locked": false,
  "lockpick_dc": 15,
  "smash_dc": 18,
  "position": [10, 5]
}
```

### Locked Doors with Easy DC
Use for:
- Early game challenges
- Training players in door mechanics
- Minor security

```json
{
  "horizontal": false,
  "locked": true,
  "lockpick_dc": 10,
  "smash_dc": 15,
  "position": [20, 8]
}
```

### Hard Locked Doors
Use for:
- Treasure rooms
- Boss areas
- Secret areas
- Late-game content

```json
{
  "horizontal": true,
  "locked": true,
  "lockpick_dc": 20,
  "smash_dc": 25,
  "position": [30, 10]
}
```

### Keyed Doors
Use for:
- Quest progression
- Multi-stage puzzles
- Forcing exploration

```json
{
  "horizontal": false,
  "locked": true,
  "lockpick_dc": 25,
  "smash_dc": 30,
  "key_id": "boss_key",
  "position": [15, 15]
}
```

## Class Advantages

### Rogue
- **Best at lockpicking**: Gets level + DEX modifier
- **Example**: Level 5 Rogue with 16 DEX = +8 bonus
- **Strategy**: Use lockpicking whenever possible

### Fighter
- **Best at smashing**: Gets (level/2) + STR modifier
- **Example**: Level 6 Fighter with 18 STR = +7 bonus
- **Strategy**: Smash when lockpicking seems too difficult
- **Note**: Smashing is permanent - door can't be closed again

### Other Classes
- **Lockpicking**: Only DEX modifier
- **Smashing**: Only STR modifier
- **Strategy**: Choose based on ability scores

## Map Examples

### Simple Room with Door
```json
{
  "tiles": [
    "##########",
    "#........#",
    "#........#",
    "##########"
  ],
  "doors": [
    {
      "horizontal": false,
      "locked": false,
      "lockpick_dc": 15,
      "smash_dc": 18,
      "position": [5, 3]
    }
  ]
}
```

### Treasure Room with Hard Lock
```json
{
  "tiles": [
    "##########",
    "#...##...#",
    "#...$#...#",
    "#...##...#",
    "##########"
  ],
  "doors": [
    {
      "horizontal": false,
      "locked": true,
      "lockpick_dc": 20,
      "smash_dc": 24,
      "position": [4, 1]
    }
  ],
  "chests": [[4, 2]]
}
```

### Multiple Difficulty Doors
```json
{
  "doors": [
    {
      "horizontal": true,
      "locked": true,
      "lockpick_dc": 10,
      "smash_dc": 15,
      "position": [5, 3]
    },
    {
      "horizontal": false,
      "locked": true,
      "lockpick_dc": 18,
      "smash_dc": 22,
      "position": [15, 5]
    },
    {
      "horizontal": true,
      "locked": true,
      "lockpick_dc": 25,
      "smash_dc": 30,
      "position": [25, 7]
    }
  ]
}
```

## Statistics Tracking

The game tracks door-related statistics:
- `doors_picked`: Total doors successfully lockpicked
- `doors_smashed`: Total doors smashed open

These appear in the final game statistics screen.

## Technical Details

### Implementation
- Door class in `door.py` handles all door logic
- DungeonMap stores doors as `(door, x, y)` tuples
- Tiles have a `door` attribute referencing the Door object
- GameState manages door interactions and skill checks

### Skill Check Formula
```python
# Lockpicking
if character.char_class == "Rogue":
    bonus = character.level + character.get_ability_modifier('dexterity')
else:
    bonus = character.get_ability_modifier('dexterity')
roll = d20() + bonus
success = (roll >= door.lockpick_dc)

# Smashing
bonus = character.get_ability_modifier('strength')
if character.char_class == "Fighter":
    bonus += character.level // 2
roll = d20() + bonus
success = (roll >= door.smash_dc)
```

### State Management
- Doors persist in visited levels
- Door state (open/closed/destroyed) is preserved
- Doors serialize to map files with current state

## Example Usage

See `maps/door_example.json` for a complete example dungeon with doors of varying difficulty.

## Testing

Run the door test suite:
```bash
python test_doors.py
```

This tests:
- Basic door mechanics
- Lockpicking and smashing
- Serialization
- Map integration
- Game integration
- Difficulty scaling

## Tips for Players

1. **Check your stats**: If you have high DEX, try lockpicking first
2. **Check your class**: Rogues should always try lockpicking
3. **Fighters can smash**: Don't be afraid to break down doors
4. **Multiple attempts**: You can retry failed attempts
5. **Move away to cancel**: If you change your mind about a door
6. **Plan your route**: Smashed doors can't be closed - monsters can follow
