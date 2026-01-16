"""
Spell system based on OGL D20 rules
"""
import dice


class Spell:
    """Base spell class"""
    
    def __init__(self, name, level, school, casting_time="1 action", 
                 range_ft=30, duration="Instantaneous", description=""):
        self.name = name
        self.level = level  # 0 for cantrips, 1-9 for spell levels
        self.school = school  # Evocation, Abjuration, etc.
        self.casting_time = casting_time
        self.range_ft = range_ft
        self.duration = duration
        self.description = description
        
    def cast(self, caster, target=None):
        """
        Cast the spell. Override in subclasses.
        
        Args:
            caster: Character casting the spell
            target: Target of the spell (can be caster, enemy, or None)
            
        Returns:
            Result description
        """
        return f"{caster.name} casts {self.name}!"
        
    def __str__(self):
        level_str = "Cantrip" if self.level == 0 else f"Level {self.level}"
        return f"{self.name} ({level_str} {self.school}): {self.description}"


class MagicMissile(Spell):
    """Magic Missile spell - automatic hit"""
    
    def __init__(self):
        super().__init__(
            name="Magic Missile",
            level=1,
            school="Evocation",
            range_ft=120,
            description="Three glowing darts strike unerringly. Each dart deals 1d4+1 force damage."
        )
        
    def cast(self, caster, target=None):
        if target is None:
            return "No target selected for Magic Missile"
            
        missiles = 3
        total_damage = 0
        for _ in range(missiles):
            damage = dice.d4(1, 1)
            total_damage += damage
            
        target.take_damage(total_damage)
        return f"{self.name} hits {target.name} for {total_damage} force damage!"


class Fireball(Spell):
    """Fireball spell - area effect damage"""
    
    def __init__(self):
        super().__init__(
            name="Fireball",
            level=3,
            school="Evocation",
            range_ft=150,
            description="A bright streak explodes with a roar dealing 8d6 fire damage. Reflex save DC 15 for half."
        )
        
    def cast(self, caster, target=None):
        if target is None:
            return "No target selected for Fireball"
            
        damage = dice.d6(8)
        
        # Target makes Reflex save
        save_dc = 15
        save_roll = target.saving_throw('reflex')
        
        if save_roll >= save_dc:
            damage = damage // 2
            result = f"{target.name} saves! Takes {damage} fire damage (halved)."
        else:
            result = f"{target.name} fails save! Takes {damage} fire damage!"
            
        target.take_damage(damage)
        return f"{self.name} engulfs the area! {result}"


class CureWounds(Spell):
    """Cure Light Wounds - healing spell"""
    
    def __init__(self):
        super().__init__(
            name="Cure Light Wounds",
            level=1,
            school="Conjuration",
            range_ft=0,
            casting_time="1 action",
            description="Heals 1d8 + caster's Wisdom modifier hit points."
        )
        
    def cast(self, caster, target=None):
        if target is None:
            target = caster
            
        wis_mod = caster.get_ability_modifier('wisdom')
        healing = dice.d8(1, wis_mod)
        target.heal(healing)
        
        return f"{self.name} heals {target.name} for {healing} HP! ({target.current_hp}/{target.max_hp})"


class Shield(Spell):
    """Shield spell - protective magic"""
    
    def __init__(self):
        super().__init__(
            name="Shield",
            level=1,
            school="Abjuration",
            range_ft=0,
            duration="1 round",
            description="An invisible barrier grants +4 to AC until your next turn."
        )
        
    def cast(self, caster, target=None):
        if target is None:
            target = caster
            
        # Temporarily increase AC
        target.armor_class += 4
        return f"A shimmering shield surrounds {target.name}! AC increased to {target.armor_class}."


class BurningHands(Spell):
    """Burning Hands - cone of fire"""
    
    def __init__(self):
        super().__init__(
            name="Burning Hands",
            level=1,
            school="Evocation",
            range_ft=15,
            description="A cone of fire deals 3d4 fire damage. Reflex save DC 13 for half."
        )
        
    def cast(self, caster, target=None):
        if target is None:
            return "No target selected for Burning Hands"
            
        damage = dice.d4(3)
        
        save_dc = 13
        save_roll = target.saving_throw('reflex')
        
        if save_roll >= save_dc:
            damage = damage // 2
            result = f"{target.name} partially dodges! Takes {damage} fire damage (halved)."
        else:
            result = f"{target.name} is engulfed! Takes {damage} fire damage!"
            
        target.take_damage(damage)
        return f"Flames shoot from {caster.name}'s hands! {result}"


class LightningBolt(Spell):
    """Lightning Bolt - line of electricity"""
    
    def __init__(self):
        super().__init__(
            name="Lightning Bolt",
            level=3,
            school="Evocation",
            range_ft=120,
            description="A stroke of lightning deals 8d6 electricity damage. Reflex save DC 15 for half."
        )
        
    def cast(self, caster, target=None):
        if target is None:
            return "No target selected for Lightning Bolt"
            
        damage = dice.d6(8)
        
        save_dc = 15
        save_roll = target.saving_throw('reflex')
        
        if save_roll >= save_dc:
            damage = damage // 2
            result = f"{target.name} partially evades! Takes {damage} electricity damage (halved)."
        else:
            result = f"{target.name} is struck! Takes {damage} electricity damage!"
            
        target.take_damage(damage)
        return f"A bolt of lightning streaks forth! {result}"


class Bless(Spell):
    """Bless - buff spell"""
    
    def __init__(self):
        super().__init__(
            name="Bless",
            level=1,
            school="Enchantment",
            duration="1 minute",
            description="Allies gain +1 to attack rolls and saving throws."
        )
        
    def cast(self, caster, target=None):
        if target is None:
            target = caster
            
        # Simple implementation: temporary BAB boost
        target.base_attack_bonus += 1
        return f"{target.name} is blessed! Attack bonus increased."


class DetectMagic(Spell):
    """Detect Magic cantrip"""
    
    def __init__(self):
        super().__init__(
            name="Detect Magic",
            level=0,
            school="Divination",
            range_ft=60,
            duration="Concentration, up to 1 minute",
            description="Sense the presence of magic within 60 feet."
        )
        
    def cast(self, caster, target=None):
        return f"{caster.name} senses magical auras in the area..."


class RayOfFrost(Spell):
    """Ray of Frost cantrip"""
    
    def __init__(self):
        super().__init__(
            name="Ray of Frost",
            level=0,
            school="Evocation",
            range_ft=60,
            description="A frigid beam deals 1d8 cold damage."
        )
        
    def cast(self, caster, target=None):
        if target is None:
            return "No target selected for Ray of Frost"
            
        # Make a ranged touch attack
        int_mod = caster.get_ability_modifier('intelligence')
        attack_roll = dice.d20(1, caster.base_attack_bonus + int_mod)
        
        if attack_roll >= target.armor_class:
            damage = dice.d8()
            target.take_damage(damage)
            return f"A ray of frost strikes {target.name} for {damage} cold damage!"
        else:
            return f"The ray of frost misses {target.name}!"


# Spell library - available spells
SPELL_LIBRARY = {
    # Cantrips (Level 0)
    'detect_magic': DetectMagic(),
    'ray_of_frost': RayOfFrost(),
    
    # Level 1
    'magic_missile': MagicMissile(),
    'cure_light_wounds': CureWounds(),
    'shield': Shield(),
    'burning_hands': BurningHands(),
    'bless': Bless(),
    
    # Level 3
    'fireball': Fireball(),
    'lightning_bolt': LightningBolt(),
}


def get_spell(spell_name):
    """Get a spell from the library by name"""
    return SPELL_LIBRARY.get(spell_name.lower().replace(' ', '_'))


def list_spells_by_level(level):
    """List all spells of a given level"""
    return [spell for spell in SPELL_LIBRARY.values() if spell.level == level]
