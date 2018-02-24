from HeartstoneAI.cards import Minion, Spell
import HeartstoneAI.abilities as abilities
from HeartstoneAI.abilities import CHARGE, DIVINE_SHIELD, DEATHRATTLE, TAUNT
from functools import partial

ABUSIVE_SERGEANT = "abusive_sergeant"
ARGENT_SQUIRE = "argent_squire"
DIVINE_STRENGTH = "divine_strength"
SELFLESS_HERO = "selfless_hero"
DIVINE_FAVOR = "divine_favor"
SEAL_OF_CHAMPIONS = "seal_of_champions"
STEWARD_OF_DARKSHIRE = "steward_of_darkshire"
WOLFRIDER = "wolfrider"
BLESSING_OF_KINGS = "blessing_of_kings"
DEFENDER_OF_ARGUS = "defender_of_argus"

abusive_sergeant = Minion(name=ABUSIVE_SERGEANT, cost=1, abilities=dict(), attack=1, health=1, minion_type=None)
abusive_sergeant.abilities['add_specs_turn'] = partial(abilities.add_specs_to_own_minion_for_turn, attack=2)

agent_squire = Minion(name=ARGENT_SQUIRE, cost=1, abilities=dict(), attack=1, health=1, minion_type=None)
agent_squire.abilities[DIVINE_SHIELD] = partial(abilities.divine_shield)

divine_strength = Spell(name=DIVINE_STRENGTH, cost=1, abilities=dict())
divine_strength.abilities['add_specs'] = partial(abilities.add_specs_to_own_minion, attack=1, health=2)

selfless_hero = Minion(name=SELFLESS_HERO, cost=1, abilities=dict(), attack=2, health=1, minion_type=None)
selfless_hero.abilities[DEATHRATTLE] = partial(abilities.add_shield_to_own_minion)

divine_favor = Spell(name=DIVINE_FAVOR, cost=3, abilities=dict())
divine_favor.abilities['draw_cards_to_match_opponent'] = partial(abilities.draw_cards_to_match_opponent)

seal_of_champions = Spell(name=SEAL_OF_CHAMPIONS, cost=3, abilities=dict())
seal_of_champions.abilities['add_attack_and_shield'] = partial(abilities.add_ability_and_specs_to_own_minion,
                                                               ability={DIVINE_SHIELD: partial(abilities.divine_shield)}, attack=3)

steward_of_darshire = Minion(name=STEWARD_OF_DARKSHIRE, cost=3, abilities=dict(), attack=3, health=3, minion_type=None)
steward_of_darshire.abilities[DIVINE_SHIELD] = partial(abilities.divine_shield)

wolfrider = Minion(name=WOLFRIDER, cost=3, abilities=dict(), attack=3, health=1, minion_type=None)
wolfrider.abilities[CHARGE] = partial(abilities.charge, minion=wolfrider)

blessing_of_kings = Spell(name=BLESSING_OF_KINGS, cost=4, abilities=dict())
blessing_of_kings.abilities['add_specs'] = partial(abilities.add_specs_to_own_minion, attack=4, health=4)

defender_of_argus = Minion(name=DEFENDER_OF_ARGUS, cost=4, abilities=dict(), attack=2, health=3, minion_type=None)
defender_of_argus.abilities['add_specs_and_taunt_1'] = partial(abilities.add_ability_and_specs_to_own_minion,
                                                               ability={TAUNT: partial(abilities.taunt)},
                                                               attack=1, health=1)



