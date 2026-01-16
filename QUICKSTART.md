# Quick Start Guide - DungeonSurvival

## Getting Started in 5 Minutes

### 1. Verify Installation

```bash
cd /home/ricardo/Documentos/Projects/DungeonSurvival
python3 -c "import character, monster, dice; print('✓ Ready to play!')"
```

### 2. Run the Game

```bash
python3 main.py
```

### 3. Basic Controls

**Movement:**
- Arrow Keys or WASD to move your party
- Explore the dungeon looking for treasure

**When you find monsters:**
- Press `A` to attack
- Press `F` to flee

**Finding features:**
- `$` symbols are treasure chests (walk over them)
- `<` are stairs down to deeper levels
- `>` are stairs up (escape the dungeon)

### 4. Understanding the Display

```
================================================================================
 DUNGEON SURVIVAL - Level 1 | Turn 5
================================================================================

#######################
#.....................#
#...........G.........#     <- Map view (G = Goblin)
#...........#.........#
#######################

--------------------------------------------------------------------------------
Party:
  1. Warrior (Fighter) [██████████] 10/10 HP
  2. Mage (Wizard) [████░░░░░░] 4/6 HP        <- Your party status
  3. Healer (Cleric) [████████░░] 8/10 HP

--------------------------------------------------------------------------------
Messages:
  Welcome to Dungeon Survival!                <- Recent events
  Your quest: Survive and collect treasure!
  You moved north

--------------------------------------------------------------------------------
Controls: Arrow keys/WASD to move | D: descend | U: ascend | Q: quit
================================================================================
```

## Your First Adventure

### Step-by-Step Tutorial

1. **Start the Game**
   ```bash
   python3 main.py
   ```

2. **Orient Yourself**
   - You start as `1` on the map
   - Look for `$` (treasure) and avoid monsters at first

3. **Move to a Treasure Chest**
   - Use arrow keys to reach a `$`
   - You'll automatically collect gold

4. **Engage a Monster**
   - Move into a letter (e.g., `G` for Goblin)
   - Combat starts automatically

5. **Combat**
   - Press `A` to attack
   - Watch the combat messages
   - Keep attacking until victory or press `F` to flee

6. **Explore Deeper**
   - Find the `<` stairs
   - Press `D` to descend
   - Face tougher monsters for better rewards

7. **Escape**
   - Return to level 1
   - Find the `>` stairs
   - Press `U` to win the game!

## Tips for Success

### Combat Tips
- **Flee if necessary**: Press `F` if your HP is low
- **Attack order**: Focus on one enemy at a time
- **HP management**: Keep your party healthy

### Exploration Tips
- **Map everything**: Explore all rooms before descending
- **Collect gold**: You'll need it for future upgrades
- **Watch your HP**: No healing between levels yet

### Strategy
- **Level 1**: Easy monsters, learn the controls
- **Level 2-3**: Moderate difficulty, collect gold
- **Level 4+**: Hard monsters, high rewards
- **Escape**: Return to level 1 and exit for victory

## Common Questions

**Q: How do I save the game?**
A: Currently no save system - play in one session

**Q: Can I customize my party?**
A: Yes! Edit the `create_default_party()` function in main.py

**Q: How do I heal?**
A: Healing items not yet implemented - manage HP carefully

**Q: What happens if my party dies?**
A: Game over - restart and try again!

**Q: Can I use spells?**
A: Spell system is partially implemented, press `S` in combat

## Example Play Session

```
Turn 1: Move east, exploring first room
Turn 2: Find treasure chest, gain 25 gold
Turn 3: Move north into corridor
Turn 4: Encounter Goblin!
Turn 5-7: Fight Goblin (Attack! Attack! Attack!)
Turn 8: Victory! Gain 100 XP
Turn 9: Move to stairs down
Turn 10: Descend to level 2
...
Turn 50: Return to level 1
Turn 51: Ascend stairs and escape!
VICTORY!
```

## Next Steps

Once you're comfortable with the basics:

1. **Check examples.py** for customization ideas
   ```bash
   python3 examples.py
   ```

2. **Read README.md** for complete documentation

3. **Explore ARCHITECTURE.md** to understand the code

4. **Modify config.py** to adjust game difficulty

5. **Create custom monsters** using the Monster class

6. **Design custom dungeons** with DungeonMap

## Troubleshooting

**Problem: Arrow keys don't work**
- Try using WASD keys instead
- Check terminal compatibility

**Problem: Display looks wrong**
- Increase terminal window size (minimum 80x30)
- Use a monospaced font

**Problem: Game crashes**
- Check Python version (need 3.6+)
- Run the test: `python3 examples.py`

**Problem: Can't quit**
- Press `Q` to quit
- Or use Ctrl+C as emergency exit

## Have Fun!

DungeonSurvival is a framework - customize it to make it your own!

Check out the examples and documentation to learn how to:
- Create new character classes
- Design custom monsters
- Add new spells
- Create unique dungeon types
- Implement new game mechanics

Happy dungeon crawling! 🗡️🐉💰
