class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message

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
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):

    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        callories_1 = self.coeff_calorie_1 * self.get_mean_speed()
        callories_2 = (callories_1 - self.coeff_calorie_2) * self.weight
        res = callories_2 / self.M_IN_KM * self.duration * 60
        return res
#(18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах

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
        return (self.coeff_walk_calorie_1 * self.weight +
                (self.get_mean_speed() ** self.coeff_walk_calorie_2 //
                 self.height) * self.coeff_walk_calorie_3 *
                self.weight) * self.duration * 60


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
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() +
                self.coeff_swim_calorie_1) * self.coeff_swim_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dickt = {'SWM': Swimming, 'WLK': SportsWalking, 'RUN': Running}
    return type_dickt[workout_type](*data)


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
