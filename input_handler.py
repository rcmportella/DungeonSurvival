"""
Input handling for keyboard controls
"""
import sys
import tty
import termios
import select


class InputHandler:
    """
    Handles keyboard input for the game
    """
    
    # Key mappings
    ARROW_UP = '\x1b[A'
    ARROW_DOWN = '\x1b[B'
    ARROW_RIGHT = '\x1b[C'
    ARROW_LEFT = '\x1b[D'
    
    def __init__(self):
        self.old_settings = None
        
    def __enter__(self):
        """Set terminal to raw mode for character-by-character input"""
        if sys.platform != 'win32':
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
        return self
        
    def __exit__(self, type, value, traceback):
        """Restore terminal settings"""
        if sys.platform != 'win32' and self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            
    def get_key(self, timeout=None):
        """
        Get a single keypress from the user
        
        Args:
            timeout: Optional timeout in seconds (None for blocking)
            
        Returns:
            The key pressed as a string, or None if timeout
        """
        if sys.platform == 'win32':
            # Windows implementation
            import msvcrt
            if timeout:
                # Non-blocking with timeout
                import time
                start = time.time()
                while True:
                    if msvcrt.kbhit():
                        char = msvcrt.getch().decode('utf-8', errors='ignore')
                        # Check for arrow keys (special case on Windows)
                        if char in ('\x00', '\xe0'):
                            char2 = msvcrt.getch().decode('utf-8', errors='ignore')
                            if char2 == 'H':
                                return self.ARROW_UP
                            elif char2 == 'P':
                                return self.ARROW_DOWN
                            elif char2 == 'M':
                                return self.ARROW_RIGHT
                            elif char2 == 'K':
                                return self.ARROW_LEFT
                        return char
                    if time.time() - start > timeout:
                        return None
                    time.sleep(0.01)
            else:
                # Blocking
                char = msvcrt.getch().decode('utf-8', errors='ignore')
                if char in ('\x00', '\xe0'):
                    char2 = msvcrt.getch().decode('utf-8', errors='ignore')
                    if char2 == 'H':
                        return self.ARROW_UP
                    elif char2 == 'P':
                        return self.ARROW_DOWN
                    elif char2 == 'M':
                        return self.ARROW_RIGHT
                    elif char2 == 'K':
                        return self.ARROW_LEFT
                return char
        else:
            # Unix/Linux implementation
            if timeout:
                ready, _, _ = select.select([sys.stdin], [], [], timeout)
                if not ready:
                    return None
                    
            char = sys.stdin.read(1)
            
            # Check for escape sequences (arrow keys, etc.)
            if char == '\x1b':
                # Read the next two characters for arrow keys
                char += sys.stdin.read(2)
                
            return char
            
    def parse_movement_key(self, key):
        """
        Parse a key into movement delta
        
        Args:
            key: Key string from get_key()
            
        Returns:
            Tuple (dx, dy) or None if not a movement key
        """
        movement_map = {
            self.ARROW_UP: (0, -1),
            self.ARROW_DOWN: (0, 1),
            self.ARROW_LEFT: (-1, 0),
            self.ARROW_RIGHT: (1, 0),
            'w': (0, -1),
            'W': (0, -1),
            's': (0, 1),
            'S': (0, 1),
            'a': (-1, 0),
            'A': (-1, 0),
            'd': (1, 0),
            'D': (1, 0),
            # Numpad
            '8': (0, -1),
            '2': (0, 1),
            '4': (-1, 0),
            '6': (1, 0),
            '7': (-1, -1),  # Diagonal up-left
            '9': (1, -1),   # Diagonal up-right
            '1': (-1, 1),   # Diagonal down-left
            '3': (1, 1),    # Diagonal down-right
        }
        
        return movement_map.get(key)


# Simple cross-platform input (fallback for testing)
def simple_input(prompt=""):
    """Simple blocking input (not for main game, but useful for menus)"""
    return input(prompt)
