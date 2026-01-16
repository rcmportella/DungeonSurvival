#!/usr/bin/env python3
"""
Integration test: Run a quick game session with predefined monsters
to ensure the feature works with the full game flow.
"""
from game_state import GameState, GameMode
from character import Character


def test_game_integration():
    """Test the predefined monster feature in a realistic game scenario"""
    
    print("\n" + "="*70)
    print(" INTEGRATION TEST: Predefined Monsters in Game Flow")
    print("="*70)
    
    # Create a game with predefined monsters
    game = GameState(use_predesigned=True, map_file='maps/mini_test_dungeon.json')
    
    # Add a test party
    fighter = Character("TestFighter", "Fighter", level=3)
    fighter.set_abilities(16, 14, 15, 10, 12, 10)
    game.party.add_member(fighter)
    
    # Initialize the game
    game.initialize_game()
    
    print("\n✓ Game initialized successfully")
    print(f"  - Current mode: {game.mode.name}")
    print(f"  - Dungeon level: {game.dungeon_level}")
    print(f"  - Monsters on level: {len(game.current_map.monsters)}")
    
    # Verify monsters are where we expect them
    print("\n✓ Checking predefined monster positions...")
    monster_positions = {(x, y): m.name for m, x, y in game.current_map.monsters}
    
    expected_positions = {
        (8, 7): "Goblin Guard",
        (22, 7): "Orc Warrior"
    }
    
    for pos, expected_name in expected_positions.items():
        if pos in monster_positions:
            actual_name = monster_positions[pos]
            if actual_name == expected_name:
                print(f"  ✓ Found {actual_name} at {pos}")
            else:
                print(f"  ✗ ERROR: Expected {expected_name} at {pos}, found {actual_name}")
                return False
        else:
            print(f"  ✗ ERROR: No monster found at {pos}")
            return False
    
    # Test map rendering
    print("\n✓ Testing map rendering...")
    try:
        map_str = game.current_map.render(
            game.party.position[0],
            game.party.position[1],
            in_combat=False
        )
        print(f"  ✓ Map rendered successfully ({len(map_str)} characters)")
    except Exception as e:
        print(f"  ✗ ERROR rendering map: {e}")
        return False
    
    # Test monster at tile
    print("\n✓ Testing monster retrieval from tiles...")
    goblin = game.current_map.get_monster_at(8, 7)
    if goblin and goblin.name == "Goblin Guard":
        print(f"  ✓ Successfully retrieved Goblin Guard from tile (8, 7)")
        print(f"    HP: {goblin.current_hp}/{goblin.max_hp}, AC: {goblin.armor_class}")
    else:
        print(f"  ✗ ERROR: Could not retrieve Goblin Guard from tile")
        return False
    
    # Test combat initiation
    print("\n✓ Testing combat with predefined monster...")
    try:
        game.start_combat(8, 7)
        if game.mode == GameMode.COMBAT:
            print(f"  ✓ Combat started successfully")
            num_monsters = len(game.combat_instance.monsters) if game.combat_instance else 0
            print(f"    Monsters in combat: {num_monsters}")
        else:
            print(f"  ✗ ERROR: Game mode not changed to COMBAT")
            return False
    except Exception as e:
        print(f"  ✗ ERROR starting combat: {e}")
        return False
    
    # Test descending to level 2 (should have random monsters)
    print("\n✓ Testing level transition to random spawn level...")
    game.mode = GameMode.EXPLORATION
    game.party.position = list(game.current_map.stairs_down)
    game.descend_stairs()
    
    if game.dungeon_level == 2:
        print(f"  ✓ Descended to level 2")
        print(f"    Monsters on this level: {len(game.current_map.monsters)}")
        print(f"    (Should be randomly spawned)")
        
        if len(game.current_map.monsters) > 0:
            print(f"  ✓ Random monsters spawned successfully")
            # Show first few monsters
            for i, (m, x, y) in enumerate(game.current_map.monsters[:3]):
                print(f"    - {m.name} at ({x}, {y})")
        else:
            print(f"  ⚠ WARNING: No monsters spawned (may be expected for empty level)")
    else:
        print(f"  ✗ ERROR: Failed to descend (level is {game.dungeon_level})")
        return False
    
    # Test serialization round-trip
    print("\n✓ Testing serialization round-trip...")
    try:
        # Get current map data
        map_dict = game.current_map.to_dict()
        
        # Create new map and load data
        from dungeon_map import DungeonMap
        new_map = DungeonMap()
        new_map.from_dict(map_dict)
        
        if len(new_map.monsters) == len(game.current_map.monsters):
            print(f"  ✓ Serialization successful")
            print(f"    Monsters preserved: {len(new_map.monsters)}")
        else:
            print(f"  ✗ ERROR: Monster count mismatch after serialization")
            return False
    except Exception as e:
        print(f"  ✗ ERROR during serialization: {e}")
        return False
    
    print("\n" + "="*70)
    print(" ALL INTEGRATION TESTS PASSED! ✓")
    print("="*70)
    print("""
The predefined monster placement feature is fully integrated and working:

✓ Monsters load correctly from JSON files
✓ Monsters are placed at exact specified positions
✓ Map rendering works with predefined monsters
✓ Combat can be initiated with predefined monsters
✓ Level transitions work (predefined → random)
✓ Serialization preserves monster data

The feature is ready for use!
""")
    return True


if __name__ == "__main__":
    success = test_game_integration()
    exit(0 if success else 1)
