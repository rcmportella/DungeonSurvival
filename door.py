"""
Door system with open/closed states, locking, and interaction mechanics
"""
import dice


class Door:
    """
    Represents a door that can be opened, locked, picked, or smashed
    """
    
    def __init__(self, horizontal=True, locked=False, 
                 lockpick_dc=15, smash_dc=18, key_id=None):
        """
        Initialize a door.
        
        Args:
            horizontal: True for horizontal door (-), False for vertical (|)
            locked: Whether the door starts locked
            lockpick_dc: Difficulty Class for lockpicking (10-30)
            smash_dc: Difficulty Class for smashing (15-25)
            key_id: Optional key ID required to unlock without picking
        """
        self.horizontal = horizontal
        self.is_open = not locked  # If locked, starts closed
        self.is_locked = locked
        self.lockpick_dc = lockpick_dc
        self.smash_dc = smash_dc
        self.key_id = key_id
        self.is_destroyed = False  # True if smashed open
        
    def get_char(self):
        """Get the character representation of the door"""
        if self.is_open or self.is_destroyed:
            return '.'  # Open/destroyed doors show as floor
        return '-' if self.horizontal else '|'
        
    def is_passable(self):
        """Check if the door can be passed through"""
        return self.is_open or self.is_destroyed
        
    def is_blocking_sight(self):
        """Check if the door blocks line of sight"""
        return not (self.is_open or self.is_destroyed)
        
    def attempt_open(self, character):
        """
        Attempt to open the door.
        
        Args:
            character: The character attempting to open the door
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if self.is_open:
            return True, "The door is already open."
            
        if self.is_destroyed:
            return True, "The door has been destroyed - you can pass through."
            
        if not self.is_locked:
            # Unlocked door - just open it
            self.is_open = True
            return True, "You open the door."
            
        # Door is locked
        return False, f"The door is locked. (L)ockpick it or (S)mash it?"
        
    def attempt_lockpick(self, character):
        """
        Attempt to pick the lock.
        
        Args:
            character: The character attempting to pick the lock
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.is_locked:
            return True, "The door is not locked."
            
        if self.is_destroyed:
            return True, "The door is already destroyed."
            
        # Calculate lockpick bonus
        # Rogues get their level as bonus, others get DEX modifier
        if character.char_class == "Rogue":
            bonus = character.level + character.get_ability_modifier('dexterity')
        else:
            bonus = character.get_ability_modifier('dexterity')
            
        # Make skill check
        roll = dice.d20(1, bonus)
        
        if roll >= self.lockpick_dc:
            self.is_locked = False
            self.is_open = True
            return True, f"Lockpick successful! (Roll: {roll} vs DC {self.lockpick_dc})"
        else:
            return False, f"Failed to pick the lock. (Roll: {roll} vs DC {self.lockpick_dc})"
            
    def attempt_smash(self, character):
        """
        Attempt to smash the door open.
        
        Args:
            character: The character attempting to smash the door
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if self.is_open:
            return True, "The door is already open."
            
        if self.is_destroyed:
            return True, "The door is already destroyed."
            
        # Calculate smash bonus (STR based)
        bonus = character.get_ability_modifier('strength')
        
        # Fighters get advantage on smashing
        if character.char_class == "Fighter":
            bonus += character.level // 2
            
        # Make strength check
        roll = dice.d20(1, bonus)
        
        if roll >= self.smash_dc:
            self.is_locked = False
            self.is_open = True
            self.is_destroyed = True
            return True, f"You smash the door open! (Roll: {roll} vs DC {self.smash_dc})"
        else:
            return False, f"Failed to smash the door. (Roll: {roll} vs DC {self.smash_dc})"
            
    def unlock_with_key(self, key_id):
        """
        Unlock the door with a key.
        
        Args:
            key_id: The key ID to try
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.is_locked:
            return True, "The door is not locked."
            
        if self.key_id and key_id == self.key_id:
            self.is_locked = False
            self.is_open = True
            return True, "You unlock the door with the key."
        else:
            return False, "The key doesn't fit this lock."
            
    def to_dict(self):
        """Convert door to dictionary for serialization"""
        return {
            'horizontal': self.horizontal,
            'locked': self.is_locked,
            'lockpick_dc': self.lockpick_dc,
            'smash_dc': self.smash_dc,
            'key_id': self.key_id,
            'is_open': self.is_open,
            'is_destroyed': self.is_destroyed
        }
        
    @staticmethod
    def from_dict(data):
        """Create door from dictionary"""
        door = Door(
            horizontal=data.get('horizontal', True),
            locked=data.get('locked', False),
            lockpick_dc=data.get('lockpick_dc', 15),
            smash_dc=data.get('smash_dc', 18),
            key_id=data.get('key_id', None)
        )
        door.is_open = data.get('is_open', not door.is_locked)
        door.is_destroyed = data.get('is_destroyed', False)
        return door
        
    def __str__(self):
        """String representation for debugging"""
        state = "open" if self.is_open else "closed"
        if self.is_destroyed:
            state = "destroyed"
        locked = " (locked)" if self.is_locked else ""
        return f"Door({state}{locked}, DC {self.lockpick_dc}/{self.smash_dc})"


def create_easy_door(horizontal=True):
    """Create an easy door (low DC)"""
    return Door(horizontal=horizontal, locked=True, lockpick_dc=10, smash_dc=15)
    

def create_medium_door(horizontal=True):
    """Create a medium difficulty door"""
    return Door(horizontal=horizontal, locked=True, lockpick_dc=15, smash_dc=18)
    

def create_hard_door(horizontal=True):
    """Create a hard door (high DC)"""
    return Door(horizontal=horizontal, locked=True, lockpick_dc=20, smash_dc=23)
    

def create_very_hard_door(horizontal=True):
    """Create a very hard door"""
    return Door(horizontal=horizontal, locked=True, lockpick_dc=25, smash_dc=28)
