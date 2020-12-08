class DropletsRegistry:
    __instance = None

    def __init__(self):
        if DropletsRegistry.__instance:
            raise Exception("DropletsRegistry class is a singleton class!")
        else:
            self.__droplets = set()
            DropletsRegistry.__instance = self

    @staticmethod
    def get_instance():
        if DropletsRegistry.__instance is None:
            DropletsRegistry()
        return DropletsRegistry.__instance

    def get_droplets(self):
        return self.__droplets

    def add_droplet(self, droplet):
        self.__droplets.add(droplet)

    def remove_droplet(self, droplet):
        self.__droplets.remove(droplet)

    def remove_all_droplets(self):
        self.__droplets = set()
