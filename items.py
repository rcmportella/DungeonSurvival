"""
Item system: Item is the base class for consumables, weapons, armor and treasure
"""
import dice


class Item:
    """Base class for all items"""

    def __init__(self, name, description="", consumable=False, value=0):
        self.name = name
        self.description = description
        self.consumable = consumable
        self.value = value  # worth in gold pieces

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

    def __init__(self, name, damage, bonus=0, description="", value=0):
        super().__init__(name, description, consumable=False, value=value)
        self.damage = damage
        self.bonus = bonus

    def __str__(self):
        bonus_str = f" +{self.bonus}" if self.bonus > 0 else ""
        return f"{self.name}{bonus_str} ({self.damage} damage)"


class Armor(Item):
    """Armor item"""

    def __init__(self, name, ac_bonus, description="", value=0):
        super().__init__(name, description, consumable=False, value=value)
        self.ac_bonus = ac_bonus

    def __str__(self):
        return f"{self.name} (+{self.ac_bonus} AC)"


class Treasure(Item):
    """Valuables such as gems and jewelry, kept for their gold value"""

    def __init__(self, name, value, description=""):
        super().__init__(name, description, consumable=False, value=value)

    def __str__(self):
        return f"{self.name} ({self.value} gp)"


# Common items
COMMON_ITEMS = {
    'healing_potion': HealingPotion(),
    'longsword': Weapon("Longsword", "1d8", 0, "A versatile steel blade"),
    'greatsword': Weapon("Greatsword", "2d6", 0, "A massive two-handed sword"),
    'dagger': Weapon("Dagger", "1d4", 0, "A small, quick blade"),
    'mace': Weapon("Mace", "1d6", 0, "A blunt weapon favored by clerics"),
    'staff': Weapon("Quarterstaff", "1d6", 0, "A simple wooden staff"),
    'battle_axe': Weapon("Battle Axe", "1d8", 0, "A heavy axe made for war"),
    'large_club': Weapon("Large Club", "2d6", 0, "A huge, crude club"),
    'magic_sword': Weapon("Magic Sword", "1d8", 1, "A finely enchanted blade", value=2000),
    'ruby': Treasure("Ruby", 1000, "A flawless blood-red gem"),
    'leather_armor': Armor("Leather Armor", 2, "Light, flexible armor"),
    'chain_mail': Armor("Chain Mail", 5, "Heavy metal armor"),
    'scale_mail': Armor("Scale Mail", 4, "Medium armor made of metal scales")
}
