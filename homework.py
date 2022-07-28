class InfoMessage:
    """Информационное сообщение о тренировке."""

    TEXT = message = ('Тип тренировки: {}; '
                      'Длительность: {} ч.; '
                      'Дистанция: {} км; '
                      'Ср. скорость: {} км/ч; '
                      'Потрачено ккал: {}.')

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type: str = training_type
        self.duration: str = "%.3f" % duration
        self.speed: str = "%.3f" % speed
        self.calories: str = "%.3f" % calories
        self.distance: str = "%.3f" % distance

    def get_message(self) -> str:
        return self.TEXT.format(self.training_type,
                                self.duration,
                                self.distance,
                                self.speed,
                                self.calories)


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(type(self).__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    ENERGY: int = 18
    COEF_CALLORIES: int = 20
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        callories_1 = self.ENERGY * self.get_mean_speed()
        callories_2 = (callories_1 - self.COEF_CALLORIES) * self.weight
        res = callories_2 / self.M_IN_KM * self.duration * self.MIN_IN_HOUR
        return res


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_walk_calorie_1: float = 0.035
    coeff_walk_calorie_2: int = 2
    coeff_walk_calorie_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (self.coeff_walk_calorie_1 * self.weight
                + (self.get_mean_speed() ** self.coeff_walk_calorie_2
                   // self.height) * self.coeff_walk_calorie_3
                * self.weight) * self.duration * 60


class Swimming(Training):
    LEN_STEP: float = 1.38
    coeff_swim_calorie_1: float = 1.1
    coeff_swim_calorie_2: int = 2
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        pool_speed = self.length_pool * self.count_pool
        res = pool_speed / self.M_IN_KM / self.duration
        return res

    def get_spent_calories(self) -> float:
        calories_1 = (self.get_mean_speed() + self.coeff_swim_calorie_1)
        res = calories_1 * self.coeff_swim_calorie_2 * self.weight
        return res


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_sport = {'SWM': Swimming, 'WLK': SportsWalking, 'RUN': Running}
    return type_sport[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
