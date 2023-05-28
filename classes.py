from dataclasses import dataclass

from skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(
    name='Воин',
    max_health=60,
    max_stamina=30,
    attack=0.8,
    stamina=0.9,
    armor=1.2,
    skill=FuryPunch(),
)


RogueClass = UnitClass(
    name='Вор',
    max_health=50,
    max_stamina=25,
    attack=1.5,
    stamina=1.2,
    armor=1,
    skill=HardShot(),
)


unit_classes = {
    RogueClass.name: RogueClass,
    WarriorClass.name: WarriorClass,
}
