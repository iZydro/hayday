from model import *
from model.processing_building import *


class Field:

    items = None

    def __init__(self):

        self.items = {}

    def add(self, name, pb, data):

        self.items[name] = {"ProcessingBuilding": pb, "data": data}

    def show(self):

        for item in self.items:
            #print(item + " => " + self.items[item]["ProcessingBuilding"])
            print(item, self.items[item])

    def search(self, search_item):

        for item in self.items:
            if item == search_item:
                building = self.items[item]["ProcessingBuilding"]
                data = self.items[item] # ["data"]
                return data
                #print("fields available:" + building)

        return
