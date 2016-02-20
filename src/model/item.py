from model import *

class Item:

    items = None

    def __init__(self):

        self.items = {}

    def add(self, name, pb):

        self.items[name] = {"ProcessingBuilding": pb}

    def show(self):

        for item in self.items:
            print(item + " => " + self.items[item]["ProcessingBuilding"])

    def search(self, search_item, generators):
        print("Searching: " + str(search_item))
        for item in self.items:
            if item == search_item:
                building = self.items[item]["ProcessingBuilding"]
                print("Found in building: " + building)
                if building == "Fishing":
                    print(generators[building].search(item))
                    return None
                elif building == "Vegetables":
                    return generators[building].search(item)
                elif building == "Trees":
                    return generators[building].search(item)
                elif building == "Animals":
                    return generators[building].search(item)
                    #return None
                elif building == "Fruits":
                    return generators[building].search(item)
                else:
                    return(generators["ProcessingBuildings"].search(item))

        return
