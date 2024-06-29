from evercraft.domain_models.model import Character, Fighter, Rogue, Monk, Paladin, Weapon, Armor, Item

"""
### Iteration 4 - Weapons, Armor & Items

Items that enhance a characters capabilities.

#### Feature: Weapons

> As a character I want to be able to wield a single weapon so that I can achieve victory through superior firepower

- character can wield only one weapon

##### Ideas

- basic weapons that improve damage (dagger)
- basic weapons that improve to attacks (+1 sword)
- magic weapons with special properties (knife of ogre slaying)
- weapons that certain classes or races can or cannot wield

##### Samples

> As a character I want to be able to wield a longsword so that I can look cool

- does 5 points of damage

> As a character I want to be able to wield a +2 waraxe that so that I can *be* cool

- does 6 points of damage
- +2 to attack
- +2 to damage
- triple damage on a critical (quadruple for a Rogue)

> As an elf I want to be able to wield a elven longsword that so I can stick it to that orc with the waraxe

- does 5 points of damage
- +1 to attack and damage
- +2 to attack and damage when wielded by an elf *or* against an orc
- +5 to attack and damage when wielded by an elf *and* against orc

> As a monk I want nun chucks that work with my martial arts so that I can kick ass like Chuck Norris

- does 6 points of damage
- when used by a non-monk there is a -4 penalty to attack

#### Feature: Armor

> As a character I want to be able to don armor and shield so that I can protect myself from attack

- character can only don one shield and wear one suit of armor

##### Ideas

- basic armor that improves armor class (plate)
- magic armor that has special properties
- armor and shields that are or are not usable by certain races or classes

##### Samples

> As a character I want to the be able to wear leather armor so that I can soften attacks against me

- +2 to Armor Class

> As a fighter (or dwarf) I want to be able to wear plate armor so that I can ignore the blows of my enemies

- +8 to Armor Class
- can only be worn by fighters (of any race) and dwarves (of any class)

> As a character I want to the be able to wear magical leather armor of damage reduction so that I can soften attacks against me

- +2 to Armor Class
- -2 to all damage received

> As an elf I want to be able to wear elven chain mail so that I can fit in with all the other elves

- +5 to Armor Class
- +8 to Armor Class if worn by an elf
- +1 to attack if worn by an elf

> As a fighter I want to be able to hold a shield in my off-hand so that I can block incoming blows

- +3 to Armor Class
- -4 to attack
- -2 to attack if worn by a fighter

#### Feature: Items

> As a character I want to be able to have items that enhance my capabilities so that I can be more bad-ass

- can carry multiple items

##### Ideas

- items that improve combat with types of weapons
- items that improve stats against enemies with a certain alignment or race
- items that improve abilities

##### Samples

> As a character I want to be able to wear a ring of protection so that I can be protected from attack

  - adds +2 to armor class

> As a character I want to be able to wear a belt of giant strength so that I can be even stronger in combat

  - add +4 to Strength Score

> As a character I want to be able to wear an amulet of the heavens so that I can strike down evil with holy power

  - +1 to attack against Neutral enemies
  - +2 to attack against Evil enemies
  - double above bonuses if worn by a paladin

"""


# Test cases for Iteration 4 - Weapons, Armor & Items

def test_long_sword():
    character = Character()
    weapon = Weapon(name='Longsword', damage=5)
    character.equip_weapon(weapon)
    assert character.weapon.name == 'Longsword'
    assert character.weapon.damage == 5

def test_waraxe():
    character = Character()
    weapon = Weapon(name='Waraxe', damage=6, attack_bonus=2, damage_bonus=2, crit_multiplier=3)
    character.equip_weapon(weapon)
    assert character.weapon.name == 'Waraxe'
    assert character.weapon.damage == 6
    assert character.weapon.attack_bonus == 2
    assert character.weapon.damage_bonus == 2
    assert character.weapon.crit_multiplier == 3

def test_elven_longsword():
    elf = Character(race='Elf')
    weapon = Weapon(name='Elven Longsword', damage=5, attack_bonus=1, damage_bonus=1)
    elf.equip_weapon(weapon)
    assert elf.weapon.name == 'Elven Longsword'
    assert elf.weapon.damage == 5
    assert elf.weapon.attack_bonus == 1
    assert elf.weapon.damage_bonus == 1

# does 6 points of damage
def test_nunchucks_for_monk():
    monk = Monk()
    weapon = Weapon(name='Nunchucks', damage=6)
    monk.equip_weapon(weapon)
    assert monk.weapon.name == 'Nunchucks'
    assert monk.weapon.damage == 6

def test_leather_armor():
    character = Character()
    armor = Armor(name='Leather Armor', armor_class_bonus=2)
    character.equip_armor(armor)
    assert character.armor.name == 'Leather Armor'
    assert character.armor.armor_class_bonus == 2

def test_plate_armor_for_fighter():
    fighter = Fighter()
    armor = Armor(name='Plate Armor', armor_class_bonus=8)
    fighter.equip_armor(armor)
    assert fighter.armor.name == 'Plate Armor'
    assert fighter.armor.armor_class_bonus == 8

def test_magical_leather_armor():
    character = Character()
    armor = Armor(name='Magical Leather Armor', armor_class_bonus=2, damage_reduction=2)
    character.equip_armor(armor)
    assert character.armor.name == 'Magical Leather Armor'
    assert character.armor.armor_class_bonus == 2
    assert character.armor.damage_reduction == 2

def test_ring_of_protection():
    character = Character()
    item = Item(name='Ring of Protection', armor_class_bonus=2)
    character.equip_item(item)
    assert character.item.name == 'Ring of Protection'
    assert character.item.armor_class_bonus == 2

def test_belt_of_giant_strength():
    character = Character()
    item = Item(name='Belt of Giant Strength', strength_bonus=4)
    character.equip_item(item)
    assert character.item.name == 'Belt of Giant Strength'
    assert character.item.strength_bonus == 4

def test_amulet_of_the_heavens():
    # If equip item against neutral, +1 to attack
    character = Character()
    item = Item(name='Amulet of the Heavens')
    character.equip_item(item, "Neutral")
    assert character.item.name == 'Amulet of the Heavens'
    assert character.item.attack_bonus == 1
    
    # If equip item against evil, +2 to attack
    item = Item(name='Amulet of the Heavens')
    character.equip_item(item,"Evil")
    assert character.item.attack_bonus == 2

def test_amulet_of_the_heavens_for_paladin():
    # If equip item against neurtral, evil then double attack as compare to normal character
    paladin = Paladin()
    item = Item(name='Amulet of the Heavens')
    paladin.equip_item(item,"Neutral")
    assert paladin.item.name == 'Amulet of the Heavens'

    assert paladin.item.attack_bonus == 2

    item = Item(name='Amulet of the Heavens')
    paladin.equip_item(item,"Evil")
    assert paladin.item.attack_bonus  == 4
