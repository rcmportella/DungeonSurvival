#!/usr/bin/env python3
"""
Create a mini test dungeon - small and quick for testing
"""
from dungeon_map import DungeonMap, Tile
import os


def create_mini_level_1():
    """Create a small single-room level"""
    dungeon = DungeonMap(width=30, height=15)
    
    # Single room
    for y in range(3, 12):
        for x in range(5, 25):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Place stairs
    dungeon.stairs_up = (10, 7)
    dungeon.stairs_down = (20, 7)
    dungeon.tiles[7][10] = Tile(Tile.STAIRS_UP, blocked=False)
    dungeon.tiles[7][20] = Tile(Tile.STAIRS_DOWN, blocked=False)
    
    # Add a single chest
    dungeon.place_chest(15, 7)
    
    return dungeon


def create_mini_level_2():
    """Create a small corridor level"""
    dungeon = DungeonMap(width=30, height=15)
    
    # Left room
    for y in range(5, 10):
        for x in range(3, 10):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Corridor
    for y in range(7, 8):
        for x in range(10, 20):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Right room
    for y in range(5, 10):
        for x in range(20, 27):
            dungeon.tiles[y][x] = Tile.create_floor()
    
    # Place stairs
    dungeon.stairs_up = (6, 7)
    dungeon.stairs_down = (24, 7)
    dungeon.tiles[7][6] = Tile(Tile.STAIRS_UP, blocked=False)
    dungeon.tiles[7][24] = Tile(Tile.STAIRS_DOWN, blocked=False)
    
    # Add chests
    dungeon.place_chest(6, 8)
    dungeon.place_chest(24, 8)
    
    return dungeon


def main():
    """Create and save mini test dungeon"""
    print("Creating mini test dungeon...")
    
    level1 = create_mini_level_1()
    level2 = create_mini_level_2()
    
    levels = [level1, level2]
    
    # Save to file in maps directory
    os.makedirs("maps", exist_ok=True)
    filename = "maps/mini_test_dungeon.json"
    DungeonMap.save_multilevel_dungeon(levels, filename)
    
    print(f"Saved 2-level mini dungeon to {filename}")
    print("\nLevel dimensions:")
    for i, level in enumerate(levels, 1):
        print(f"  Level {i}: {level.width}x{level.height}")
        print(f"    Stairs up: {level.stairs_up}")
        print(f"    Stairs down: {level.stairs_down}")
        print(f"    Chests: {len(level.chests)}")


if __name__ == "__main__":
    main()
