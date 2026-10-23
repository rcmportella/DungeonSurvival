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

    def __init__(self, name, damage, bonus=0, description="", value=0, is_magic=False):
        super().__init__(name, description, consumable=False, value=value, is_magic=is_magic)
        self.damage = damage
        self.bonus = bonus

    def __str__(self):
        bonus_str = f" +{self.bonus}" if self.bonus > 0 else ""
        return f"{self.name}{bonus_str} ({self.damage} damage)"


class Armor(Item):
    """Armor item"""

    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    TYPES = (LIGHT, MEDIUM, HEAVY)

    def __init__(self, name, ac_bonus, description="", value=0, armor_type=LIGHT, is_magic=False):
        super().__init__(name, description, consumable=False, value=value, is_magic=is_magic)
        if armor_type not in self.TYPES:
            raise ValueError(f"armor_type must be one of {self.TYPES}, got {armor_type!r}")
        self.ac_bonus = ac_bonus
        self.armor_type = armor_type  # Light, Medium or Heavy

    def __str__(self):
        return f"{self.name} ({self.armor_type}, +{self.ac_bonus} AC)"


class Treasure(Item):
    """Valuables such as gems and jewelry, kept for their gold value"""

    def __init__(self, name, value, description="", is_magic=False):
        super().__init__(name, description, consumable=False, value=value, is_magic=is_magic)

    def __str__(self):
        return f"{self.name} ({self.value} gp)"


# Common items
COMMON_ITEMS = {
    'healing_potion': HealingPotion(),
    'longsword': Weapon("Longsword", "1d8", 0, "A versatile steel blade", value=15),
    'greatsword': Weapon("Greatsword", "2d6", 0, "A massive two-handed sword", value=50),
    'dagger': Weapon("Dagger", "1d4", 0, "A small, quick blade", value=2),
    'mace': Weapon("Mace", "1d6", 0, "A blunt weapon favored by clerics", value=12),
    'staff': Weapon("Quarterstaff", "1d6", 0, "A simple wooden staff", value=5),
    'battle_axe': Weapon("Battle Axe", "1d8", 0, "A heavy axe made for war", value=20),
    'large_club': Weapon("Large Club", "2d6", 0, "A huge, crude club", value=15),
    'magic_sword': Weapon("Magic Sword", "1d8", 1, "A finely enchanted blade", value=2000, is_magic=True),
    'ruby': Treasure("Ruby", 1000, "A flawless blood-red gem"),
    'leather_armor': Armor("Leather Armor", 1, "Light, flexible armor", value=10, armor_type=Armor.LIGHT),
    'chain_mail': Armor("Chain Mail", 6, "Heavy metal armor", value=75, armor_type=Armor.HEAVY),
    'scale_mail': Armor("Scale Mail", 7, "Heavy armor made of metal scales", value=200, armor_type=Armor.HEAVY)
}
