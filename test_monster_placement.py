#!/usr/bin/env python3
"""
Test script for predefined monster placement feature
"""
from dungeon_map import DungeonMap
from game_state import GameState
from character import Character
from party import Party


def test_predefined_monsters():
    """Test loading a map with predefined monsters"""
    print("="*60)
    print("TEST 1: Loading map with predefined monsters")
    print("="*60)
    
    # Load the mixed spawn example
    game = GameState(use_predesigned=True, map_file='maps/mixed_spawn_example.json')
    game.initialize_game()
    
    # Check level 1 (should have 5 predefined monsters)
    print(f"\nLevel 1:")
    print(f"  Number of monsters: {len(game.current_map.monsters)}")
    print(f"  Predefined: Yes" if game.current_map.monsters else "  Random spawn")
    
    for monster, x, y in game.current_map.monsters:
        print(f"    - {monster.name} at ({x}, {y})")
        print(f"      HP: {monster.current_hp}/{monster.max_hp}, AC: {monster.armor_class}")
    
    # Move to level 2 (should have random monsters)
    game.dungeon_level = 2
    game.visited_levels = {}  # Clear visited levels to force regeneration
    game.generate_dungeon_level()
    
    print(f"\nLevel 2:")
    print(f"  Number of monsters: {len(game.current_map.monsters)}")
    print(f"  Random spawn: Yes" if game.current_map.monsters else "  No monsters")
    
    for monster, x, y in game.current_map.monsters:
        print(f"    - {monster.name} at ({x}, {y})")
        print(f"      HP: {monster.current_hp}/{monster.max_hp}, AC: {monster.armor_class}")
    
    print("\n" + "="*60)
    print("TEST 2: Loading mini_test_dungeon with predefined monsters")
    print("="*60)
    
    game2 = GameState(use_predesigned=True, map_file='maps/mini_test_dungeon.json')
    game2.initialize_game()
    
    print(f"\nLevel 1:")
    print(f"  Number of monsters: {len(game2.current_map.monsters)}")
    
    for monster, x, y in game2.current_map.monsters:
        print(f"    - {monster.name} at ({x}, {y})")
        print(f"      HP: {monster.current_hp}/{monster.max_hp}, AC: {monster.armor_class}")
    
    print("\n" + "="*60)
    print("TEST 3: Random generation (no predesigned map)")
    print("="*60)
    
    game3 = GameState(use_predesigned=False)
    game3.initialize_game()
    
    print(f"\nRandomly generated level:")
    print(f"  Number of monsters: {len(game3.current_map.monsters)}")
    print(f"  All randomly spawned")
    
    for monster, x, y in game3.current_map.monsters[:5]:  # Show first 5
        print(f"    - {monster.name} at ({x}, {y})")
        print(f"      HP: {monster.current_hp}/{monster.max_hp}, AC: {monster.armor_class}")
    
    if len(game3.current_map.monsters) > 5:
        print(f"    ... and {len(game3.current_map.monsters) - 5} more")
    
    print("\n" + "="*60)
    print("TEST 4: Serialization test")
    print("="*60)
    
    # Test that we can serialize and deserialize a map with monsters
    test_map = DungeonMap(width=50, height=25)
    test_map.generate(max_rooms=3, min_room_size=3, max_room_size=6)
    
    # Add some monsters
    from monster import Monster
    goblin = Monster("Test Goblin", "2d8", 13, 2, "1d6+1")
    
    # Find a valid floor tile to place the monster
    for y in range(test_map.height):
        for x in range(test_map.width):
            if not test_map.is_blocked(x, y):
                test_map.place_monster(goblin, x, y)
                break
        if test_map.monsters:
            break
    
    # Serialize
    map_dict = test_map.to_dict()
    print(f"\nSerialized map has {len(map_dict['monsters'])} monster(s)")
    
    # Deserialize
    new_map = DungeonMap()
    new_map.from_dict(map_dict)
    print(f"Deserialized map has {len(new_map.monsters)} monster(s)")
    
    if new_map.monsters:
        m, x, y = new_map.monsters[0]
        print(f"  Monster: {m.name} at ({x}, {y})")
        print(f"  HP: {m.current_hp}/{m.max_hp}, AC: {m.armor_class}")
    
    print("\n" + "="*60)
    print("All tests completed successfully!")
    print("="*60)


if __name__ == "__main__":
    test_predefined_monsters()
