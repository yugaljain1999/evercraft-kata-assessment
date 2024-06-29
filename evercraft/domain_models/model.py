from math import ceil, floor  

class Character:
    ALIGN_EVIL = "Evil"
    ALIGN_GOOD = "Good"
    ALIGN_NEUTRAL = "Neutral"
    
    RACE_HUMAN = "Human"
    RACE_ORC = "Orc"
    RACE_DWARF = "Dwarf"
    RACE_ELF = "Elf"
    RACE_HALFLING = "Halfling"

    ABILITIES_DICT = {
        "1": -5,
        "2": -4,
        "3": -4,
        "4": -3,
        "5": -3,
        "6": -2,
        "7": -2,
        "8": -1,
        "9": -1,
        "10": 0,
        "11": 0,
        "12": 1,
        "13": 1,
        "14": 2,
        "15": 2,
        "16": 3,
        "17": 3,
        "18": 4,
        "19": 4,
        "20": 5,
    }
    
    class_counter = 0

    def __init__(self, name=None, alignment=None, race=None):
        self.armor_class = 10
        self.hit_points = 5
        self.xp = 0
        self.level = 1
        self.alive = 1

        self.id = Character.class_counter
        Character.class_counter += 1

        self.strength = '10'
        self.dexterity = '10'
        self.constitution = '10'
        self.wisdom = '10'
        self.intelligence = '10'
        self.charisma = '10'

        self.name = name if name else 'User'
        self.alignment = alignment if alignment else Character.ALIGN_NEUTRAL
        self.race = race if race else Character.RACE_HUMAN

        self.apply_race_modifiers()

    def apply_race_modifiers(self):
        if self.race == Character.RACE_ORC:
            self.strength = str(int(self.strength) + 2)
            self.intelligence = str(int(self.intelligence) - 1)
            self.wisdom = str(int(self.wisdom) - 1)
            self.charisma = str(int(self.charisma) - 1)
            self.armor_class += 2
        elif self.race == Character.RACE_DWARF:
            self.constitution = str(int(self.constitution) + 1)
            self.charisma = str(int(self.charisma) - 1)
        elif self.race == Character.RACE_ELF:
            self.dexterity = str(int(self.dexterity) + 1)
            self.constitution = str(int(self.constitution) - 1)
        elif self.race == Character.RACE_HALFLING:
            self.dexterity = str(int(self.dexterity) + 1)
            self.strength = str(int(self.strength) - 1)
            self.armor_class += 2   

     # SETTERS AND GETTERS   
    def get_name(self):
        return self.name

    def set_alignment(self, alignment):
        self.alignment = alignment

    def get_alignment(self):
        return self.alignment

    def set_dexterity(self, dexVal):
      self.dexterity = dexVal
      self.armor_class = self.armor_class + self.ABILITIES_DICT[self.dexterity]

    # If constitution is updated, hit points also need to be updated
    def set_constitution(self, consVal):
        self.constitution = consVal
        add_me = self.ABILITIES_DICT[self.constitution]
        if add_me < 1:
            add_me = 1
        self.hit_points = self.hit_points + add_me
    
    def attack_attempt(self, opponent, number_roll):
        # +1 to dice for every even level reached
        if self.level > 1:
            number_roll = number_roll + floor(self.level / 2)
        
        attack_bonus = self.weapon.attack_bonus if hasattr(self, 'weapon') else 0
        attack_roll = number_roll + self.ABILITIES_DICT[self.strength] + attack_bonus

        if attack_roll == 20:
            return self.critical_hit(opponent)
        elif attack_roll >= opponent.armor_class:
            return self.hit(opponent)
        else:
            return self.miss(opponent)

    def critical_hit(self, opponent):
        self.add_xp()
        crit_multiplier = self.weapon.crit_multiplier if hasattr(self, 'weapon') else 1
        subtract_me = crit_multiplier * (2 + (2 * self.ABILITIES_DICT[self.strength]))
        if subtract_me < 1:
            subtract_me = 1
        opponent.hit_points -= subtract_me
        if opponent.hit_points <= 0:
            opponent.alive = 0
        return opponent.hit_points

    def hit(self, opponent):
        self.add_xp()
        damage_bonus = self.weapon.damage_bonus if hasattr(self, 'weapon') else 0
        subtract_me = (1 + self.ABILITIES_DICT[self.strength] + damage_bonus)
        if subtract_me < 1:
            subtract_me = 1
        opponent.hit_points -= subtract_me
        if opponent.hit_points <= 0:
            opponent.alive = 0
        return opponent.hit_points

    # Attack --> +10 xp AND checks level increase every time 
    def add_xp(self):
        self.xp = self.xp + 10
        if self.xp >= 1000:
            check = floor(self.xp / 1000) + 1
            if (check != self.level):
                self.level = check
                self.hit_points = self.hit_points + 5 + self.ABILITIES_DICT[self.constitution]
    
    def equip_weapon(self, weapon):
        self.weapon = weapon

    def equip_armor(self, armor):
        self.armor = armor
        self.armor_class += armor.armor_class_bonus

    def equip_item(self, item, alignment = ""):
        self.item = item
        self.armor_class += item.armor_class_bonus

        if alignment == self.ALIGN_NEUTRAL:
            self.item.attack_bonus = self.item.attack_bonus + 1
        elif alignment == self.ALIGN_EVIL:
            self.item.attack_bonus = self.item.attack_bonus + 2

    # Called from rogue class
    def fix_AC(self):
      # From rogue class...Rogue opponent doesn't get to apply dexterity to AC
        self.armor_class = self.armor_class - self.ABILITIES_DICT[self.dexterity]
        return self.armor_class

    def switch_back_AC(self):
        # From rogue class...Rogue opponent gets dexterity back after attack
        self.armor_class = self.armor_class + self.ABILITIES_DICT[self.dexterity]
        return self.armor_class

    def miss(self, opponent):
        return opponent.hit_points


# Children of character class

class Fighter(Character):
    """
    Attack roll is increased by +1 for every level instead of every other level
    10 XP added per level instead of 5
    """
    def attack_attempt(self, opponent, number_roll):
        attack_roll = number_roll + self.ABILITIES_DICT[self.strength] + self.level
        if attack_roll == 20:
            return self.critical_hit(opponent)
        elif attack_roll >= opponent.armor_class:
            return self.hit(opponent)
        elif attack_roll < opponent.armor_class:
            return self.miss(opponent)

    def add_xp(self):
        self.xp = self.xp + 10
        if self.xp >= 1000:
            check = floor(self.xp / 1000) + 1
            if (check != self.level):
                self.level = check
                self.hit_points = self.hit_points + 10 + self.ABILITIES_DICT[self.constitution]

class Rogue(Character):
    """
    Triple damage on critical hits
    Opponent cannot use POSITIVE dex modifier to increase armor class
    Cannot have Good alignment
    Sub strength for dex modifier in attack roll
    """
    def set_alignment(self, alignment):
        if alignment == 'Good':
            return "Rogues cannot be of Good alignment"
        else:
            self.alignment = alignment

    def critical_hit(self, opponent):
        if (opponent.ABILITIES_DICT[opponent.dexterity]) > 0:
            opponent.fix_AC()
        self.add_xp()
        subtract_me = ((2*3) + (2 * self.ABILITIES_DICT[self.strength]))
        if subtract_me < 1:
            subtract_me = 1
        opponent.hit_points = opponent.hit_points - subtract_me
        if opponent.hit_points <= 0:
            opponent.alive = 0
        if (opponent.ABILITIES_DICT[opponent.dexterity]) > 0:
            opponent.switch_back_AC()
        return opponent.hit_points
            
    def attack_attempt(self, opponent, number_roll):
        if self.level > 1:
            if self.level % 2 == 0:
                number_roll = number_roll + (self.level / 2)
            elif self.level % 2 != 0:
                number_roll = number_roll + floor(self.level / 2)
        attack_roll = number_roll + self.ABILITIES_DICT[self.dexterity]
        if attack_roll == 20:
            return self.critical_hit(opponent)
        elif attack_roll >= opponent.armor_class:
            return self.hit(opponent)
        elif attack_roll < opponent.armor_class:
            return self.miss(opponent)
        
    def hit(self, opponent):
        if (opponent.ABILITIES_DICT[opponent.dexterity]) > 0:
            opponent.fix_AC()
        self.add_xp()
        subtract_me = (1 + self.ABILITIES_DICT[self.strength]) 
        if subtract_me < 1: 
            subtract_me = 1 

        opponent.hit_points = opponent.hit_points - subtract_me

        if opponent.hit_points <= 0: 
            opponent.alive = 0
        if (opponent.ABILITIES_DICT[opponent.dexterity]) > 0:
            opponent.switch_back_AC()
        return opponent.hit_points



class Monk(Character):
    """
    6 HP per level instead of 5
    3 points of damage on successful attack instead of 1
    armor class is wisdom modifier and dex modifier
    Plus one for attack roll every 2nd and 3rd level
    """
    def set_wisdom(self, wisVal):
        self.wisdom = wisVal
        if self.ABILITIES_DICT[self.wisdom] >= 0:
            self.armor_class = self.armor_class + self.ABILITIES_DICT[self.dexterity] + self.ABILITIES_DICT[self.wisdom]
        else:
            self.armor_class = self.armor_class + self.ABILITIES_DICT[self.dexterity]

    def add_xp(self):
        self.xp = self.xp + 10
        if self.xp >= 1000:
            check = floor(self.xp / 1000) + 1
            if (check != self.level):
                self.level = check
                self.hit_points = self.hit_points + 6 + self.ABILITIES_DICT[self.constitution]

    def attack_attempt(self, opponent, number_roll):
        if self.level > 1:
            add_me = self.level - ceil(self.level / 3)
            attack_roll = number_roll + self.ABILITIES_DICT[self.strength] + add_me
        else:
            attack_roll = number_roll + self.ABILITIES_DICT[self.strength]
        if attack_roll == 20:
            return self.critical_hit(opponent)
        elif attack_roll >= opponent.armor_class:
            return self.hit(opponent)
        elif attack_roll < opponent.armor_class:
            return self.miss(opponent)

    def critical_hit(self, opponent):
        self.add_xp()
        subtract_me = (3 + (2 * self.ABILITIES_DICT[self.strength]))
        if subtract_me < 1:
            subtract_me = 1
        opponent.hit_points = opponent.hit_points - subtract_me
        if opponent.hit_points <= 0:
            opponent.alive = 0
        return opponent.hit_points

    def hit(self, opponent):
        self.add_xp()
        subtract_me = (3 + self.ABILITIES_DICT[self.strength]) 
        if subtract_me < 1: 
            subtract_me = 1 
        opponent.hit_points = opponent.hit_points - subtract_me
        if opponent.hit_points <= 0: 
            opponent.alive = 0
        return opponent.hit_points

class Paladin(Character):
    
    """8 HP per level instead of 5
    For evil opponents:
        +2 damage
        Triple damange for critical hits
    Attack roll increased by 1 for every level
    Good alignment only"""

    def set_alignment(self, alignment):
        if alignment == 'Good':
            self.alignment = alignment
        else:
            return "Paladin is Good!"
        
    def equip_item(self, item, alignment = ""):
        """If item equip by paladin
        +2 to attack against Neutral enemies
        +4 to attack against Evil enemies"""
        self.item = item
        self.armor_class += item.armor_class_bonus

        if alignment == self.ALIGN_NEUTRAL:
            self.item.attack_bonus = self.item.attack_bonus + 2
        elif alignment == self.ALIGN_EVIL:
            self.item.attack_bonus = self.item.attack_bonus + 4

    def add_xp(self):
        self.xp = self.xp + 10
        if self.xp >= 1000:
            check = floor(self.xp / 1000) + 1
            if (check != self.level):
                self.level = check
                self.hit_points = self.hit_points + 8 + self.ABILITIES_DICT[self.constitution]

    def attack_attempt(self, opponent, number_roll):
        if self.level > 1:
            if self.level % 2 == 0:
                number_roll = number_roll + (self.level / 2)
            elif self.level % 2 != 0:
                number_roll = number_roll + floor(self.level / 2)
        attack_roll = 2 + number_roll + self.ABILITIES_DICT[self.strength] + self.level
        if attack_roll == 20:
            return self.critical_hit(opponent)
        elif attack_roll >= opponent.armor_class:
            return self.hit(opponent)
        elif attack_roll < opponent.armor_class:
            return self.miss(opponent)

    def critical_hit(self, opponent):
        self.add_xp()
        if opponent.alignment == 'Evil':    
            subtract_me = 3 * (2 + 2 + (2 * self.ABILITIES_DICT[self.strength]))
        else: 
            subtract_me = (2 + (2 * self.ABILITIES_DICT[self.strength]))
        if subtract_me < 1:
            subtract_me = 1
        opponent.hit_points = opponent.hit_points - subtract_me
        if opponent.hit_points <= 0:
            opponent.alive = 0
        return opponent.hit_points
            
    def hit(self, opponent):
        self.add_xp()
        if opponent.alignment == 'Evil':    
            subtract_me = (1 + 2 + (self.ABILITIES_DICT[self.strength]))
        else: 
            subtract_me = (1 + (self.ABILITIES_DICT[self.strength]))
        if subtract_me < 1: 
            subtract_me = 1 
        opponent.hit_points = opponent.hit_points - subtract_me
        if opponent.hit_points <= 0: 
            opponent.alive = 0
        return opponent.hit_points

class Dwarf(Character):
    # doubles Constitution Modifier when adding to hit points per level (if positive)
    def add_xp(self):
        self.xp += 10
        if self.xp >= 1000:
            check = floor(self.xp / 1000) + 1
            if check != self.level:
                self.level = check
                additional_hp = self.ABILITIES_DICT[self.constitution] * 2
                if additional_hp < 1:
                    additional_hp = 1
                self.hit_points += 5 + additional_hp

class Elf(Character):
    # does adds 1 to critical range for critical hits (20 -> 19-20, 19-20 -> 18-20)
    def critical_hit(self, opponent):
        self.add_xp()
        subtract_me = (2 + (2 * self.ABILITIES_DICT[self.strength]))
        if subtract_me < 1:
            subtract_me = 1
        opponent.hit_points -= subtract_me
        if opponent.hit_points <= 0:
            opponent.alive = 0
        return opponent.hit_points

class Halfling(Character):
    # cannot have evil alignment
    def set_alignment(self, alignment):
        if alignment == Character.ALIGN_EVIL:
            return "Halflings cannot be of Evil alignment"
        else:
            self.alignment = alignment

class Weapon:
    def __init__(self, name, damage, attack_bonus=0, damage_bonus=0, crit_multiplier=2):
        self.name = name
        self.damage = damage
        self.attack_bonus = attack_bonus
        self.damage_bonus = damage_bonus
        self.crit_multiplier = crit_multiplier

class Armor:
    def __init__(self, name, armor_class_bonus, damage_reduction=0, attack_penalty=0):
        self.name = name
        self.armor_class_bonus = armor_class_bonus
        self.damage_reduction = damage_reduction
        self.attack_penalty = attack_penalty

class Item:
    def __init__(self, name, armor_class_bonus=0, attack_bonus=0, strength_bonus=0, special_effects=None):
        self.name = name
        self.armor_class_bonus = armor_class_bonus
        self.attack_bonus = attack_bonus
        self.strength_bonus = strength_bonus
        self.special_effects = special_effects if special_effects else []
