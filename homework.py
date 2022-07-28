class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.speed: float = speed
        self.calories: float = calories
        self.distance: float = distance

    def get_message(self) -> str:
        return self.MESSAGE.format(self.training_type,
                                   self.duration,
                                   self.distance,
                                   self.speed,
                                   self.calories)


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR = 60

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
        return self.get_distance() / self.duration

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
    """Тренировка: бег."""
    ENERGY: int = 18
    COEF_CALORIES: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories_1 = self.ENERGY * self.get_mean_speed()
        calories_2 = (calories_1 - self.COEF_CALORIES) * self.weight
        res = calories_2 / self.M_IN_KM * self.duration * self.MIN_IN_HOUR
        return res


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CALORIE_1: float = 0.035
    WALK_CALORIE_2: int = 2
    WALK_CALORIE_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (self.WALK_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** self.WALK_CALORIE_2
                   // self.height) * self.WALK_CALORIE_3
                * self.weight) * self.duration * self.MIN_IN_HOUR


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_CALORIE_1: float = 1.1
    SWIM_CALORIE_2: int = 2

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
        calories_1 = (self.get_mean_speed() + self.SWIM_CALORIE_1)
        res = calories_1 * self.SWIM_CALORIE_2 * self.weight
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
