"""
Item system: Item is the base class for consumables, weapons, armor and treasure
"""
import dice


class Item:
    """Base class for all items"""

    def __init__(self, name, description="", consumable=False, value=0, is_magic=False):
        self.name = name
        self.description = description
        self.consumable = consumable
        self.value = value  # worth in gold pieces
        self.is_magic = is_magic

    def use(self, character):
        """Use the item. Override in subclasses."""
        return f"Used {self.name}"

    def __str__(self):
        return self.name


class HealingPotion(Item):
    """Potion that restores HP"""

    def __init__(self):
        super().__init__(
            name="Potion of Healing",
            description="Restores 2d4+2 hit points",
            consumable=True,
            value=50
        )

    def use(self, character):
        healing = dice.d4(2, 2)
        character.heal(healing)
        return f"{character.name} drinks a healing potion and recovers {healing} HP! ({character.current_hp}/{character.max_hp})"


class Weapon(Item):
    """Weapon item"""

    SIMPLE = "Simple"
    MARTIAL = "Martial"
    CATEGORIES = (SIMPLE, MARTIAL)

    MELEE = "Melee"
    RANGED = "Ranged"
    COMBAT_TYPES = (MELEE, RANGED)

    def __init__(self, name, damage, bonus=0, description="", value=0, is_magic=False,
                 category=SIMPLE, combat_type=MELEE, light=False, heavy=False,
                 two_handed=False, versatile=False, versatile_damage=None,
                 finesse=False, reach=False, thrown=False):
        """
        Args:
            category: Weapon.SIMPLE or Weapon.MARTIAL
            combat_type: Weapon.MELEE or Weapon.RANGED
            light / heavy: weapon size properties (mutually exclusive)
            two_handed: must be wielded with both hands
            versatile: can be wielded with one or two hands
            versatile_damage: damage dice when a versatile weapon is used two-handed
            finesse: may use Strength or Dexterity for attack and damage rolls
            reach: melee weapon that can hit from a larger distance
            thrown: can be used in melee or thrown as a ranged attack (then lost until the battle ends)
        """
        super().__init__(name, description, consumable=False, value=value, is_magic=is_magic)
        if category not in self.CATEGORIES:
            raise ValueError(f"category must be one of {self.CATEGORIES}, got {category!r}")
        if combat_type not in self.COMBAT_TYPES:
            raise ValueError(f"combat_type must be one of {self.COMBAT_TYPES}, got {combat_type!r}")
        if light and heavy:
            raise ValueError("a weapon cannot be both light and heavy")
        if two_handed and versatile:
            raise ValueError("a weapon cannot be both two-handed and versatile")
        if reach and combat_type != self.MELEE:
            raise ValueError("only melee weapons can have reach")
        self.damage = damage
        self.bonus = bonus
        self.category = category
        self.combat_type = combat_type
        self.light = light
        self.heavy = heavy
        self.two_handed = two_handed
        self.versatile = versatile
        self.versatile_damage = versatile_damage if versatile else None
        self.finesse = finesse
        self.reach = reach
        self.thrown = thrown

    @property
    def properties(self):
        """Names of the special properties this weapon has"""
        names = []
        for label, flag in (("Light", self.light), ("Heavy", self.heavy),
                            ("Two-handed", self.two_handed), ("Versatile", self.versatile),
                            ("Finesse", self.finesse), ("Reach", self.reach),
                            ("Thrown", self.thrown)):
            if flag:
                names.append(label)
        return names

    def __str__(self):
        bonus_str = f" +{self.bonus}" if self.bonus > 0 else ""
        return f"{self.name}{bonus_str} ({self.damage} damage)"

    def describe(self):
        """Detailed one-line description including category, type and properties"""
        parts = [self.category, self.combat_type] + self.properties
        return f"{self} - {', '.join(parts)}"


class Armor(Item):
    """Armor item"""

    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    TYPES = (LIGHT, MEDIUM, HEAVY)

    def __init__(self, name, ac_bonus, description="", value=0, armor_type=LIGHT, is_magic=False,
                 min_strength=0, stealth_disadvantage=False):
        super().__init__(name, description, consumable=False, value=value, is_magic=is_magic)
        if armor_type not in self.TYPES:
            raise ValueError(f"armor_type must be one of {self.TYPES}, got {armor_type!r}")
        self.ac_bonus = ac_bonus
        self.armor_type = armor_type  # Light, Medium or Heavy
        self.min_strength = min_strength  # wearer needs Strength greater than this (0 = no limit)
        self.stealth_disadvantage = stealth_disadvantage

    def can_wear(self, strength):
        """True if a wearer with this Strength score meets the requirement"""
        return strength > self.min_strength

    def __str__(self):
        return f"{self.name} ({self.armor_type}, +{self.ac_bonus} AC)"

    def describe(self):
        """Detailed one-line description including requirements and penalties"""
        extras = []
        if self.min_strength:
            extras.append(f"Str > {self.min_strength}")
        if self.stealth_disadvantage:
            extras.append("Stealth disadvantage")
        return f"{self} - " + ", ".join(extras) if extras else str(self)


class Shield(Item):
    """Shield held in one hand; cannot be combined with a two-handed weapon"""

    def __init__(self, name, ac_bonus, description="", value=0, is_magic=False):
        super().__init__(name, description, consumable=False, value=value, is_magic=is_magic)
        self.ac_bonus = ac_bonus

    def __str__(self):
        return f"{self.name} (+{self.ac_bonus} AC)"


class Treasure(Item):
    """Valuables such as gems and jewelry, kept for their gold value"""

    def __init__(self, name, value, description="", is_magic=False):
        super().__init__(name, description, consumable=False, value=value, is_magic=is_magic)

    def __str__(self):
        return f"{self.name} ({self.value} gp)"


# Common items
COMMON_ITEMS = {
    'healing_potion': HealingPotion(),
    'longsword': Weapon("Longsword", "1d8", 0, "A versatile steel blade", value=15,
                       category=Weapon.MARTIAL, versatile=True, versatile_damage="1d10"),
    'greatsword': Weapon("Greatsword", "2d6", 0, "A massive two-handed sword", value=50,
                         category=Weapon.MARTIAL, heavy=True, two_handed=True),
    'dagger': Weapon("Dagger", "1d4", 0, "A small, quick blade", value=2,
                     category=Weapon.SIMPLE, light=True, finesse=True, thrown=True),
    'mace': Weapon("Mace", "1d6", 0, "A blunt weapon favored by clerics", value=12,
                  category=Weapon.SIMPLE),
    'staff': Weapon("Quarterstaff", "1d6", 0, "A simple wooden staff", value=5,
                   category=Weapon.SIMPLE, versatile=True, versatile_damage="1d8"),
    'battle_axe': Weapon("Battle Axe", "1d8", 0, "A heavy axe made for war", value=20,
                      category=Weapon.MARTIAL, versatile=True, versatile_damage="1d10"),
    'large_club': Weapon("Large Club", "2d6", 0, "A huge, crude club", value=15,
                      category=Weapon.SIMPLE, heavy=True, two_handed=True),
    'magic_sword': Weapon("Magic Sword", "1d8", 1, "A finely enchanted blade", value=2000, is_magic=True,
                        category=Weapon.MARTIAL, versatile=True, versatile_damage="1d10"),
    'shield': Shield("Shield", 2, "A sturdy shield of wood and iron", value=10),
    'ruby': Treasure("Ruby", 1000, "A flawless blood-red gem"),
    'leather_armor': Armor("Leather Armor", 1, "Light, flexible armor", value=10, armor_type=Armor.LIGHT),
    'chain_mail': Armor("Chain Mail", 6, "Heavy metal armor", value=75, armor_type=Armor.HEAVY,
                        min_strength=13, stealth_disadvantage=True),
    'scale_mail': Armor("Scale Mail", 4, "Medium armor made of metal scales", value=50,
                        armor_type=Armor.MEDIUM, stealth_disadvantage=True),
    'splint_mail': Armor("Splint Mail", 7, "Vertical metal strips riveted to leather", value=200,
                         armor_type=Armor.HEAVY, min_strength=15, stealth_disadvantage=True),
    'plate_mail': Armor("Plate Mail", 8, "Full suit of interlocking metal plates", value=1500,
                        armor_type=Armor.HEAVY, min_strength=15, stealth_disadvantage=True)
}
