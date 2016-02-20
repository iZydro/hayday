from model import *
from model.processing_building import *


class Fish:

    items = None

    def __init__(self):

        self.items = {}

    def add(self, name, pb, data):

        self.items[name] = {"ProcessingBuilding": pb, "data": data}

    def show(self):

        for item in self.items:
            print(item, self.items[item])
            #print(item + " => " + self.items[item]["ProcessingBuilding"])

    def search(self, search_item):

        for item in self.items:
            if item == search_item:
                building = self.items[item]["ProcessingBuilding"]
                #print(building)

        return
