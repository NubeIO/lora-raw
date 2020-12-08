class DropletsRegistry:
    __instance = None

    def __init__(self):
        if DropletsRegistry.__instance:
            raise Exception("DropletsRegistry class is a singleton class!")
        else:
            self.__droplets = {}
            DropletsRegistry.__instance = self

    @staticmethod
    def get_instance():
        if DropletsRegistry.__instance is None:
            DropletsRegistry()
        return DropletsRegistry.__instance

    def get_droplets(self):
        return self.__droplets

    def get_uuid_from_droplets(self, droplet):
        return self.__droplets[droplet]

    def add_droplet(self, droplet, uuid):
        self.__droplets[droplet] = uuid

    def remove_droplet(self, droplet):
        self.__droplets.pop(droplet, None)

    def remove_all_droplets(self):
        self.__droplets = {}
