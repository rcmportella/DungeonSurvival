"""
Combat system with D20 mechanics
"""
import copy
import random
import dice
from items import Item, HealingPotion, Weapon, Armor, Shield, Treasure, COMMON_ITEMS  # noqa: F401 (re-exported)


class Combat:
    """
    Handles turn-based combat between character and monsters
    """
    
    def __init__(self, party_members, monsters):
        """
        Initialize combat and roll initiative once for the whole fight.
        
        Args:
            party_members: List of party characters (or a single character)
            monsters: List of monsters or single monster
        """
        if not isinstance(party_members, (list, tuple)):
            party_members = [party_members]
        self.party_members = list(party_members)
        self.character = self.party_members[0]
        
        if not isinstance(monsters, list):
            self.monsters = [monsters]
        else:
            self.monsters = monsters
            
        self.round = 1
        self.turn_index = 0
        self.status = 'ongoing'
        self.menu = None  # pending UI selection (spell/item/target)
        self.combat_log = []
        self.initiative_order = self.roll_initiative()
        self.combat_log.append("Initiative order: " + ", ".join(
            f"{c.name} ({init})" for c, init, _ in self.initiative_order))
        self.start()
        
    def roll_initiative(self):
        """
        Roll initiative for all combatants.
        
        Returns:
            Ordered list of (combatant, initiative, is_player) tuples
        """
        entries = []
        for member in self.party_members:
            entries.append((member, member.roll_initiative(),
                            member.get_initiative_modifier(), True))
        for monster in self.monsters:
            entries.append((monster, monster.roll_initiative(),
                            monster.get_initiative_modifier(), False))

        # D20 rules: highest total acts first; ties go to the higher modifier,
        # then a coin flip
        entries.sort(key=lambda e: (e[1], e[2], dice.roll(20)), reverse=True)
        return [(c, init, is_player) for c, init, _, is_player in entries]

    def _party_alive(self):
        return any(m.is_alive() for m in self.party_members)
        
    def alive_monsters(self):
        return [m for m in self.monsters if m.is_alive()]

    def current_actor(self):
        """Party member whose turn it is, or None when combat is over"""
        if self.status != 'ongoing':
            return None
        return self.initiative_order[self.turn_index][0]

    def _result(self, new_log_start, message=None):
        messages = {
            'victory': 'All enemies defeated!',
            'defeat': 'Your party has been defeated!',
            'fled': 'The party fled from combat!',
            'ongoing': 'Turn complete.',
        }
        result = {
            'status': self.status,
            'message': message or messages[self.status],
            'log': self.combat_log[new_log_start:],
        }
        if self.status == 'victory':
            result['rewards'] = self._collect_rewards()
        return result

    def _check_end(self):
        if not self.alive_monsters():
            self.status = 'victory'
        elif not self._party_alive():
            self.status = 'defeat'
        return self.status != 'ongoing'

    def _next_turn(self):
        self.turn_index += 1
        if self.turn_index >= len(self.initiative_order):
            self.turn_index = 0
            self.round += 1
            self.combat_log.append(f"--- Round {self.round} ---")

    def _run_until_player(self):
        """Resolve monster turns until a living party member must act"""
        while not self._check_end():
            actor, _, is_player = self.initiative_order[self.turn_index]
            if not actor.is_alive():
                self._next_turn()
            elif is_player:
                return
            else:
                self._monster_turn(actor)
                self._next_turn()

    def start(self):
        """Begin combat; returns the result after any leading monster turns"""
        start = len(self.combat_log)
        self.combat_log.append("--- Round 1 ---")
        self._run_until_player()
        return self._result(start)

    def _monster_turn(self, monster):
        target = random.choice([m for m in self.party_members if m.is_alive()])
        roll = dice.roll(20)
        total = roll + monster.attack_bonus
        ac = target.get_armor_class()
        log = self.combat_log
        log.append(f"{monster.name} attacks {target.name}: d20={roll} {monster.attack_bonus:+d} = {total} vs AC {ac}")
        if total >= ac:
            damage = monster._roll_damage()
            target.take_damage(damage)
            log.append(f"  HIT! {damage} damage ({monster.damage}) to {target.name} (HP {target.current_hp}/{target.max_hp})")
            if not target.is_alive():
                log.append(f"  {target.name} has fallen!")
        else:
            log.append(f"  MISS! {target.name} is not hurt.")

    def _attack(self, member, target):
        str_mod = member.get_ability_modifier('strength')
        bonus = member.base_attack_bonus + str_mod
        roll = dice.roll(20)
        total = roll + bonus
        weapon = member.equipped_weapon.name if member.equipped_weapon else "unarmed"
        log = self.combat_log
        log.append(f"{member.name} attacks {target.name} with {weapon}: d20={roll} {bonus:+d} = {total} vs AC {target.armor_class}")
        if total >= target.armor_class:
            dmg_dice = member.get_weapon_damage()
            damage = max(1, member._roll_damage(dmg_dice) + str_mod)
            target.take_damage(damage)
            log.append(f"  HIT! {damage} damage ({dmg_dice}{str_mod:+d}) to {target.name} (HP {max(0, target.current_hp)}/{target.max_hp})")
            if not target.is_alive():
                log.append(f"  {target.name} is defeated!")
        else:
            log.append(f"  MISS! {target.name} is not hurt.")

    def perform(self, action, target=None):
        """
        Perform the current party member's action, then resolve monster turns
        until the next party member must act.

        Args:
            action: {'type': 'attack'}, {'type': 'spell', 'spell': spell},
                    {'type': 'item', 'item_name': name}, {'type': 'defend'}
                    or {'type': 'flee'}
            target: Monster or party member targeted by the action

        Returns:
            Dictionary with status, message and the new log lines
        """
        member = self.current_actor()
        if member is None:
            return self._result(len(self.combat_log))
        start = len(self.combat_log)
        kind = action['type']
        log = self.combat_log

        if kind == 'attack':
            self._attack(member, target)
        elif kind == 'spell':
            spell = action['spell']
            hp_before = target.current_hp
            ok, text = member.cast_spell(spell, target)
            log.append(f"{member.name} casts {spell.name} on {target.name}")
            log.append(f"  {text}")
            diff = hp_before - target.current_hp
            if ok and diff > 0:
                log.append(f"  {target.name} takes {diff} damage (HP {max(0, target.current_hp)}/{target.max_hp})")
                if not target.is_alive():
                    log.append(f"  {target.name} is defeated!")
        elif kind == 'item':
            text = member.use_item(action['item_name'])
            log.append(f"{member.name}: {text or 'Cannot use ' + action['item_name'] + '!'}")
        elif kind == 'flee':
            roll = dice.roll(20)
            mod = member.get_ability_modifier('dexterity')
            log.append(f"{member.name} tries to flee: d20={roll} {mod:+d} = {roll + mod} (needs 10)")
            if roll + mod >= 10:
                log.append("  The party escapes!")
                self.status = 'fled'
                return self._result(start)
            log.append("  Failed to flee!")

        if not self._check_end():
            self._next_turn()
            self._run_until_player()
        return self._result(start)
        
    def _collect_rewards(self):
        """Collect treasure from defeated monsters"""
        rewards = {
            'gold': 0,
            'items': [],
            'experience': 0
        }
        
        for monster in self.monsters:
            rewards['gold'] += monster.gold
            rewards['items'].extend(copy.copy(item) for item in monster.treasure)
                    
            rewards['experience'] += monster.xp
            
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
