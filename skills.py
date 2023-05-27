from abc import abstractmethod, ABC


class Skill(ABC):
    """
    Базовый класс умения
    """
    def __init__(self):
        self.user = None
        self.target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass


    @abstractmethod
    def skill_effect(self) -> str:
        """
        Эффект умения
        """
        pass

    def _is_stamina_enough(self):
        """
        Приватный метод проверки: хватает ли выносливости для использования навыка
        """
        return self.user.stamina >= self.stamina

    def use(self, user, target) -> str:
        """
        Метод использования навыка:
        Проверка, хватит ли выносливости у игрока для применения умения;
        Для вызова умения везде используется use.
        """
        self.user = user
        self.target = target

        if self._is_stamina_enough():
            return self.skill_effect()
        return f'{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости'


class FuryPunch(Skill):
    name = 'Свирепый пинок'
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        """
        Логика использования скилла
        в классе нам доступны экземпляры user и target - можно использовать любые их методы
        именно здесь происходит уменшение стамины у игрока применяющего умение и
        уменьшение здоровья цели.
        Результат применения возвращаем строкой
        """
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику'


class HardShot(Skill):
    name = 'Мощный укол'
    stamina = 5
    damage = 15

    def skill_effect(self) -> str:
        """
        Логика по аналогии с одноименным методом из класса FuryPunch
        """
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику'
