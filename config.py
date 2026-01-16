"""
Game configuration and constants

Modify these values to customize game behavior
"""

# Display settings
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
MESSAGE_LOG_SIZE = 10

# Map generation settings
DEFAULT_MAP_WIDTH = 80
DEFAULT_MAP_HEIGHT = 24
MAX_ROOMS = 10
MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 10

# Monster spawn settings
BASE_MONSTER_COUNT = 3
MONSTERS_PER_LEVEL = 2  # Additional monsters per dungeon level

# Treasure settings
CHEST_SPAWN_CHANCE = 0.3  # 30% chance per room
BASE_GOLD_MIN = 10
BASE_GOLD_MAX = 50

# Combat settings
BASE_WEAPON_DAMAGE = "1d8"
FLEE_SUCCESS_CHANCE = 0.5  # 50% chance to flee

# Character progression
XP_PER_LEVEL = 1000
MAX_PARTY_SIZE = 6

# Starting conditions
STARTING_DUNGEON_LEVEL = 1
STARTING_GOLD = 0

# Game balance
DIFFICULTY_MULTIPLIER = 1.0  # Increase for harder game

# Symbol definitions (for consistency)
class Symbols:
    """ASCII symbols used in the game"""
    FLOOR = '.'
    WALL = '#'
    DOOR_HORIZONTAL = '-'
    DOOR_VERTICAL = '|'
    CHEST = '$'
    STAIRS_DOWN = '<'
    STAIRS_UP = '>'
    PARTY = '1'
    
    # HP bar symbols
    HP_FILLED = '█'
    HP_EMPTY = '░'


# Character class definitions
CHARACTER_CLASSES = {
    'Fighter': {
        'hit_die': 10,
        'base_attack_progression': 'full',  # BAB = level
        'good_saves': ['fortitude'],
        'description': 'Master of weapons and combat'
    },
    'Wizard': {
        'hit_die': 4,
        'base_attack_progression': 'half',  # BAB = level // 2
        'good_saves': ['will'],
        'description': 'Wielder of arcane magic'
    },
    'Cleric': {
        'hit_die': 8,
        'base_attack_progression': 'medium',  # BAB = (level * 3) // 4
        'good_saves': ['fortitude', 'will'],
        'description': 'Divine spellcaster and healer'
    },
    'Rogue': {
        'hit_die': 6,
        'base_attack_progression': 'medium',
        'good_saves': ['reflex'],
        'description': 'Skilled in stealth and precision'
    }
}


# Monster difficulty tiers
MONSTER_TIERS = {
    'trivial': {
        'cr_range': (0.25, 0.5),
        'xp': 50,
        'dungeon_levels': [1, 2]
    },
    'easy': {
        'cr_range': (1, 2),
        'xp': 100,
        'dungeon_levels': [1, 2, 3]
    },
    'medium': {
        'cr_range': (3, 5),
        'xp': 300,
        'dungeon_levels': [3, 4, 5, 6]
    },
    'hard': {
        'cr_range': (6, 8),
        'xp': 600,
        'dungeon_levels': [5, 6, 7, 8, 9]
    },
    'deadly': {
        'cr_range': (9, 12),
        'xp': 1200,
        'dungeon_levels': [8, 9, 10]
    }
}


# Color codes (if terminal supports ANSI colors)
class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright variants
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    @staticmethod
    def colorize(text, color):
        """Wrap text in color codes"""
        return f"{color}{text}{Colors.RESET}"


# Feature flags (enable/disable features)
class Features:
    """Toggle features on/off"""
    USE_COLORS = False  # Set to True if terminal supports colors
    PERMADEATH = False  # Game over on party death
    AUTO_SAVE = False   # Auto-save on level change
    SHOW_MONSTER_HP = True  # Show monster HP bars
    DIAGONAL_MOVEMENT = True  # Allow diagonal movement
    FOG_OF_WAR = False  # Hide unexplored areas (not yet implemented)
    
    
# Key bindings (for customization)
class KeyBindings:
    """Keyboard control mappings"""
    MOVE_NORTH = ['w', 'W', '8']
    MOVE_SOUTH = ['s', 'S', '2']
    MOVE_EAST = ['d', 'D', '6']
    MOVE_WEST = ['a', 'A', '4']
    MOVE_NORTHEAST = ['9']
    MOVE_NORTHWEST = ['7']
    MOVE_SOUTHEAST = ['3']
    MOVE_SOUTHWEST = ['1']
    
    DESCEND = ['d', 'D']
    ASCEND = ['u', 'U']
    INVENTORY = ['i', 'I']
    CHARACTER = ['c', 'C']
    QUIT = ['q', 'Q']
    
    # Combat
    ATTACK = ['a', 'A']
    SPELL = ['s', 'S']
    ITEM = ['i', 'I']
    FLEE = ['f', 'F']


def get_monster_count(dungeon_level):
    """Calculate number of monsters for a dungeon level"""
    return int((BASE_MONSTER_COUNT + (dungeon_level * MONSTERS_PER_LEVEL)) * DIFFICULTY_MULTIPLIER)


def get_gold_reward(dungeon_level):
    """Calculate gold reward for a dungeon level"""
    import random
    min_gold = BASE_GOLD_MIN * dungeon_level
    max_gold = BASE_GOLD_MAX * dungeon_level
    return random.randint(min_gold, max_gold)


def get_xp_reward(monster_name, dungeon_level):
    """Calculate XP reward for defeating a monster"""
    base_xp = 50 * dungeon_level
    return int(base_xp * DIFFICULTY_MULTIPLIER)


# Version info
VERSION = "0.1.0"
GAME_NAME = "DungeonSurvival"
AUTHOR = "DungeonSurvival Framework"
