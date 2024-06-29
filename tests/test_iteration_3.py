from evercraft.domain_models.model import Character

"""
### Iteration 3 - Races

Races that a character can be.

#### Feature: Characters Have Races

> As a player I want to play a Human so that I can be boring and unoriginal

- all characters default to Human

> As a player I want a character to have races other than Human that customize its capabilities so that I can play more interesting characters and wont be boring and unoriginal

##### Ideas

- changes in abilities
- increased critical range or damage
- bonuses/penalties versus other races
- special abilities
- alignment limitations

##### Samples

> As a player I want to play an Orc so that I can be crude, drunk, and stupid

- +2 to Strength Modifier, -1 to Intelligence, Wisdom, and Charisma Modifiers
- +2 to Armor Class due to thick hide

> As a player I want to play a Dwarf so that I can drink more than the orc

- +1 to Constitution Modifier, -1 to Charisma Modifier
- doubles Constitution Modifier when adding to hit points per level (if positive)
- +2 bonus to attack/damage when attacking orcs (Dwarves hate Orcs)

> As a player I want to play an Elf so that I can drink wine and snub my nose at the crude dwarf and orc

- +1 to Dexterity Modifier, -1 to Constitution Modifier
- does adds 1 to critical range for critical hits (20 -> 19-20, 19-20 -> 18-20)
- +2 to Armor Class when being attacked by orcs

> As a player I want to play a Halfling so that I can steal from the other drunk characters

- +1 to Dexterity Modifier, -1 to Strength Modifier
- +2 to Armor Class when being attacked by non Halfling (they are small and hard to hit)
- cannot have Evil alignment
"""


# Test cases for Iteration 3 - Races

def test_default_human_character():
    character = Character()
    assert character.race == 'Human'
    assert character.armor_class == 10
    assert character.hit_points == 5

def test_orc_character():
    orc = Character(race='Orc')
    assert orc.strength == '12'  # +2 strength modifier
    assert orc.intelligence == '9'  # -1 intelligence modifier
    assert orc.wisdom == '9'  # -1 wisdom modifier
    assert orc.charisma == '9'  # -1 charisma modifier
    assert orc.armor_class == 12  # +2 armor class due to thick hide

def test_dwarf_character():
    dwarf = Character(race='Dwarf')
    assert dwarf.constitution == '11'  # +1 constitution modifier
    assert dwarf.charisma == '9'  # -1 charisma modifier
    # Double constitution modifier when adding to hit points per level (if positive)
    dwarf.add_xp()
    assert dwarf.hit_points == 5 + (2 * int(dwarf.ABILITIES_DICT[dwarf.constitution]))  # base + (double constitution modifier)

# +2 bonus to attack/damage when attacking orcs (Dwarves hate Orcs)
def test_dwarf_attack_orc():
    dwarf = Character(race='Dwarf')
    orc = Character(race='Orc')
    initial_orc_hp = orc.hit_points
    dwarf.attack_attempt(orc, 15)  # Assume 15 is a successful roll
    expected_damage = 2 + dwarf.ABILITIES_DICT[dwarf.strength] - 1  # Base damage + 2 bonus against Orcs
    if expected_damage < 1:
        expected_damage = 1
    assert orc.hit_points == initial_orc_hp - expected_damage # Orc should have taken {expected_damage} damage from Dwarf's attack

def test_elf_character():
    elf = Character(race='Elf')
    assert elf.dexterity == '11'  # +1 dexterity modifier
    assert elf.constitution == '9'  # -1 constitution modifier

def test_halfling_character():
    halfling = Character(race='Halfling')
    assert halfling.dexterity == '11'  # +1 dexterity modifier
    assert halfling.strength == '9'  # -1 strength modifier
    assert halfling.armor_class == 12  # +2 armor class when being attacked by non-halflings
    assert halfling.alignment != 'Evil'  # cannot have Evil alignment

