"""
Combat system with D20 mechanics
"""
import dice


class Combat:
    """
    Handles turn-based combat between character and monsters
    """
    
    def __init__(self, character, monsters):
        """
        Initialize combat.
        
        Args:
            character: Player character
            monsters: List of monsters or single monster
        """
        self.character = character
        
        # Ensure monsters is a list
        if not isinstance(monsters, list):
            self.monsters = [monsters]
        else:
            self.monsters = monsters
            
        self.round = 0
        self.combat_log = []
        
    def roll_initiative(self):
        """
        Roll initiative for all combatants.
        
        Returns:
            Ordered list of (name, initiative, is_player) tuples
        """
        initiatives = []
        
        # Player initiative
        dex_mod = self.character.get_ability_modifier('dexterity')
        player_init = dice.d20(1, dex_mod)
        initiatives.append((self.character.name, player_init, True))
        
        # Monster initiatives
        for monster in self.monsters:
            monster_init = dice.d20()
            initiatives.append((monster.name, monster_init, False))
            
        # Sort by initiative (highest first)
        initiatives.sort(key=lambda x: x[1], reverse=True)
        return initiatives
        
    def execute_round(self, player_action=None, target_index=0):
        """
        Execute one round of combat.
        
        Args:
            player_action: Dictionary with action details
                          {'type': 'attack', 'weapon_damage': '1d8'}
                          {'type': 'spell', 'spell': spell_object, 'target': index}
                          {'type': 'item', 'item_name': 'Potion of Healing'}
                          {'type': 'flee'}
            target_index: Index of target monster (default 0)
            
        Returns:
            Dictionary with combat results
        """
        self.round += 1
        round_log = [f"\n--- Round {self.round} ---"]
        
        # Default action is attack
        if player_action is None:
            player_action = {'type': 'attack'}
            
        # Check if combat should end
        if not self.character.is_alive():
            return {
                'status': 'defeat',
                'message': 'You have been defeated!',
                'log': self.combat_log
            }
            
        alive_monsters = [m for m in self.monsters if m.is_alive()]
        if not alive_monsters:
            return {
                'status': 'victory',
                'message': 'All enemies defeated!',
                'log': self.combat_log,
                'rewards': self._collect_rewards()
            }
            
        # Get initiative order
        init_order = self.roll_initiative()
        
        # Execute actions in initiative order
        for name, init, is_player in init_order:
            if is_player:
                # Player's turn
                if player_action['type'] == 'attack':
                    if target_index < len(alive_monsters):
                        target = alive_monsters[target_index]
                        weapon_dmg = player_action.get('weapon_damage', None)
                        hit, damage, attack_roll = self.character.attack_roll(target.armor_class, weapon_dmg)
                        
                        # Detailed log entry
                        char_ac = self.character.get_armor_class()
                        weapon_name = self.character.equipped_weapon.name if self.character.equipped_weapon else "unarmed"
                        round_log.append(f"[{self.character.name}] Attack roll: {attack_roll} vs AC {target.armor_class} (weapon: {weapon_name})")
                        
                        if hit:
                            target.take_damage(damage)
                            msg = f"  -> HIT! {self.character.name} hits {target.name} for {damage} damage! ({target.name} HP: {target.current_hp}/{target.max_hp})"
                            if not target.is_alive():
                                msg += f" {target.name} is defeated!"
                        else:
                            msg = f"  -> MISS! {self.character.name} misses {target.name}!"
                        round_log.append(msg)
                        
                elif player_action['type'] == 'spell':
                    spell = player_action['spell']
                    target = alive_monsters[target_index] if target_index < len(alive_monsters) else None
                    success, result = self.character.cast_spell(spell, target)
                    round_log.append(result)
                    
                elif player_action['type'] == 'item':
                    item_name = player_action['item_name']
                    result = self.character.use_item(item_name)
                    if result:
                        round_log.append(result)
                    else:
                        round_log.append(f"Cannot use {item_name}!")
                        
                elif player_action['type'] == 'flee':
                    # Attempt to flee (DEX check)
                    flee_roll = dice.d20(1, self.character.get_ability_modifier('dexterity'))
                    if flee_roll >= 10:
                        return {
                            'status': 'fled',
                            'message': 'You successfully fled from combat!',
                            'log': self.combat_log + round_log
                        }
                    else:
                        round_log.append(f"{self.character.name} fails to flee!")
            else:
                # Monster's turn
                for monster in self.monsters:
                    if monster.name == name and monster.is_alive():
                        hit, mattack_roll, damage, msg = monster.attack(self.character)
                        
                        # Add detailed log entry for monster attack
                        char_ac = self.character.get_armor_class()
                        round_log.append(f"[{monster.name}] Attack roll: {mattack_roll} vs AC {char_ac}")
                        round_log.append(f"  -> {msg}")
                        if hit:
                            round_log.append(f"  -> {self.character.name} takes {damage} damage! (HP: {self.character.current_hp}/{self.character.max_hp})")
                        break
                        
        # Update combat log
        self.combat_log.extend(round_log)
        
        # Check end conditions again
        if not self.character.is_alive():
            return {
                'status': 'defeat',
                'message': 'You have been defeated!',
                'log': self.combat_log
            }
            
        alive_monsters = [m for m in self.monsters if m.is_alive()]
        if not alive_monsters:
            return {
                'status': 'victory',
                'message': 'All enemies defeated!',
                'log': self.combat_log,
                'rewards': self._collect_rewards()
            }
            
        # Combat continues
        return {
            'status': 'ongoing',
            'message': f'Round {self.round} complete.',
            'log': self.combat_log,
            'alive_monsters': alive_monsters,
            'character_hp': f"{self.character.current_hp}/{self.character.max_hp}"
        }
        
    def _collect_rewards(self):
        """Collect treasure from defeated monsters"""
        rewards = {
            'gold': 0,
            'items': [],
            'experience': 0
        }
        
        for monster in self.monsters:
            # Add treasure
            for item in monster.treasure:
                if 'gold' in item.lower():
                    # Extract gold amount
                    amount = int(''.join(filter(str.isdigit, item)))
                    rewards['gold'] += amount
                else:
                    rewards['items'].append(item)
                    
            # Award XP based on monster HD
            hd = int(monster.hit_dice.split('d')[0])
            rewards['experience'] += hd * 100
            
        return rewards
        
    def get_combat_summary(self):
        """Get current combat status summary"""
        alive_monsters = [m for m in self.monsters if m.is_alive()]
        
        summary = [
            f"\n{'='*50}",
            f"COMBAT STATUS - Round {self.round}",
            f"{'='*50}",
            f"Player: {self.character.name}",
            f"  HP: {self.character.current_hp}/{self.character.max_hp}",
            f"  AC: {self.character.get_armor_class()}",
            f"\nEnemies:"
        ]
        
        for i, monster in enumerate(alive_monsters):
            summary.append(f"  [{i}] {monster.name}")
            summary.append(f"      HP: {monster.current_hp}/{monster.max_hp}")
            summary.append(f"      AC: {monster.armor_class}")
            
        return '\n'.join(summary)


class Item:
    """Base class for items"""
    
    def __init__(self, name, description, consumable=False):
        self.name = name
        self.description = description
        self.consumable = consumable
        
    def use(self, character):
        """Use the item. Override in subclasses."""
        return f"Used {self.name}"


class HealingPotion(Item):
    """Potion that restores HP"""
    
    def __init__(self):
        super().__init__(
            name="Potion of Healing",
            description="Restores 2d4+2 hit points",
            consumable=True
        )
        
    def use(self, character):
        healing = dice.d4(2, 2)
        character.heal(healing)
        return f"{character.name} drinks a healing potion and recovers {healing} HP! ({character.current_hp}/{character.max_hp})"


class Weapon:
    """Weapon class"""
    
    def __init__(self, name, damage, bonus=0, description=""):
        self.name = name
        self.damage = damage
        self.bonus = bonus
        self.description = description
        
    def __str__(self):
        bonus_str = f"+{self.bonus}" if self.bonus > 0 else ""
        return f"{self.name} {bonus_str} ({self.damage} damage)"


class Armor:
    """Armor class"""
    
    def __init__(self, name, ac_bonus, description=""):
        self.name = name
        self.ac_bonus = ac_bonus
        self.description = description
        
    def __str__(self):
        return f"{self.name} (+{self.ac_bonus} AC)"


# Common items
COMMON_ITEMS = {
    'healing_potion': HealingPotion(),
    'longsword': Weapon("Longsword", "1d8", 0, "A versatile steel blade"),
    'greatsword': Weapon("Greatsword", "2d6", 0, "A massive two-handed sword"),
    'dagger': Weapon("Dagger", "1d4", 0, "A small, quick blade"),
    'mace': Weapon("Mace", "1d6", 0, "A blunt weapon favored by clerics"),
    'staff': Weapon("Quarterstaff", "1d6", 0, "A simple wooden staff"),
    'leather_armor': Armor("Leather Armor", 2, "Light, flexible armor"),
    'chain_mail': Armor("Chain Mail", 5, "Heavy metal armor"),
    'scale_mail': Armor("Scale Mail", 4, "Medium armor made of metal scales")   
}
