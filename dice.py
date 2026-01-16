"""
Dice rolling utilities for D20 system
"""
import random


def roll(sides, count=1, modifier=0):
    """
    Roll dice with modifier.
    
    Args:
        sides: Number of sides on the die
        count: Number of dice to roll
        modifier: Modifier to add to the result
        
    Returns:
        Total result of the roll
    """
    total = sum(random.randint(1, sides) for _ in range(count))
    return total + modifier


def d4(count=1, modifier=0):
    """Roll d4"""
    return roll(4, count, modifier)


def d6(count=1, modifier=0):
    """Roll d6"""
    return roll(6, count, modifier)


def d8(count=1, modifier=0):
    """Roll d8"""
    return roll(8, count, modifier)


def d10(count=1, modifier=0):
    """Roll d10"""
    return roll(10, count, modifier)


def d12(count=1, modifier=0):
    """Roll d12"""
    return roll(12, count, modifier)


def d20(count=1, modifier=0):
    """Roll d20"""
    return roll(20, count, modifier)


def d100(count=1, modifier=0):
    """Roll d100 (percentile)"""
    return roll(100, count, modifier)


def ability_score():
    """
    Roll 4d6 and drop lowest, standard method for ability scores.
    
    Returns:
        Ability score (3-18)
    """
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.sort()
    return sum(rolls[1:])  # Drop lowest


def modifier(score):
    """
    Calculate ability modifier from ability score.
    
    Args:
        score: Ability score
        
    Returns:
        Modifier value
    """
    return (score - 10) // 2
