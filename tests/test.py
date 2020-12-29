from src.utils.singleton import Singleton


class Props:

    def __init__(self):
        self.enabled = False
        self._xyz = 123
        self.__abc = 'aha'

    def reload(self, setting: dict):
        print(self.__dict__)
        print(dir(self))
        print(vars(self))
        self.__dict__ = {k: setting[k] or v for k, v in self.__dict__.items()}
        print(self.__dict__)
        return self

    @property
    def abc(self):
        return self.__abc

    @property
    def xyz(self):
        return self._xyz


class SingletonX(metaclass=Singleton):
    def __init__(self):
        self.__c = None

    def load(self, config):
        self.__c = config

    @property
    def c(self):
        return self.__c

    def fun(self):
        return self.__c


if __name__ == '__main__':
    s = Props()
    print(s.__dict__)
    print([n for n in dir(s) if not n.startswith('_')])
    print(vars(s))
    # print(s.enabled)
    # s.reload({'enabled': True, 'abc': 123})
    # print(s.enabled)
    # print(s.abc)
    x1 = SingletonX()
    x2 = SingletonX()
    x3 = SingletonX()
    print(x1)
    print(x2)
    print(x3)
    print(x1 is x2 is x3)
    print(x1.c or 'nothing')
    x1.load({'a': 5})
    print(x2.c)
    print(x3.fun())
    print(x1.c is x2.c is x3.fun())
