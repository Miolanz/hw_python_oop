from dataclasses import asdict, dataclass, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.INFO.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60
    SPENT_CALORIES_ERROR = 'Определите get_spent_calories в {}.'

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            self.SPENT_CALORIES_ERROR.format(self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029
    KMH_TO_MPS_MULTIPLIER = 0.278
    SENTIMETERS_IN_METER = 100

    def get_spent_calories(self) -> float:
        return (
            (self.WEIGHT_MULTIPLIER_1 * self.weight
                + ((self.get_mean_speed()
                    * self.KMH_TO_MPS_MULTIPLIER) ** 2
                    / (self.height
                        / self.SENTIMETERS_IN_METER))
                * self.WEIGHT_MULTIPLIER_2
                * self.weight)
            * (self.duration * self.MIN_IN_HOUR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int

    LEN_STEP = 1.38
    MEAN_SPEED_TERM = 1.1
    WEIGHT_MULTIPLIER = 2

    def get_mean_speed(self):
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self):
        return (
            (self.get_mean_speed() + self.MEAN_SPEED_TERM)
            * self.WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


TRAINING_DATA = {
    'SWM': (Swimming, len(fields(Swimming))),
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking)))
}

WORKOUT_TYPE_ERROR = 'Тип тренировки {} не найден'
WORKOUT_LEN_ERROR = ('Неверное число аргументов тренировки {}. '
                     'Получено {}, ожидается {}')


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAINING_DATA:
        raise ValueError(WORKOUT_TYPE_ERROR.format(workout_type))
    if TRAINING_DATA[workout_type][1] != len(data):
        raise ValueError(
            WORKOUT_LEN_ERROR.format(
                workout_type,
                len(data),
                TRAINING_DATA[workout_type][1]
            )
        )
    return TRAINING_DATA[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
