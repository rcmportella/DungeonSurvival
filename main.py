#!/usr/bin/env python3
"""
DungeonSurvival - A roguelike game using OGL D20 system
Main game entry point
"""
import os
import sys
import shutil
from game_state import GameState, GameMode
from character import Character
from input_handler import InputHandler

# Global variables
width = 80  # Default terminal width

def raw_print(text=''):
    """Print with proper line endings for raw terminal mode"""
    sys.stdout.write(text + '\r\n')
    sys.stdout.flush()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
    # Move cursor to home position after clear (for raw terminal mode)
    sys.stdout.write('\r')
    sys.stdout.flush()


def render_game(game_state):
    """Render the current game state"""
    global width
    clear_screen()
    
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    width = min(columns, 120)  # Cap at 120 for readability
    
    # Debug output
    raw_print(f"DEBUG: Terminal columns={columns}, rows={rows}, width={width}")
    raw_print(f"DEBUG: Equals line length={len('=' * width)}")
    
    display = game_state.get_display()
    
    # Title
    raw_print("=" * width)
    raw_print(f"DUNGEON SURVIVAL - Level {display['dungeon_level']} | Turn {display['turn_count']}")
    raw_print("=" * width)
    raw_print()
    
    # Map or combat view
    if display['map']:
        for line in display['map'].split('\n'):
            raw_print(line)
        raw_print()
    
    # Party info
    raw_print("-" * width)
    raw_print("Party:")
    for info in display['party_info']:
        raw_print(f"  {info}")
    raw_print()
    
    # Message log
    raw_print("-" * width)
    raw_print("Messages:")
    for msg in display['messages'][-5:]:  # Show last 5 messages
        raw_print(f"  {msg}")
    raw_print()

    # Controls hint
    raw_print("-" * width)
    if display['mode'] == GameMode.EXPLORATION:
        # Check if there's a pending door action
        if hasattr(game_state, 'pending_door_action') and game_state.pending_door_action:
            raw_print("Door Controls: L: lockpick | S: smash | Move away to cancel")
        else:
            raw_print("Controls: Arrow keys/WASD to move | D: descend stairs | U: ascend stairs | Q: quit | I: inventory | C: character")
    elif display['mode'] == GameMode.COMBAT:
        raw_print("Combat: A: attack | S: spell | I: item | F: flee | Q: quit")
    raw_print("=" * width)


def create_default_party():
    """Create a default starting party"""
    from party import Party
    from combat import COMMON_ITEMS, HealingPotion
    from spell import SPELL_LIBRARY
    from spell import RayOfFrost
    
    party = Party()
    
    # Create a fighter
    fighter = Character("Warrior", "Fighter", level=1)
    #fighter.roll_abilities()
    fighter.set_abilities(str_score=15, dex=10, con=16, int_score=10, wis=10, cha=10)
    # Add items to fighter's inventory
    longsword = COMMON_ITEMS['longsword']
    chain_mail = COMMON_ITEMS['chain_mail']
    fighter.inventory.append(longsword)
    fighter.inventory.append(chain_mail)
    fighter.inventory.append(HealingPotion())  # Fresh instance
    fighter.inventory.append(HealingPotion())
    # Equip weapon and armor from inventory
    fighter.equipped_weapon = longsword
    fighter.equipped_armor = chain_mail
    party.add_member(fighter)
    
    # Create a wizard
    wizard = Character("Mage", "Wizard", level=1)
    #wizard.roll_abilities()
    wizard.set_abilities(str_score=10, dex=10, con=10, int_score=16, wis=12, cha=10)
    staff = COMMON_ITEMS['staff']
    wizard.inventory.append(staff)
    wizard.inventory.append(HealingPotion())
    # Equip weapon from inventory
    wizard.equipped_weapon = staff
    # Add wizard spells
    wizard.known_spells.append(SPELL_LIBRARY['magic_missile'])
    wizard.known_spells.append(RayOfFrost())
    wizard.known_spells.append(RayOfFrost())
    party.add_member(wizard)
    
    # Create a cleric
    cleric = Character("Healer", "Cleric", level=1)
    #cleric.roll_abilities()
    cleric.set_abilities(str_score=12, dex=10, con=14, int_score=10, wis=16, cha=13)
    mace = COMMON_ITEMS['mace']
    scale_mail = COMMON_ITEMS['scale_mail']
    cleric.inventory.append(mace)
    cleric.inventory.append(scale_mail)
    cleric.inventory.append(HealingPotion())
    cleric.inventory.append(HealingPotion())
    # Equip weapon and armor from inventory
    cleric.equipped_weapon = mace
    cleric.equipped_armor = scale_mail
    # Add cleric spells
    cleric.known_spells.append(SPELL_LIBRARY['cure_light_wounds'])
    cleric.known_spells.append(SPELL_LIBRARY['bless'])
    party.add_member(cleric)
    
    return party


def handle_exploration_input(game_state, key):
    """Handle input during exploration mode"""
    input_handler = InputHandler()
    
    # Check for special commands first (before movement)
    if key.lower() == 'q':
        return False  # Quit game
    
    # Handle door interaction commands
    if game_state.pending_door_action:
        if key.lower() == 'l':
            game_state.attempt_lockpick_door()
            return True
        elif key.lower() == 's':
            game_state.attempt_smash_door()
            return True
        # Allow other movements to cancel door action
        game_state.pending_door_action = None
    
    # Check if on stairs and trying to use stairs commands
    party_pos = tuple(game_state.party.position)
    on_stairs_down = (party_pos == game_state.current_map.stairs_down)
    on_stairs_up = (party_pos == game_state.current_map.stairs_up)
    
    # Handle stairs commands when on stairs (before checking movement)
    if key.lower() == 'd' and on_stairs_down:
        game_state.descend_stairs()
        return True
    elif key.lower() == 'u' and on_stairs_up:
        game_state.ascend_stairs()
        return True
    
    # Movement (including 'd' for moving right when not on stairs)
    movement = input_handler.parse_movement_key(key)
    if movement:
        dx, dy = movement
        game_state.move_party(dx, dy)
        return True
        
    # Other commands
    if key.lower() == 'i':
        game_state.add_message("Inventory not yet implemented")
    elif key.lower() == 'c':
        # Display character sheets for all party members
        display_character_sheets(game_state)
        
    return True


def display_character_sheets(game_state):
    """Display character sheets for all party members"""
    clear_screen()
    raw_print("=" * 80)
    raw_print(" CHARACTER SHEETS")
    raw_print("=" * 80)
    raw_print()
    
    for member in game_state.party.members:
        # Use simplified version
        sheet = member.get_character_sheet(detailed=False)
        for line in sheet.split('\n'):
            raw_print(line)
        raw_print()
    
    raw_print("=" * 80)
    raw_print("Press any key to continue...")
    raw_print("=" * 80)
    
    # Wait for key press
    input_handler = InputHandler()
    with input_handler:
        input_handler.get_key()


def handle_combat_input(game_state, key):
    """Handle input during combat mode"""
    if not game_state.combat_instance:
        game_state.mode = GameMode.EXPLORATION
        return True
        
    combat = game_state.combat_instance
    
    if key.lower() == 'a':
        # Attack
        if combat.character.is_alive() and combat.monsters:
            alive_monsters = [m for m in combat.monsters if m.is_alive()]
            if alive_monsters:
                result = combat.execute_round(
                    player_action={'type': 'attack'},
                    target_index=0
                )
                
                # Debug: Write combat log to file
                with open('combat_debug.log', 'a') as f:
                    f.write("\n=== COMBAT LOG DEBUG ===\n")
                    for log_entry in result.get('log', []):
                        f.write(log_entry + "\n")
                    f.write("========================\n\n")
                
                if result['status'] == 'victory':
                    game_state.add_message(result['message'])
                    # Award XP
                    xp = 100 * len(combat.monsters)
                    game_state.party.distribute_experience(xp)
                    game_state.add_message(f"Gained {xp} experience!")
                    
                    # Track statistics
                    game_state.stats['monsters_defeated'] += len(combat.monsters)
                    game_state.stats['total_experience'] += xp
                    
                    # Remove dead monsters from map
                    for monster in combat.monsters:
                        for i, (m, mx, my) in enumerate(game_state.current_map.monsters):
                            if m == monster:
                                game_state.current_map.remove_monster(mx, my)
                                
                    game_state.mode = GameMode.EXPLORATION
                    game_state.combat_instance = None
                    
                elif result['status'] == 'defeat':
                    game_state.add_message(result['message'])
                    game_state.mode = GameMode.GAME_OVER
                    
    elif key.lower() == 's':
        game_state.add_message("Spell casting not yet fully implemented")
        
    elif key.lower() == 'i':
        game_state.add_message("Item use not yet implemented")
        
    elif key.lower() == 'f':
        # Flee
        game_state.add_message("You flee from combat!")
        game_state.mode = GameMode.EXPLORATION
        game_state.combat_instance = None
        # Move party back one tile
        game_state.party.position[0] -= 1
        
    elif key.lower() == 'q':
        return False
        
    return True


def get_available_maps():
    """Get list of available predesigned map files"""
    maps_dir = "maps"
    if not os.path.exists(maps_dir):
        return []
    
    map_files = []
    for filename in os.listdir(maps_dir):
        if filename.endswith('.json'):
            map_files.append(filename)
    
    return sorted(map_files)


def main():
    """Main game loop"""
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    global width
    width = min(columns, 120)  # Cap at 120 for readability
    raw_print(f"Width: {width}")
    raw_print(f"Height: {rows}")
    raw_print()
    raw_print("=" * width)
    raw_print(" DUNGEON SURVIVAL")
    raw_print(" A Roguelike Adventure")
    raw_print("=" * width)
    raw_print()
    
    # Ask for map type
    raw_print("Select dungeon type:")
    raw_print("  1. Random generated dungeon")
    raw_print("  2. Predesigned dungeon")
    raw_print()
    
    map_choice = None
    while map_choice not in ['1', '2']:
        map_choice = input("Enter your choice (1 or 2): ").strip()
    
    use_predesigned = (map_choice == '2')
    map_file = None
    
    # If predesigned, let user choose which map
    if use_predesigned:
        available_maps = get_available_maps()
        
        if not available_maps:
            raw_print()
            raw_print("No predesigned maps found in 'maps/' directory!")
            raw_print("Falling back to random generation...")
            use_predesigned = False
        else:
            raw_print()
            raw_print("Available predesigned dungeons:")
            for i, map_name in enumerate(available_maps, 1):
                raw_print(f"  {i}. {map_name}")
            raw_print()
            
            map_index = None
            while map_index is None:
                try:
                    choice = input(f"Select map (1-{len(available_maps)}): ").strip()
                    idx = int(choice) - 1
                    if 0 <= idx < len(available_maps):
                        map_index = idx
                    else:
                        raw_print(f"Please enter a number between 1 and {len(available_maps)}")
                except ValueError:
                    raw_print("Please enter a valid number")
            
            map_file = os.path.join("maps", available_maps[map_index])
    
    raw_print()
    if use_predesigned:
        raw_print(f"Loading predesigned dungeon: {os.path.basename(map_file)}")
    else:
        raw_print("Generating random dungeon...")
    raw_print()
    raw_print("Creating your party...")
    input("Press Enter to continue...")
    
    # Initialize game
    game_state = GameState(use_predesigned=use_predesigned, map_file=map_file)
    game_state.party = create_default_party()
    game_state.initialize_game()
    
    game_state.add_message("Welcome to Dungeon Survival!")
    game_state.add_message("Your quest: Survive and collect treasure!")
    
    # Main game loop
    running = True
    
    try:
        with InputHandler() as input_handler:
            while running:
                # Render
                render_game(game_state)
                
                # Check win/lose conditions
                if game_state.mode == GameMode.GAME_OVER:
                    raw_print()
                    raw_print("╔" + "═" * 58 + "╗")
                    raw_print("║" + " " * 22 + "GAME OVER" + " " * 27 + "║")
                    raw_print("║" + " " * 17 + "Your party has been defeated!" + " " * 12 + "║")
                    raw_print("╚" + "═" * 58 + "╝")
                    raw_print()
                    for line in game_state.get_game_statistics():
                        raw_print(line)
                    break
                elif game_state.mode == GameMode.VICTORY:
                    raw_print()
                    raw_print("╔" + "═" * 58 + "╗")
                    raw_print("║" + " " * 23 + "VICTORY!" + " " * 27 + "║")
                    raw_print("║" + " " * 15 + "You have escaped the dungeon!" + " " * 14 + "║")
                    raw_print("╚" + "═" * 58 + "╝")
                    raw_print()
                    for line in game_state.get_game_statistics():
                        raw_print(line)
                    break
                    
                # Get input
                key = input_handler.get_key()
                
                if key:
                    # Handle input based on game mode
                    if game_state.mode == GameMode.EXPLORATION:
                        running = handle_exploration_input(game_state, key)
                    elif game_state.mode == GameMode.COMBAT:
                        running = handle_combat_input(game_state, key)
                        
    except KeyboardInterrupt:
        raw_print("\n\nGame interrupted by user.")
    except Exception as e:
        raw_print(f"\n\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        #clear_screen()
        raw_print("Thanks for playing Dungeon Survival!")
        raw_print()


if __name__ == "__main__":
    main()
