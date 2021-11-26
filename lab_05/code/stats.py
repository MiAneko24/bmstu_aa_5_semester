import random
import uuid

PC = 'qwertyuiopasdfghjklzxcvbnm1234567890'
PCS = len(PC)


class User:
    def __init__(self, login: str = None, password: str = None):
        if login is None:
            self.__login = str(uuid.uuid4())
        else:
            self.__login = login
        if password is None:
            self.__password = self.__generate_pass()
        else:
            self.__password = password

    @staticmethod
    def __generate_pass():
        size = random.randint(16, 2**9)
        a = ''
        for i in range(size):
            a += PC[random.randint(0, PCS - 1)]
        return a

    def login(self):
        return self.__login

    def password(self):
        return self.__password


class Time:
    def __init__(self):
        self.__time_in = None
        self.__time_out = None

    def set(self, t, is_in: bool):
        if is_in:
            if self.__time_in is not None:
                raise Exception("Время поступления на ленту уже записано!")
            self.__time_in = t
        elif not is_in:
            if self.__time_out is not None:
                raise Exception("Время выхода с ленты уже записано!")
            self.__time_out = t
        else:
            raise Exception("При установке параметр is_in - обязательный!")

    def get(self, is_in: bool = None):
        if is_in is None:
            if self.__time_out is None and self.__time_in is None:
                raise Exception("Время не установлено!")
            elif self.__time_out is None:
                raise Exception("Время поступления на ленту не установлено!")
            elif self.__time_out is None:
                raise Exception("Время выхода с ленты не установлено!")
            return [self.__time_in, self.__time_out]
        elif is_in:
            if self.__time_out is None:
                raise Exception("Время поступления на ленту не установлено!")
            return self.__time_in
        else:
            if self.__time_out is None:
                raise Exception("Время выхода с ленты не установлено!")
            return self.__time_out


class UserStats:
    cnt = 0

    def __init__(self, login: str = None, password: str = None, do_not_init: bool = True):
        self.__times = [Time() for _ in range(3)]
        self.__number = self.cnt
        if do_not_init:
            self.user = None
        else:
            self.user = User(login, password)
        self.current = ''
        UserStats.cnt += 1

    def set_time(self, time_, stage: int, is_in: bool):
        # is_in - True, если на вход, False, если на выход
        # stage - номер ленты
        if stage < 0 or stage > 2 or stage is None:
            raise Exception("Неправильный номер ленты!")
        self.__times[stage].set(time_, is_in)

    def get_time(self, is_in: bool = None, stage: int = None):
        # is_in - True, если на вход, False, если на выход, обязательный
        # stage - номер ленты, None = выдать все

        if stage is not None and (stage < 0 or stage > 2):
            raise Exception("Неправильный номер ленты!")
        if stage is None:
            if is_in is None:
                return [self.__times[i].get() for i in range(3)]
            else:
                return [self.__times[i].get(is_in) for i in range(3)]
        else:
            return self.__times[stage].get(is_in)

    def get_number(self):
        return self.__number


if __name__ == "__main__":
    print("Пример использования")
    s = [UserStats() for _ in range(10)]
    for u in s:
        print(u.user.login(), u.user.password(), u.get_number())
    u = s[0]
    u.set_time(3, 0, True)  # время 3 для первого конвейера на вход
    u.set_time(4, 0, False)  # время 4 для первого конвейера на выход
    u.set_time(6, 1, True)
    u.set_time(9, 1, False)
    u.set_time(12, 2, True)
    u.set_time(13, 2, False)
    print(u.get_time())  # все времена
    # print(u.get_time(is_in=True))  # все времена входа
    # print(u.get_time(is_in=False))  # все времена выхода
    # print(u.get_time(stage=0))  # время первого конвейера
    # print(u.get_time(stage=1))  # время второго конвейера
    # print(u.get_time(is_in=True, stage=0))  # конкретное время - вход первого конвейера
    # print(u.get_time(is_in=False, stage=0))  # конкретное время - вход первого конвейера
    # print(u.get_time(is_in=True, stage=1))  # конкретное время - вход первого конвейера
    # print(u.get_time(is_in=False, stage=1))  # конкретное время - вход первого конвейера
    # print(u.get_time(is_in=True, stage=2))  # конкретное время - вход первого конвейера
    # print(u.get_time(is_in=False, stage=2))  # конкретное время - вход первого конвейера
    # print(u.get_time())  # под конец слови экспешн - время всегда должны быть установлено для получения
