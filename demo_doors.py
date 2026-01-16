#!/usr/bin/env python3
"""
Quick demo of the door system
"""
from door import create_easy_door, create_medium_door, create_hard_door
from character import Character


def demo_door_system():
    """Demonstrate door mechanics"""
    
    print("="*70)
    print(" DOOR SYSTEM DEMONSTRATION")
    print("="*70)
    
    # Create test characters
    print("\n1. Creating test characters...")
    
    rogue = Character("Sneaky Pete", "Rogue", level=3)
    rogue.set_abilities(10, 16, 12, 14, 12, 10)  # High DEX
    print(f"   {rogue.name} - Rogue Level {rogue.level}")
    print(f"   DEX: {rogue.dexterity} (Modifier: {rogue.get_ability_modifier('dexterity')})")
    
    fighter = Character("Smash McGee", "Fighter", level=3)
    fighter.set_abilities(18, 10, 14, 10, 10, 10)  # High STR
    print(f"   {fighter.name} - Fighter Level {fighter.level}")
    print(f"   STR: {fighter.strength} (Modifier: {fighter.get_ability_modifier('strength')})")
    
    # Demo unlocked door
    print("\n" + "="*70)
    print("2. UNLOCKED DOOR")
    print("="*70)
    
    door = create_easy_door()
    door.is_locked = False
    print(f"   Door: {door}")
    success, message = door.attempt_open(rogue)
    print(f"   Action: {message}")
    print(f"   Result: Door is {'passable' if door.is_passable() else 'blocked'}")
    
    # Demo lockpicking
    print("\n" + "="*70)
    print("3. LOCKPICKING (Rogue)")
    print("="*70)
    
    door = create_medium_door()
    print(f"   Door: {door}")
    print(f"   Lockpick DC: {door.lockpick_dc}")
    print(f"   Rogue Bonus: Level({rogue.level}) + DEX({rogue.get_ability_modifier('dexterity')}) = {rogue.level + rogue.get_ability_modifier('dexterity')}")
    
    for attempt in range(1, 4):
        if door.is_locked:
            success, message = door.attempt_lockpick(rogue)
            print(f"   Attempt {attempt}: {message}")
            if success:
                break
        else:
            break
    
    # Demo smashing
    print("\n" + "="*70)
    print("4. SMASHING (Fighter)")
    print("="*70)
    
    door = create_medium_door()
    print(f"   Door: {door}")
    print(f"   Smash DC: {door.smash_dc}")
    str_mod = fighter.get_ability_modifier('strength')
    level_bonus = fighter.level // 2
    print(f"   Fighter Bonus: STR({str_mod}) + Level/2({level_bonus}) = {str_mod + level_bonus}")
    
    for attempt in range(1, 4):
        if not door.is_open:
            success, message = door.attempt_smash(fighter)
            print(f"   Attempt {attempt}: {message}")
            if success:
                print(f"   Final state: {door}")
                break
        else:
            break
    
    # Demo difficulty levels
    print("\n" + "="*70)
    print("5. DIFFICULTY LEVELS")
    print("="*70)
    
    easy = create_easy_door()
    medium = create_medium_door()
    hard = create_hard_door()
    
    print(f"\n   Easy Door:")
    print(f"     Lockpick DC: {easy.lockpick_dc} | Smash DC: {easy.smash_dc}")
    print(f"     Best for: Level 1-2 characters")
    
    print(f"\n   Medium Door:")
    print(f"     Lockpick DC: {medium.lockpick_dc} | Smash DC: {medium.smash_dc}")
    print(f"     Best for: Level 3-5 characters")
    
    print(f"\n   Hard Door:")
    print(f"     Lockpick DC: {hard.lockpick_dc} | Smash DC: {hard.smash_dc}")
    print(f"     Best for: Level 6+ characters")
    
    # Demo map integration
    print("\n" + "="*70)
    print("6. MAP INTEGRATION")
    print("="*70)
    
    print("\n   In your map JSON file, add:")
    print('''
   "doors": [
     {
       "horizontal": false,
       "locked": true,
       "lockpick_dc": 15,
       "smash_dc": 18,
       "position": [10, 5]
     }
   ]
    ''')
    
    print("\n   See maps/door_example.json for complete examples!")
    
    # Summary
    print("\n" + "="*70)
    print(" SUMMARY")
    print("="*70)
    print("""
   Door System Features:
   ✓ Open/Closed states
   ✓ Locked/Unlocked mechanics
   ✓ Lockpicking with DEX-based skill checks
   ✓ Smashing with STR-based checks
   ✓ Class bonuses (Rogues for lockpicking, Fighters for smashing)
   ✓ Multiple difficulty levels
   ✓ Persistent state (destroyed doors stay destroyed)
   ✓ Map JSON integration
   ✓ In-game controls (L for lockpick, S for smash)
   
   Player Controls:
   - Walk into unlocked door → Opens automatically
   - Walk into locked door → Shows options
   - Press L → Attempt lockpick
   - Press S → Attempt smash
   - Move away → Cancel
   
   See DOOR_SYSTEM_GUIDE.md for full documentation!
    """)
    print("="*70)


if __name__ == "__main__":
    demo_door_system()
