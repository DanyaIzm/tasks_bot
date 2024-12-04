from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    phone: str

    def __post_init__(self):
        """
        Validation name length between 3 and 15
        Validation phone number correct
        """

        if len(self.phone) not in [11, 12] or not 3 <= len(self.name) <= 15:
            raise ValueError("Incorrect data")

        # Здесь можно усложнить проверку данных, например проверять номер телефона через регулярное выражение


@dataclass
class Task:
    id: int
    user_id: int
    name: str
    description: str
    is_completed: bool
