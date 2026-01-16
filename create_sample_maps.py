#!/usr/bin/env python3
"""
Create sample predesigned dungeon maps
"""
from dungeon_map import DungeonMap, Tile


def create_level_1():
    """Create first level - Simple cross layout"""
    dungeon = DungeonMap(width=50, height=20)
    
    # Top room
    for y in range(2, 7):
        for x in range(20, 30):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Vertical corridor
    for y in range(7, 13):
        for x in range(23, 27):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Bottom room
    for y in range(13, 18):
        for x in range(15, 35):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Left room
    for y in range(8, 12):
        for x in range(5, 23):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Right room
    for y in range(8, 12):
        for x in range(27, 45):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Place stairs
    dungeon.stairs_up = (25, 3)
    dungeon.stairs_down = (25, 16)
    dungeon.tiles[3][25] = Tile(Tile.STAIRS_UP, blocked=False)
    dungeon.tiles[16][25] = Tile(Tile.STAIRS_DOWN, blocked=False)
    
    # Place chests
    dungeon.place_chest(10, 10)
    dungeon.place_chest(40, 10)
    dungeon.place_chest(20, 15)
    
    return dungeon


def create_level_2():
    """Create second level - Large hall with chambers"""
    dungeon = DungeonMap(width=50, height=20)
    
    # Central hall
    for y in range(5, 15):
        for x in range(10, 40):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Top left chamber
    for y in range(2, 5):
        for x in range(12, 20):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Top right chamber
    for y in range(2, 5):
        for x in range(30, 38):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Bottom left chamber
    for y in range(15, 18):
        for x in range(12, 20):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Bottom right chamber
    for y in range(15, 18):
        for x in range(30, 38):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Connect chambers to hall
    for y in range(5, 7):
        dungeon.tiles[y][16] = Tile.create_floor()
        dungeon.tiles[y][34] = Tile.create_floor()
    
    for y in range(14, 16):
        dungeon.tiles[y][16] = Tile.create_floor()
        dungeon.tiles[y][34] = Tile.create_floor()
    
    # Place stairs
    dungeon.stairs_up = (25, 7)
    dungeon.stairs_down = (25, 12)
    dungeon.tiles[7][25] = Tile(Tile.STAIRS_UP, blocked=False)
    dungeon.tiles[12][25] = Tile(Tile.STAIRS_DOWN, blocked=False)
    
    # Place chests
    dungeon.place_chest(16, 3)
    dungeon.place_chest(34, 3)
    dungeon.place_chest(16, 16)
    dungeon.place_chest(34, 16)
    
    return dungeon


def create_level_3():
    """Create third level - Maze-like"""
    dungeon = DungeonMap(width=50, height=20)
    
    # Create a maze pattern
    # Base floor area
    for y in range(2, 18):
        for x in range(5, 45):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Add internal walls to create maze
    # Vertical walls
    for y in range(4, 16):
        if y not in [8, 9, 10]:
            dungeon.tiles[y][15] = Tile.create_wall()
            dungeon.tiles[y][25] = Tile.create_wall()
            dungeon.tiles[y][35] = Tile.create_wall()
    
    # Horizontal walls
    for x in range(7, 43):
        if x not in [15, 25, 35]:
            if x < 23 or x > 27:
                dungeon.tiles[6][x] = Tile.create_wall()
            if x < 13 or x > 17:
                dungeon.tiles[13][x] = Tile.create_wall()
    
    # Place stairs
    dungeon.stairs_up = (10, 3)
    dungeon.stairs_down = (40, 16)
    dungeon.tiles[3][10] = Tile(Tile.STAIRS_UP, blocked=False)
    dungeon.tiles[16][40] = Tile(Tile.STAIRS_DOWN, blocked=False)
    
    # Place chests in corners
    dungeon.place_chest(7, 4)
    dungeon.place_chest(42, 4)
    dungeon.place_chest(7, 15)
    dungeon.place_chest(20, 10)
    
    return dungeon


def main():
    """Create and save sample dungeon levels"""
    print("Creating sample dungeon levels...")
    
    # Create three levels
    level1 = create_level_1()
    level2 = create_level_2()
    level3 = create_level_3()
    
    levels = [level1, level2, level3]
    
    # Save to file in maps directory
    import os
    os.makedirs("maps", exist_ok=True)
    filename = "maps/sample_dungeon.json"
    DungeonMap.save_multilevel_dungeon(levels, filename)
    
    print(f"Saved 3-level dungeon to {filename}")
    print("\nLevel dimensions:")
    for i, level in enumerate(levels, 1):
        print(f"  Level {i}: {level.width}x{level.height}")
        print(f"    Stairs up: {level.stairs_up}")
        print(f"    Stairs down: {level.stairs_down}")
        print(f"    Chests: {len(level.chests)}")
    
    # Test loading
    print("\nTesting load...")
    loaded_levels = DungeonMap.load_multilevel_dungeon(filename)
    print(f"Successfully loaded {len(loaded_levels)} levels")


if __name__ == "__main__":
    main()
