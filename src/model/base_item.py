from model import *
#from model.processing_building import *


class BaseItem:

    items = None

    def __init__(self):

        self.items = {}

    def add(self, name, pb, data):

        self.items[name] = {"Mill": pb, "data": data}

    def show(self):

        for item in self.items:
            print(item, self.items[item])
            #print(item + " => " + self.items[item]["ProcessingBuilding"])

    def search(self, search_item):

        print("Searching base_item: " + search_item)
        for item in self.items:
            if item == search_item:
                building = self.items[item]["Mill"]

                # Let's check if in the product definition there is a ProcessingBuilding defined
                if "ProcessingBuilding" in self.items[item]["data"]:
                    building = self.items[item]["data"]["ProcessingBuilding"]

                print("BaseItem found in: " + building)
                #data = self.items[item]["data"]
                return self.items[item], item
        return
