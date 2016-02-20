from model import *
from model.base import Base


class ProcessingBuilding:

    buildings = None

    def __init__(self):

        self.buildings = {}

    def add(self, name, item: Base):

        self.buildings[name] = item

    def search(self, search_item):

        for building in self.buildings:
            for item in self.buildings[building].items:
                if item == search_item:
                    print(item + " done at " + building)
                    item_data = self.buildings[building].items[item]
                    return(item_data)

        return
