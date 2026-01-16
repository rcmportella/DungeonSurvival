"""
Game state management and main game loop
"""
from enum import Enum
from party import Party
from dungeon_map import DungeonMap
from combat import Combat
from monster import Monster
import random


class GameMode(Enum):
    """Different game modes"""
    EXPLORATION = 1
    COMBAT = 2
    MENU = 3
    INVENTORY = 4
    CHARACTER_SHEET = 5
    GAME_OVER = 6
    VICTORY = 7


class GameState:
    """
    Manages the overall game state
    """
    
    def __init__(self, use_predesigned=False, map_file=None):
        self.mode = GameMode.EXPLORATION
        self.party = Party()
        self.current_map = None
        self.dungeon_level = 1
        self.turn_count = 0
        self.combat_instance = None
        self.message_log = []
        self.max_log_messages = 10
        
        # Map generation settings
        self.use_predesigned = use_predesigned
        self.map_file = map_file
        self.predesigned_levels = []  # Template maps loaded from file
        self.visited_levels = {}  # Dictionary to store instantiated levels {level_num: DungeonMap}
        
        # Door interaction state
        self.pending_door_action = None  # (x, y, door) when waiting for L/S input
        
        # Statistics tracking
        self.stats = {
            'monsters_defeated': 0,
            'total_gold_collected': 0,
            'chests_opened': 0,
            'max_dungeon_level': 1,
            'total_experience': 0,
            'doors_picked': 0,
            'doors_smashed': 0
        }
        
    def initialize_game(self):
        """Initialize a new game"""
        # Load predesigned maps if specified
        if self.use_predesigned and self.map_file:
            self.predesigned_levels = DungeonMap.load_multilevel_dungeon(self.map_file)
            self.add_message(f"Loaded predesigned dungeon with {len(self.predesigned_levels)} levels")
        
        # Generate first dungeon level
        self.generate_dungeon_level()
        
        # Place party at stairs up position
        if self.current_map.stairs_up:
            self.party.position = list(self.current_map.stairs_up)
        else:
            # Fallback to first room center
            if self.current_map.rooms:
                self.party.position = list(self.current_map.rooms[0].center())
        
        # Initialize field of view
        self.current_map.update_fov(
            self.party.position[0],
            self.party.position[1],
            radius=3
        )
                
    def generate_dungeon_level(self):
        """Generate a new dungeon level"""
        # Check if we've already visited this level
        if self.dungeon_level in self.visited_levels:
            # Reuse the existing level with its current state
            self.current_map = self.visited_levels[self.dungeon_level]
            self.add_message(f"Returned to dungeon level {self.dungeon_level}")
            return
        
        # Use predesigned level if available
        if self.use_predesigned and self.predesigned_levels:
            level_index = self.dungeon_level - 1
            if level_index < len(self.predesigned_levels):
                # Create a copy of the predesigned level
                import copy
                self.current_map = copy.deepcopy(self.predesigned_levels[level_index])
                self.add_message(f"Entered predesigned dungeon level {self.dungeon_level}")
            else:
                # Fall back to random generation if we run out of predesigned levels
                self._generate_random_level()
                self.add_message(f"Entered randomly generated level {self.dungeon_level} (beyond predesigned levels)")
        else:
            # Generate random level
            self._generate_random_level()
            
        # Populate with monsters based on dungeon level (only for new levels)
        # Check if monsters are already predefined in the map
        if not self.current_map.monsters:
            # No predefined monsters, spawn randomly
            monster_count = 3 + self.dungeon_level * 2
            self.current_map.populate_monsters(
                lambda: self.create_random_monster(),
                count=monster_count
            )
            self.add_message(f"Monsters spawned randomly ({monster_count} monsters)")
        else:
            # Monsters were predefined in the map
            self.add_message(f"Found {len(self.current_map.monsters)} predefined monsters")
        
        # Place some treasure chests only if not in predesigned map with chests
        if not (self.use_predesigned and self.current_map.chests):
            for room in getattr(self.current_map, 'rooms', []):
                if random.random() < 0.3:  # 30% chance per room
                    cx, cy = room.center()
                    self.current_map.place_chest(cx, cy)
        
        # Store this level as visited
        self.visited_levels[self.dungeon_level] = self.current_map
    
    def _generate_random_level(self):
        """Generate a random dungeon level"""
        self.current_map = DungeonMap(width=80, height=24)
        self.current_map.generate(max_rooms=10, min_room_size=4, max_room_size=10)
        self.add_message(f"Entered dungeon level {self.dungeon_level}")
                
        self.add_message(f"Entered dungeon level {self.dungeon_level}")
        
    def create_random_monster(self):
        """Create a random monster appropriate for the dungeon level"""
        monster_types = [
            ("Goblin", "1d8", 12, 1, "1d6"),
            ("Orc", "2d8", 13, 2, "1d8+1"),
            ("Skeleton", "1d8", 13, 1, "1d6"),
            ("Zombie", "2d8+2", 11, 1, "1d6+1"),
            ("Kobold", "1d6", 12, 0, "1d4"),
        ]
        
        # Higher level dungeons get tougher monsters
        if self.dungeon_level >= 3:
            monster_types.extend([
                ("Bugbear", "3d8+3", 14, 3, "1d8+2"),
                ("Ogre", "4d8+8", 13, 5, "2d6+3"),
            ])
            
        name, hd, ac, ab, dmg = random.choice(monster_types)
        return Monster(name, hit_dice=hd, armor_class=ac, attack_bonus=ab, damage=dmg)
        
    def move_party(self, dx, dy):
        """
        Move the party in exploration mode
        
        Args:
            dx, dy: Movement delta
            
        Returns:
            True if move was successful
        """
        if self.mode != GameMode.EXPLORATION:
            return False
            
        new_x = self.party.position[0] + dx
        new_y = self.party.position[1] + dy
        
        # Check bounds and walls
        if self.current_map.is_blocked(new_x, new_y):
            # Check if it's a door
            door = self.current_map.get_door_at(new_x, new_y)
            if door:
                self.handle_door_interaction(new_x, new_y, door)
                return False
            else:
                self.add_message("Cannot move there - blocked")
                return False
            
        # Check for monsters
        monster = self.current_map.get_monster_at(new_x, new_y)
        if monster and monster.is_alive():
            self.add_message(f"You encounter a {monster.name}!")
            self.start_combat(new_x, new_y)
            return False
            
        # Check for treasure
        if (new_x, new_y) in self.current_map.chests:
            self.handle_chest(new_x, new_y)
            
        # Check for stairs
        if (new_x, new_y) == self.current_map.stairs_down:
            self.add_message("Found stairs going down. Press 'D' to descend")
        elif (new_x, new_y) == self.current_map.stairs_up:
            self.add_message("Found stairs going up. Press 'U' to ascend")
        else:
            # Reset descent confirmation if moving away from stairs
            if hasattr(self, '_descend_confirmed'):
                self._descend_confirmed = False
            
        # Move party
        self.party.position = [new_x, new_y]
        self.turn_count += 1
        return True
        
    def start_combat(self, x, y):
        """Start combat at given location"""
        # Gather all monsters in adjacent tiles
        monsters = []
        monster_at_pos = self.current_map.get_monster_at(x, y)
        if monster_at_pos:
            monsters.append(monster_at_pos)
            
        if monsters:
            self.mode = GameMode.COMBAT
            # For now, use first party member in combat
            if self.party.members:
                self.combat_instance = Combat(self.party.members[0], monsters)
                self.add_message(f"Combat started against {len(monsters)} enemy(ies)!")
            
    def handle_chest(self, x, y):
        """Handle opening a treasure chest"""
        if (x, y) in self.current_map.chests:
            gold = random.randint(10, 50) * self.dungeon_level
            self.party.distribute_gold(gold)
            self.stats['total_gold_collected'] += gold
            self.stats['chests_opened'] += 1
            self.add_message(f"Found {gold} gold!")
            self.current_map.chests.remove((x, y))
            # Change tile back to floor
            self.current_map.tiles[y][x].char = '.'
            
    def handle_door_interaction(self, x, y, door):
        """
        Handle player attempting to interact with a door.
        
        Args:
            x, y: Door position
            door: Door object
        """
        # Use first party member for skill checks
        if not self.party.members:
            return
            
        character = self.party.members[0]
        success, message = door.attempt_open(character)
        self.add_message(message)
        
        if not success and door.is_locked:
            # Door is locked, set up pending action
            self.pending_door_action = (x, y, door)
        elif success:
            # Door opened or was already open
            self.current_map.update_door_tile(x, y)
            self.pending_door_action = None
            
    def attempt_lockpick_door(self):
        """Attempt to lockpick the pending door"""
        if not self.pending_door_action:
            return
            
        x, y, door = self.pending_door_action
        
        if not self.party.members:
            return
            
        character = self.party.members[0]
        success, message = door.attempt_lockpick(character)
        self.add_message(message)
        
        if success:
            self.stats['doors_picked'] += 1
            self.current_map.update_door_tile(x, y)
            self.pending_door_action = None
        
        self.turn_count += 1
            
    def attempt_smash_door(self):
        """Attempt to smash the pending door"""
        if not self.pending_door_action:
            return
            
        x, y, door = self.pending_door_action
        
        if not self.party.members:
            return
            
        character = self.party.members[0]
        success, message = door.attempt_smash(character)
        self.add_message(message)
        
        if success:
            self.stats['doors_smashed'] += 1
            self.current_map.update_door_tile(x, y)
            self.pending_door_action = None
        else:
            # Failed smash makes noise - could alert monsters in future
            pass
        
        self.turn_count += 1
            
    def descend_stairs(self):
        """Go down to next dungeon level"""
        if tuple(self.party.position) == self.current_map.stairs_down:
            # Check if party level is significantly lower than next dungeon level
            next_level = self.dungeon_level + 1
            avg_party_level = self.party.average_level()
            
            # Warn if dungeon level is higher than party average level
            if next_level > avg_party_level:
                self.add_message(f"WARNING: Level {next_level} ahead! Monsters will be dangerous!")
                self.add_message("Press 'D' again to confirm descent, or move away to cancel.")
                # Set a flag to require confirmation
                if not hasattr(self, '_descend_confirmed'):
                    self._descend_confirmed = False
                
                if not self._descend_confirmed:
                    self._descend_confirmed = True
                    return
                else:
                    # Reset confirmation flag
                    self._descend_confirmed = False
            
            self.dungeon_level += 1
            if self.dungeon_level > self.stats['max_dungeon_level']:
                self.stats['max_dungeon_level'] = self.dungeon_level
            self.generate_dungeon_level()
            # Place party at stairs up
            if self.current_map.stairs_up:
                self.party.position = list(self.current_map.stairs_up)
            # Update field of view for new level
            self.current_map.update_fov(
                self.party.position[0],
                self.party.position[1],
                radius=3
            )
                
    def ascend_stairs(self):
        """Go up to previous dungeon level"""
        if tuple(self.party.position) == self.current_map.stairs_up:
            if self.dungeon_level > 1:
                self.dungeon_level -= 1
                self.generate_dungeon_level()
                # Place party at stairs down
                if self.current_map.stairs_down:
                    self.party.position = list(self.current_map.stairs_down)
                # Update field of view for new level
                self.current_map.update_fov(
                    self.party.position[0],
                    self.party.position[1],
                    radius=3
                )
            else:
                self.add_message("You have escaped the dungeon!")
                self.mode = GameMode.VICTORY
                
    def add_message(self, message):
        """Add a message to the message log"""
        self.message_log.append(message)
        if len(self.message_log) > self.max_log_messages:
            self.message_log.pop(0)
            
    def get_display(self):
        """
        Get the current display to render
        
        Returns:
            Dictionary with display information
        """
        display = {
            'mode': self.mode,
            'map': None,
            'messages': self.message_log,
            'party_info': self.get_party_info(),
            'dungeon_level': self.dungeon_level,
            'turn_count': self.turn_count
        }
        
        if self.mode == GameMode.EXPLORATION:
            # Update field of view before rendering
            self.current_map.update_fov(
                self.party.position[0],
                self.party.position[1],
                radius=3
            )
            display['map'] = self.current_map.render(
                self.party.position[0],
                self.party.position[1]
            )
        elif self.mode == GameMode.COMBAT:
            display['map'] = self.get_combat_display()
            
        return display
        
    def get_party_info(self):
        """Get formatted party information"""
        info = []
        for i, member in enumerate(self.party.members):
            hp_bar = self.create_hp_bar(member.current_hp, member.max_hp)
            info.append(f"{i+1}. {member.name} ({member.char_class}) {hp_bar}")
        return info
        
    def create_hp_bar(self, current, maximum, length=10):
        """Create a visual HP bar"""
        if maximum <= 0:
            return "[DEAD]"
        ratio = current / maximum
        filled = int(ratio * length)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}] {current}/{maximum} HP"
        
    def get_combat_display(self):
        """Get combat display information"""
        if not self.combat_instance:
            return ""
            
        lines = []
        lines.append("=== COMBAT ===")
        lines.append("")
        lines.append("Party:")
        for i, member in enumerate(self.party.members):
            hp_bar = self.create_hp_bar(member.current_hp, member.max_hp)
            lines.append(f"  {i+1}. {member.name} {hp_bar}")
            
        lines.append("")
        lines.append("Enemies:")
        for i, monster in enumerate(self.combat_instance.monsters):
            if monster.is_alive():
                hp_bar = self.create_hp_bar(monster.current_hp, monster.max_hp)
                lines.append(f"  {chr(65+i)}. {monster.name} {hp_bar}")
            else:
                lines.append(f"  {chr(65+i)}. {monster.name} [DEAD]")
                
        return '\n'.join(lines)
    
    def get_game_statistics(self):
        """Get formatted game statistics for end-game display"""
        stats_lines = []
        stats_lines.append("="*60)
        stats_lines.append("GAME STATISTICS")
        stats_lines.append("="*60)
        stats_lines.append("")
        stats_lines.append(f"Turns Survived:        {self.turn_count}")
        stats_lines.append(f"Deepest Level Reached: {self.stats['max_dungeon_level']}")
        stats_lines.append(f"Monsters Defeated:     {self.stats['monsters_defeated']}")
        stats_lines.append(f"Chests Opened:         {self.stats['chests_opened']}")
        stats_lines.append(f"Gold Collected:        {self.stats['total_gold_collected']}")
        stats_lines.append(f"Experience Gained:     {self.stats['total_experience']}")
        stats_lines.append("")
        stats_lines.append("Party Status:")
        for member in self.party.members:
            status = "ALIVE" if member.is_alive() else "DEFEATED"
            stats_lines.append(f"  {member.name} (Level {member.level} {member.char_class}): {status} - {member.current_hp}/{member.max_hp} HP")
        stats_lines.append("")
        stats_lines.append("="*60)
        return stats_lines
