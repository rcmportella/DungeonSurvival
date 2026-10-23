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
import colors

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
    
    display = game_state.get_display()
    
    # Title
    raw_print("=" * width)
    raw_print(f"DUNGEON SURVIVAL - Level {display['dungeon_level']} | Turn {display['turn_count']}")
    raw_print("=" * width)
    raw_print()
    
    # Controls hint
    raw_print("-" * width)
    if display['mode'] == GameMode.EXPLORATION:
        # Check if there's a pending door action
        if hasattr(game_state, 'pending_door_action') and game_state.pending_door_action:
            raw_print("Door Controls: L: lockpick | S: smash | Move away to cancel")
        else:
            raw_print("Controls: Arrow keys/WASD to move | D: descend stairs | U: ascend stairs | Q: quit | I: inventory | C: character | K: colors on/off")
    elif display['mode'] == GameMode.INVENTORY:
        raw_print("Backpack: choose with the listed keys | X: back/close")
    elif display['mode'] == GameMode.COMBAT:
        raw_print("Combat (current character acts): A: attack | S: spell | I: item | F: flee (whole party) | Q: quit")
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

    # Map or combat view
    raw_print("-" * width)
    if display['map']:
        for line in display['map'].split('\n'):
            raw_print(line)
        raw_print()
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
        game_state.open_inventory()
    elif key.lower() == 'k':
        state = "on" if colors.toggle() else "off"
        game_state.add_message(f"Colors {state}.")
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


def _finish_combat(game_state, combat, result):
    """Apply the outcome of a finished combat"""
    status = result['status']
    if status == 'victory':
        # Stay in the combat screen so the final blow is visible;
        # rewards are granted on the next key press
        combat.menu = None
    elif status == 'defeat':
        game_state.add_message(result['message'])
        game_state.mode = GameMode.GAME_OVER
    elif status == 'fled':
        game_state.add_message(result['message'])
        game_state.mode = GameMode.EXPLORATION
        game_state.combat_instance = None
        game_state.party.position[0] -= 1


def _collect_victory_rewards(game_state, combat):
    """Award XP and treasure, remove the monsters and resume exploration"""
    rewards = combat._collect_rewards()
    xp = rewards['experience']
    gold = rewards['gold']
    game_state.add_message("Victory! All enemies defeated!")
    game_state.party.distribute_experience(xp)
    game_state.add_message(f"Gained {xp} experience!")
    game_state.stats['monsters_defeated'] += len(combat.monsters)
    game_state.stats['total_experience'] += xp
    if gold:
        game_state.party.distribute_gold(gold)
        game_state.stats['total_gold_collected'] += gold
        game_state.add_message(f"Found {gold} gold!")
    if rewards['items']:
        game_state.add_message("Found: " + ", ".join(str(item) for item in rewards['items']))
        looter = game_state.party.get_alive_members()[0]
        for item in rewards['items']:
            looter.add_item(item)
        game_state.add_message(f"{looter.name} carries the loot.")
    for monster in combat.monsters:
        for m, mx, my in list(game_state.current_map.monsters):
            if m == monster:
                game_state.current_map.remove_monster(mx, my)
    game_state.mode = GameMode.EXPLORATION
    game_state.combat_instance = None


def _perform(game_state, combat, action, target=None):
    combat.menu = None
    result = combat.perform(action, target)
    if result['status'] != 'ongoing':
        _finish_combat(game_state, combat, result)


def _is_support_spell(spell):
    from spell import CureWounds, Shield, Bless, DetectMagic
    return isinstance(spell, (CureWounds, Shield, Bless, DetectMagic))


def _choose_target(combat, action):
    """Open target selection, or act immediately if there is only one choice"""
    actor = combat.current_actor()
    if action['type'] == 'spell' and _is_support_spell(action['spell']):
        choices = [m for m in combat.party_members if m.is_alive()]
    else:
        choices = combat.alive_monsters()
    return actor, choices


def handle_combat_input(game_state, key):
    """Handle input during combat mode (one command per character turn)"""
    combat = game_state.combat_instance
    if not combat:
        game_state.mode = GameMode.EXPLORATION
        return True

    if combat.status == 'victory':
        _collect_victory_rewards(game_state, combat)
        return True

    actor = combat.current_actor()
    if actor is None:
        return True
    key = key.lower()
    menu = combat.menu

    if key == 'q':
        return False

    # Sub-menus: cancel, spell/item/target selection
    if menu:
        if key in ('\x1b', 'x'):
            combat.menu = None
            return True
        if not key.isdigit() or key == '0':
            return True
        index = int(key) - 1
        if menu['stage'] == 'spell':
            spells = menu['options']
            if index < len(spells):
                spell = spells[index]
                if not actor.can_cast_spell(spell):
                    game_state.add_message(f"{actor.name} cannot cast {spell.name} (no spell slots).")
                    return True
                action = {'type': 'spell', 'spell': spell}
                _, choices = _choose_target(combat, action)
                if len(choices) == 1:
                    _perform(game_state, combat, action, choices[0])
                else:
                    combat.menu = {'stage': 'target', 'action': action, 'options': choices}
        elif menu['stage'] == 'item':
            items = menu['options']
            if index < len(items):
                _perform(game_state, combat, {'type': 'item', 'item_name': items[index]})
        elif menu['stage'] == 'target':
            choices = menu['options']
            if index < len(choices):
                _perform(game_state, combat, menu['action'], choices[index])
        return True

    if key == 'a':
        enemies = combat.alive_monsters()
        if len(enemies) == 1:
            _perform(game_state, combat, {'type': 'attack'}, enemies[0])
        else:
            combat.menu = {'stage': 'target', 'action': {'type': 'attack'}, 'options': enemies}
    elif key == 's':
        if actor.known_spells:
            combat.menu = {'stage': 'spell', 'options': list(actor.known_spells)}
        else:
            game_state.add_message(f"{actor.name} knows no spells.")
    elif key == 'i':
        names = []
        for item in actor.inventory:
            if getattr(item, 'consumable', False) and item.name not in names:
                names.append(item.name)
        if names:
            combat.menu = {'stage': 'item', 'options': names}
        else:
            game_state.add_message(f"{actor.name} has no usable items.")
    elif key == 'f':
        _perform(game_state, combat, {'type': 'flee'})

    return True


def handle_inventory_input(game_state, key):
    """Handle input in the inventory (backpack) screens"""
    if key.lower() == 'q':
        return False
    game_state.inventory_input(key)
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
    if '--no-color' in sys.argv:
        colors.set_enabled(False)
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
                    elif game_state.mode == GameMode.INVENTORY:
                        running = handle_inventory_input(game_state, key)
                        
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
