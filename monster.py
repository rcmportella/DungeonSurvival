"""
Monster and enemy classes for D20 combat
"""
import dice


class Monster:
    """
    Generic monster/enemy following D20 rules
    """
    
    def __init__(self, name, hit_dice="1d8", armor_class=10, 
                 attack_bonus=0, damage="1d6", 
                 special_abilities=None, treasure=None):
        self.name = name
        self.hit_dice = hit_dice
        self.armor_class = armor_class
        self.attack_bonus = attack_bonus
        self.damage = damage
        self.special_abilities = special_abilities or []
        self.treasure = treasure or []
        
        # Calculate HP from hit dice
        self.max_hp = self._roll_hit_points()
        self.current_hp = self.max_hp
        
        # Basic saving throws (can be customized per monster)
        self.fortitude_save = 0
        self.reflex_save = 0
        self.will_save = 0
        
    def _roll_hit_points(self):
        """Roll hit points based on hit dice"""
        if 'd' in self.hit_dice:
            count, sides = self.hit_dice.split('d')
            count = int(count)
            sides = int(sides.split('+')[0].split('-')[0])  # Handle modifiers
            
            hp = 0
            for _ in range(count):
                hp += dice.roll(sides)
                
            # Add any flat modifier
            if '+' in self.hit_dice:
                modifier = int(self.hit_dice.split('+')[1])
                hp += modifier
            elif '-' in self.hit_dice:
                modifier = int(self.hit_dice.split('-')[1])
                hp -= modifier
                
            return max(1, hp)
        else:
            return int(self.hit_dice)
            
    def attack(self, target):
        """
        Attack a target character.
        
        Args:
            target: Character being attacked
            
        Returns:
            Tuple of (hit: bool, damage: int, message: str)
        """
        attack_roll = dice.d20(1, self.attack_bonus)
        
        if attack_roll >= target.get_armor_class():
            # Hit!
            damage_dealt = self._roll_damage()
            target.take_damage(damage_dealt)
            return True, attack_roll,damage_dealt, f"{self.name} hits {target.name} for {damage_dealt} damage!"
        else:
            return False, attack_roll,0, f"{self.name} misses {target.name}!"
            
    def _roll_damage(self):
        """Roll damage dice"""
        if '+' in self.damage:
            dice_part, mod = self.damage.split('+')
            mod = int(mod)
        elif '-' in self.damage:
            dice_part, mod = self.damage.split('-')
            mod = -int(mod)
        else:
            dice_part = self.damage
            mod = 0
            
        count, sides = dice_part.split('d')
        count = int(count)
        sides = int(sides)
        
        return max(1, dice.roll(sides, count, mod))
        
    def take_damage(self, damage):
        """Take damage and return True if still alive"""
        self.current_hp -= damage
        return self.current_hp > 0
        
    def is_alive(self):
        """Check if monster is still alive"""
        return self.current_hp > 0
        
    def saving_throw(self, save_type):
        """Make a saving throw"""
        if save_type == 'fortitude':
            return dice.d20(1, self.fortitude_save)
        elif save_type == 'reflex':
            return dice.d20(1, self.reflex_save)
        elif save_type == 'will':
            return dice.d20(1, self.will_save)
        else:
            return dice.d20()
            
    def __str__(self):
        return f"{self.name} (AC {self.armor_class}, HP {self.current_hp}/{self.max_hp})"


# Predefined monsters
class Goblin(Monster):
    """Weak humanoid enemy"""
    def __init__(self):
        super().__init__(
            name="Goblin",
            hit_dice="2d6",
            armor_class=12,
            attack_bonus=0,
            damage="1d4+2",
            treasure=["10 gold pieces"]
        )
        self.reflex_save = 3


class Orc(Monster):
    """Medium humanoid warrior"""
    def __init__(self):
        super().__init__(
            name="Orc",
            hit_dice="2d8",
            armor_class=13,
            attack_bonus=1,
            damage="1d8",
            treasure=["20 gold pieces", "Battle axe"]
        )
        self.fortitude_save = 3


class Skeleton(Monster):
    """Undead warrior"""
    def __init__(self):
        super().__init__(
            name="Skeleton",
            hit_dice="1d12",
            armor_class=13,
            attack_bonus=2,
            damage="1d6+1",
            special_abilities=["Undead: immune to mind-affecting"],
            treasure=[]
        )
        self.will_save = -2


class Ogre(Monster):
    """Large giant enemy"""
    def __init__(self):
        super().__init__(
            name="Ogre",
            hit_dice="4d8+8",
            armor_class=16,
            attack_bonus=8,
            damage="2d8+7",
            treasure=["50 gold pieces", "Large club"]
        )
        self.fortitude_save = 5


class Dragon(Monster):
    """Powerful dragon boss"""
    def __init__(self):
        super().__init__(
            name="Young Red Dragon",
            hit_dice="13d12+39",
            armor_class=21,
            attack_bonus=18,
            damage="2d6+7",
            special_abilities=["Breath Weapon: 8d10 fire damage, Reflex DC 19 for half"],
            treasure=["500 gold pieces", "Magic sword +1", "Ruby worth 1000gp"]
        )
        self.fortitude_save = 11
        self.reflex_save = 8
        self.will_save = 8
        
    def breath_weapon(self, target):
        """Dragon's breath weapon attack"""
        damage = dice.d10(8)
        save_roll = target.saving_throw('reflex')
        
        if save_roll >= 19:
            damage = damage // 2
            result = f"{target.name} dodges! Takes {damage} fire damage (halved)."
        else:
            result = f"{target.name} is burned! Takes {damage} fire damage!"
            
        target.take_damage(damage)
        return f"{self.name} breathes fire! {result}"


class GiantSpider(Monster):
    """Venomous spider"""
    def __init__(self):
        super().__init__(
            name="Giant Spider",
            hit_dice="2d8",
            armor_class=14,
            attack_bonus=4,
            damage="1d6",
            special_abilities=["Poison: DC 14 Fort save or 1d4 STR damage"],
            treasure=[]
        )
        self.reflex_save = 4


class Zombie(Monster):
    """Slow undead creature"""
    def __init__(self):
        super().__init__(
            name="Zombie",
            hit_dice="2d12+3",
            armor_class=11,
            attack_bonus=2,
            damage="1d6+1",
            special_abilities=["Undead: immune to mind-affecting"],
            treasure=[]
        )
        self.fortitude_save = 3
        self.will_save = -2


class Troll(Monster):
    """Regenerating monster"""
    def __init__(self):
        super().__init__(
            name="Troll",
            hit_dice="6d8+36",
            armor_class=16,
            attack_bonus=9,
            damage="1d6+6",
            special_abilities=["Regeneration 5: heals 5 HP per round"],
            treasure=["30 gold pieces"]
        )
        self.fortitude_save = 9


# Monster factory
MONSTER_TYPES = {
    'goblin': Goblin,
    'orc': Orc,
    'skeleton': Skeleton,
    'ogre': Ogre,
    'dragon': Dragon,
    'giant_spider': GiantSpider,
    'zombie': Zombie,
    'troll': Troll,
}


def create_monster(monster_type):
    """
    Create a monster by type name.
    
    Args:
        monster_type: String name of monster type
        
    Returns:
        Monster instance
    """
    monster_class = MONSTER_TYPES.get(monster_type.lower())
    if monster_class:
        return monster_class()
    else:
        # Default generic monster
        return Monster(name="Unknown Creature", hit_dice="2d8", armor_class=12)
