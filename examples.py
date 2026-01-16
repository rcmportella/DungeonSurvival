"""
Example: How to customize and extend DungeonSurvival

This file demonstrates how to:
1. Create custom characters
2. Create custom monsters
3. Customize dungeon generation
4. Create custom game scenarios
"""

from character import Character
from monster import Monster
from party import Party
from dungeon_map import DungeonMap
from game_state import GameState


def create_custom_party():
    """Example: Create a custom party with specific characters"""
    party = Party()
    
    # Create a tank fighter
    tank = Character("Bjorn the Bold", "Fighter", level=3)
    tank.set_abilities(str_score=18, dex=12, con=16, int_score=8, wis=10, cha=8)
    party.add_member(tank)
    
    # Create a glass cannon wizard
    wizard = Character("Elara Starweaver", "Wizard", level=3)
    wizard.set_abilities(str_score=8, dex=14, con=10, int_score=18, wis=14, cha=12)
    party.add_member(wizard)
    
    # Create a stealthy rogue
    rogue = Character("Shadow", "Rogue", level=3)
    rogue.set_abilities(str_score=12, dex=18, con=12, int_score=14, wis=10, cha=14)
    party.add_member(rogue)
    
    # Create a support cleric
    cleric = Character("Brother Marcus", "Cleric", level=3)
    cleric.set_abilities(str_score=14, dex=10, con=14, int_score=10, wis=16, cha=14)
    party.add_member(cleric)
    
    return party


def create_boss_monster():
    """Example: Create a powerful boss monster"""
    dragon = Monster(
        name="Young Red Dragon",
        hit_dice="10d8+20",
        armor_class=18,
        attack_bonus=8,
        damage="2d6+6",
        special_abilities=["Fire Breath", "Flight", "Frightful Presence"],
        treasure=["500 gold", "Magic Sword +1", "Ring of Protection"]
    )
    return dragon


def create_themed_monsters():
    """Example: Create a set of themed monsters for a specific dungeon type"""
    
    # Undead crypt theme
    undead_monsters = [
        Monster("Skeleton Warrior", "2d8", 13, 2, "1d8"),
        Monster("Zombie", "2d8+4", 11, 1, "1d6+2"),
        Monster("Ghoul", "3d8", 14, 3, "1d6+1"),
        Monster("Wight", "4d8+8", 15, 4, "1d8+2"),
    ]
    
    # Goblin warren theme
    goblin_monsters = [
        Monster("Goblin", "1d8", 12, 1, "1d6"),
        Monster("Hobgoblin", "2d8+2", 14, 2, "1d8"),
        Monster("Bugbear", "3d8+3", 13, 3, "2d6+2"),
        Monster("Goblin Shaman", "2d8", 13, 2, "1d6", special_abilities=["Cast Magic Missile"]),
    ]
    
    return {
        'undead_crypt': undead_monsters,
        'goblin_warren': goblin_monsters
    }


def create_large_dungeon():
    """Example: Create a larger, more complex dungeon"""
    large_map = DungeonMap(width=120, height=60)
    
    # Generate with more rooms
    large_map.generate(
        max_rooms=20,
        min_room_size=5,
        max_room_size=15
    )
    
    return large_map


def create_small_arena():
    """Example: Create a small arena for combat encounters"""
    arena = DungeonMap(width=30, height=20)
    
    # Generate with few, smaller rooms
    arena.generate(
        max_rooms=3,
        min_room_size=3,
        max_room_size=8
    )
    
    return arena


def setup_boss_encounter():
    """Example: Setup a specific boss encounter scenario"""
    # Create a custom game state
    game = GameState()
    
    # Create powerful party
    game.party = create_custom_party()
    
    # Create small boss arena
    game.current_map = create_small_arena()
    
    # Place boss in the last room
    if game.current_map.rooms:
        boss = create_boss_monster()
        boss_x, boss_y = game.current_map.rooms[-1].center()
        game.current_map.place_monster(boss, boss_x, boss_y)
    
    # Place party at first room
    if game.current_map.rooms:
        party_x, party_y = game.current_map.rooms[0].center()
        game.party.position = [party_x, party_y]
    
    game.add_message("Boss encounter: Prepare for battle!")
    
    return game


def customize_monster_spawn_rates():
    """Example: Create custom monster spawn logic"""
    import random
    
    def spawn_dungeon_level_monsters(dungeon_level):
        """Spawn monsters appropriate for dungeon level"""
        
        # Define monster pools by difficulty
        easy_monsters = [
            lambda: Monster("Rat", "1d4", 10, 0, "1d3"),
            lambda: Monster("Kobold", "1d6", 12, 0, "1d4"),
            lambda: Monster("Goblin", "1d8", 12, 1, "1d6"),
        ]
        
        medium_monsters = [
            lambda: Monster("Orc", "2d8", 13, 2, "1d8+1"),
            lambda: Monster("Skeleton", "1d8", 13, 1, "1d6"),
            lambda: Monster("Wolf", "2d8+2", 14, 2, "1d6+1"),
        ]
        
        hard_monsters = [
            lambda: Monster("Ogre", "4d8+8", 13, 5, "2d6+3"),
            lambda: Monster("Troll", "6d8+18", 15, 6, "1d6+4"),
            lambda: Monster("Wraith", "5d8", 15, 5, "1d8+2"),
        ]
        
        # Select monster pool based on level
        if dungeon_level <= 2:
            pool = easy_monsters
        elif dungeon_level <= 5:
            pool = easy_monsters + medium_monsters
        elif dungeon_level <= 8:
            pool = medium_monsters + hard_monsters
        else:
            pool = hard_monsters
        
        # Return a random monster from the pool
        return random.choice(pool)()
    
    return spawn_dungeon_level_monsters


# Example usage
if __name__ == "__main__":
    print("DungeonSurvival Framework Examples")
    print("=" * 60)
    print()
    
    # Example 1: Custom party
    print("1. Creating custom party...")
    party = create_custom_party()
    print(f"   Created party with {len(party)} members:")
    for member in party:
        print(f"   - {member.name} ({member.char_class}, Level {member.level})")
    print()
    
    # Example 2: Boss monster
    print("2. Creating boss monster...")
    boss = create_boss_monster()
    print(f"   {boss.name}: AC {boss.armor_class}, HP {boss.max_hp}")
    print(f"   Special abilities: {', '.join(boss.special_abilities)}")
    print()
    
    # Example 3: Themed monsters
    print("3. Creating themed monster sets...")
    themed = create_themed_monsters()
    for theme, monsters in themed.items():
        print(f"   {theme}: {len(monsters)} monster types")
    print()
    
    # Example 4: Large dungeon
    print("4. Generating large dungeon...")
    large = create_large_dungeon()
    print(f"   Created {large.width}x{large.height} dungeon with {len(large.rooms)} rooms")
    print()
    
    # Example 5: Boss encounter
    print("5. Setting up boss encounter...")
    boss_game = setup_boss_encounter()
    print(f"   Boss arena ready with {len(boss_game.party)} heroes")
    print(f"   Map size: {boss_game.current_map.width}x{boss_game.current_map.height}")
    print()
    
    # Example 6: Custom spawn rates
    print("6. Testing custom spawn rates...")
    spawner = customize_monster_spawn_rates()
    for level in [1, 3, 5, 7, 10]:
        monster = spawner(level)
        print(f"   Level {level}: {monster.name} (AC {monster.armor_class}, HP {monster.max_hp})")
    print()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print()
    print("Use these examples as templates to customize your game.")
