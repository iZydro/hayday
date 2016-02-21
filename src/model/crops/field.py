from model.main import *


class FieldManager:

    items = None
    main = None

    def __init__(self, main_ref: Main):

        self.items = []
        self.main = main_ref
        pass

    def add(self):

        _item = Field(self)
        self.items.append(_item)
        return _item

        pass

    def update(self, time):
        print("Update ts: " + str(time))
        for item in self.items:
            item.update(time)

    def show(self):
        for item in self.items:
            print(item, item.name, item.data, item.ts, item.status)


class Field:

    name = None
    data = None
    ts = None
    parent = None
    status = "Empty"

    def __init__(self, parent_ref):
        self.parent = parent_ref
        pass

    def find(self, crop_name):

        self.parent.main.items.search(crop_name)

        pass

    def plant(self, crop_name, crop_data, timestamp):
        self.name = crop_name
        self.data = crop_data
        self.ts = int(timestamp)
        self.status = "Planted"
        pass

    def update(self, timestamp):
        if self.name:
            if timestamp - self.ts > int(self.data["TimeMin"])*60*1000:
                self.status = "Ready"

if __name__ == "__main__":

    main = Main()
    main.init_data()
    manager = FieldManager(main)

    print("Fielding")

    time = 0

    carrot, carrot_name = main.items.search("Carrot", main.generators)
    wheat, wheat_name = main.items.search("Wheat", main.generators)
    print(carrot_name, carrot)
    print(wheat_name, wheat)

    manager.add().plant(wheat_name, wheat, time)
    manager.add().plant(carrot_name, carrot, time)
    manager.add()

    manager.show()

    time += 1000*5*60
    manager.update(time)
    manager.show()

    time += 1000*7*60
    manager.update(time)
    manager.show()
