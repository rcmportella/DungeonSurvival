"""
Dungeon map generation and rendering
"""
import random
import json


class Tile:
    """Represents a single tile on the map"""
    
    FLOOR = '.'
    WALL = '#'
    DOOR_HORIZONTAL = '-'
    DOOR_VERTICAL = '|'
    CHEST = '$'
    STAIRS_DOWN = '<'
    STAIRS_UP = '>'
    PARTY = '1'
    
    def __init__(self, char=FLOOR, blocked=False, block_sight=False):
        self.char = char
        self.blocked = blocked
        self.block_sight = block_sight
        self.explored = False
        self.visible = False
        self.monster = None  # Reference to monster on this tile
        self.door = None  # Reference to door on this tile
        
    @staticmethod
    def create_wall():
        """Create a wall tile"""
        return Tile(Tile.WALL, blocked=True, block_sight=True)
        
    @staticmethod
    def create_floor():
        """Create a floor tile"""
        return Tile(Tile.FLOOR, blocked=False, block_sight=False)
        
    @staticmethod
    def create_door(horizontal=True):
        """Create a door tile"""
        char = Tile.DOOR_HORIZONTAL if horizontal else Tile.DOOR_VERTICAL
        return Tile(char, blocked=True, block_sight=True)


class Room:
    """Represents a rectangular room in the dungeon"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def center(self):
        """Return center coordinates of the room"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return (center_x, center_y)
        
    def intersects(self, other):
        """Check if this room intersects with another room"""
        return (self.x <= other.x + other.width and
                self.x + self.width >= other.x and
                self.y <= other.y + other.height and
                self.y + self.height >= other.y)


class DungeonMap:
    """
    Dungeon map with procedural generation
    """
    
    def __init__(self, width=80, height=40):
        self.width = width
        self.height = height
        self.tiles = [[Tile.create_wall() for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.monsters = []  # List of (monster, x, y) tuples
        self.chests = []    # List of (x, y) tuples
        self.doors = []     # List of (door, x, y) tuples
        self.stairs_down = None
        self.stairs_up = None
        
    def generate(self, max_rooms=10, min_room_size=4, max_room_size=10):
        """Generate a random dungeon with rooms and corridors"""
        for _ in range(max_rooms):
            # Random room size
            w = random.randint(min_room_size, max_room_size)
            h = random.randint(min_room_size, max_room_size)
            # Random position
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)
            
            new_room = Room(x, y, w, h)
            
            # Check if room intersects with existing rooms
            if not any(new_room.intersects(other) for other in self.rooms):
                self._create_room(new_room)
                
                # Connect to previous room with a corridor
                if self.rooms:
                    prev_center = self.rooms[-1].center()
                    new_center = new_room.center()
                    
                    if random.random() < 0.5:
                        # Horizontal then vertical
                        self._create_h_tunnel(prev_center[0], new_center[0], prev_center[1])
                        self._create_v_tunnel(prev_center[1], new_center[1], new_center[0])
                    else:
                        # Vertical then horizontal
                        self._create_v_tunnel(prev_center[1], new_center[1], prev_center[0])
                        self._create_h_tunnel(prev_center[0], new_center[0], new_center[1])
                        
                self.rooms.append(new_room)
                
        # Place stairs
        if self.rooms:
            first_room = self.rooms[0].center()
            last_room = self.rooms[-1].center()
            self.stairs_up = first_room
            self.stairs_down = last_room
            self.tiles[first_room[1]][first_room[0]] = Tile(Tile.STAIRS_UP)
            self.tiles[last_room[1]][last_room[0]] = Tile(Tile.STAIRS_DOWN)
            
    def _create_room(self, room):
        """Create floor tiles for a room"""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.tiles[y][x] = Tile.create_floor()
                    
    def _create_h_tunnel(self, x1, x2, y):
        """Create a horizontal tunnel"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = Tile.create_floor()
                
    def _create_v_tunnel(self, y1, y2, x):
        """Create a vertical tunnel"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = Tile.create_floor()
                
    def is_blocked(self, x, y):
        """Check if a tile blocks movement"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        return self.tiles[y][x].blocked
        
    def place_monster(self, monster, x, y):
        """Place a monster on the map"""
        if not self.is_blocked(x, y):
            self.monsters.append((monster, x, y))
            self.tiles[y][x].monster = monster
            return True
        return False
        
    def remove_monster(self, x, y):
        """Remove a monster from the map"""
        self.monsters = [(m, mx, my) for m, mx, my in self.monsters if not (mx == x and my == y)]
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x].monster = None
            
    def get_monster_at(self, x, y):
        """Get monster at specified position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x].monster
        return None
        
    def place_chest(self, x, y):
        """Place a treasure chest"""
        if not self.is_blocked(x, y):
            self.chests.append((x, y))
            self.tiles[y][x].char = Tile.CHEST
            return True
        return False
        
    def place_door(self, door, x, y):
        """Place a door on the map"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.doors.append((door, x, y))
            self.tiles[y][x].door = door
            self.tiles[y][x].char = door.get_char()
            self.tiles[y][x].blocked = not door.is_passable()
            self.tiles[y][x].block_sight = door.is_blocking_sight()
            return True
        return False
        
    def get_door_at(self, x, y):
        """Get door at specified position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x].door
        return None
        
    def update_door_tile(self, x, y):
        """Update tile appearance and properties based on door state"""
        if 0 <= x < self.width and 0 <= y < self.height:
            door = self.tiles[y][x].door
            if door:
                self.tiles[y][x].char = door.get_char()
                self.tiles[y][x].blocked = not door.is_passable()
                self.tiles[y][x].block_sight = door.is_blocking_sight()
        
    def populate_monsters(self, monster_factory, count=5):
        """Populate dungeon with random monsters"""
        placed = 0
        attempts = 0
        max_attempts = count * 10
        
        while placed < count and attempts < max_attempts:
            attempts += 1
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            if not self.is_blocked(x, y) and not self.get_monster_at(x, y):
                monster = monster_factory()
                if self.place_monster(monster, x, y):
                    placed += 1
                    
    def update_fov(self, party_x, party_y, radius=3):
        """
        Update field of view around the party position
        
        Args:
            party_x, party_y: Party position
            radius: Vision radius (default 3)
        """
        # Clear all visible flags
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x].visible = False
        
        # Mark tiles within radius as visible and explored
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                # Calculate distance (using Chebyshev distance for square radius)
                distance = max(abs(dx), abs(dy))
                if distance <= radius:
                    tx = party_x + dx
                    ty = party_y + dy
                    
                    if 0 <= tx < self.width and 0 <= ty < self.height:
                        self.tiles[ty][tx].visible = True
                        self.tiles[ty][tx].explored = True
    
    def render(self, party_x, party_y, in_combat=False):
        """
        Render the map as ASCII with fog of war
        
        Args:
            party_x, party_y: Party position
            in_combat: If True, don't show party symbol (combat view)
        """
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                tile = self.tiles[y][x]
                
                # Show only explored tiles
                if not tile.explored:
                    line.append(' ')  # Unexplored area
                elif tile.visible:
                    # Currently visible
                    if x == party_x and y == party_y and not in_combat:
                        line.append(Tile.PARTY)
                    elif tile.monster and tile.monster.is_alive():
                        # Show monster as its first letter (uppercase)
                        line.append(tile.monster.name[0].upper())
                    else:
                        line.append(tile.char)
                else:
                    # Explored but not currently visible - show darker/grayed version
                    if tile.char == Tile.WALL:
                        line.append(Tile.WALL)
                    else:
                        line.append('·')  # Dimmed floor for explored areas
            lines.append(''.join(line))
        return '\n'.join(lines)
    
    def to_dict(self):
        """
        Convert map to dictionary for serialization
        
        Returns:
            Dictionary representation of the map
        """
        map_data = {
            'width': self.width,
            'height': self.height,
            'tiles': [],
            'stairs_up': self.stairs_up,
            'stairs_down': self.stairs_down,
            'chests': self.chests,
            'monsters': [],  # Add monsters list
            'doors': []  # Add doors list
        }
        
        # Save tile layout
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = self.tiles[y][x]
                row.append(tile.char)
            map_data['tiles'].append(''.join(row))
        
        # Save monsters with their positions and stats
        for monster, x, y in self.monsters:
            monster_data = {
                'name': monster.name,
                'hit_dice': monster.hit_dice,
                'armor_class': monster.armor_class,
                'attack_bonus': monster.attack_bonus,
                'damage': monster.damage,
                'position': [x, y]
            }
            map_data['monsters'].append(monster_data)
        
        # Save doors with their positions and state
        for door, x, y in self.doors:
            door_data = door.to_dict()
            door_data['position'] = [x, y]
            map_data['doors'].append(door_data)
        
        return map_data
    
    def from_dict(self, map_data):
        """
        Load map from dictionary
        
        Args:
            map_data: Dictionary representation of the map
        """
        from monster import Monster
        
        self.width = map_data['width']
        self.height = map_data['height']
        self.stairs_up = tuple(map_data['stairs_up']) if map_data['stairs_up'] else None
        self.stairs_down = tuple(map_data['stairs_down']) if map_data['stairs_down'] else None
        self.chests = [tuple(chest) for chest in map_data['chests']]
        
        # Load tiles
        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                char = map_data['tiles'][y][x]
                
                if char == Tile.WALL or char == '#':
                    tile = Tile.create_wall()
                elif char == Tile.FLOOR or char == '.':
                    tile = Tile.create_floor()
                elif char == Tile.STAIRS_UP or char == '>':
                    tile = Tile(Tile.STAIRS_UP, blocked=False)
                elif char == Tile.STAIRS_DOWN or char == '<':
                    tile = Tile(Tile.STAIRS_DOWN, blocked=False)
                elif char == Tile.CHEST or char == '$':
                    tile = Tile(Tile.CHEST, blocked=False)
                else:
                    tile = Tile.create_floor()
                
                tile.char = char
                row.append(tile)
            self.tiles.append(row)
        
        self.rooms = []
        self.monsters = []
        self.doors = []
        
        # Load predefined monsters if they exist in the map data
        if 'monsters' in map_data and map_data['monsters']:
            for monster_data in map_data['monsters']:
                monster = Monster(
                    name=monster_data['name'],
                    hit_dice=monster_data['hit_dice'],
                    armor_class=monster_data['armor_class'],
                    attack_bonus=monster_data['attack_bonus'],
                    damage=monster_data['damage']
                )
                x, y = monster_data['position']
                self.place_monster(monster, x, y)
        
        # Load predefined doors if they exist in the map data
        if 'doors' in map_data and map_data['doors']:
            from door import Door
            for door_data in map_data['doors']:
                door = Door.from_dict(door_data)
                x, y = door_data['position']
                self.place_door(door, x, y)
    
    def save_to_file(self, filename):
        """
        Save single map level to file
        
        Args:
            filename: Path to save file
        """
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def load_from_file(self, filename):
        """
        Load single map level from file
        
        Args:
            filename: Path to load file
        """
        with open(filename, 'r') as f:
            map_data = json.load(f)
        self.from_dict(map_data)
    
    @staticmethod
    def save_multilevel_dungeon(levels, filename):
        """
        Save multiple dungeon levels to a single file
        
        Args:
            levels: List of DungeonMap objects
            filename: Path to save file
        """
        dungeon_data = {
            'num_levels': len(levels),
            'levels': [level.to_dict() for level in levels]
        }
        
        with open(filename, 'w') as f:
            json.dump(dungeon_data, f, indent=2)
    
    @staticmethod
    def load_multilevel_dungeon(filename):
        """
        Load multiple dungeon levels from a single file
        
        Args:
            filename: Path to load file
            
        Returns:
            List of DungeonMap objects
        """
        with open(filename, 'r') as f:
            dungeon_data = json.load(f)
        
        levels = []
        for level_data in dungeon_data['levels']:
            dungeon_map = DungeonMap()
            dungeon_map.from_dict(level_data)
            levels.append(dungeon_map)
        
        return levels
    
    @staticmethod
    def create_simple_map_designer():
        """
        Helper method to create a simple predesigned map
        
        Returns:
            DungeonMap object with a basic layout
        """
        dungeon = DungeonMap(width=50, height=20)
        
        # Create a simple cross-shaped dungeon
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
        
        # Place some chests
        dungeon.place_chest(10, 10)
        dungeon.place_chest(40, 10)
        dungeon.place_chest(20, 15)
        
        return dungeon
