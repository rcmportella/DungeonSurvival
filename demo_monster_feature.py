#!/usr/bin/env python3
"""
Quick demo to show the predefined monster feature in action
"""
from game_state import GameState


def demo_predefined_monsters():
    """Show a visual demo of predefined vs random monsters"""
    
    print("\n" + "="*70)
    print(" PREDEFINED MONSTER PLACEMENT DEMO")
    print("="*70)
    
    # Demo 1: Predefined monsters
    print("\n1. LOADING MAP WITH PREDEFINED MONSTERS (mixed_spawn_example.json)")
    print("-" * 70)
    
    game = GameState(use_predesigned=True, map_file='maps/mixed_spawn_example.json')
    game.initialize_game()
    
    print(f"\nMap Preview (Level 1 - Predefined Monsters):")
    print(game.current_map.render(game.party.position[0], game.party.position[1]))
    
    print(f"\nMonsters on this level:")
    for monster, x, y in game.current_map.monsters:
        print(f"  • {monster.name:20s} at ({x:2d}, {y:2d}) - HP: {monster.current_hp:2d}/{monster.max_hp:2d}, AC: {monster.armor_class}")
    
    # Demo 2: Random spawning
    print("\n\n2. RANDOM MONSTER SPAWNING (same file, level 2)")
    print("-" * 70)
    
    # Move to level 2
    game.dungeon_level = 2
    game.visited_levels = {}
    game.generate_dungeon_level()
    
    if game.current_map.stairs_up:
        game.party.position = list(game.current_map.stairs_up)
    
    game.current_map.update_fov(
        game.party.position[0],
        game.party.position[1],
        radius=3
    )
    
    print(f"\nMap Preview (Level 2 - Random Spawn):")
    print(game.current_map.render(game.party.position[0], game.party.position[1]))
    
    print(f"\nMonsters on this level (randomly spawned):")
    for monster, x, y in game.current_map.monsters:
        print(f"  • {monster.name:20s} at ({x:2d}, {y:2d}) - HP: {monster.current_hp:2d}/{monster.max_hp:2d}, AC: {monster.armor_class}")
    
    # Demo 3: Show mini_test_dungeon
    print("\n\n3. MINI TEST DUNGEON (predefined guards)")
    print("-" * 70)
    
    game2 = GameState(use_predesigned=True, map_file='maps/mini_test_dungeon.json')
    game2.initialize_game()
    
    print(f"\nMap Preview:")
    print(game2.current_map.render(game2.party.position[0], game2.party.position[1]))
    
    print(f"\nGuarding monsters (predefined):")
    for monster, x, y in game2.current_map.monsters:
        print(f"  • {monster.name:20s} at ({x:2d}, {y:2d}) - HP: {monster.current_hp:2d}/{monster.max_hp:2d}, AC: {monster.armor_class}")
    
    print("\n" + "="*70)
    print(" FEATURE SUMMARY")
    print("="*70)
    print("""
The framework now supports TWO monster spawning modes:

1. PREDEFINED PLACEMENT (JSON files with monsters array)
   - Define exact monster types and positions
   - Perfect for boss fights and scripted encounters
   - Consistent gameplay experience
   
2. RANDOM SPAWNING (empty/missing monsters array)
   - Automatically populates levels with appropriate monsters
   - High replayability
   - Dynamic difficulty scaling

You can MIX both approaches in a single dungeon file!
- Level 1: Predefined boss encounter
- Level 2: Random exploration
- Level 3: Predefined ambush
- Etc.

See MONSTER_PLACEMENT_GUIDE.md for detailed documentation.
""")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_predefined_monsters()
